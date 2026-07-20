
lc = 0.1;
furo = 0.05;
Lx = 4.0;
Ly = 1.0;
rh = 0.1;
rv = 0.1;
//+
Point(1) = {0.0-Lx/2, 0.0-Ly/2, 0, lc};
Point(2) = { Lx-Lx/2, 0.0-Ly/2, 0, lc};
Point(3) = { Lx-Lx/2,  Ly-Ly/2, 0, lc};
Point(4) = {0.0-Lx/2,  Ly-Ly/2, 0, lc};
//+
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};

//+ aerofolio (pontos do NACA)
Point(5) = { 1.000340 , 0.001213 ,0, furo};
Point(6) = { 0.994409 , 0.003757 ,0, furo};
Point(7) = { 0.976723 , 0.011171 ,0, furo};
Point(8) = { 0.947599 , 0.022828 ,0, furo};
Point(9) = { 0.907583 , 0.037755 ,0, furo};
Point(11) = {0.857459 , 0.054724 ,0, furo};
Point(12) = {0.798262 , 0.072364 ,0, furo};
Point(13) = {0.731278 , 0.089264 ,0, furo};
Point(14) = {0.658036 , 0.104081 ,0, furo};
Point(15) = {0.580291 , 0.115625 ,0, furo};
Point(16) = {0.500000 , 0.122940 ,0, furo};
Point(17) = {0.419282 , 0.125380 ,0, furo};
Point(18) = {0.340356 , 0.122669 ,0, furo};
Point(19) = {0.265458 , 0.114943 ,0, furo};
Point(20) = {0.196735 , 0.102764 ,0, furo};
Point(21) = {0.136137 , 0.087072 ,0, furo};
Point(22) = {0.085318 , 0.069095 ,0, furo};
Point(23) = {0.045573 , 0.050198 ,0, furo};
Point(24) = {0.017809 , 0.031706 ,0, furo};
Point(25) = {0.002557 , 0.014728 ,0, furo};
Point(26) = {0.000000 , 0.000000 ,0, furo};
Point(27) = {0.009755 ,-0.011302 ,0, furo};
Point(28) = {0.031135 ,-0.018337 ,0, furo};
Point(29) = {0.063421 ,-0.021343 ,0, furo};
Point(30) = {0.105665 ,-0.020727 ,0, furo};
Point(31) = {0.156756 ,-0.017072 ,0, furo};
Point(32) = {0.215480 ,-0.011132 ,0, furo};
Point(33) = {0.280552 ,-0.003798 ,0, furo};
Point(34) = {0.350627 , 0.003963 ,0, furo};
Point(35) = {0.424284 , 0.011194 ,0, furo};
Point(36) = {0.500000 , 0.017060 ,0, furo};
Point(37) = {0.576144 , 0.020949 ,0, furo};
Point(38) = {0.650981 , 0.022550 ,0, furo};
Point(39) = {0.722713 , 0.021881 ,0, furo};
Point(40) = {0.789523 , 0.019268 ,0, furo};
Point(41) = {0.849648 , 0.015276 ,0, furo};
Point(42) = {0.901434 , 0.010614 ,0, furo};
Point(43) = {0.943408 , 0.006027 ,0, furo};
Point(44) = {0.974334 , 0.002198 ,0, furo};
Point(45) = {0.993279 ,-0.000331 ,0, furo};
Point(46) = {0.999660 ,-0.001213 ,0, furo};

// pontos do aerofólio
airfoilPts[] = {
  5, 6, 7, 8, 9,
  11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
  21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
  31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
  41, 42, 43, 44, 45, 46
};

// cria linhas do aerofólio
airfoilLines[] = {};

For i In {0:#airfoilPts[]-2}
  lnew = newl;
  Line(lnew) = {airfoilPts[i], airfoilPts[i+1]};
  airfoilLines[] += {lnew};
EndFor

// fecha o aerofólio: último ponto -> primeiro ponto
lnew = newl;
Line(lnew) = {airfoilPts[#airfoilPts[]-1], airfoilPts[0]};
airfoilLines[] += {lnew};

Curve Loop(1) = {3, 4, 1, 2};
Curve Loop(2) = {airfoilLines[]};

Plane Surface(1) = {1, 2};

// high order element
Mesh.ElementOrder = 2;
Mesh.SecondOrderIncomplete = 0;

Physical Curve("cc1") = {1};
Physical Curve("cc2") = {2};
Physical Curve("cc3") = {3};
Physical Curve("cc4") = {4};
Physical Curve("furo") = {airfoilLines[]};
Physical Surface("surface") = {1};
