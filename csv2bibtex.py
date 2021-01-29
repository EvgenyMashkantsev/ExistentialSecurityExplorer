#!/usr/bin/env python3
import os
import subprocess
import datetime
import ansicolors


class BibTeX:

    def __init__(self):
        self.text = ''


class BibliographyStats:

    def __init__(self):
        self.count = 0
        self.summary_relevance = 0.0
        self.mean_year = 0.0

    def mean_relevance(self):
        return self.summary_relevance / self.count


def do_csv2bibtex(filename='ExistentialRiskBibliography.csv',
                  do_statistics=True):
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
    relevance_index = csv_head_splitted.index('Relevance')
    stats = BibliographyStats()
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
        if do_statistics:
            stats.count += 1
            stats.summary_relevance += float(splitted_line[relevance_index]
                                             .replace('"', ''))
            stats.mean_year += year
    if do_statistics:
        stats.mean_year = stats.mean_year / stats.count
        subprocess.Popen(['cp', 'BibliographyStats.csv',
                          'BibliographyStats.csv.old'])
        file_backup = open('BibliographyStats.csv.old', 'wt')
        file_backup_text = ''
        try:
            with open('BibliographyStats.csv', 'rt') as file:
                file_backup_text += file.read()
                file_backup.write(file_backup_text)
        except IOError:
            pass
        finally:
            file_backup.close()
        file = open('BibliographyStats.csv', 'wt')
        old_record = ''
        old_date = ''
        old_count = 0
        old_summary_relevance = 0.0
        old_mean_year = 0.0
        is_getting_old_record_success = 0
        if os.path.getsize('BibliographyStats.csv') != 0:
            try:
                old_record += file.readlines()[-1]
                old_record_splitted = old_record.replace('"', '').split(sep=',')
                old_date += old_record_splitted[0]
                old_count += old_record_splitted[1]
                old_summary_relevance += old_record_splitted[2]
                old_mean_year += old_record_splitted[3]
                is_getting_old_record_success += 1
            except Exception:
                pass
        else:
            statistics_csv_head = "\"" + 'Date' + "\"" + ',' \
                                  + "\"" + 'Count' + "\"" + ',' \
                                  + "\"" + 'Summary relevance' + "\"" + ',' \
                                  + "\"" + 'Mean year of publication' + "\""
            file.write(statistics_csv_head)
        if is_getting_old_record_success > 0:
            print("[||][||][||][||][||][||][||][||][||][||][||][||]")
            print('Bibliography changes in ' + filename + ' since ' + old_date
                  + ':')
            mean_relevance = stats.mean_relevance()
            old_mean_relevance = old_summary_relevance / old_count
            if stats.count > old_count:
                print(ansicolors.ANSI_GREEN + '+'
                      + str(stats.count - old_count)
                      + 'bibliographic objects' + ansicolors.ANSI_RESET)
            elif stats.count > old_count:
                print(ansicolors.ANSI_YELLOW + str(stats.count - old_count)
                      + 'bibliographic objects' + ansicolors.ANSI_RESET)
            if mean_relevance > old_mean_relevance:
                print(ansicolors.ANSI_GREEN + '+'
                      + str(stats.mean_relevance() - old_mean_relevance)
                      + 'mean relevance' + ansicolors.ANSI_RESET)
            elif mean_relevance < old_mean_relevance:
                print(ansicolors.ANSI_YELLOW
                      + str(stats.mean_relevance() - old_mean_relevance)
                      + 'mean relevance' + ansicolors.ANSI_RESET)
            if stats.mean_year > old_mean_year:
                print(ansicolors.ANSI_GREEN
                      + 'Mean year of publication increased'
                      + '(+' + str(stats.mean_year - old_mean_relevance) + ')'
                      + ansicolors.ANSI_RESET)
                print(ansicolors.ANSI_GREEN
                      + 'Mean year of publication decreased'
                      + '(' + str(stats.mean_year - old_mean_relevance) + ')'
                      + ansicolors.ANSI_RESET)
            print("[||][||][||][||][||][||][||][||][||][||][||][||]")
        new_record = "\n\"" + datetime.date.today().isoformat() + "\"" + ',' \
                     + "\"" + str(stats.count) + "\"" + ',' \
                     + str(stats.summary_relevance) + "\"" + ',' \
                     + "\"" + str(stats.mean_year) + "\""
        file.write(new_record)
    print(bibtex.text)
    return 0


do_csv2bibtex()
