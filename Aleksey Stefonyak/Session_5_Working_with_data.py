import pandas as pd


# # Python Practice - Session 4


def sorting_file_strings(path, file):
    """ # ### Task 4.1
        # Open file `data/unsorted_names.txt` in data folder.
         Sort the names and write them to a new file called `sorted_names.txt`.
         Each name should start with a new line.
    """
    with open(path + '\\' + file, 'r') as unsorted_file:
        sorted_file_lines = sorted(unsorted_file.readlines())
        print(sorted_file_lines)
    with open(path + '\\' + 'sorted_' + file, 'w+') as sorted_file:
        sorted_file.write(''.join(sorted_file_lines))


# path = 'D:\\Python\\EPAM Course\\Session_5\\data'
# file = 'unsorted_names.txt'
# sorting_file_strings(path, file)


def most_common_words(path: str, file: str, words_num):
    """
    # ### Task 4.2
    # Implement a function which search for most common words in the file.
    # Use `data/lorem_ipsum.txt` file as a example.
    """
    with open(path + '\\' + file, 'r') as unsorted_file:
        file_lines = unsorted_file.read()
        chars_removed = '!,?&.;:%*$#^(){}[]'
        for char in chars_removed:
            file_lines.replace(char, ' ')
        words_list = file_lines.split()
        word_freq_dict = {}
        for word in words_list:
            word_freq_dict[word] = words_list.count(word)
        most_common_words_list = []
        for word, freq in word_freq_dict.items():
            if freq >= words_num:
                most_common_words_list.append(word)
        return most_common_words_list


# path = 'D:\\Python\\EPAM Course\\Session_5\\data'
# file = 'lorem_ipsum.txt'
# print(most_common_words(path, file, 8))


def get_top_performers(path, file, main_col='student name', criteria='average mark', number_of_top=5):
    """ Task 4.3
        # File `data/students.csv` stores information about students in [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) format.
        # This file contains the student’s names, age and average mark.
        # 1) Implement a function which receives file path and returns names of top performer students"""
    with open(path + '\\' + file, 'r') as csv_file:
        df_csv = pd.read_csv(csv_file)
        df = pd.DataFrame(df_csv).sort_values(criteria, ascending=False)
        top_list = (df[main_col].head(number_of_top)).values.tolist()
        print(top_list)


path = 'D:\\Python\\EPAM Course\\Session_5\\data'
file = 'students.csv'


# print(get_top_performers("students.csv"))


def get_sorted_csv(path, file, sorting_col='age', ascending=False):
    """Task 4.3
    # File `data/students.csv` stores information about students in [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) format.
    # This file contains the student’s names, age and average mark.
    # 2) Implement a function which receives the file path with srudents info and writes CSV student information to the new file in descending order of age."""
    with open(path + '\\' + file, 'r') as csv_file:
        df_csv = pd.read_csv(csv_file)
        df = pd.DataFrame(df_csv).sort_values(sorting_col, ascending=ascending)
        df.to_csv(path + '\\' + 'sorted_' + sorting_col + '_' + file)


# get_sorted_csv(path, file)


def enclosing_function():
    """
    # ### Task 4.4
    # Look through file `modules/legb.py`.
    # 1) Find a way to call `inner_function` without moving it from inside of `enclosed_function`.
    """
    a = "I am variable from enclosed function!"

    def inner_function():

        a = "I am local variable!"
        print(a)

    inner_function()


# enclosing_function()


a = "I am global variable!"


def enclosing_function_global():
    """
    # ### Task 4.4
    # Look through file `modules/legb.py`.
    # 2.1) Modify ONE LINE in `inner_function` to make it print variable 'a' from global scope.
    """
    a = "I am variable from enclosed function!"

    def inner_function():
        global a
        print(a)

    inner_function()


# enclosing_function_global()


def enclosing_function_nonlocal():
    """ # ### Task 4.4
        # Look through file `modules/legb.py`.
        # 2.2) Modify ONE LINE in `inner_function` to make it print variable 'a' form enclosing function.
    """
    a = "I am variable from enclosed function!"

    def inner_function():
        nonlocal a
        print(a)

    inner_function()


# enclosing_function_nonlocal()


def remember_result(func):
    """ ### Task 4.5
            Implement a decorator `remember_result` which remembers last result of function it decorates and prints it before next call.
    """
    last_result = None

    def wrapper(*args):
        nonlocal last_result
        print(f"Last result = '{last_result}'")
        last_result = func(*args)

    return wrapper


@remember_result
def sum_list(*args):
    result = ""
    for item in args:
        result += item
    print(f"Current result = '{result}'")
    return result


# sum_list('1', '2', '3')
# sum_list('3', '2', '1')
# sum_list('1', '2', '3')


def call_once(func):
    """ ### Task 4.6
        # Implement a decorator `call_once` which runs a function or method once and caches the result.
        # All consecutive calls to this function should return cached result no matter the arguments.
        """
    result = None

    def wrapper(*args):
        nonlocal result
        if result is None:
            result = func(*args)
        return result

    return wrapper


@call_once
def sum_of_numbers(a, b):
    return a + b


# print(sum_of_numbers(13, 42))
# print(sum_of_numbers(123, 42))
# print(sum_of_numbers(13, 423))
# print(sum_of_numbers(123, 423))
