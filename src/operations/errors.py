import sympy as sp
import math
from collections import OrderedDict
import numpy as np


class Errors(object):

    def compute(self, input_str, var_names, var_values, var_errors):
        '''
        input_str : function
        var_names : ['a','b']
        var_values : [1,3]
        var_errors : [0.1,0.2]
        '''
        # Get user function and delete old symbols

        self.function = sp.S(input_str)
        self.symbols = []

        # Get values as dict
        vals = OrderedDict({})
        for var_name, var_value in zip(var_names,var_values):
            symbol = sp.Symbol(var_name)
            vals.update({symbol : var_value})

        # Get every derivative
        derivs = []
        for symbol in vals.keys():
            derivs.append(sp.diff(self.function, symbol))

        error_sq = np.empty_like(var_values[0])
        for deriv, error in zip(derivs,var_errors):
            f = sp.lambdify(vals.keys(), deriv, "numpy")
            #temp = deriv.evalf(subs=dict(vals))
            temp = f(*vals.values())
            temp *= error
            temp *= temp
            error_sq += temp


        f = sp.lambdify(vals.keys(), self.function, "numpy")

        print("Result: {} +- {}".format(f(*vals.values()),np.sqrt(error_sq)))
e = Errors()
#e.compute("a**b",['a','b'],[2,2],[0.1,0.1])

a = np.array([1.,2.])
b = a
e.compute("a*b",['a','b'],[a,b],[np.sqrt(a),np.sqrt(b)])
