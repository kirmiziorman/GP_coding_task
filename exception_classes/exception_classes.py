class ColumnNameError(Exception):
    def __init__(self, dataset, message="Required columns are missing"):
        self.message = message
        self.dataset = dataset
        super().__init__(self.dataset + ' - ' + self.message)

class FirstNameError(Exception):
    def __init__(self, dataset, message="FirstName column contains non-alphabetic values"):
        self.message = message
        self.dataset = dataset
        super().__init__(self.dataset + ' - ' + self.message)

class LastNameError(Exception):
    def __init__(self, dataset, message="LastName column contains non-alphabetic values"):
        self.message = message
        self.dataset = dataset
        super().__init__(self.dataset + ' - ' + self.message)

class DateOfBirthError(Exception):
    def __init__(self, dataset, message="DateOfBirth column contains values that cannot be converted to datetime"):
        self.message = message
        self.dataset = dataset
        super().__init__(self.dataset + ' - ' + self.message)

class UniqueIntError(Exception):
    def __init__(self, dataset, column_name, message="column does not contain unique integer values"):
        self.message = message
        self.dataset = dataset
        self.column_name = column_name
        super().__init__(self.dataset + ' - ' + self.column_name + ' ' + self.message)