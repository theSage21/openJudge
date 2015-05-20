import sys


def print_output(filepath):
    f = open(filepath, 'r')
    for line in (f.readlines()):
        print(line)
    f.close()
if __name__ == '__main__':
    test_file_path = sys.argv[1]
    print_output(test_file_path)
