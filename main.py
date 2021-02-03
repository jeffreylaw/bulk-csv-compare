import csv
import sys

    
def compare_files(file1, file2):
    with open(file1, 'r') as file1, open(file2, 'r') as file2:
        reader1 = csv.reader(file1)
        reader2 = csv.reader(file2)

        all(next(reader1) for i in range(7))
        all(next(reader2) for i in range(7))

        file1_chat = {}
        file2_chat = {}

        for row in reader1:
            # print(''.join(row))
            file1_chat[reader1.line_num-7] = ''.join(row)

        for row in reader2:
            file2_chat[reader2.line_num-7] = ''.join(row)

        for i in file1_chat:
            print('Line ' + str(i) + ' ' + file1_chat[i])
            print('Line ' + str(i) + ' ' + file2_chat[i])
            if (file1_chat[i] != file2_chat[i]):
                print("\nChat histories don't match.")
                print(f"See line {i} or line {i+7} in the csv file.")
                break


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(1)
    file1 = sys.argv[1]
    file2 = sys.argv[2]

    compare_files(file1, file2)