n is the number of vertices in the lattice

s is the number of atomic species

xi yi zi are the coordinates of the ith vertex on the lattice

pi_j is the local potential (linear term) of the ith vertex when the jth atomic species is present

e is the number of edges

File format:
```
n s
d
x1 y1 (z1)
x2 y2 (z2)
x3 y2 (z3)
.
.
.
xn yn (zn)
p1_1 p1_2 .. p1_s
p2_1 p2_2 .. p2_s
.
.
.
pn_1 pn_2 .. pn_s
e
e1_1 e1_2 p_00 p_01 ... p_0(s-1) p_10 p_11 p_12 ... p_1(s-1) ... p_(s-1)(s-1)
e2_1 e2_2 p_00 p_01 ... p_0(s-1) p_10 p_11 p_12 ... p_1(s-1) ... p_(s-1)(s-1)
.
.
.
ev_1 ev_2 p_00 p_01 ... p_0(s-1) p_10 p_11 p_12 ... p_1(s-1) ... p_(s-1)(s-1)
```

ei_1 and ei_2 are the indices of the vertices connected by the ith edge.

For each edge, we provide p_ij, which indicates the interaction energy between ei_1 and ei_2 when the atomic species are of the ith and jth types. Note that p_ij and p_ji are the same. But are duplicated for the simplicity of presentation.
