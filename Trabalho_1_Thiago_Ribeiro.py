#Trabalho 1
import numpy as np
import matplotlib.pyplot as plt

# Função para chamar o gerador de malha

class Elementos:
    def __init__(self, tipo, tamanho_x, quantidade_x, tamanho_y, quantidade_y, disposicao):
        self.tipo = tipo
        self.tamanho_x = float(tamanho_x)
        self.quantidade_x = int(quantidade_x)
        self.tamanho_y = float(tamanho_y)
        self.quantidade_y = int(quantidade_y)
        self.disposicao = disposicao

    def mostrar_informacoes(self):
        print(f"Tipo do elemento: {self.tipo}")
        print(f"Tamanho do elemento em x: {self.tamanho_x}")
        print(f"Número de elementos em x: {self.quantidade_x}")
        print(f"Tamanho do elemento em y: {self.tamanho_y}")
        print(f"Número de elementos em y: {self.quantidade_y}")
        print(f"Disposição: {self.disposicao}")

    def gerar_malha_1D(self):
        if self.tipo != "1D":
            print("Este elemento não é 1D.")
            return

        L = self.tamanho_x          # comprimento total
        N = self.quantidade_x       # número de elementos

        if self.disposicao == "1":
            # N elementos -> N+1 nós
            x = np.linspace(0, L, N + 1)

        elif self.disposicao == "2":
            # pontos aleatórios no domínio + extremos
            internos = np.sort(np.random.rand(N - 1) * L)
            x = np.concatenate(([0.0], internos, [L]))

        else:
            print("Disposição inválida.")
            return

        self.malha_x = x

        print("Malha 1D (nós):")
        print(x)


        # Plot simples
        plt.figure(figsize=(6, 1))
        plt.plot(x, np.zeros_like(x), "-", linewidth=1)
        plt.plot(x, np.zeros_like(x), "o")
        plt.title(f"Malha 1D ({self.disposicao})")
        plt.xlabel("Posição X")
        plt.yticks([])
        plt.grid(True)
        for i, xi in enumerate(x):
            plt.text(
                xi,                 # posição x
                0.02,               # posição y (um pouco acima da linha)
                str(i),              # número do nó
                ha='center',
                va='bottom',
                fontsize=10
            )
        plt.show()

    def gerar_conectividade_1D(self):
        if self.tipo != "1D":
            print("Este elemento não é 1D.")
            return

        if not hasattr(self, "malha_x"):
            print("Gere a malha 1D antes de criar a conectividade.")
            return

        n_nos = len(self.malha_x)
        self.conectividade = []

        # Matriz de conectividade (n_elementos x 2)
        self.conectividade = np.zeros((n_nos - 1, 2), dtype=int)

        for e in range(n_nos - 1):
            self.conectividade[e, 0] = e
            self.conectividade[e, 1] = e + 1

        print("Conectividade 1D:")
        print(self.conectividade)

    def gerar_malha_2D(self):

        if self.tipo != "2D":
            print("Este elemento não é 2D.")
            return

        Lx, Ly = self.tamanho_x, self.tamanho_y
        Nx, Ny = self.quantidade_x, self.quantidade_y

        # Identifica tipo e disposição
        if self.disposicao == "1":
            tipo_elemento = "tri"
            aleatoria = False
        elif self.disposicao == "2":
            tipo_elemento = "quad"
            aleatoria = False
        elif self.disposicao == "3":
            tipo_elemento = "tri"
            aleatoria = True
        elif self.disposicao == "4":
            tipo_elemento = "quad"
            aleatoria = True
        else:
            print("Disposição inválida.")
            return

        # Nós
        x = np.linspace(0, Lx, Nx + 1)
        y = np.linspace(0, Ly, Ny + 1)
        X, Y = np.meshgrid(x, y)

        if aleatoria:
            hx = Lx / Nx
            hy = Ly / Ny
            ruido = 0.3 * min(hx, hy)
            X += np.random.uniform(-ruido, ruido, X.shape)
            Y += np.random.uniform(-ruido, ruido, Y.shape)

        self.X, self.Y = X, Y

        plt.figure(figsize=(6, 5))
        plt.scatter(X, Y, c='k')

        # Numeração dos nós
        npx = Nx + 1
        for j in range(Ny + 1):
            for i in range(Nx + 1):
                no = j*npx + i
                plt.text(X[j,i], Y[j,i], str(no), color='red', fontsize=8)

        conectividade = []

        for j in range(Ny):
            for i in range(Nx):

                n1 = j*npx + i
                n2 = n1 + 1
                n4 = n1 + npx
                n3 = n4 + 1

                if tipo_elemento == "quad":
                    conectividade.append([n1, n2, n3, n4])

                    xe = [X[j,i], X[j,i+1], X[j+1,i+1], X[j+1,i], X[j,i]]
                    ye = [Y[j,i], Y[j,i+1], Y[j+1,i+1], Y[j+1,i], Y[j,i]]
                    plt.plot(xe, ye, 'b-')

                elif tipo_elemento == "tri":
                    conectividade.append([n1, n2, n3])
                    conectividade.append([n1, n3, n4])

                    plt.plot([X[j,i], X[j,i+1], X[j+1,i+1], X[j,i]],
                             [Y[j,i], Y[j,i+1], Y[j+1,i+1], Y[j,i]], 'b-')
                    plt.plot([X[j,i], X[j+1,i+1], X[j+1,i], X[j,i]],
                             [Y[j,i], Y[j+1,i+1], Y[j+1,i], Y[j,i]], 'b-')

        self.conectividade = np.array(conectividade)

        plt.title(f"Malha 2D - {tipo_elemento.upper()} ({'aleatória' if aleatoria else 'uniforme'})")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.axis("equal")
        plt.grid(True)
        plt.show()

    def gerar_conectividade_2D(self):

        if self.tipo != "2D":
            print("Este elemento não é 2D.")
            return

        if not hasattr(self, "X") or not hasattr(self, "Y"):
            print("Gere a malha 2D antes da conectividade.")
            return

        Nx, Ny = self.quantidade_x, self.quantidade_y
        npx = Nx + 1

        # Identifica tipo de elemento pelo código da disposição
        if self.disposicao in ["1", "3"]:
            tipo_elemento = "tri"
        elif self.disposicao in ["2", "4"]:
            tipo_elemento = "quad"
        else:
            print("Disposição inválida.")
            return

        conectividade = []

        for j in range(Ny):
            for i in range(Nx):

                n1 = j*npx + i
                n2 = n1 + 1
                n4 = n1 + npx
                n3 = n4 + 1

                if tipo_elemento == "quad":
                    conectividade.append([n1, n2, n3, n4])

                elif tipo_elemento == "tri":
                    conectividade.append([n1, n2, n3])
                    conectividade.append([n1, n3, n4])

        self.conectividade = np.array(conectividade, dtype=int)

        print("\nConectividade 2D:")
        print(self.conectividade)


    @staticmethod
    def _area_assinada(xs, ys):
        """Área assinada de um polígono pela fórmula do cadarço (shoelace).

        O sinal indica a orientação: > 0 anti-horário (orientação correta),
        < 0 horário (elemento invertido). A área geométrica é o valor absoluto.
        Funciona para triângulos (3 vértices) e quadriláteros (4 vértices).
        """
        xs = np.asarray(xs, dtype=float)
        ys = np.asarray(ys, dtype=float)
        n = len(xs)
        soma = 0.0
        for i in range(n):
            j = (i + 1) % n
            soma += xs[i] * ys[j] - xs[j] * ys[i]
        return 0.5 * soma

    @staticmethod
    def _estatisticas(valores, rotulo):
        """Imprime e devolve as estatísticas de um vetor de medidas."""
        valores = np.asarray(valores, dtype=float)
        stats = {
            "n": len(valores),
            "total": valores.sum(),
            "min": valores.min(),
            "max": valores.max(),
            "media": valores.mean(),
            "desvio": valores.std(),
            "razao_max_min": valores.max() / valores.min() if valores.min() > 0 else np.inf,
        }
        print(f"\n--- Estatísticas de qualidade da malha ({rotulo}) ---")
        print(f"Número de elementos : {stats['n']}")
        print(f"{rotulo} total          : {stats['total']:.6f}")
        print(f"{rotulo} mínima         : {stats['min']:.6f}")
        print(f"{rotulo} máxima         : {stats['max']:.6f}")
        print(f"{rotulo} média          : {stats['media']:.6f}")
        print(f"Desvio padrão          : {stats['desvio']:.6f}")
        print(f"Razão máx/mín          : {stats['razao_max_min']:.4f}  "
              f"(1.0 = malha perfeitamente uniforme)")
        return stats

    def calcular_comprimentos_1D(self):
        """Calcula o comprimento (medida) de cada elemento 1D e as estatísticas."""
        if self.tipo != "1D":
            print("Este elemento não é 1D.")
            return
        if not hasattr(self, "conectividade"):
            print("Gere a conectividade 1D antes de calcular os comprimentos.")
            return

        x = self.malha_x
        comprimentos = np.array([abs(x[b] - x[a]) for a, b in self.conectividade])
        self.comprimentos = comprimentos

        print("\n--- Comprimento de cada elemento 1D ---")
        for e, L in enumerate(comprimentos):
            print(f"Elemento {e:>3d}: L = {L:.6f}")

        self.estatisticas_1D = self._estatisticas(comprimentos, "Comprimento")
        return comprimentos

    def calcular_areas_2D(self):
        """Calcula a área de cada elemento 2D (triângulo ou quadrilátero)
        e as estatísticas de qualidade da malha."""
        if self.tipo != "2D":
            print("Este elemento não é 2D.")
            return
        if not hasattr(self, "conectividade"):
            print("Gere a conectividade 2D antes de calcular as áreas.")
            return

        # coordenadas dos nós na numeração global (no = j*npx + i)
        x = self.X.ravel()
        y = self.Y.ravel()

        n_elem = len(self.conectividade)
        areas = np.zeros(n_elem)
        areas_assinadas = np.zeros(n_elem)

        for e, elem in enumerate(self.conectividade):
            xs = x[elem]
            ys = y[elem]
            a = self._area_assinada(xs, ys)
            areas_assinadas[e] = a
            areas[e] = abs(a)

        self.areas = areas
        self.areas_assinadas = areas_assinadas

        print("\n--- Área de cada elemento 2D ---")
        for e, A in enumerate(areas):
            print(f"Elemento {e:>3d}: A = {A:.6f}")

        self.estatisticas_2D = self._estatisticas(areas, "Área")

        # verificação: a soma das áreas deve ser igual à área do domínio
        area_dominio = self.tamanho_x * self.tamanho_y
        print(f"\nSoma das áreas   : {areas.sum():.6f}")
        print(f"Área do domínio  : {area_dominio:.6f}  "
              f"(diferença = {abs(areas.sum() - area_dominio):.2e})")

        return areas


class DadoElementos:
    def __init__(self):
        self.elementos = []

    def criar_elementos(self):
        tipo = input("Informe o tipo do elemento (1D ou 2D): ")
        if tipo == "1D":
            disposicao = input("Informe a disposição dos elementos (1 - uniforme\n 2 - aleatoria): ")
            tamanho_x = input("Informe o tamanho do elemento: ")
            quantidade_x = int(input("Informe o número de elementos: "))
            tamanho_y = 0
            quantidade_y = 0
        elif tipo == "2D":
            disposicao = input("Informe a disposição dos elementos (1 - uniforme triangular, 2 - uniforme quad, 3 - aleatoria triangular, 4 - aleatoria quad): ")
            tamanho_x = input("Informe o tamanho do elemento em x: ")
            quantidade_x = int(input("Informe o número de elementos em x: "))
            tamanho_y = input("Informe o tamanho do elemento em y: ")
            quantidade_y = int(input("Informe o número de elementos em y: "))
        else:
            print("Tipo inválido! Por favor, escolha entre '1D' ou '2D'.")
            return  # encerra a função sem continuar
        novo_elemento = Elementos(tipo, tamanho_x, quantidade_x, tamanho_y, quantidade_y, disposicao)
        self.elementos.append(novo_elemento)
        print("Elemento criado com sucesso!\n")

    def listar_elementos(self):
        if not self.elementos:
            print("Nenhum elemento criado ainda.")
        else:
            for i, e in enumerate(self.elementos, 1):
                print(f"\nElemento {i}:")
                e.mostrar_informacoes()


        # --- Execução principal ---
if __name__ == "__main__":
    gerenciador = DadoElementos()

    while True:
        print("\n--- MENU ---")
        print("1 - Criar novo elemento")
        print("2 - Listar elementos")
        print("3 - Gerar malha")
        print("4 - Analisar qualidade da malha (área/comprimento)")
        print("5 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            gerenciador.criar_elementos()
        elif opcao == "2":
            gerenciador.listar_elementos()
        elif opcao == "3":
            ultimo = gerenciador.elementos[-1]

            if ultimo.tipo == "1D":
                ultimo.gerar_malha_1D()
                ultimo.gerar_conectividade_1D()
                ultimo.calcular_comprimentos_1D()

            elif ultimo.tipo == "2D":
                ultimo.gerar_malha_2D()
                ultimo.gerar_conectividade_2D()
                ultimo.calcular_areas_2D()

        elif opcao == "4":
            if not gerenciador.elementos:
                print("Crie e gere uma malha antes de analisar a qualidade.")
            else:
                ultimo = gerenciador.elementos[-1]
                if ultimo.tipo == "1D":
                    ultimo.calcular_comprimentos_1D()
                elif ultimo.tipo == "2D":
                    ultimo.calcular_areas_2D()

        elif opcao == "5":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida, tente novamente.")
