from past.builtins import xrange

from Questionnaire import Questionnaire
from HumanResearcher import HumanResearcher


if __name__ == '__main__':
    # Creating human researcher class for
    # researching all the human entries
    hr = HumanResearcher()
    # Making virtual columns from csv files
    hr.fill_columns()
    # Making blank dictionary structure with +- 50K income
    hr.cascade_column_dict()
    # Making blank dictionary structure with class probability dictionary
    hr.cascade_class_dict()
    # Fulfilling dictionary +-50K with data
    # and class probability dictionary with data
    hr.fill_column_dicts()
    # Probability of person getting >50K
    p_more = hr.get_p_more()
    # Probability of person getting <=50K
    p_less = hr.get_p_less()
    # Getting column dictionary with probabilities of class
    class_d = hr.get_class_column_dict()
    # Column dictionary with +- 50K probability
    prob_d = hr.get_column_dict()
    # Making a specific questionnaire for a person to answer questions
    ques = Questionnaire(prob_d, class_d, p_more, p_less)
