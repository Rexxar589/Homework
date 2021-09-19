import pandas as pd
import ast


def str_length():
    """
    # ### Task 1.1
    # Write a Python program to calculate the length of a string without using the `len` function
    """
    some_str = input('Please, input the string length of which you want to find out: ')
    string_length = 0
    for _ in some_str:
        string_length += 1
    print(string_length)
    return string_length


def char_freq():
    """
    # ### Task 1.2
    # Write a Python program to count the number of characters (character frequency) in a string (ignore case of letters).
    # Input: 'Oh, it is python'
    # Output: {',': 1, ' ': 3, 'o': 2, 'h': 2, 'i': 2, 't': 2, 's': 1, 'p': 1, 'y': 1, 'n': 1}
    """
    some_str = input('Please, input the string to count the character frequency: ').lower()
    some_set = set(some_str)
    char_freq_dict = {}
    for char in some_set:
        char_freq_dict[char] = some_str.count(char)
    print(char_freq_dict)
    return char_freq_dict


def unique_el():
    """
    # ### Task 1.3
    # Write a Python program that accepts a comma separated sequence of words as input and prints the unique words in sorted form.
    # Input: ['red', 'white', 'black', 'red', 'green', 'black']
    # Output: ['black', 'green', 'red', 'white', 'red']
    """
    el_list = input('Input the list of words, separated by coma to find unique: ').replace(', ', ',').split(',')
    el_set = sorted(set(el_list))
    print(', '.join(el_set))
    return el_set


def find_divisors():
    """
    # ### Task 1.3
    # Create a program that asks the user for a number and then prints out a list of all the [divisors]  of that number.
    # Input: 60
    # Output: {1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60}
    """
    numb = int(input('Please, input the number to find it\'s divisors: '))
    div = numb
    div_list = []
    while div > 0:
        if numb % div == 0:
            div_list.append(div)
        div -= 1
    print(div_list)
    return div_list


def dict_key_sort():
    """
    # ### Task 1.4
    # Write a Python program to sort a dictionary by key.
    """
    some_dict = ast.literal_eval(input('Input dictionary that should be sorted in python dict format: '))
    sorted_dict = dict(sorted(some_dict.items()))
    print(sorted_dict)
    return sorted_dict


def dict_unique_values():
    """
    # ### Task 1.5
    # Write a Python program to print all unique values of all dictionaries in a list.
    # Input: [{"V":"S001"}, {"V": "S002"}, {"VI": "S001"}, {"VI": "S005"}, {"VII":"S005"}, {"V":"S009"},{"VIII":"S007"}]
    # Output: {'S005', 'S002', 'S007', 'S001', 'S009'}

    """
    dict_list = list(input('Please, input the list of dictionaries, separated by coma: ').replace(', ', ',').split(','))
    some_list = []
    for some_dict in dict_list:
        some_dict = ast.literal_eval(some_dict)
        for value in some_dict.values():
            some_list.append(value)
    some_set = set(some_list)
    print(some_set)
    return some_dict


def tuple_to_int():
    """
    # ### Task 1.6
    # Write a Python program to convert a given tuple of positive integers into an integer.
    # Input: (1, 2, 3, 4)
    # Output: 1234
    :return: int
    """
    some_tuple = tuple(input('Input elements of the tuple of positive integers, separated by coma:\n').replace(', ', ',').split(','))
    some_str = ''
    for el in some_tuple:
        some_str += str(el)
        print(el)
    some_int = int(some_str)
    print(some_int)
    return some_int


def multiplication_table():
    """
    # ### Task 1.6
    # Write a program which makes a pretty print of a part of the multiplication table.
    # Input:
    # a = 2
    # b = 4
    # c = 3
    # d = 7
    #
    # Output:
    # 	3	4	5	6	7
    # 2	6	8	10	12	14
    # 3	9	12	15	18	21
    # 4	12	16	20	24	28
    # ```
    :return: pandas.DataFrame
    """
    col_lower = int(input('Please, input the lower border of table columns: '))
    col_upper = int(input('Please, input the upper border of table columns: '))
    row_lower = int(input('Please, input the lower border of table rows: '))
    row_upper = int(input('Please, input the upper border of table rows: '))
    col_nums_list = list(range(col_lower, col_upper+1))
    row_nums_list = list(range(row_lower, row_upper+1))
    df = pd.DataFrame(columns=col_nums_list)
    for row_el in row_nums_list:
        result_list = []
        for col_el in col_nums_list:
            result = col_el*row_el
            result_list.append(result)
        df.loc[row_el] = result_list
    print(df)
    return df


# ### Materials
# * [Python Data Types](https://realpython.com/python-data-types/)
# * [Python Data Structures](https://realpython.com/python-data-structures/)
# * [Conditional Statements](https://realpython.com/python-conditional-statements/)
# * [While loop](https://realpython.com/python-while-loop/)
# * [For loop](https://realpython.com/python-for-loop/)
# * [Operators](http://pythonicway.com/python-operators)

task_list = ['Task 1.1: Write a Python program to calculate the length of a string without using the `len` function.',
             'Task 1.2 Write a Python program to count the number of characters (character frequency) in a string (ignore case of letters).',
             'Task 1.3 Write a Python program that accepts a comma separated sequence of words as input and prints the unique words in sorted form.',
             'Task 1.3 Create a program that asks the user for a number and then prints out a list of all the [divisors] of that number.',
             'Task 1.4 Write a Python program to sort a dictionary by key.',
             'Task 1.5 Write a Python program to print all unique values of all dictionaries in a list.',
             'Task 1.6 Write a Python program to convert a given tuple of positive integers into an integer.',
             'Task 1.6 Write a program which makes a pretty print of a part of the multiplication table.']


def print_list_num_el(s_list):
    print('ID', 'Name')
    for i, el in enumerate(s_list):
        print(i + 1, '', el)


def task_check():
    print_list_num_el(task_list)
    print('\'/q\' to exit\n\'/list\' to show task list')
    while 1:
        task_id = input('Please, input the number of the task you want to check: ')
        if task_id == '1':
            str_length()
        elif task_id == '2':
            char_freq()
        elif task_id == '3':
            unique_el()
        elif task_id == '4':
            find_divisors()
        elif task_id == '5':
            dict_key_sort()
        elif task_id == '6':
            dict_unique_values()
        elif task_id == '7':
            tuple_to_int()
        elif task_id == '8':
            multiplication_table()
        elif task_id == '/list':
            print_list_num_el(task_list)
        elif task_id == '/q':
            break
        else:
            print('Task number should be in the list')
            continue


task_check()
