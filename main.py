import csv
import sys
import os
import glob
import json


def compare_files(file1, file2):
    filename = os.path.basename(file1).split('-')[0]
    with open(file1, 'r', encoding="utf8") as file1, open(file2, 'r', encoding="utf8") as file2:
        reader1 = csv.reader(file1)
        reader2 = csv.reader(file2)

        for i in range(7):
            next(reader1)
            next(reader2)

        file1_chat = {}
        file2_chat = {}

        message_num = 1
        for row in reader1:
            file1_chat[message_num] = ''.join(row)
            message_num += 1

        message_num = 1
        for row in reader2:
            file2_chat[message_num] = ''.join(row)
            message_num += 1

        result_dict = {filename: "Pass"}

        for i in file1_chat:
            try:
                if (file1_chat[i] != file2_chat[i]):
                    print('\n')
                    print(filename.center(80, '='))
                    print('EXPECTED MESSAGE'.center(80, '-'))
                    print(file1_chat[i])
                    print('FOUND MESSAGE'.center(80, '-'))
                    print(file2_chat[i])
                    print('-' * 80)
                    print(
                        f"\nError: Chat histories don't match. See line {i+7} in the Excel file.")
                    result_dict = {filename: "Failed"}
                    break
            except Exception:
                # print()
                # print()
                # print('Filename: ' + filename)
                # print(str(i) + ': ' + file1_chat[i] + ' (expected)')
                # print('~')
                # print('Error, line not found')
                # print(
                #     '|---------------------------------------------------------------------------------------------|\n')
                result_dict = {filename: "Failed"}
    return result_dict


if __name__ == '__main__':
    results = {}

    if len(sys.argv) == 3:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
        result = compare_files(file1, file2)
        results.update(result)

    if len(sys.argv) == 1:
        csv_files = {}
        path = os.getcwd()
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".csv"):
                    filename = file.split('-')[0]
                    if filename in csv_files.keys():
                        csv_files[filename] = csv_files[filename] + 1
                    else:
                        csv_files[filename] = 1
        for i in csv_files:
            if csv_files[i] == 2:
                result = compare_files(i + '-A.csv', i + '-B.csv')
                results.update(result)
            elif csv_files[i] == 1:
                results[filename] = "Missing second file"

    # print(json.dumps(results, indent=4, default=str))

    print('\n\n')
    print('RESULTS'.center(50))
    print('#' * 50)
    print('Filename:'.ljust(30) + '|Chat history sync:')
    print('-' * 50)
    for key, value in results.items():
        print(key.ljust(30) + '|' + value)
    print('#' * 50)
