import datetime
import configparser
import plotly.graph_objects as go

DEBUG = True

class MetaapproachModelV001:
    """Stores parameters and methods in metaapproach model.
        More information about the metaapproach here:
        https://github.com/EvgenyMashkantsev/ExistencialRiskShieldsApproach
    """

    """
    One of the main goals of this program is building model to calculate
    global security rate and predict changes according to changes of
    various parameters.
    Initial value (-1.0 or 0.0) indicates that value is not calculated.
    Global security rate supposed to be number in [0.0;1.0].
    """

    def __init__(self):
        self.current_year = datetime.date.today().year
        self.duration_in_years = 10000
        # Current values of key parameters:
        self.global_security_rate = (-1.0)
        self.depth_of_study_of_global_security = (-1.0)
        self.amount_of_measures_to_provide_global_security = (-1.0)
        self.quality_of_measures_to_provide_global_security = (-1.0)
        self.time_spent_studying_global_security = (-1.0)
        self.other_resources_spent_studying_global_security = (-1.0)
        self.technogenic_risk_from_the_security_system = (-1.0)
        self.creative_potential = (-1.0)
        self.scientific_potential = (-1.0)
        self.technological_level = (-1.0)
        self.economic_level = (-1.0)
        self.production_of_consumption_sector = (-1.0)
        self.production_of_safety_sector = (-1.0)
        self.time_before_possible_existential_catastrophe = (-1.0)
        self.influence_of_technological_level_to_scientific_potential = 0.5
        # Changes of parameters values in the current year:
        self.global_security_rate_delta = 0.0
        self.depth_of_study_of_global_security_delta = 0.0
        self.amount_of_measures_to_provide_global_security_delta = 0.0
        self.quality_of_measures_to_provide_global_security_delta = 0.0
        self.time_spent_studying_global_security_delta = 0.0
        self.other_resources_spent_studying_global_security_delta = 0.0
        self.technogenic_risk_from_the_security_system_delta = 0.0
        self.creative_potential_delta = 0.0
        self.scientific_potential_delta = 0.0
        self.technological_level_delta = 0.0
        self.economic_level_delta = 0.0
        self.production_of_consumption_sector_delta = 0.0
        self.production_of_safety_sector_delta = 0.0
        self.time_before_possible_existential_catastrophe_delta = 0.0
        # Changes of parameters values in the current year
        # (not depending on key parameters in this simulation):
        self.global_security_rate_natural_delta = 0.0
        self.depth_of_study_of_global_security_natural_delta = 0.0
        self.amount_of_measures_to_provide_global_security_natural_delta = 0.0
        self.quality_of_measures_to_provide_global_security_natural_delta = 0.0
        self.time_spent_studying_global_security_natural_delta = 0.0
        self.other_resources_spent_studying_global_security_natural_delta = 0.0
        self.technogenic_risk_from_the_security_system_natural_delta = 0.0
        self.creative_potential_natural_delta = 0.0
        self.scientific_potential_natural_delta = 0.0
        self.technological_level_natural_delta = 0.0
        self.economic_level_natural_delta = 0.0
        self.production_of_consumption_sector_natural_delta = 0.0
        self.production_of_safety_sector_natural_delta = 0.0
        self.time_before_possible_existential_catastrophe_natural_delta = 0.0
        # Chronology of key parameters values (one item - one year):
        self.global_security_rate_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.depth_of_study_of_global_security_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.amount_of_measures_to_provide_global_security_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.quality_of_measures_to_provide_global_security_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.time_spent_studying_global_security_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.other_resources_spent_studying_global_security_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.technogenic_risk_from_the_security_system_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.creative_potential_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.scientific_potential_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.technological_level_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.economic_level_delta_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.production_of_consumption_sector_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.production_of_safety_sector_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.time_before_possible_existential_catastrophe_chronology = \
            [0.0] * (self.duration_in_years + 1)
        # Chronology of change (one item - one year):
        self.global_security_rate_delta_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.depth_of_study_of_global_security_delta_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.amount_of_measures_to_provide_global_security_delta_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.quality_of_measures_to_provide_global_security_delta_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.time_spent_studying_global_security_delta_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.other_resources_spent_studying_global_security_delta_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.technogenic_risk_from_the_security_system_delta_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.creative_potential_delta_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.scientific_potential_delta_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.technological_level_delta_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.economic_level_delta_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.production_of_consumption_sector_delta_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.production_of_safety_sector_delta_chronology = \
            [0.0] * (self.duration_in_years + 1)
        self.time_before_possible_existential_catastrophe_delta_chronology = \
            [0.0] * (self.duration_in_years + 1)

    def print_current_variables_values(self):
        """No comment"""
        print("GLOBAL SECURITY RATE:",
              self.global_security_rate,
              "\nDEPTH OF STUDY OF GLOBAL SECURITY:",
              self.depth_of_study_of_global_security,
              "\nAMOUNT OF MEASURES TO PROVIDE GLOBAL SECURITY:",
              self.amount_of_measures_to_provide_global_security,
              "\nQUALITY OF MEASURES TO PROVIDE GLOBAL SECURITY:",
              self.quality_of_measures_to_provide_global_security,
              "\nTIME SPENT STUDYING GLOBAL SECURITY:",
              self.time_spent_studying_global_security,
              "\nOTHER RESOURCES SPENT STUDYING GLOBAL SECURITY:",
              self.other_resources_spent_studying_global_security,
              "\nTECHNOGENIC RISK FROM THE SECURITY SYSTEM:",
              self.technogenic_risk_from_the_security_system,
              "\nCREATIVE POTENTIAL:",
              self.creative_potential,
              "\nSCIENTIFIC POTENTIAL:",
              self.scientific_potential,
              "\nTECHNOLOGICAL LEVEL:",
              self.technological_level,
              "\nECONOMIC LEVEL:",
              self.economic_level,
              "\nPRODUCTION OF CONSUMPTION SECTOR:",
              self.production_of_consumption_sector,
              "\nPRODUCTION OF SAFETY SECTOR:",
              self.production_of_safety_sector,
              "\nTIME BEFORE POSSIBLE EXISTENTIAL CATASTROPHE:",
              self.time_before_possible_existential_catastrophe
              )

    def get_parameters_from_file(self, filename='global_parameters.cfg'):
        """If ok, returns dictionary 'variable-value'.
        Otherwise, can throw exception or just return None.
        """
        config_parser = configparser.ConfigParser()
        config_parser.read(filename)
        is_initial_values_enabled = config_parser \
            .getboolean(section='parameters',
                        option='ENABLE_THESE_INITIAL_VALUES')
        if not is_initial_values_enabled:
            print(
                """
    File with global parameters values exist but option
    ENABLE_THESE_INITIAL_VALUES is set to false.
    Global Security Explorer will try to define this values,
    but it is a serious research challenge.
                """
            )
        else:
            # GLOBAL SECURITY RATE:
            global_security_rate2 = config_parser \
                .getfloat(section='parameters',
                          option='GLOBAL_SECURITY_RATE')
            if global_security_rate2 >= 0.0:
                self.global_security_rate = global_security_rate2
            # DEPTH OF STUDY OF GLOBAL SECURITY:
            depth_of_study_of_global_security2 = config_parser \
                .getfloat(section='parameters',
                          option='DEPTH_OF_STUDY_OF_GLOBAL_SECURITY')
            if depth_of_study_of_global_security2 >= 0.0:
                self.depth_of_study_of_global_security = \
                    depth_of_study_of_global_security2
            # AMOUNT OF MEASURES TO PROVIDE GLOBAL SECURITY:
            amount_of_measures_to_provide_global_security2 = config_parser \
                .getfloat(section='parameters',
                          option='AMOUNT_OF_MEASURES_TO_PROVIDE_'
                                 'GLOBAL_SECURITY')
            if amount_of_measures_to_provide_global_security2 >= 0.0:
                self.amount_of_measures_to_provide_global_security = \
                    amount_of_measures_to_provide_global_security2
            # QUALITY OF MEASURES TO PROVIDE GLOBAL SECURITY:
            quality_of_measures_to_provide_global_security2 = config_parser \
                .getfloat(section='parameters',
                          option='QUALITY_OF_MEASURES_TO_PROVIDE_'
                                 'GLOBAL_SECURITY')
            if quality_of_measures_to_provide_global_security2 >= 0.0:
                self.quality_of_measures_to_provide_global_security = \
                    quality_of_measures_to_provide_global_security2
            # TIME SPENT STUDYING GLOBAL SECURITY:
            time_spent_studying_global_security2 = config_parser \
                .getfloat(section='parameters',
                          option='TIME_SPENT_STUDYING_GLOBAL_SECURITY')
            if time_spent_studying_global_security2 >= 0.0:
                self.time_spent_studying_global_security = \
                    time_spent_studying_global_security2
            # OTHER RESOURCES SPENT STUDYING GLOBAL SECURITY:
            other_resources_spent_studying_global_security2 = config_parser \
                .getfloat(section='parameters',
                          option='OTHER_RESOURCES_SPENT_STUDYING_'
                                 'GLOBAL_SECURITY')
            if other_resources_spent_studying_global_security2 >= 0.0:
                self.quality_of_measures_to_provide_global_security = \
                    other_resources_spent_studying_global_security2
            # TECHNOGENIC RISK FROM THE SECURITY SYSTEM:
            technogenic_risk_from_the_security_system2 = config_parser \
                .getfloat(section='parameters',
                          option='TECHNOGENIC_RISK_FROM_THE_SECURITY_SYSTEM')
            if technogenic_risk_from_the_security_system2 >= 0.0:
                self.technogenic_risk_from_the_security_system = \
                    technogenic_risk_from_the_security_system2
            # CREATIVE_POTENTIAL:
            creative_potential2 = config_parser \
                .getfloat(section='parameters',
                          option='CREATIVE_POTENTIAL')
            if creative_potential2 >= 0.0:
                self.creative_potential = creative_potential2
            # SCIENTIFIC_POTENTIAL
            scientific_potential2 = config_parser \
                .getfloat(section='parameters',
                          option='SCIENTIFIC_POTENTIAL')
            if scientific_potential2 > 0.0:
                self.scientific_potential = scientific_potential2
            # TECHNOLOGICAL LEVEL:
            technological_level2 = config_parser \
                .getfloat(section='parameters',
                          option='TECHNOLOGICAL_LEVEL')
            if technological_level2 >= 0.0:
                self.technological_level = technological_level2
            # ECONOMIC LEVEL:
            economic_level2 = config_parser \
                .getfloat(section='parameters',
                          option='ECONOMIC_LEVEL')
            if economic_level2 >= 0.0:
                self.economic_level = economic_level2
            # PRODUCTION OF CONSUMPTION SECTOR:
            production_of_consumption_sector2 = config_parser \
                .getfloat(section='parameters',
                          option='PRODUCTION_OF_CONSUMPTION_SECTOR')
            if production_of_consumption_sector2 >= 0.0:
                self.production_of_consumption_sector = \
                    production_of_consumption_sector2
            # PRODUCTION OF SAFETY SECTOR:
            production_of_safety_sector2 = config_parser \
                .getfloat(section='parameters',
                          option='PRODUCTION_OF_SAFETY_SECTOR')
            if production_of_safety_sector2 >= 0.0:
                self.production_of_safety_sector = \
                    production_of_safety_sector2
            time_before_possible_existential_catastrophe2 = config_parser \
                .getfloat(section='parameters',
                          option='TIME_BEFORE_POSSIBLE_GLOBAL_CATASTROPHE')
            # TIME BEFORE POSSIBLE EXISTENTIAL CATASTROPHE:
            if time_before_possible_existential_catastrophe2 >= 0.0:
                self.time_before_possible_existential_catastrophe = \
                    time_before_possible_existential_catastrophe2

    def run_metaapproach_simulation(self):
        """Metaapproach simulation trying to predict global variables dynamics.
        """
        years = list(range(self.current_year, self.duration_in_years + 1))
        is_science_dead = False
        is_creative_dead = False
        for year in range(self.current_year, self.duration_in_years + 1):
            self.current_year = year
            if DEBUG:
                if self.current_year == 4041:
                    print('current year is 4041')
                    pass
                if self.current_year == 4042:
                    print('current year is 4042')
                    pass
            self.scientific_potential_delta = \
                self.scientific_potential_natural_delta \
                + self.creative_potential_delta  # + self.technological_level \
#                * self.influence_of_technological_level_to_scientific_potential
            self.scientific_potential += self.scientific_potential_delta
            self.creative_potential_delta = \
                self.creative_potential_natural_delta + \
                self.scientific_potential_delta
            self.creative_potential += self.creative_potential_delta
#            self.technological_level_delta = \
#                self.technological_level_natural_delta \
#                + self.scientific_potential_delta
            self.scientific_potential_chronology[year] = \
                self.scientific_potential
            self.creative_potential_chronology[year] = \
                self.creative_potential
            self.scientific_potential_delta_chronology[year] = \
                self.scientific_potential_delta
            self.creative_potential_delta_chronology[year] = \
                self.creative_potential_delta
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years,
                                 y=self.scientific_potential_chronology,
                                 name='scientific potential'))
        fig.add_trace(go.Scatter(x=years,
                                 y=self.creative_potential_chronology,
                                 name='creative potential'))
        print("Saving results...")
        fig.write_html("metaapproach_results.html")
