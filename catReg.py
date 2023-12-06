import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats as st
import statsmodels.api as sm
from statsmodels.formula.api import ols
from bioinfokit.analys import stat


class categoricalRegression:
    'This class for dealing with categorical data for regression problem'
    def __init__(self,target_name , dataframe):
        self.target_name = target_name
        self.dataframe = dataframe

 


    def categories_values(self):
        'Count the values of each categorical'
        values_for_each_category = []
        df = self.dataframe
        for category in df[self.variable_name].unique():
            values_for_each_category.append(df[df[self.variable_name] == category][self.target_name])
        self.cate_count = len(values_for_each_category)
        return values_for_each_category




    def cate_info(self, variable_name ):
        '''That function is plot the distribtion of each category and check assumption of 
            linearity and equal variance .'''
        self.variable_name = variable_name
        
        plt.figure(figsize=(20,8))

        plt.subplot(1,3,1)
        plt.title(f'{variable_name} Histogram')
        sns.countplot(x = variable_name , data = self.dataframe, palette=("Blues_d"))

        plt.subplot(1,3,2)
        plt.title(f'{variable_name} vs Price')
        sns.boxplot(x= variable_name, y=self.target_name, data=self.dataframe,  palette=("PuBuGn") , showmeans = True)
        self.check_signifcat()


    def test_check(self , groups):
        'This function is used to check the normality and the variance homogeneity to see where we would use the parametric or non-paramertric tests'
        for group in groups:
            if  st.shapiro(group)[1] < 0.05:
                return 'non-parametric'
            else:
                pass

        p_value =  st.levene(*(groups))[1]
        if p_value < 0.05:
            return 'non-parametric'
        
        return 'parametric'

    
       
    
    def check_signifcat(self ):
        '''This fucntion is for check if the variable is significant or not'''
        groups = self.categories_values()
        test_type = self.test_check(groups)
        if test_type == 'parametric':
            if self.cate_count == 2 :
                statistics , p_value = st.ttest_ind(*(groups))
                print(f'p-value for significant difference between categories : {p_value}')
            else:
                statistics , p_value = st.f_oneway(*(groups))
                print(f'p-value for significant difference between categories : {p_value}')

        elif test_type == 'non-parametric':
            if self.cate_count == 2 :
                statistics , p_value = st.mannwhitneyu(*(groups))
                print(f'p-value for significant difference between categories : {p_value}')
            else:
                statistics , p_value = st.kruskal(*(groups))
                print(f'p-value for significant difference between categories : {p_value}')
                

            