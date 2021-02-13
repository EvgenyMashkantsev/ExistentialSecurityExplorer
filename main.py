"""
Global Security Explorer is program for doing research
and making comprehensive approach to the global security.

author: EvgenyMashkantsev<zande.com@gmail.com>
"""

__author__ = "EvgenyMashkantsev"
__email__ = "zande.com@gmail.com"
__version__ = "0.0.0.6"

import os
import time
import datetime
import requests
import ansicolors
import subprocess
import csv2bibtex
import metaapproach


class ResponseWrapper:
    """Class for store response and response time.
    Storing variables in class prevents shadowing.
    """

    def __init__(self, response_):
        self.response: requests.Response = response_
        self.time = datetime.datetime.utcnow()


MAX_REQUEST_ATTEMPT_COUNT = 3


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
    os.getenv('PATH')
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
    try:
        csv2bibtex.backup_file('ExistentialRiskBibliography.csv',
                               'ExistentialRiskBibliography.csv.old')
    except Exception:
        pass
    with subprocess.Popen(['bash', 'update_existential_risk_bibliography_csv.bash'],
                          stdout=subprocess.PIPE) as bibliography_subprocess:
        print(bibliography_subprocess.stdout.read().decode())
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
        csv2bibtex.compare_bibliography()
    except Exception as e:
        print(ansicolors.ANSI_RED + 'Failed to performing '
                                    'other operations with bibliography'
              + ansicolors.ANSI_RESET)
    METAAPPROACH_MODEL_V001 = metaapproach.MetaapproachModelV001()
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
    print("Running metaapproach simulation...")
    METAAPPROACH_MODEL_V001.run_metaapproach_simulation()
