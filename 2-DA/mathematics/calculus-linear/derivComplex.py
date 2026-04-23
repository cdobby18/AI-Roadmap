import sympy as sp

x = sp.symbols('x')

f = 3*x**2 + 5*x + 2

derivative = sp.diff(f,x)

print("Function: ", f)
print("Derivative: ", derivative)