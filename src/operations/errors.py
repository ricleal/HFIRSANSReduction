import sympy as sp
import math
from collections import OrderedDict
import numpy as np


def compute(input_str, values, error_values):
    '''
    compute uncertainty

    input_str : function
    values : : {'x':[1,3,4,...], 'y':[34,5,5,6,..]}
    error_values : {'x':[1,3,4,...], 'y':[34,5,5,6,..]}
    '''

    function = sp.S(input_str)
    symbols = [str(x) for x in function.atoms(sp.Symbol)]

    # Resulting array
    error_sq = np.zeros_like(list(error_values.values())[0], dtype=np.float64)

    for symbol,error in zip(symbols,list(error_values.values())):
        deriv = sp.diff(function, symbol)
        deriv_symbols = [str(x) for x in deriv.atoms(sp.Symbol)]

        f = sp.lambdify(deriv_symbols, deriv, "numpy")
        values_to_evaluate = [values[k] for k in deriv_symbols]
        if not values_to_evaluate:
            deriv_result = f()
        else:
            deriv_result = f(*values_to_evaluate) #upack list
        #print([deriv, deriv_symbols, values_to_evaluate, temp])
        error_sq += (deriv_result * error)**2

    return np.sqrt(error_sq)


def main():
    # Testing
    input_str = 'x*x*y*y'
    values = {
     'x' : np.array([2.0]),
     'y' : np.array([3.0])
    }
    error_values = {
     'x' : np.array([0.1]),
     'y' : np.array([0.2])
    }
    v = compute(input_str, values, error_values)
    print(v)


if __name__ == "__main__":
    main()
