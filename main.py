import csv
import sys
import os
import glob
import json
import re
from datetime import date
import pandas


def compare_files(file1, file2):
    filename = os.path.basename(file1)
    with open(file1, 'r', encoding='utf8') as file1, open(file2, 'r', encoding='utf8') as file2:
        reader1 = csv.reader(file1)
        reader2 = csv.reader(file2)

        # for row in reader1:
        #     print(row)
        contents = file1.readlines()
        participants = contents[3].split()[1].split(';')[:-1]
        participants = [i.split('@')[0] for i in participants]
        participants.append('Me')
        # print(participants)


        contents = ''.join(contents[7:])
        
        # print(contents)
        regex_str = ''
        for i in range(len(participants)):
            regex_str += participants[i]
            if i != len(participants) - 1:
                regex_str += '|'
        print(regex_str)

        contents = contents.split('Me,')
        print(contents)

        # print(re.split(regex_str, contents))
        # contents = re.split('')



        # for i in range(7):
        #     next(reader1)
        #     next(reader2)

        # file1_chat = {}
        # file2_chat = {}

        # message_num = 1
        # for row in reader1:
        #     file1_chat[message_num] = ''.join(row)
        #     message_num += 1

        # message_num = 1
        # for row in reader2:
        #     file2_chat[message_num] = ''.join(row)
        #     message_num += 1

        result_dict = {filename: 'Pass'}

        # for i in file1_chat:
        #     try:
        #         if (file1_chat[i] != file2_chat[i]):
        #             print('\n')
        #             print(filename)
        #             print('EXPECTED MESSAGE'.center(80, '-'))
        #             print(file1_chat[i])
        #             print('FOUND MESSAGE'.center(80, '-'))
        #             print(file2_chat[i])
        #             print('-' * 80)
        #             print(
        #                 f"\nError: Chat histories don't match. See row {i+7} in the Excel file.")
        #             result_dict = {filename: 'Fail'}
        #             break
        #     except Exception:
        #         print('\n')
        #         print(filename)
        #         print('EXPECTED MESSAGE'.center(80, '-'))
        #         print(file1_chat[i])
        #         print('-' * 80)
        #         print('Error: Missing messages')
        #         print(
        #             f"\nError: Chat histories don't match. See row {i+7} in the Excel file.")

        #         result_dict = {filename: 'Fail'}
    return result_dict


if __name__ == '__main__':
    results = {}

    if len(sys.argv) == 3:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
        result = compare_files(file1, file2)
        results.update(result)

    if len(sys.argv) == 1:
        if not os.path.exists('before') or not os.path.isdir('before'):
            print('Missing \'before\' directory')
            exit(1)
        if not os.path.exists('after') or not os.path.isdir('after'):
            print('Missing \'after\' directory')
            exit(1)

        csv_files = {}

        before_path = os.getcwd() + '\\before'
        for root, dirs, files in os.walk(before_path):
            dirs.clear()
            for file in files:
                if file.endswith(".csv"):
                    if file in csv_files.keys():
                        csv_files[file] = csv_files[file] + 1
                    else:
                        csv_files[file] = 1

        after_path = os.getcwd() + '\\after'
        for root, dirs, files in os.walk(after_path):
            dirs.clear()
            for file in files:
                if file.endswith('.csv'):
                    if file in csv_files.keys():
                        csv_files[file] = csv_files[file] + 1
                    else:
                        csv_files[file] = 1

        for i in csv_files:
            if csv_files[i] == 2:
                result = compare_files(
                    before_path + '\\' + i, after_path + '\\' + i)
                results.update(result)
            elif csv_files[i] == 1:
                results[i] = 'Missing second file to compare with'
            else:
                results[i] = 'Found more than 2 copies'

    print('\n\n')
    print('RESULTS'.center(50))
    print('#' * 50)
    print('Filename:'.ljust(30) + '|Chat history sync:')
    print('-' * 50)
    for key, value in results.items():
        print(key.ljust(30) + '|' + value)
    print('#' * 50)
