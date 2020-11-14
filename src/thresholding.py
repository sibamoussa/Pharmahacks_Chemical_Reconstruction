
import os

#Numerical Data Handling
import numpy as np
import pandas as pd
from sklearn.feature_selection import VarianceThreshold

#Import written code
from data_processing import clean_mordred_data
from config import *
from multi_output_regressor import run_multi_output_regressor


def find_threshold():

    #run clean data script
    X, y = clean_mordred_data()

    # regress data
    x_output = run_multi_output_regressor(X, y)
    y_output = np.array([X.shape[1]])

    n = 0
    i = 1
    x_size = X.shape[1]
    while x_size > 0 and n < 2000000:
        print("Iteration " + str(i))

        #Remove features with variance less than desired variance
        sel = VarianceThreshold(threshold=n)
        train_x = sel.fit_transform(X)
        x_size = train_x.shape[1]
        print("Removed descriptors with variance less than " + str(n) + ". X has size: " + str(x_size))

        #re-run model with removed descriptors
        x_output = np.vstack((x_output, run_multi_output_regressor(train_x, y)))

        #list the number of the descriptors resulting in variance>threshold
        y_output = np.vstack((y_output, x_size))

        #arbitrary diverging equation for variance
        n = (n + 1.2*(n+0.25))
        i = i + 1

    pd.DataFrame(x_output).to_csv(os.path.join(results_path, "x_output.csv"))
    pd.DataFrame(y_output).to_csv(os.path.join(results_path, "y_output.csv"))


if __name__ == '__main__':
    find_threshold()