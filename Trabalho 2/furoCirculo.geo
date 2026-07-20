
lc = 0.1;
furo = 0.05;
Lx = 2.0;
Ly = 1.0;
rh = 0.1;
rv = 0.1;
//+
Point(1) = {0.0, 0.0, 0, lc};
Point(2) = { Lx, 0.0, 0, lc};
Point(3) = { Lx,  Ly, 0, lc};
Point(4) = {0.0,  Ly, 0, lc};
//+
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};

//+
Point(5) = {1.0, 0.5, 0, furo}; //centro
Point(6) = {1.0, 0.5-rv, 0, furo};  // baixo
Point(7) = {1.0+rh, 0.5, 0, furo}; // direita
Point(8) = {1.0, 0.5+rv, 0, furo}; // cima
Point(9) = {1.0-rh, 0.5, 0, furo}; // esquerda
//+
Ellipse(5) = {6, 5, 5, 7};
Ellipse(6) = {7, 5, 5, 8};
Ellipse(7) = {8, 5, 5, 9};
Ellipse(8) = {9, 5, 5, 6};

// high order element
Mesh.ElementOrder = 2;
Mesh.SecondOrderIncomplete = 0;

//+
Curve Loop(1) = {3, 4, 1, 2};
Curve Loop(2) = {7, 8, 5, 6};
Plane Surface(1) = {1, 2};
//+
Physical Curve("cc1") = {1};
Physical Curve("cc2") = {2};
Physical Curve("cc3") = {3};
Physical Curve("cc4") = {4};
Physical Curve("furo") = {7, 8, 5, 6};
Physical Surface("surface") = {1};
