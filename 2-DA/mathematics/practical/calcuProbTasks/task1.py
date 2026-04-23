
# TASK 1: COMPUTE DERIVATIVE USING SYMPY

import sympy as sp

x = sp.symbols('x')
f = 5*x**3 + 2*x

# Compute derivative
derivative = sp.diff(f,x)
print("Derivative: ", derivative)