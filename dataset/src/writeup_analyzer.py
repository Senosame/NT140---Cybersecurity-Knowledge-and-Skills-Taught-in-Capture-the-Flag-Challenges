"""
MIT License

Copyright (c) 2020 Silvia Brisakova <brisakova@mail.muni.cz>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import json
import re
from statistics import mean
from statistics import median
import sys
from scipy import stats
from termgraph import termgraph as tg
import pandas as pd

# ------------------------ Names of Knowledge Units, used in displaying the results. ------------------------------ #

KU_NAMES = ['Cryptography', 'Digital Forensics', 'Data Integrity and Authentication', 'Access Control',
            'Secure Communication Protocols', 'Cryptanalysis', 'Data Privacy', 'Information Storage Security',  # KA1
            'Fundamental Principles', 'Design', 'Implementation', 'Analysis and Testing',
            'Deployment and Maintenance', 'Documentation', 'Ethics',                                            # KA2
            'Component Design', 'Component Procurement', 'Component Testing', 'Component Reverse Engineering',  # KA3
            'Physical Media', 'Physical Interfaces and Connectors', 'Hardware Architecture',
            'Distributed Systems Architecture', 'Network Architecture', 'Network Implementations', 'Network Services',
            'Network Defense',                                                                                  # KA4
            'System Thinking', 'System Management', 'System Access', 'System Control', 'System Retirement',
            'System Testing', 'Common Systems Architecture',                                                    # KA5
            'Identity Management', 'Social Engineering', 'Personal Compliance with Cybersecurity ...',
            'Awareness and Understanding', 'Social and Behavioral Privacy', 'Personal Data Privacy and Security',
            'Usable Security and Privacy',                                                                      # KA6
            'Risk Management', 'Security Governance and Policy', 'Analytical Tools', 'Systems Administration',
            'Cybersecurity Planning', 'Business Continuity, Disaster Recovery, and Incident Management',
            'Security Program Management', 'Personnel Security', 'Security Operations',                         # KA7
            'Cybercrime', 'Cyber Law', 'Cyber Ethics', 'Cyber Policy', 'Privacy'                                # KA8
            ]

# -------------------------- Names of Knowledge Areas, used in displaying the results. ---------------------------- #

KA_NAMES = ['Data Security', 'Software Security', 'Component Security', 'Connection Security',
            'System Security', 'Human Security', 'Organizational Security', 'Societal Security']


# ----------------------------------------------- Functions: ------------------------------------------------------ #

def draw_termgraph(data):
    """
    Draw graph in terminal based on the
    provided data.
    :param data: array of int arrays with data to put in the graph
                 cannot contain decimal data
    """
    labels = KA_NAMES
    normal_data = data
    len_categories = 1
    args = {'filename': 'data', 'title': None, 'width': 50,
            'format': '{:<5.2f}', 'suffix': '%', 'no_labels': False,
            'color': None, 'vertical': False, 'stacked': False,
            'different_scale': False, 'calendar': False,
            'start_dt': None, 'custom_tick': '', 'delim': '',
            'verbose': False, 'version': False}
    colors = [91]
    tg.stacked_graph(labels, data, normal_data, len_categories, args, colors)

def check_args():
    """
    Checks whether an additional argument was specified when executing this script.
    The first argument should specify path to the folder containing writeups in TXT format.
    If the folder path is provided, it must be correct - the folder must exists.
    If the folder path is not provided, this script will use writeups in the
    default folder. (../data)
    """
    if len(sys.argv) > 1:
        firstarg = sys.argv[1]
        if os.path.isdir(firstarg):
            os.chdir(firstarg)
        else:
            print("Provided folder does not exist, aborting.")
            sys.exit()
    else:
        if not os.path.isdir('../data'):
            os.mkdir('../data')
        os.chdir('../data')


def perform_anderson_darling_test(data_matrix):
    """
    Perform Anderson-Darling normality test on given dataset and print the results
    :param data_matrix: measured values, a matrix
    :return: None
    """
    all_values = []
    for row in data_matrix:
        for value in row:
            all_values.append(value)
    print('Anderson-Darling test on the data:')
    anderson_stat, crit, sig = stats.anderson(all_values, dist='norm')
    print(anderson_stat, crit, sig)


def perform_mann_whitney_u_test(sample1, sample2):
    """
    Perform Mann-Whitney U test on the two provided samples and print the results
    :param sample1: list of numbers
    :param sample2: list of numbers
    :return: None
    """
    print('Mann-Whitney U test results:')
    stat_value, p_value = stats.mannwhitneyu(sample1, sample2)
    print('U =', stat_value, 'p =', p_value)


def perform_kruskal_wallis_test(observations_matrix):
    """
    Perform Kruskal-Wallis test on 'observations' list and print the results
    :param observations_matrix: list containing lists of measurements
    :return: None
    """
    stat_value, p_value = stats.kruskal(*observations_matrix)
    print('Kruskal-Wallis test results:')
    print('x^2 =', stat_value, 'p =', p_value)


def sum_matrix_cols(matrix):
    """
    Sum the values of columns of the matrix
    Source: https://stackoverflow.com/a/23145759
    :return: a list containing sums of each column
    """
    return [sum(col) for col in zip(*matrix)]


def normalize(rows):
    """
    Normalize given lists contained in rows
    :param rows: list of lists to normalize
    :return: normalized input rows
    """
    normalized = []
    for row in rows:
        row_sum = sum(row)
        if row_sum != 0:
            norm_row = [number / row_sum for number in row]
            normalized.append(norm_row)
    return normalized


def find_max(TF_list):
    """
    Find maximum value and its position in TF_list
    :param TF_list: a list
    :return: max = maximal value in TF_list
             pos = position of the max item
    """
    max_value = -1
    pos = -1
    num_of_items = len(TF_list)
    for i in range(num_of_items):
        if TF_list[i] > max_value:
            max_value = TF_list[i]
            pos = i
    return max_value, pos

def count_not_found_keywords(matrix):
    """
    Calculate the total number of keywords that
    were not matched in any of the provided writeups.
    """
    keyword_found = False
    n_of_keywords = len(matrix[0])
    not_found_keywords = 0
    for i in range(0, n_of_keywords):
        keyword_found = False
        for row in matrix:
            if row[i] != 0:
                keyword_found = True
        if keyword_found is not True:
            not_found_keywords += 1
    return not_found_keywords

def print_stats(start_year, end_year):
    """
    Calculate and display the following statistics for all writeups posted:
    minimal, maximal, average and median length of writeups
    where length = number of characters in the writeup
    Separate statistics are printed for Jeopardy, Attack-Defense and all writeups together.
    :return: None
    """
    all_lengths, jeop_lengths, ad_lengths = [], [], []
    lengths_list = [all_lengths, jeop_lengths, ad_lengths]
    rows = [[], [], []]

    for year in range(start_year, end_year + 1):
        for game_format in ['Jeopardy', 'Attack-Defense']:
            path = os.path.join('writeups', str(year), game_format)
            writeups = os.listdir(path) if os.path.exists(path) else []

            for writeup in writeups:
                with open(os.path.join(path, writeup), "r", encoding="utf-8") as file:
                    writeup_length = len(file.read())
                if game_format == 'Jeopardy':
                    jeop_lengths.append(writeup_length)
                else:
                    ad_lengths.append(writeup_length)
                all_lengths.append(writeup_length)

    print('len all:', len(all_lengths), 'len jeop:', len(jeop_lengths), 'len ad:', len(ad_lengths))
    for j in range(3):
        rows[j].append(min(lengths_list[j]))
        rows[j].append(max(lengths_list[j]))
        rows[j].append(mean(lengths_list[j]))
        rows[j].append(median(lengths_list[j]))

    print(pd.DataFrame(rows,
                       index=['All', 'Jeopardy', 'Attack-Defense'],
                       columns=['min', 'max', 'mean', 'median']))

def check_if_abbreviation(abbreviation, writeup_str):
    """
    Check whether abbreviation is in the provided writeup and
    return the number of occurrences of it
    :param abbreviation: keyword we are looking for
    :param writeup_str: writeup content data
    :return: number of occurrences of the abbreviation in writeup_str
    """
    matches = 0
    if abbreviation.lower() in writeup_str:
        # get iterators to all found keyword matches in the writeup
        iters = [m.start() for m in re.finditer(abbreviation.lower(), writeup_str)]
        for i in iters:
            if i == 0:
                # found a keyword match at the start of the file
                if len(abbreviation) < len(writeup_str):
                    if not (writeup_str[len(abbreviation)]).isalpha():
                        matches += 1
                elif len(abbreviation) == len(writeup_str):
                    matches = matches + 1
            elif i == (len(writeup_str) - len(abbreviation)):
                # found a keyword match at the end of the file
                if not writeup_str[i - 1].isalpha():
                    matches = matches + 1
            else:
                if not (writeup_str[i - 1]).isalpha() and not (writeup_str[i + len(abbreviation)]).isalpha():
                    # found a keyword match in the middle of the file
                    matches = matches + 1
    return matches


def find_keyword_matches(data, writeup_str, keyword_TF_matrix):
    """
    Look for keywords defined by data in writeup_str and
    put the number of the occurrences of each keyword into keyword_TF_matrix.
    :param data: content of keyword.json file
    :param writeup_str: text in which we look for the keywords
    :param keyword_TF_matrix: matrix with the keyword occurrences, writeup x keyword TF
    :return:
    """
    KU_num_of_keywords = []
    writeup_str = writeup_str.lower()
    row = []
    for knowledge_area in data:
        for knowledge_unit in knowledge_area['Knowledge Units']:
            keywords_num_in_KU = 0
            for topic in knowledge_unit['topics']:
                for keyword in topic['keywords']:
                    keywords_num_in_KU += 1
                    keyword_matches = 0
                    # is the keyword an abbreviation?
                    if any(letter.isupper() for letter in keyword) and len(keyword) < 5:
                        keyword_matches += check_if_abbreviation(keyword, writeup_str)
                    # keyword is not an abbreviation
                    elif keyword.lower() in writeup_str:
                        # get iterators to all found keyword matches in the writeup
                        iters = [m.start() for m in re.finditer(keyword.lower(), writeup_str)]
                        keyword_matches = keyword_matches + len(iters)
                    row.append(keyword_matches)
            KU_num_of_keywords.append(keywords_num_in_KU)
    keyword_TF_matrix.append(row)
    return KU_num_of_keywords

def print_matrix_stats(matrix):
    """
    Sum all the keywords find in the writeups
    and divide them by total number of keywords.
    """
    sum_of_keywords = 0
    for row in matrix:
        sum_of_keywords += sum(row)
    print('\tWe identified', sum_of_keywords, 'keywords in', len(matrix), 'writeups.')
    print('\tKeywords / writeups ratio is:', sum_of_keywords / len(matrix))

def count_keywords(condition):
    """
    Count keywords in the writeups specified by the condition
    :param condition: specifies the format and year of writeups to include
    :return keyword_TF_matrix: matrix, where each row represents writeup and contains normalized keyword occurrences
            KU_keyword_nums:  a list containing total number of keywords belong to each KU
    """
    keyword_TF_matrix = []
    for year in condition[1]:
        for game_format in condition[0]:
            path = os.path.join('writeups', str(year), game_format)
            if os.path.exists(path):
                all_files = os.listdir(path)
            else:
                all_files = []

            for file in all_files:
                with open(os.path.join(path, file), 'r', encoding='utf-8') as file:
                    writeup_str = file.read()
                with open('keywords.json') as keywords:
                    data = json.load(keywords)

                KU_keyword_nums = find_keyword_matches(data, writeup_str, keyword_TF_matrix)

    print_matrix_stats(keyword_TF_matrix)
    keyword_TF_matrix = normalize(keyword_TF_matrix)

    print('\tWe have', len(keyword_TF_matrix), 'writeups containing keywords.')
    print('\tOut of', len(keyword_TF_matrix[0]), 'keywords,', count_not_found_keywords(keyword_TF_matrix), 'were not found in any of the writeups.\n')

    perform_anderson_darling_test(keyword_TF_matrix)
    return keyword_TF_matrix, KU_keyword_nums


def build_KU_TFs_matrix(matrix, KU_keyword_nums):
    """
    Groups TFs of keywords to KUs
    The number of columns of the matrix is reduced from 1639 to 55
    :param matrix: matrix writeup X keyword matches
    :param KU_keyword_nums: list containing numbers specifying how many keywords belong to each KU,
           len(KU_keyword_nums) = number of KUs
    :return: matrix writeup x KU TFsums
    """
    KU_matrix = []
    # count TFs
    for row in matrix:
        start = 0
        end = 0
        KU_row = []
        for i in range(55):
            end = end + (KU_keyword_nums[i])
            KU_row.append(sum(row[start:end]))
            start += KU_keyword_nums[i]
        KU_matrix.append(KU_row)

    return KU_matrix


def build_KU_and_KA_TF_sums(matrix):
    """
    Calculate the TF sums for KUs across all writeups
    writeups == rows in matrix
    then normalize the results: divide all TF sums by the number of writeups
    :param matrix: writeup x KU TFs
    :return: norm_KU_results: a list containing 55 values,
                              each representing TF sum for the corresponding KU TFs
             KA_results:      a list containing 8 values,
                              each representing TF sum for the corresponding KA TFs
    """
    # count TFs of all KUs across the writeups
    KU_results = sum_matrix_cols(matrix)
    # normalize the row by dividing it by number of writeups
    norm_KU_results = [float(tf) / len(matrix) for tf in KU_results]

    KA_results = [sum(norm_KU_results[0:8]), sum(norm_KU_results[8:15]), sum(norm_KU_results[15:19]),
                  sum(norm_KU_results[19:27]), sum(norm_KU_results[27:34]), sum(norm_KU_results[34:41]),
                  sum(norm_KU_results[41:50]), sum(norm_KU_results[50:54]) + norm_KU_results[54]]
    return norm_KU_results, KA_results


def print_KU_rankings(TF_list):
    """
    Print the distribution of Knowledge Units in the writeups in descending order
    :param list: list containing Term Frequency sums for KUs
    :return: None
    """
    tmp_list = TF_list.copy()
    print('-' * 120)
    print('Analysis results:\n')
    print('Knowledge Units displayed from the most frequent to the least freque:\n')
    for j in range(1, 56):
        top_first, position = find_max(tmp_list)
        print('\t', j, ':', top_first, ' ', KU_NAMES[position])
        tmp_list[position] = -1
    print('-' * 120)


def print_KA_rankings(KA_values):
    """
    Print distribution of Knowledge Areas in the writeups in descending order
    :param list: list containing Term Frequency sums for KAs
    :return: None
    """
    data_values = []
    print('Knowledge Areas results:\n')
    for value in KA_values:
        data_values.append([value*100])
    draw_termgraph(data_values)

    average = mean(KA_values)
    print('\nAverage of the KA TFs =', average)
    print('Median of the KA TFs =', median(KA_values), '\n')
    print('-' * 120)


def get_results(condition):
    """
    Print KU and KA distribution for writeups specified by the condition
    :param condition: specifies format and year of writeups included in analysis
    :return: list matrix with TF values for keywords
    """
    # needs reworking, looks chaotic and random
    keyword_TF_matrix, KU_keyword_nums = count_keywords(condition)
    KU_TFs_matrix = build_KU_TFs_matrix(keyword_TF_matrix, KU_keyword_nums)
    KU_TF_sums, KA_TF_sums = build_KU_and_KA_TF_sums(KU_TFs_matrix)
    print_KU_rankings(KU_TF_sums)
    print_KA_rankings(KA_TF_sums)
    return KU_TF_sums, KA_TF_sums

def fill_array(start_num, end_num):
    array = []
    for year in range(start_num, end_num + 1):
        array.append(year)
    return array


def start_analysis(start_year, end_year):
    """
    Starts the analysis, print results required for each Research Question, and perform statistical tests
    :return: None
    """
    print('All ready and set.')
    print('-' * 120)
    print('Calculating statistics of the writeups.')
    print_stats(start_year, end_year)
    print('-' * 120)
    print('Starting the analysis.')

    # Get KA and KU distribution for all writeups from start_year to end_year.
    print('1RQ - Term Frequency for all KUs and KAs.\n')
    print('Calculating TF values for all writeups...\n')
    both_formats = ['Jeopardy', 'Attack-Defense']
    condition = (both_formats, fill_array(start_year, end_year))
    get_results(condition)

    # Get KA and KU distribution for Jeopardy and Attack-Defense writeups separately.
    print('2RQ - Jeopardy and Attack-Defense distribution.')
    jeop_and_ad_KU_TFs = []
    jeop_and_ad_KA_TFs = []
    conditions = [(['Jeopardy'], fill_array(start_year, end_year)),
                  (['Attack-Defense'], fill_array(start_year, end_year))]
    for cond in conditions:
        print('\nCalculating TF values for', cond[0][0], 'writeups...\n')
        res_KU, res_KA = get_results(cond)
        jeop_and_ad_KU_TFs.append(res_KU)
        jeop_and_ad_KA_TFs.append(res_KA)
    # Perform Mann-Whitney U test on KU distribution.
    perform_mann_whitney_u_test(jeop_and_ad_KU_TFs[0], jeop_and_ad_KU_TFs[1])

    # Get KA and KU distribution for writeups in each year from 2012 to 2019.
    print('3RQ - distribution over the years 2012-2019\n')
    KU_TFs_by_year = []
    KA_TFs_by_year = []
    conditions = []
    for year in range(start_year, end_year + 1):
        conditions.append((both_formats, [year]))
    for cond in conditions:
        print('\nCalculating TF values for writeups from year:', cond[1][0])
        res_KU, res_KA = get_results(cond)
        KU_TFs_by_year.append(res_KU)
        KA_TFs_by_year.append(res_KA)
    # Perform Kruskal-Wallis test on KUs and then on KAs.
    perform_kruskal_wallis_test(KU_TFs_by_year)
    perform_kruskal_wallis_test(KA_TFs_by_year)

    print('\nAnalysis finished.')

if __name__ == '__main__':
    check_args()
    start_analysis(2012, 2020)
