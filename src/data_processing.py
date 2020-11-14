import os
import pandas as pd
from config import data_path


def clean_mordred_data():
    #import all data sets from specified data path
    df1 = pd.read_csv(os.path.join(data_path,"compound_set1.csv"),low_memory=False)
    df2 = pd.read_csv(os.path.join(data_path,"compound_set2.csv"),low_memory=False)
    df3 = pd.read_csv(os.path.join(data_path, "compound_set3.csv"),low_memory=False)
    #make sure dataframes are same size
    assert list(df1.columns) == list(df2.columns) == list(df3.columns)
    #generate one large dataframe from individual dataframes
    df = pd.concat([df1, df2, df3], ignore_index=1)

    # drop useless indices
    df = df.drop('Unnamed: 0', axis=1)
    df = df.drop('Lipinski', axis=1)
    df = df.drop('GhoseFilter', axis=1)

    # extract only columns with numerical data
    df=df._get_numeric_data()

    #remove all rows and columns with NaN
    df = df.dropna(axis=1)
    df = df.dropna(axis=0)

    # loc gets rows/columns with particular labels from the index
    #iloc gets rows/columns at particular positions
    # extract the key predictors (17 columns) for our dependent variables
    mordred_y = df.iloc[:, df.columns.get_loc('nAromAtom'):df.columns.get_loc('nX') + 1]
    mordred_y = mordred_y.drop('nSpiro', axis=1)
    mordred_y = mordred_y.drop('nBridgehead', axis=1)

    # leave the remaining descriptors  as explanatory variables
    mordred_x = df.drop(df.columns[df.columns.get_loc('nAromAtom'):df.columns.get_loc('nX') + 1], axis=1)

    #Convert to array and return all elements except for last column
    return mordred_x.to_numpy()[:-1], mordred_y.to_numpy()[:-1]