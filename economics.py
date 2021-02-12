import datetime
import numpy as np


class EconomicModel:
    # TODO: add getting reliable global gross domestic product for any year
    def __init__(self):
        self.initial_gross_domestic_product = 1.0
        self.global_gross_domestic_product = 0.0
        self.consumption_percentage = 0.0
        self.production_of_consumption_sector = 0.0
        self.production_of_safety_sector = 0.0

    def calculate_gross_domestic_value(self, year=datetime.date.today().year):
        kondratiev_cycles = np.sin((1.0 / 51.5)) * np.float_(year)
        trend = 0.1 * year
        self.global_gross_domestic_product = \
            self.initial_gross_domestic_product + kondratiev_cycles + trend

    def calculate_all(self, year=datetime.date.today().year,
                      change_gross_domestic_product=True):
        if change_gross_domestic_product:
            self.calculate_gross_domestic_value(year)
        self.consumption_percentage = \
            min(100.0, 99.0 - self.global_gross_domestic_product / 10000.0)
        self.production_of_consumption_sector =\
            self.global_gross_domestic_product\
            * (self.consumption_percentage / 100.0)
        self.production_of_safety_sector = \
            self.global_gross_domestic_product\
            - self.production_of_consumption_sector

    def change_global_gross_domestic_product(self, new_value):
        self.global_gross_domestic_product = new_value
        self.calculate_all(change_gross_domestic_product=False)
