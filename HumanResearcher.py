import csv
from collections import defaultdict

class HumanResearcher:
    # additional methods
    @staticmethod
    def is_int(input):
        try:
            num = int(input)
        except ValueError:
            return False
        return True
    @staticmethod
    def is_float(input):
        try:
            num = float(input)
        except ValueError:
            return False
        return True

    plus_income = '>50K'
    minus_income = '<=50K'

    def __init__(self):
        # csv file with details
        self.path = 'adult.csv'
        # full number of rows
        self.row_num = self.__get_sum()
        # Number of people getting >50K
        self.plus = self.__get_p_more_less(HumanResearcher.plus_income)
        # Number of people getting <=50K
        self.minus = self.__get_p_more_less(HumanResearcher.minus_income)
        # Probability of person getting >50K
        self.p_more = self.plus/self.row_num
        # Probability of person getting <=50K
        self.p_less = self.minus/self.row_num
        # each value in each column is appended to a list
        self.columns = defaultdict(list)
        # column dictionary with +- 50K probability
        self.column_dict = {}
        # column dictionary with probability of change of getting specific class out of set
        # ex.(Race: P(White) = 0.7, P(Black) = 0.3
        self.class_column_dict = {}

    # getting number of rows
    def __get_sum(self):
        with open(self.path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            return sum(1 for i in csv_reader)

    # Getting probabilities with income more that 50K and less than 50K
    def __get_p_more_less(self, income_str):
        with open(self.path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            return sum(1 for row in csv_reader if row[14]==income_str)

    # Making blank dictionary structure with +- 50K income
    def cascade_column_dict(self):
        with open(self.path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            row = next(csv_reader)
            for r in row:
                r_set = set(self.columns[r])
                in_dict = {}
                for r_s in r_set:
                    in_dict[r_s] = {HumanResearcher.plus_income:0, HumanResearcher.minus_income:0}
                self.column_dict[r] = in_dict

    # Making blank dictionary structure with class probability dictionary
    def cascade_class_dict(self):
        with open(self.path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            row = next(csv_reader)
            for r in row:
                r_set = set(self.columns[r])
                in_dict = {}
                for r_s in r_set:
                    in_dict[r_s] = 0
                self.class_column_dict[r] = in_dict


    # Getting column dictionary with +- 50K probability
    def get_column_dict(self):
        return self.column_dict

    # Getting column dictionary with probabilities of class
    def get_class_column_dict(self):
        return self.class_column_dict

    def get_p_more(self):
        return self.p_more

    def get_p_less(self):
        return self.p_less

    # Finding minimum and maximum values for dividing into even pieces
    def __find_min_max(self, r):
        min = float('inf')
        max = float('-inf')
        for val in self.columns[r]:
            if(HumanResearcher.is_int(val)):
                val = int(val)
            elif(HumanResearcher.is_float(val)):
                val = float(val)
            if (int(val) < min):
                min = int(val)
            if (int(val) > max):
                max = int(val)
        return min, max

    # Making virtual columns from csv files
    def fill_columns(self):
        with open(self.path) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                for (k, v) in row.items():
                    self.columns[k].append(v)

    # Fulfilling dictionary +-50K with data
    # and class probability dictionary with data
    def fill_column_dicts(self):
        with open(self.path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            header = next(csv_reader)
            for row in csv_reader:
                h_num = 0
                for head in header:
                    # >50K or <=50K
                    income = row[len(row)-1]
                    self.column_dict[head][row[h_num]][income] += 1
                    self.class_column_dict[head][row[h_num]] += 1
                    h_num += 1
            self.__make_col_dict_probabilities()
            self.__make_col_class_dict_probabilities()

    def __make_col_dict_probabilities(self):
        for head, values in self.column_dict.items():
            for val, inc in values.items():
                if(inc[HumanResearcher.plus_income] == 0):
                    inc[HumanResearcher.plus_income] += 1
                if(inc[HumanResearcher.minus_income] == 0):
                    inc[HumanResearcher.minus_income] += 1
                inc[HumanResearcher.plus_income] /= self.plus
                inc[HumanResearcher.minus_income] /= self.minus


    def __make_col_class_dict_probabilities(self):
        for head, values in self.class_column_dict.items():
            for val in values:
                self.class_column_dict[head][val] /= self.row_num

