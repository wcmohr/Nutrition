import re
import numpy as np
import pandas as pd

def format_cols(df):
    """format the columns of the foods DataFrame"""
    pattern = r'[^a-zA-Z0-9_]+'
    form_cols = [re.sub(pattern, '_', col) for col in df.columns]
    form_cols = [re.sub('_+$', '', col).lower() for col in form_cols]
    df.columns = form_cols
    return df

def float_match(float_pattern, x):
    """match the float numeric component of a string"""
    float_val = np.nan
    try:
         float_val = float(re.match(float_pattern,x)[0])
    except: 
        float_val = float(x)
    return float_val

def find_duplicate_columns(df):
    """
    Find columns with the same values in a DataFrame.
    Returns a list of column names with duplicates.
    """
    duplicate_columns = []
    for column1 in df.columns:
        for column2 in df.columns:
            if column1 != column2 and (df[column1] == df[column2]).all():
                duplicate_columns.append(column1)
                break
    return duplicate_columns

# Credit: Chat-gpt
def find_exact_matches(array1, array2):
    exact_matches = []
    for element1 in array1:
        match_found = any(element1 == element2 for element2 in array2)
        exact_matches.append(match_found)
    return exact_matches


def getUnit(vals):
    '''Take tuple of strings being either min and max vals with units or NaN 
    values and return the unit component'''
    
    for val in vals:
        try:
            return val.split(' ')[1]
        except: 
            pass
    return None

def getNumber(val):
    '''Take tuple of strings being either min and max vals with units or NaN 
    values and return the numeric component'''
    try:
        return float(val.split(' ')[0])
    except:
        return float(val)