#!/bin/python3

import numpy as np
from sklearn.linear_model import LinearRegression

class RegressiveAnalysis:
    def __init__( self, x, y):

        # X is the timestamps.
        X = np.array(x).reshape( (-1, 1) )

        # Y is the prices over time.
        Y = np.array(y)


        model = LinearRegression().fit( X, Y )

        coefficient_of_determination = model.score( X, Y )

        intercept = model.intercept_
        coefficient = model.coef_

        self.prediction = intercept + coefficient * X
