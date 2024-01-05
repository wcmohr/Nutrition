import pulp as plp
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpAffineExpression, \
LpConstraint, PULP_CBC_CMD
import numpy as np

# functions list ---> CorrelationCutoff, formulateMP, checkFeasibility, infeasibilitySearch

def CorrelationCutoff(a_series, corr):
    """Take in a series with correlation values and a correlation cutoff point.
    Return the indices for which the correlations are greater than or equal to
    the cutoff."""
    return a_series[a_series.values>=corr].index

def formulateMP(foods, nutrient_constraints, servings_constraints,integer='true'):
    '''return the PuLP lp formulation for minimizing
    calories.
    
    Args --> DataFrame: foods (food types, nutrient values)
    DataFrame: nutrient_constraints (nutrients, min/max values)
    DataFrame: 
    
    '''
    
    # Decision Variables
    food_vars  = {food:
    plp.LpVariable(cat=[plp.LpInteger if integer else plp.LpContinuous][0], 
                   lowBound=servings_constraints.loc[food][0],
                   upBound=servings_constraints.loc[food][1],
                   name=f"{food}")
    for food in foods.index.values}

    # Objective Function
    min_cals = plp.LpProblem("Min_Calories",plp.LpMinimize)
    min_cals += lpSum([foods.calories[food]*food_vars[food] 
                        for food in foods.index.values])
    # Add constraints
    for c in nutrient_constraints.index:
        if not np.isnan(nutrient_constraints.loc[c][0]):
            min_cals += LpConstraint(e=lpSum([foods.loc[food,c]*food_vars[food] 
                                              for food in foods.index]),
                                 sense=plp.LpConstraintGE, 
                                 rhs=nutrient_constraints.loc[c][0],
                                 name=f'min_{c}'
                                )
        if not np.isnan(nutrient_constraints.loc[c][1]):
            min_cals += LpConstraint(e=lpSum([foods.loc[food,c]*food_vars[food] 
                                              for food in foods.index]),
                                 sense=plp.LpConstraintLE, 
                                 rhs=nutrient_constraints.loc[c][1],
                                 name=f'max_{c}'
                                )
    
    return min_cals

def checkFeasibility(foods, constraints):
    '''Formulate lp problem and return status and optimal coefficients if 
    feasible as 2-tuple'''
    
    min_cals = formulateMP(foods,constraints)
    min_cals.solve(PULP_CBC_CMD(msg=0))
    return min_cals.status, min_cals.coefficients

def infeasibilitySearch(foods, constraints):
    '''return 2d array with indices of constraints that constitute a solvable model
    and second the indices which cause an insolvable model when included.'''
    
    solvable = []
    brk_pts = []
    for i in range(0,constraints.shape[0]):
        candidates = [j for j in range(0,i+1) if j not in brk_pts]
        status = checkFeasibility(foods,constraints.iloc[candidates,:])[0]
        if (status == -1):
            brk_pts.append(i)
        else:
            solvable.append(i)
    return [solvable,brk_pts]