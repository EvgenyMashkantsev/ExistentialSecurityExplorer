#!/usr/bin/env python3
import os
import subprocess
import datetime
import ansicolors
import pandas


class BibTeX:

    def __init__(self):
        self.text = ''


def do_csv2bibtex(filename='ExistentialRiskBibliography.csv'):
    csv_file = open(filename, 'rt')
    csv_text = csv_file.read()
    csv_file.close()
    csv_text = csv_text.splitlines()
    csv_head = csv_text[0]
    csv_head = csv_head.replace('"', '')
    csv_head_splitted = csv_head.split(',')
    authors_index = csv_head_splitted.index('Authors')
    year_index = csv_head_splitted.index('Year')
    title_index = csv_head_splitted.index('Title')
    journal_index = csv_head_splitted.index('Journal')
    volume_index = csv_head_splitted.index('Volume')
    bibtex = BibTeX()
    for line in csv_text[1::]:
        splitted_line = line.split('",')
        authors = splitted_line[authors_index].replace('"', '')
        year = int(splitted_line[year_index].replace('"', ''))
        title = splitted_line[title_index].replace('"', '')
        journal = splitted_line[journal_index].replace('"', '')
        volume = splitted_line[volume_index].replace('"', '')
        if journal != '':
            bibtex.text = bibtex.text + '@ARTICLE'
        else:
            bibtex.text = bibtex.text + '@MISC'
        void_str = ''
        bibtex_key = void_str.join(
            list(filter(lambda x: x.isalpha() or x.isspace(), title)))
        bibtex_key = bibtex_key.replace(' ', '-') + str(year)
        bibtex.text = bibtex.text + '{' + bibtex_key + ",\n"
        bibtex.text = bibtex.text + 'author = {' + authors + "},\n"
        bibtex.text = bibtex.text + 'title = {{' + title + "}},\n"
        if journal != '':
            bibtex.text = bibtex.text + 'journal = {{' + journal + "}},\n"
        if volume != '':
            bibtex.text = bibtex.text + 'volume = {' + volume + "},\n"
        bibtex.text = bibtex.text + 'year = {' + str(year) + "}\n"
        bibtex.text = bibtex.text + "}\n"
    print(bibtex.text)
    return bibtex.text


def backup_file(original_filename,
                backup_filename):
    file_backup = open(backup_filename, 'wt')
    file_backup_text = ''
    try:
        with open(original_filename, 'rt') as file:
            file_backup_text += file.read()
            file_backup.write(file_backup_text)
    except IOError:
        pass
    finally:
        file_backup.close()


def backup_bibtex_file():
    backup_file(original_filename='ExistentialRiskBibliography.bib',
                backup_filename='ExistentialRiskBibliography.bib.old')


def backup_bibliography_stats():
    backup_file(original_filename='BibliographyStats.csv',
                backup_filename='BibliographyStats.csv.old')


def make_bibliography_stats(
        input_bibliography_csv='ExistentialRiskBibliography.csv',
        output_bibliography_stats_csv='BibliographyStats.csv'):
    bibliography_date = datetime \
        .date \
        .fromtimestamp(os
                       .path
                       .getctime('ExistentialRiskBibliography.csv')).isoformat()
    input_bibliography_csv = pandas.read_csv(input_bibliography_csv)
    records_count = input_bibliography_csv['Title'].count()
    mean_year = input_bibliography_csv['Year'].mean()
    mean_relevance = input_bibliography_csv['Relevance'].mean()
    old_bibliography_stats = ''
    if not os.path.exists(output_bibliography_stats_csv):
        # It will create the file
        with open(output_bibliography_stats_csv, 'wt'):
            pass
    with open(output_bibliography_stats_csv, 'rt') as output_file:
        old_bibliography_stats += output_file.read()
    try:
        with open(output_bibliography_stats_csv, 'at') as output_file:
            statistics_csv_head = "\"" + 'Date' + "\"" + ',' \
                                  + "\"" + 'Count' + "\"" + ',' \
                                  + "\"" + 'Summary relevance' + "\"" + ',' \
                                  + "\"" + 'Mean year' + "\""
            if statistics_csv_head not in old_bibliography_stats:
                output_file.write(statistics_csv_head)
            new_record = "\n\"" + str(bibliography_date) + "\"" + ',' \
                         + "\"" + str(records_count) + "\"" + ',' \
                         + "\"" + str(mean_relevance) + "\"" + ',' \
                         + "\"" + str(mean_year) + "\""
            output_file.write(new_record)
    except IOError:
        pass


def compare_bibliography(csv_stats_filename='BibliographyStats.csv'):
    csv = pandas.read_csv(csv_stats_filename)
    record_count = csv.count()['Date']
    if record_count > 1:
        old_date = csv['Date'][record_count - 2]
        count = csv['Count'][record_count - 1]
        old_count = csv['Count'][record_count - 2]
        summary_relevance = csv['Summary relevance'][record_count - 1]
        old_summary_relevance = csv['Summary relevance'][record_count - 2]
        mean_relevance = summary_relevance / count
        old_mean_relevance = old_summary_relevance / old_count
        mean_year = csv['Mean year'][record_count - 1]
        old_mean_year = csv['Mean year'][record_count - 2]
        print("================================================")
        print('Bibliography changes in ExistentialRiskBibliography.csv since '
              + str(old_date) + ':')
        print("================================================")
        if count > old_count:
            print(ansicolors.ANSI_GREEN + '+'
                  + str(count - old_count)
                  + ' bibliographic objects' + ansicolors.ANSI_RESET)
        elif count > old_count:
            print(ansicolors.ANSI_YELLOW + str(count - old_count)
                  + ' bibliographic objects' + ansicolors.ANSI_RESET)
        if mean_relevance > old_mean_relevance:
            print(ansicolors.ANSI_GREEN + '+'
                  + str(mean_relevance - old_mean_relevance)
                  + ' mean relevance' + ansicolors.ANSI_RESET)
        elif mean_relevance < old_mean_relevance:
            print(ansicolors.ANSI_YELLOW
                  + str(mean_relevance - old_mean_relevance)
                  + ' mean relevance' + ansicolors.ANSI_RESET)
        if mean_year > old_mean_year:
            print(ansicolors.ANSI_GREEN
                  + 'Mean year of publication increased'
                  + ' (+' + str(mean_year - old_mean_relevance) + ')'
                  + ansicolors.ANSI_RESET)
            print(ansicolors.ANSI_GREEN
                  + 'Mean year of publication decreased'
                  + ' (' + str(mean_year - old_mean_relevance) + ')'
                  + ansicolors.ANSI_RESET)
        diff_subprocess = \
            subprocess.Popen(
                "diff ExistentialRiskBibliography.csv "
                "ExistentialRiskBibliography.csv.old",
                shell=True,
                stdout=subprocess.PIPE)
        out = diff_subprocess.communicate()
        print("================================================")
