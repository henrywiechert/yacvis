from brain_plasma import Brain

DEATHS_TABLE_NAME = 'df_covid_deaths'
CASES_TABLE_NAME = 'df_covid_cases'


class Data(Brain):
    def __init__(self):
        # check if there is data, otherwise raise exception (or read the data ?)
        pass

    def cases(self):
        return self[CASES_TABLE_NAME]

    def deaths(self):
        return self[DEATHS_TABLE_NAME]

    def cases(countries):
        return cases[[countries]]
