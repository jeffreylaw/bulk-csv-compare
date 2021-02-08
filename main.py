import csv
import sys
import os
import glob
import json
import re

def get_value(dic,value):
    for i in dic:
        if dic[i] == value:
            return i
import platform

def compare_files(file1, file2):
    filename = os.path.basename(file1).split('-')[0]
    with open(file1, 'r', encoding='utf8') as file1, open(file2, 'r', encoding='utf8') as file2:
        reader1 = csv.reader(file1)
        reader2 = csv.reader(file2)

        file1_participants = ['Me']
        file2_participants = ['Me']

        for i in range(7):
            if i == 1:
                downloader_participant = next(reader1)[0].split(': ')[1].split('@')[0]
                file1_participants.append(downloader_participant)

                downloader_participant = next(reader2)[0].split(': ')[1].split('@')[0]
                file2_participants.append(downloader_participant)
                continue

            if i == 3:
                participants = next(reader1)[0]
                if len(participants) > 20:
                    participants = participants.split()[1].split(';')[:-1]
                    participants = [i.split('@')[0] for i in participants]
                    file1_participants = file1_participants + participants

                participants = next(reader2)[0]
                if len(participants) > 20:
                    participants = participants.split()[1].split(';')[:-1]
                    participants = [i.split('@')[0] for i in participants]
                    file2_participants = file2_participants + participants
                continue

            next(reader1)
            next(reader2)


        file1_chat = {}
        file2_chat = {}

        participants_regex = [ '^' + i + r'\d{4}-\d{2}-\d{2}' for i in file1_participants]
        combined = "(" + ")|(".join(participants_regex) + ")"

        message_num = 1
        for i, l, in enumerate(reader1, start=1):
            current_line = ''.join(l)
            if re.match(combined, current_line):
                file1_chat[message_num] = current_line
                message_num += 1
            else:
                if not current_line:
                    file1_chat[message_num-1] = file1_chat[message_num-1] + '\n\n'
                else:
                    file1_chat[message_num-1] = file1_chat[message_num-1] + current_line

        # print(json.dumps(file1_chat, indent=4, sort_keys=True))
        # print(json.dumps(file2_chat, indent=4, sort_keys=True))


        message_num = 1
        for i, l, in enumerate(reader2, start=1):
            current_line = ''.join(l)
            if re.match(combined, current_line):
                file2_chat[message_num] = current_line
                message_num += 1
            else:
                if not current_line:
                    file2_chat[message_num-1] = file2_chat[message_num-1] + '\n\n'
                else:
                    file2_chat[message_num-1] = file2_chat[message_num-1] + current_line

        
        # message_num = 1
        # for row in reader1:
        #     print(row)
        #     file1_chat[message_num] = ''.join(row)
        #     message_num += 1

        # message_num = 1
        # for row in reader2:
        #     file2_chat[message_num] = ''.join(row)
        #     message_num += 1

        result_dict = {filename: 'Pass'}

        # missing_chat = {}

        for i in file2_chat.values():
            if i in file1_chat.values():
                key = get_value(file1_chat, i)
                del file1_chat[key]

        if len(file1_chat) > 0:
            result_dict = {filename: 'Fail'}
            print('-' * 50)
            print('Missing messages from \\after\\' + filename)
            print(json.dumps(file1_chat, indent=4, sort_keys=True)) 
            print('-' * 50)

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

        if platform.system() == 'Darwin':
            before_path = os.getcwd() + '/before'
        else:
            before_path = os.getcwd() + '\\before'

        for root, dirs, files in os.walk(before_path):
            dirs.clear()
            for file in files:
                if file.endswith(".csv"):
                    if file in csv_files.keys():
                        csv_files[file] = csv_files[file] + 1
                    else:
                        csv_files[file] = 1

        if platform.system() == 'Darwin':
            after_path = os.getcwd() + '/after'
        else:
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
                if platform.system() == 'Darwin':
                    result = compare_files(
                        before_path + '/' + i, after_path + '/' + i)            
                else:
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

    with open('results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Filename', 'Chat history sync'])
        writer.writerow([])
        for key, value in results.items():
            writer.writerow([key, value])

