# Importing useful libraries
import warnings
warnings.filterwarnings('ignore')
import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
from collections import OrderedDict
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import sklearn.preprocessing as pre
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Lasso

from sklearn.ensemble import RandomForestRegressor,BaggingRegressor,GradientBoostingRegressor,AdaBoostRegressor 
from sklearn.neural_network import MLPRegressor
#import seaborn as sns
import collections
import os
from django.conf import settings


def player_prediction(training_file,input_set):
    # importing data
    data_path =  os.path.join(settings.BASE_DIR, 'data/output.csv')
    
    # Model to find the best regression model
    data_path= training_file#'data.csv'
    model_data = pd.read_csv(data_path)
    model_data.drop(['overall'], axis=1, inplace=True)
    model_data.drop('Unnamed: 0',axis=1, inplace=True)
    # model_data.drop(['player_positions'], axis=1, inplace=True)


    target_name = 'value_eur'
    #scaler = sk.preprocessing
    X = model_data[['passing', 'dribbling', 'movement_reactions', 'power_shot_power', 
    'mentality_composure', 'attacking_short_passing', 'skill_long_passing', 
    'shooting', 'goalkeeping_diving', 'mentality_vision']]
    


    y = model_data[target_name]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123) #20% test
    models = pd.DataFrame(index=['train_mse', 'test_mse'], columns=['NULL', 'MLR', 'Ridge','KNN', 'LASSO'])

    #Null Model
    y_pred_null = y_train.mean()
   
    #Linear Regression
    gbr = GradientBoostingRegressor()

    gbr.fit(X_train, y_train)
   
    estimate = gbr.predict([input_set])
    restimate = estimate / 1000000
    restimate = list(restimate)
    
    
    return restimate
 
def player_prediction2(training_file,input_set):
    from sklearn.ensemble import GradientBoostingRegressor

    # importing data
    data_path= training_file#'data.csv'

    # Model to find the best regression model
    data_path= training_file#'data.csv'
    model_data = pd.read_csv(data_path)
   
    target_name = 'overall'
    model_data.drop('Unnamed: 0',axis=1, inplace=True)

    #scaler = sk.preprocessing
    # X = model_data.drop('overall', axis=1)
    X = model_data[['passing', 'dribbling', 'movement_reactions', 'power_shot_power', 
    'mentality_composure', 'attacking_short_passing', 'skill_long_passing', 
    'shooting', 'goalkeeping_diving', 'mentality_vision']]

    y = model_data[target_name]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
    models = pd.DataFrame(index=['train_mse', 'test_mse'], columns=['NULL', 'MLR', 'Ridge','KNN', 'LASSO'])

    #Null Model
    y_pred_null = y_train.mean()
    models.loc['train_mse','NULL'] = mean_squared_error(y_pred=np.repeat(y_pred_null, y_train.size),
                                                    y_true=y_train)
    models.loc['test_mse','NULL'] = mean_squared_error(y_pred=np.repeat(y_pred_null, y_test.size),
                                                   y_true=y_test)

    linear_regression = LinearRegression()
    linear_regression.fit(X_train, y_train)
   
   
    result = linear_regression.predict([input_set])
    return list(result)
