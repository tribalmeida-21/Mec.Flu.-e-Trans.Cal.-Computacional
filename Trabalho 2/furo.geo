
lc = 0.1;  // refino das paredes externas
lf = 0.01; // refino do furo
Lx = 2.0;
Ly = 1.0;
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
//+
Point(5) = {1, 0.8, 0, lf};
Point(6) = {0.7, 0.5, 0, lf};
Point(7) = {1, 0.2, 0, lf};
Point(8) = {1.3, 0.5, 0, lf};
//+
Line(5) = {7, 8};
Line(6) = {8, 5};
Line(7) = {5, 6};
Line(8) = {6, 7};
//+
Curve Loop(1) = {3, 4, 1, 2};
Curve Loop(2) = {7, 8, 5, 6};
Plane Surface(1) = {1, 2};

// high order element
Mesh.ElementOrder = 2;
Mesh.SecondOrderIncomplete = 0;
//+
Physical Curve("cc1") = {1};
Physical Curve("cc2") = {2};
Physical Curve("cc3") = {3};
Physical Curve("cc4") = {4};
Physical Curve("furo") = {8, 5, 6, 7};
//+
Physical Surface("surface") = {1};
