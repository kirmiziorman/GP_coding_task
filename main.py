import os
import inflection
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from exception_classes.exception_classes import *
from validation_checks.validation_checks import *

PEOPLE_INPUT_DATA_PATH = './input_data/people/'
ACTIVITIES_INPUT_DATA_PATH = './input_data/activities/'
PRACTICES_INPUT_DATA_PATH = './input_data/practices/'

REQ_PEOPLE_COLUMNS = {'FirstName', 'LastName', 'DateOfBirth', 'PersonID'}
REQ_ACTIVITIES_COLUMNS = {'ActivityCode', 'ActivityDescription'}
REQ_PRACTICES_COLUMNS = {'ActivityCode', 'ActivityDescription', 'FirstName', 'LastName'}


###############################################
# Ingestion, cleaning, and validation processes
###############################################

def clean_validate_people_data(data_path, file, required_columns):
    """
    Reads the People dataset, confirms that all required columns 
    are present, cleans string columns, confirms that columns are
    in correct data format
    """

    df = pd.read_csv(data_path + file, dtype=object)

    if not required_columns.issubset(set(df.columns)):
        raise ColumnNameError(dataset=file)

    for column in df.columns:
        df[column] = df[column].str.strip().str.lower()

    if not name_alph_check(df['FirstName']):
        raise FirstNameError(dataset=file)
    
    if not name_alph_check(df['LastName']):
        raise LastNameError(dataset=file)
    
    if not dob_datetime_check(df['DateOfBirth']):
        raise DateOfBirthError(dataset=file)

    if not id_unique_int_check(df['PersonID']):
        raise UniqueIntError(dataset=file, column_name='PersonID')

    return df


def clean_validate_activities_data(data_path, file, required_columns):
    """
    Reads the Activities dataset, corrects specific header name problem,
    confirms that all required columns are present, cleans string 
    columns, confirms that columns are in correct data format
    """
    
    df = pd.read_csv(data_path + file, dtype=object)

    df.columns = 'Activity' + df.columns
    if not required_columns.issubset(set(df.columns)):
        raise ColumnNameError(dataset=file)

    for column in df.columns:
        df[column] = df[column].str.strip().str.lower()

    if not id_unique_int_check(df['ActivityCode']):
        raise UniqueIntError(dataset=file, column_name='ActivityCode')

    return df


def clean_validate_practices_data(data_path, required_columns, activities_df):
    """
    Reads the Practices datasets, applies CamelCase on the headers,
    concatenates into one dataframe, cleans missing values,
    confirms that all required columns are present, cleans string 
    columns, confirms that columns are in correct data format
    """
    
    df_list = []
    for file in os.listdir(data_path):
        df = pd.read_csv(data_path + file, dtype=object)
        df.columns = [inflection.camelize(i) for i in df.columns]
        df_list.append(df)

    union_df = pd.concat(df_list)
    union_df = union_df.dropna(axis=0, how='all')
    union_df = union_df.dropna(axis=1, how='all')
    union_df = union_df.reset_index(drop=True)

    # Dictionaries linking activity codes and descriptions from Activities dataset
    activity_code_description_dict = dict(activities_df.values)
    activity_description_code_dict = {v: k for k, v in activity_code_description_dict.items()}

    # Fills in missing Description values by mapping from above Code-Description dictionary
    union_df['ActivityDescription'] = np.where(union_df['ActivityDescription'].isnull(),
                                               union_df['ActivityCode'].map(activity_code_description_dict),
                                               union_df['ActivityDescription'])

    # Fills in missing Code values by mapping from above Description-Code dictionary
    union_df['ActivityCode'] = np.where(union_df['ActivityCode'].isnull(),
                                        union_df['ActivityDescription'].map(activity_description_code_dict),
                                        union_df['ActivityCode'])
    
    if not required_columns.issubset(set(union_df.columns)):
        raise ColumnNameError(dataset=file)

    for column in union_df.columns:
        union_df[column] = union_df[column].str.strip().str.lower()

    if not name_alph_check(union_df['FirstName']):
        raise FirstNameError(dataset=file)
    
    if not name_alph_check(union_df['LastName']):
        raise LastNameError(dataset=file)
    
    return union_df

###############################################
# Data visualisation processes
###############################################

def print_dataframes(df_dict):
    """Prints dataframes and their titles"""

    for name, df in df_dict.items():
        print(f'cleaned_and_validated_{name}:\n')
        print(df)
        print('*'*50)


def print_heatmap(df):
    """Prints a patient-treatmap with treatment count values left in"""

    heatmap_df = df.pivot_table(values='Count', index=['FirstName','LastName'], columns='ActivityDescription')

    plt.figure(figsize=(12,5))
    axr = sns.heatmap(heatmap_df, cmap='Greens', annot=True, linewidths=0.5, cbar=False)
    axr.tick_params(top=False, bottom=False, left=False)
    plt.show()


def produce_summary(people_df, activities_df, practices_df):
    """
    Combines cleaned and validated input datasets to produce a complete dataframe
    counting the number of times (incl. zero times) each patient in the sample received 
    a particular treatment
    """

    count_df = people_df.merge(activities_df, how='cross') # Cartesian product of sample patients-activity
    count_df['Count'] = (practices_df.value_counts(['FirstName','LastName','ActivityDescription']) # Fills in count from Practices data
                                     .reindex(pd.MultiIndex.from_frame(count_df[['FirstName','LastName','ActivityDescription']]), fill_value=0)
                                     .values)
    count_df = count_df.set_index(['FirstName','LastName','DateOfBirth','PersonID','ActivityCode'])
    
    print_dataframes({'summary_df': count_df})
    print_heatmap(count_df)

###############################################
# Main
###############################################

def main():

    df_dict = {}

    df_dict['people_df'] = clean_validate_people_data(data_path=PEOPLE_INPUT_DATA_PATH, 
                                                      file='PersonTable.csv',
                                                      required_columns=REQ_PEOPLE_COLUMNS)
    
    df_dict['activities_df'] = clean_validate_activities_data(data_path=ACTIVITIES_INPUT_DATA_PATH, 
                                                              file='ActivityCodeLookup.csv',
                                                              required_columns=REQ_ACTIVITIES_COLUMNS)
    
    df_dict['practices_df'] = clean_validate_practices_data(data_path=PRACTICES_INPUT_DATA_PATH, 
                                                            required_columns=REQ_PRACTICES_COLUMNS,
                                                            activities_df=df_dict['activities_df'])

    print_dataframes(df_dict)

    produce_summary(people_df=df_dict['people_df'],
                    activities_df=df_dict['activities_df'],
                    practices_df=df_dict['practices_df'])

if __name__ == "__main__":
    main()
