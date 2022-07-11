import pandas as pd

def name_alph_check(name_column):
    """Check if dataframe column contains only alphabetic strings"""

    return name_column.str.isalpha().all()


def dob_datetime_check(dob_column):
    """
    Check if dataframe column contains only strings
    that can be converted to day-month-year datetime objects
    """

    dob_column = pd.to_datetime(dob_column, errors='coerce', format='%d/%m/%Y')
    
    return not dob_column.isnull().values.any()


def id_unique_int_check(id_column):
    """
    Check if dataframe column contains only strings
    that can be converted to unique integer values
    and are not floats
    """

    id_int_column = pd.to_numeric(id_column, errors='coerce')
    
    if id_int_column.isnull().values.any() == True: # one or more values cannot be converted to ints
        return False

    if sum(id_int_column % 1) > 0: # one of more values is a float
        return False

    if id_column.is_unique == False: # not all values are unique
        return False

    return True