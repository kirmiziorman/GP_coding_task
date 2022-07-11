import numpy as np
import pandas as pd
from validation_checks.validation_checks import *

def test_name_alph():
    input_data = np.array(['Pierce','Daniel','Sean7'])
    input_df = pd.DataFrame(columns=['Name'],
                            data=input_data)
    
    assert name_alph_check(input_df['Name']) == False

def test_dob_datetime():
    input_data = np.array(['01/01/2022','02/02/2022','13/13/2022'])
    input_df = pd.DataFrame(columns=['Date'],
                            data=input_data)
    
    assert dob_datetime_check(input_df['Date']) == False

def test_id_all_numerical():
    input_data = np.array(['1','2','a'])
    input_df = pd.DataFrame(columns=['ID'],
                            data=input_data)
    
    assert id_unique_int_check(input_df['ID']) == False

def test_id_no_floats():
    input_data = np.array(['1','2','3.1'])
    input_df = pd.DataFrame(columns=['ID'],
                            data=input_data)
    
    assert id_unique_int_check(input_df['ID']) == False

def test_id_all_unique():
    input_data = np.array(['1','2','3','3'])
    input_df = pd.DataFrame(columns=['ID'],
                            data=input_data)
    
    assert id_unique_int_check(input_df['ID']) == False
