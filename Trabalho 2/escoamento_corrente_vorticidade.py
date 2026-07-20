#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =====================================================================
# Trabalho Obrigatorio T2 - Mec. Flu. e Transf. Calor Computacional
# Escoamento incompressivel, newtoniano e transiente 2D
# Formulacao CORRENTE-VORTICIDADE (psi-omega) via MEF - elemento TRI6
#
#   d(w)/dt + v . grad(w) = (1/Re) lap(w)     (transporte de vorticidade)
#   lap(psi) = -w                             (Poisson da funcao corrente)
#   vx =  d(psi)/dy      vy = -d(psi)/dx
#
# Base: funcaoCorrente2d-mef_tri6.py (Prof. Gustavo R. Anjos)
# =====================================================================
import os
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import meshio
import matplotlib.pyplot as plt
import matplotlib.tri as mtri

# ---------------------------------------------------------------------
# 1) PARAMETROS  (mude aqui conforme a geometria/caso)
# ---------------------------------------------------------------------
MSH      = 'furoCirculo.msh'   # furoCirculo.msh | furo.msh | sym_airfoil.msh | nonSym_airfoil.msh
Re       = 100.0               # numero de Reynolds
U        = 1.0                 # velocidade da corrente livre (entrada)
dt       = 0.005               # passo de tempo
nt       = 600                 # numero de passos de tempo
beta     = 0.10                # sub-relaxacao da vorticidade de parede (0<beta<=1)
nsave    = 10                  # salva um .vtk a cada 'nsave' passos (p/ animar no ParaView)
outdir   = 'saida_vtk'         # pasta de saida das solucoes
# ---------------------------------------------------------------------

os.makedirs(outdir, exist_ok=True)

# ---------------------------------------------------------------------
# 2) LEITURA DA MALHA (GMSH via meshio) - robusto por tipo de bloco
# ---------------------------------------------------------------------
msh = meshio.read(MSH)
X = msh.points[:, 0]
Y = msh.points[:, 1]
npoints = len(X)

IEN = None            # conectividade dos triangulos de 6 nos (dominio)
IENbound = None       # conectividade das linhas de 3 nos (contorno)
bnd_phys = None       # id fisico de cada elemento de contorno
for i, cb in enumerate(msh.cells):
    if cb.type == 'triangle6':
        IEN = cb.data
    elif cb.type == 'line3':
        IENbound = cb.data
        bnd_phys = msh.cell_data['gmsh:physical'][i]
ne = IEN.shape[0]

# mapa  id_fisico -> nome  ("cc1","cc2","cc3","cc4","furo",...)
id2name = {int(v[0]): k for k, v in msh.field_data.items()}

# nome do contorno de cada no (obstaculo sobrescreve os cantos)
ccName = [''] * npoints
for target in ['cc1', 'cc3', 'cc2', 'cc4', 'furo']:
    for e in range(len(IENbound)):
        if id2name[bnd_phys[e]] == target:
            for nd in IENbound[e]:
                ccName[nd] = target

cc1  = [i for i, x in enumerate(ccName) if x == 'cc1']    # parede inferior
cc2  = [i for i, x in enumerate(ccName) if x == 'cc2']    # saida (direita)
cc3  = [i for i, x in enumerate(ccName) if x == 'cc3']    # parede superior
cc4  = [i for i, x in enumerate(ccName) if x == 'cc4']    # entrada (esquerda)
furo = [i for i, x in enumerate(ccName) if x == 'furo']   # obstaculo

print(f'malha: {MSH}  npoints={npoints}  ne={ne}')
print(f'nos de contorno -> entrada:{len(cc4)} base:{len(cc1)} '
      f'topo:{len(cc3)} saida:{len(cc2)} obstaculo:{len(furo)}')

# ---------------------------------------------------------------------
# 3) MONTAGEM DAS MATRIZES GLOBAIS (K, M, Gx, Gy) - elemento TRI6
#    K  : rigidez (laplaciano)   M  : massa
#    Gx : derivada em x          Gy : derivada em y
# ---------------------------------------------------------------------
K  = sp.lil_matrix((npoints, npoints))
M  = sp.lil_matrix((npoints, npoints))
Gx = sp.lil_matrix((npoints, npoints))
Gy = sp.lil_matrix((npoints, npoints))

for e in range(ne):
    v = IEN[e]
    area = 0.5 * (X[v[2]] * (Y[v[0]] - Y[v[1]])
                  + X[v[0]] * (Y[v[1]] - Y[v[2]])
                  + X[v[1]] * (-Y[v[0]] + Y[v[2]]))

    bi = Y[v[1]] - Y[v[2]]; bj = Y[v[2]] - Y[v[0]]; bk = Y[v[0]] - Y[v[1]]
    ci = X[v[2]] - X[v[1]]; cj = X[v[0]] - X[v[2]]; ck = X[v[1]] - X[v[0]]

    melem = (area / 180) * np.array(
        [[ 6, -1, -1,  0, -4,  0],
         [-1,  6, -1,  0,  0, -4],
         [-1, -1,  6, -4,  0,  0],
         [ 0,  0, -4, 32, 16, 16],
         [-4,  0,  0, 16, 32, 16],
         [ 0, -4,  0, 16, 16, 32]], dtype=float)

    kxelem = (1 / area) * np.array(
        [[ bi**2/4,   -bi*bj/12,  -bi*bk/12,   bi*bj/3,   0.0,       bi*bk/3],
         [-bi*bj/12,   bj**2/4,   -bj*bk/12,   bi*bj/3,   bj*bk/3,   0.0],
         [-bi*bk/12,  -bj*bk/12,   bk**2/4,    0.0,       bj*bk/3,   bi*bk/3],
         [ bi*bj/3,    bi*bj/3,    0.0,       (2/3)*(bi**2+bi*bj+bj**2),
                                              (1/3)*(bj**2+bj*bk+bi*bj+2*bi*bk),
                                              (1/3)*(bi**2+bi*bk+bi*bj+2*bj*bk)],
         [ 0.0,        bj*bk/3,    bj*bk/3,   (1/3)*(bi*bj+2*bi*bk+bj**2+bj*bk),
                                              (2/3)*(bj**2+bj*bk+bk**2),
                                              (1/3)*(2*bi*bj+bi*bk+bj*bk+bk**2)],
         [ bi*bk/3,    0.0,        bi*bk/3,   (1/3)*(bi**2+bi*bj+bi*bk+2*bj*bk),
                                              (1/3)*(2*bi*bj+bi*bk+bj*bk+bk**2),
                                              (2/3)*(bi**2+bi*bk+bk**2)]])

    kyelem = (1 / area) * np.array(
        [[ ci**2/4,   -ci*cj/12,  -ci*ck/12,   ci*cj/3,   0.0,       ci*ck/3],
         [-ci*cj/12,   cj**2/4,   -cj*ck/12,   ci*cj/3,   cj*ck/3,   0.0],
         [-ci*ck/12,  -cj*ck/12,   ck**2/4,    0.0,       cj*ck/3,   ci*ck/3],
         [ ci*cj/3,    ci*cj/3,    0.0,       (2/3)*(ci**2+ci*cj+cj**2),
                                              (1/3)*(cj**2+cj*ck+ci*cj+2*ci*ck),
                                              (1/3)*(ci**2+ci*ck+ci*cj+2*cj*ck)],
         [ 0.0,        cj*ck/3,    cj*ck/3,   (1/3)*(ci*cj+2*ci*ck+cj**2+cj*ck),
                                              (2/3)*(cj**2+cj*ck+ck**2),
                                              (1/3)*(2*ci*cj+ci*ck+cj*ck+ck**2)],
         [ ci*ck/3,    0.0,        ci*ck/3,   (1/3)*(ci**2+ci*cj+ci*ck+2*cj*ck),
                                              (1/3)*(2*ci*cj+ci*ck+cj*ck+ck**2),
                                              (2/3)*(ci**2+ci*ck+ck**2)]])

    gxelem = (1/30.) * np.array(
        [[ 2*bi, -bj,  -bk,  -bi+2*bj,  -(bj+bk),   -bi+2*bk],
         [  -bi, 2*bj, -bk,  2*bi-bj,   -bj+2*bk,   -(bi+bk)],
         [  -bi, -bj,  2*bk, -(bi+bj),  2*bj-bk,    2*bi-bk],
         [ 3*bi, 3*bj, -bk,  8*(bi+bj), 4*(bj+2*bk), 4*(bi+2*bk)],
         [  -bi, 3*bj, 3*bk, 4*(2*bi+bj), 8*(bj+bk), 4*(2*bi+bk)],
         [ 3*bi, -bj,  3*bk, 4*(bi+2*bj), 4*(2*bj+bk), 8*(bi+bk)]])

    gyelem = (1/30.) * np.array(
        [[ 2*ci, -cj,  -ck,  -ci+2*cj,  -(cj+ck),   -ci+2*ck],
         [  -ci, 2*cj, -ck,  2*ci-cj,   -cj+2*ck,   -(ci+ck)],
         [  -ci, -cj,  2*ck, -(ci+cj),  2*cj-ck,    2*ci-ck],
         [ 3*ci, 3*cj, -ck,  8*(ci+cj), 4*(cj+2*ck), 4*(ci+2*ck)],
         [  -ci, 3*cj, 3*ck, 4*(2*ci+cj), 8*(cj+ck), 4*(2*ci+ck)],
         [ 3*ci, -cj,  3*ck, 4*(ci+2*cj), 4*(2*cj+ck), 8*(ci+ck)]])

    for a in range(6):
        ia = v[a]
        for b in range(6):
            jb = v[b]
            K[ia, jb]  += kxelem[a, b] + kyelem[a, b]
            M[ia, jb]  += melem[a, b]
            Gx[ia, jb] += gxelem[a, b]
            Gy[ia, jb] += gyelem[a, b]

K  = K.tocsc();  M = M.tocsc();  Gx = Gx.tocsc();  Gy = Gy.tocsc()
print('matrizes montadas.')

# ---------------------------------------------------------------------
# 4) CONDICOES DE CONTORNO e PRE-FATORACOES
# ---------------------------------------------------------------------
Msolve = spla.factorized(M)          # para recuperar velocidades e vort. de parede

# --- Poisson da funcao corrente:  K psi = M w  ---
# Escoamento uniforme => psi = U*y nas paredes; saida (cc2) fica natural.
ybody = np.mean(Y[furo])             # linha de corrente que "envolve" o obstaculo
psi_dir = cc4 + cc1 + cc3 + furo
psi_val = np.zeros(npoints)
for i in cc4 + cc1 + cc3:
    psi_val[i] = U * Y[i]
for i in furo:
    psi_val[i] = U * ybody

Apsi = K.tolil()
for i in psi_dir:
    Apsi.rows[i] = [i]; Apsi.data[i] = [1.0]
psi_solve = spla.factorized(Apsi.tocsc())

# --- Transporte de vorticidade:  (M/dt + K/Re) w^{n+1} = M/dt w^n - conveccao ---
# Dirichlet em: entrada w=0, paredes livres w=0, obstaculo w=w_parede.
w_dir = cc4 + cc1 + cc3 + furo
Aw = (M / dt + (1.0 / Re) * K).tolil()
for i in w_dir:
    Aw.rows[i] = [i]; Aw.data[i] = [1.0]
w_solve = spla.factorized(Aw.tocsc())

# ---------------------------------------------------------------------
# 5) LACO TEMPORAL
# ---------------------------------------------------------------------
w     = np.zeros(npoints)   # vorticidade
wwall = np.zeros(npoints)   # vorticidade de parede (sub-relaxada)
frame = 0

for n in range(nt):
    # (a) resolve Poisson -> funcao corrente
    b = M @ w
    b[psi_dir] = psi_val[psi_dir]
    psi = psi_solve(b)

    # (b) velocidades a partir de psi:  M vx = Gy psi ,  M vy = -Gx psi
    vx = Msolve(Gy @ psi)
    vy = Msolve(-(Gx @ psi))

    # (c) vorticidade de parede consistente:  M w = K psi  (Thom/FEM)
    #     imposta com sub-relaxacao para estabilizar cantos afiados
    wall_new = Msolve(K @ psi)
    wwall[furo] = wwall[furo] + beta * (wall_new[furo] - wwall[furo])

    # (d) transporte de vorticidade (difusao implicita, conveccao explicita)
    conv = vx * (Gx @ w) + vy * (Gy @ w)
    rhs = (M / dt) @ w - conv
    rhs[cc4] = 0.0          # entrada: escoamento irrotacional
    rhs[cc1] = 0.0          # parede inferior (deslizamento livre)
    rhs[cc3] = 0.0          # parede superior (deslizamento livre)
    rhs[furo] = wwall[furo] # obstaculo: nao-deslizamento
    w = w_solve(rhs)

    if not np.isfinite(w).all():
        raise RuntimeError(f'solucao divergiu no passo {n}: reduza dt ou beta.')

    # (e) saida para ParaView (serie temporal)
    if n % nsave == 0 or n == nt - 1:
        veloc = np.column_stack((vx, vy, 0 * vx))
        meshio.write_points_cells(
            f'{outdir}/sol_{frame:04d}.vtk',
            points=np.column_stack((X, Y, 0 * X)),
            cells={'triangle6': IEN},
            point_data={'funcao_corrente': psi,
                        'vorticidade': w,
                        'vx': vx, 'vy': vy,
                        'velocidade': veloc})
        frame += 1
        print(f'passo {n:5d}  t={ (n+1)*dt:6.3f}  '
              f'max|w|={np.abs(w).max():8.2f}  max|vx|={np.abs(vx).max():6.3f}')

print(f'\nconcluido. {frame} arquivos .vtk em ./{outdir}/  (abra sol_..vtk no ParaView)')

# ---------------------------------------------------------------------
# 6) FIGURA-RESUMO (matplotlib) do ultimo instante
# ---------------------------------------------------------------------
tri = mtri.Triangulation(X, Y, IEN[:, 0:3])
fig, ax = plt.subplots(3, 1, figsize=(10, 8))
cf0 = ax[0].tricontour(tri, psi, 40, colors='k', linewidths=0.5)
ax[0].set_title('Linhas de corrente ($\\psi$)')
cf1 = ax[1].tricontourf(tri, w, 60, cmap='RdBu_r')
plt.colorbar(cf1, ax=ax[1]); ax[1].set_title('Vorticidade ($\\omega_z$)')
speed = np.sqrt(vx**2 + vy**2)
cf2 = ax[2].tricontourf(tri, speed, 40, cmap='inferno')
plt.colorbar(cf2, ax=ax[2]); ax[2].set_title('Modulo da velocidade')
for a in ax:
    a.set_aspect('equal')
plt.tight_layout()
plt.savefig('resumo_escoamento.png', dpi=120)
print('figura salva: resumo_escoamento.png')
plt.show()
