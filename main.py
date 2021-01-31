"""
Global Security Explorer is program for doing research
and making comprehensive approach to the global security.

author: EvgenyMashkantsev<zande.com@gmail.com>
"""

__author__ = "EvgenyMashkantsev"
__email__ = "zande.com@gmail.com"
__version__ = "0.0.0.2"

import os
import time
import datetime
import configparser
import requests
import ansicolors
import subprocess
import csv2bibtex


class ResponseWrapper:
    """Class for store response and response time.
    Storing variables in class prevents shadowing.
    """

    def __init__(self, response_):
        self.response: requests.Response = response_
        self.time = datetime.datetime.utcnow()


MAX_REQUEST_ATTEMPT_COUNT = 3


class MetaapproachModelV001:
    """Stores parameters and methods in metaapproach model.
        More information about the metaapproach here:
        https://github.com/EvgenyMashkantsev/ExistencialRiskShieldsApproach
    """

    """
    One of the main goals of this program is building model to calculate
    global security rate and predict changes according to changes of
    various parameters.
    Initial value (-1.0) indicates that value is not calculated.
    Global security rate supposed to be number in [0.0;1.0].
    """

    def __init__(self):
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
        self.metaapproach_scheme = \
            [["scientific_potential",
              "x+0.001",
              "creative_potential"],
             ["scientific_potential",
              "x+0.001",
              "technological_level"],
             ["time_spent_studying_global_security",
              "x+0.001",
              "depth_of_study_of_global_security"],
             ["other_resources_spent_studying_global_security",
              "x+0.001",
              "depth_of_study_of_global_security"],
             ["quality_of_measures_to_provide_global_security",
              "x-0.001",
              "technogenic_risk_from_the_security_system"],
             ["creative_potential",
              "x+0.001",
              "scientific_potential"],
             ["creative_potential",
              "x+0.001",
              "scientific_potential"],
             ["scientific_potential",
              "x+0.001",
              "technological_level"],
             ["technological_level",
              "x+0.001",
              "scientific_potential"],
             ["scientific_potential",
              "x+0.001",
              "depth_of_study_of_global_security"],
             ["scientific_potential",
              "x+0.001",
              "depth_of_study_of_global_security"],
             ]

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


def get_http_response(url, description=None, print_message=True,
                      error_message="Cannot get data from site",
                      final_error_message="Cannot get data. Gave up.",
                      filename_to_save_response=None,
                      max_attempt_count=MAX_REQUEST_ATTEMPT_COUNT,
                      time_before_retry=20
                      ):
    """Method for getting HTTP responses with additional features."""
    print(description)
    try:
        request_attempt_count = 0
        response_wrapper: ResponseWrapper = ResponseWrapper(requests.get(url))
        request_attempt_count += 1
        if print_message:
            print(response_wrapper.response.text)
        while True:
            if request_attempt_count >= max_attempt_count:
                print(final_error_message)
                break
            else:
                if response_wrapper.response.status_code is None:
                    print(error_message)
                    if time_before_retry > 0 & print_message:
                        print(
                            'Program will try again after '
                            '{} seconds'.format(time_before_retry))
                    time.sleep(time_before_retry)
                    if print_message:
                        print("Trying again...")
                    response_wrapper.response = requests.get(url)
                    request_attempt_count += 1
                    if print_message:
                        print(response_wrapper.response.text)
                    continue
                if (response_wrapper.response.status_code) is int:
                    if ((response_wrapper.response.status_code > 399) & (
                            response_wrapper.response.status_code != 403)) | \
                            (response_wrapper.response.status_code < 1):
                        print(error_message)
                        if time_before_retry > 0 & print_message:
                            print(
                                'Program will try again after '
                                '{} seconds'.format(time_before_retry))
                        time.sleep(time_before_retry)
                        if print_message:
                            print("Trying again...")
                        response_wrapper.response = requests.get(url)
                        request_attempt_count += 1
                        if print_message:
                            print(response_wrapper.response.text)
                        continue
                    elif response_wrapper.response.status_code == 403:
                        print(final_error_message)
                        break
                break
        print(response_wrapper.response)
        if filename_to_save_response is not None:
            with open('cache_GETAS.xhtml', 'wt') as file:
                file.write(response_wrapper.response.text)
    except Exception:
        print(final_error_message)
        return None
    return response_wrapper.response


def try_to_calculate_initial_global_security_rate():
    """Tries to calculate initial value of GLOBAL_SECURITY_RATE."""


if __name__ == '__main__':
    print("Global Security Explorer")
    print(ansicolors.ANSI_YELLOW +
          "WARNING: Pre Pre alpha version of program!" +
          ansicolors.ANSI_RESET)
    print(
        """
Humanity on planet Earth requires a Global Existential Threat Advisory System
(GETAS) to provide a comprehensive and effective means to disseminate
information regarding the existential threats to
global, continental, regional, national, and local human populations.
Present system provides warnings in the form of a set of graduated
'Threat Conditions' that increase as the (assessment of the) risk of
the threat increases. At each Threat Condition, divisions and agencies of
the Lifeboat Foundation are to implement a corresponding set of
'Protective Measures' to further reduce vulnerability or increase
response capability during a period of heightened alert.

This system is intended to create a common vocabulary, context, and structure
for an ongoing international, global discussion about the nature of the threats
that confront our species on planet Earth and the appropriate measures
that should be taken in response. It seeks to inform and facilitate decisions
appropriate to different levels of societal organization and to
private citizens at home and at work.
Global Security Explorer intended and seeks to this too.
        """
    )
    GETAS_LEVEL = "Unknown"
    try:
        RESPONSE_WRAPPER: ResponseWrapper = \
            ResponseWrapper(
                get_http_response(url="http://lifeboat.com/ex/getas",
                                  description="Getting GETAS status...",
                                  print_message=False,
                                  error_message="Cannot get GETAS status "
                                                "from lifeboat.com",
                                  final_error_message="Still cannot get GETAS "
                                                      "status from "
                                                      "lifeboat.com. "
                                                      "Gave up.",
                                  filename_to_save_response="cache_GETAS"
                                                            ".xhtml")
            )
        PROPOSED_GETAS_LEVEL = RESPONSE_WRAPPER.response.text \
            .partition("THREAT LEVEL:")[2] \
            .partition("href")[2] \
            .partition(">")[2].partition("</a>")[0]
        if len(PROPOSED_GETAS_LEVEL) > 2:
            PROPOSED_GETAS_LEVEL, GETAS_LEVEL = GETAS_LEVEL, \
                                                PROPOSED_GETAS_LEVEL
            print('[{} UTC] GETAS level: {}'.format(RESPONSE_WRAPPER.time,
                                                    GETAS_LEVEL))
    except Exception:
        print("Cannot print GETAS level")
    bibliography_subprocess = \
        subprocess.Popen("bash update_existential_risk_bibliography_csv.bash",
                         shell=True,
                         stdout=subprocess.PIPE)
    out = bibliography_subprocess.communicate()
    try:
        if os.path.exists('ExistentialRiskBibliography.bib'):
            print('Making reserve copy of '
                  'old existential risk BibTex bibliography...')
            csv2bibtex.backup_bibtex_file()
        print('Trying to convert new existential risk bibliography'
              ' from csv to BibTex...')
        BibTex_text = csv2bibtex.do_csv2bibtex()
        print('Converting completed. Saving results...')
        with open('ExistentialRiskBibliography.bib', 'wt') as bib_file:
            bib_file.write(BibTex_text)
        print('Saving completed.')
        print('You can use new BibTex bibliography in your research papers.')
    except Exception:
        print(ansicolors.ANSI_RED + 'Cannot convert csv to BibTex'
              + ansicolors.ANSI_RESET)
    try:
        print('Performing other operations with bibliography...')
        csv2bibtex.backup_bibliography_stats()
        csv2bibtex.make_bibliography_stats()
        csv2bibtex.compare_bibliography_stats()
    except Exception as e:
        print(ansicolors.ANSI_RED + 'Failed to performing '
                                    'other operations with bibliography'
              + ansicolors.ANSI_RESET)
    METAAPPROACH_MODEL_V001 = MetaapproachModelV001()
    try:
        print("Trying to get global variables values from local file...")
        METAAPPROACH_MODEL_V001.get_parameters_from_file()
    except Exception:
        print("Cannot get global variables values from local file")
    print("================================================")
    print('Current global variables values:')
    print("================================================")
    METAAPPROACH_MODEL_V001.print_current_variables_values()
    print("================================================")
