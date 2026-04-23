import sympy as sp

x = sp.symbols('x')
f = x**3

print(sp.diff(f, x))

f = x**2 + 3*x + 1
print(sp.diff(f, x))