
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
Point(5) = {  1.000000, 0.001260  ,0, furo};
Point(6) = {  0.993844, 0.002120  ,0, furo};
Point(7) = {  0.975528, 0.004642  ,0, furo};
Point(8) = {  0.945503, 0.008658  ,0, furo};
Point(9) = {  0.904508, 0.013914  ,0, furo};
Point(11) = { 0.853553, 0.020107  ,0, furo};
Point(12) = { 0.793893, 0.026905  ,0, furo};
Point(13) = { 0.726995, 0.033962  ,0, furo};
Point(14) = { 0.654508, 0.040917  ,0, furo};
Point(15) = { 0.578217, 0.047383  ,0, furo};
Point(16) = { 0.500000, 0.052940  ,0, furo};
Point(17) = { 0.421783, 0.057148  ,0, furo};
Point(18) = { 0.345492, 0.059575  ,0, furo};
Point(19) = { 0.273005, 0.059848  ,0, furo};
Point(20) = { 0.206107, 0.057714  ,0, furo};
Point(21) = { 0.146447, 0.053083  ,0, furo};
Point(22) = { 0.095492,  0.046049 ,0, furo};
Point(23) = { 0.054497,  0.036867 ,0, furo};
Point(24) = { 0.024472,  0.025893 ,0, furo};
Point(25) = { 0.006156,  0.013503 ,0, furo};
Point(26) = { 0.000000,  0.000000 ,0, furo};
Point(27) = { 0.006156, -0.013503 ,0, furo};
Point(28) = { 0.024472, -0.025893 ,0, furo};
Point(29) = { 0.054497, -0.036867 ,0, furo};
Point(30) = { 0.095492, -0.046049 ,0, furo};
Point(31) = { 0.146447, -0.053083 ,0, furo};
Point(32) = { 0.206107, -0.057714 ,0, furo};
Point(33) = { 0.273005, -0.059848 ,0, furo};
Point(34) = { 0.345492, -0.059575 ,0, furo};
Point(35) = { 0.421783, -0.057148 ,0, furo};
Point(36) = { 0.500000, -0.052940 ,0, furo};
Point(37) = { 0.578217, -0.047383 ,0, furo};
Point(38) = { 0.654508, -0.040917 ,0, furo};
Point(39) = { 0.726995, -0.033962 ,0, furo};
Point(40) = { 0.793893, -0.026905 ,0, furo};
Point(41) = { 0.853553, -0.020107 ,0, furo};
Point(42) = { 0.904508, -0.013914 ,0, furo};
Point(43) = { 0.945503, -0.008658 ,0, furo};
Point(44) = { 0.975528, -0.004642 ,0, furo};
Point(45) = { 0.993844, -0.002120 ,0, furo};
Point(46) = { 1.000000, -0.001260 ,0, furo};

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
