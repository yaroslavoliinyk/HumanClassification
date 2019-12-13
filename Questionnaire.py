from Adult import  Adult
from HumanResearcher import HumanResearcher
from collections import defaultdict

class Questionnaire:
    text_len = 70
    def __init__(self, prob_d, class_d, more50k, less50k):
        # Probability dictionary.
        # Dictionary in which: number of entries is divided by
        # number of >50K earnings and <=50K earnings respectively
        # e.g. There are 6000 males who earn >50K, and overall 7000 people make >50K,
        # which means 85% males make >50K and 15% females make >50K

        # Example 1:
        # age: 22;
        # earns >50K - 0.00165; earns <=50K - 0.03

        # Example 2:
        # sex: male
        # earns >50K - 0.85; earns <=50K - 0.61
        # sex: female
        # earns >50K - 0.15; earns <=50K 0.39
        self.prob_d = prob_d
        # Class dictionary.
        # Dictionary which represents percentage of specific class

        # Example:
        # sex: male - 0.67
        # sex: female - 0.33
        self.class_d = class_d
        self.more50k = more50k
        self.less50k = less50k
        # deleting useless entries
        del self.prob_d['workclass']
        del self.prob_d['fnlwgt']
        del self.prob_d['education.num']
        del self.prob_d['capital.gain']
        del self.prob_d['capital.loss']
        del self.prob_d['hours.per.week']
        #del self.prob_d['native.country']
        #del self.prob_d['age']

        del self.class_d['workclass']
        del self.class_d['fnlwgt']
        del self.class_d['education.num']
        del self.class_d['capital.gain']
        del self.class_d['capital.loss']
        del self.class_d['hours.per.week']
        #del self.class_d['native.country']
        #del self.class_d['age']
        # deleting +-50K
        del self.prob_d['income']
        del self.class_d['income']

        result_user = self.__user_entry()
        more, less = self.__calculate(result_user)
        self.__print_result(more, less)
    def __user_entry(self):
        adult = Adult()
        self.__inner_print('')
        self.__inner_print('Program made by Yaroslav Oliinyk, 2019')
        self.__inner_print('NAIVE BAYES ALGORITHM')
        self.__inner_print('')
        self.__inner_print('You will get to know if a person makes >50K a year or <=50K a year')
        self.__inner_print('For that, please answer following questions:')
        self.__inner_print('-')
        self.__enter_values(adult)
        return adult

    # entering values. After it we can use 'adult' object
    def __enter_values(self, adult):
        for entry, values in self.class_d.items():
            self.__inner_print('Enter ' + entry)
            if(HumanResearcher.is_int(list(values)[0])):
                while True:
                    try:
                        item = self.__enter_int(adult, entry, values)
                        adult.properties[entry] = item
                        break
                    except (ValueError, IndexError) as e:
                        print('Please, enter valid value')
            else:
                if(entry=='income'):
                    continue
                while True:
                    try:
                        item = self.__enter_str(adult, entry, values)
                        adult.properties[entry] = item
                        break
                    except (ValueError, IndexError) as e:
                        print('Please, enter valid value')


    def __enter_int(self, adult, entry, values):
        val_set = sorted(set(values))
        print('Enter number between ', val_set[0], ' and ', val_set[-1])
        num = int(input())
        if (num < 17 or num > 90):
            raise ValueError('Index is less than 17')
        return num

    def __inner_print(self, text):
        remained_len = Questionnaire.text_len - len(text)
        r_len1 = remained_len // 2 if remained_len % 2 == 0 else remained_len // 2 + 1
        r_len2 = remained_len // 2
        if(remained_len > 0):
            print('-'*r_len1, text, '-'*r_len2)
        else:
            print(text)

    def __enter_str(self, adult, entry, values):
        val_set = sorted(set(values))
        print('Choose between values:')
        for i in range(len(val_set)):
            print((i+1), '. ', val_set[i])
        index = int(input())
        if(index<1):
            raise ValueError('Index is less than 1')
        return val_set[index-1]

    def __print_result(self, more, less):
        print('This person probably earns >50K with ', self.__confirmed_result(more*100), '%')
        print('This person probably earns <=50K with ', self.__confirmed_result(less*100), '%')
    def __confirmed_result(self, number):
        if(number > 100.0):
            return 99.0
        else:
            return number

    # Naive Bayes algorithm is used here
    def __calculate(self, result_user):
        p_prob_d_plus = 1
        p_prob_d_minus= 1
        p_class_d = 1
        for head, val in result_user.properties.items():
            p_prob_d_plus *= self.prob_d[head][str(val)][HumanResearcher.plus_income]
            # prointing the above value
            p_prob_d_minus *= self.prob_d[head][str(val)][HumanResearcher.minus_income]
            p_class_d *= self.class_d[head][str(val)]
        p_prob_d_plus *= self.more50k
        p_prob_d_minus *= self.less50k

        p_prob_d_plus /= p_class_d
        p_prob_d_minus /= p_class_d
        return p_prob_d_plus, p_prob_d_minus
