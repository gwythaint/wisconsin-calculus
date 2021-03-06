#!/usr/bin/python
# Time-stamp : Fri Nov 30 16:18:35 CST 2007 angenent

from  grapher  import *
from math import *
################################################################################
def jac(X, u, v):
  eps = 0.000001
  A = map(lambda p,q: (p-q)/eps, X(u+eps/2, v), X(u-eps/2, v))
  B = map(lambda p,q: (p-q)/eps, X(u, v+eps/2), X(u, v-eps/2))
  return A[0]*B[1]-A[1]*B[0]
def bisect(f, a, b):
  eps=0.000001
  fa, fb = f(a), f(b)
  if(fa*fb >0):
    print "\n==========NO ZERO FOUND IN BISECT.==========\n"
    return 0
  while(b-a > eps):
    c=(a+b)*0.5
    fc=f(c)
    if(fa*fc<=0):
      b, fb=c, fc
    else:
      a, fa=c, fc
  return c
def fold(t, zmin, zmax):
  return bisect(lambda z:jac(psurf, t, z), zmin, zmax)
def rad(x): return 2/(2.0+x)
def surf(t, z):
  r=rad(t)
  return [t, r*cos(z), r*sin(z)]
Pmat=[[0.6, -0.3], [0.6, 0.2], [0, 1]]
def proj(X):  #linear projection of R^3 onto R^2 
  global Pmat
  x=sum([Pmat[i][0]*X[i] for i in range(3)])
  y=sum([Pmat[i][1]*X[i] for i in range(3)])
  return [x, y]
def psurf(t,z): return proj(surf(t,z))
def drawdiscF(t):
  pp = [psurf(t, 2*i*pi/100) for i in range(101)]
  polygonF(pp, fillcolor='lightGray')
  polygonC(pp)
################################################################################

setViewBox(-1.0, -1.5, 4.0, 1.5)
openOutputFile("09surf_of_rotation",360)

#x-axis and discs
line(proj([-1,0,0]), proj([0,0,0]))
drawdiscF(0)
line(proj([0,0,0]), proj([1,0,0]))
drawdiscF(1)
drawdiscF(1.1)
line(proj([1.1,0,0]), proj([2,0,0]))
drawdiscF(2)
line(proj([2,0,0]), proj([3,0,0]))
drawdiscF(3)
line(proj([3,0,0]), proj([4,0,0]))

#the graph of f
tt= [0.1*i for i in range(31)]
linewidth(2)
polygonA([psurf(t, pi/2) for t in tt])
linewidth(1)

#the folds (edges of the projected surface)
f1 = [[t, fold(t, 0, pi)] for t in tt]
curve = [psurf(f[0], f[1]) for f in f1]
polygonA(curve)
f1 = [[t, fold(t, pi, 2*pi)] for t in tt]
curve = [psurf(f[0], f[1]) for f in f1]
polygonA(curve)

#shade
linewidth(0.5)
tt= [0.025*i for i in range(121)]
f1 = [[t, fold(t, pi, 2*pi)] for t in tt]
for f in f1:
  polygonA([psurf(f[0], f[1]-k*0.01*(4-f[0])) for k in range(21)])

#Arrows
linewidth(1)
line(proj( [0,0,0] ), proj( [0,0,1.3] ))
arrow = map(proj, [[0, -0.07, 0.83], [0, 0, 1], [0, 0.07, 0.83], [0, 0, 0.92]])
polygonF(arrow, fillcolor='black')
#polygonC(arrow)
arrow = map(proj, [[4.05,0,0], [3.8, 0.1, 0], [3.9, 0, 0], [3.8, -0.1, 0], [4.05,0,0]])
polygonF(arrow, fillcolor='black')
#polygonC(arrow)

#Annotations
annotate(proj([0, -0.25, 0.25]), [0, 0],
    "\\rotatebox{90}{$r=f(x)$}")
annotate(proj([3.5, 0, 0]), [2, 2], "$x$-axis")

closeOutputFile()


