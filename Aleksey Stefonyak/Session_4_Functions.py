from string import ascii_lowercase as asc_low
# Python Practice - Session 4


def replace_symb(string, r_symbol, replacement):
    """ ### Task 4.1
        #Implement a function which receives a string and replaces all `"` symbols
        #with `'` and vise versa. """
    if isinstance(string, str):
        new_word = ""
        for symbol in string:
            if symbol == r_symbol:
                symbol = replacement
            new_word += symbol
        return new_word
    else:
        print('String should have type str, not ', type(string))


# print(replace_symb("yyyyykkjdggyyyes", "y", "n"))


def is_palindrome(string):
    """ ### Task 4.2
        # Write a function that check whether a string is a palindrome or not. Usage of
        # any reversing functions is prohibited. To check your implementation you can use
        # strings from [here](https://en.wikipedia.org/wiki/Palindrome#Famous_palindromes)."""
    if isinstance(string, str):
        chars = '.,!?:;-()" '
        clear_string = string
        for char in chars:
            clear_string = clear_string.replace(char, '')
        clear_string = clear_string.lower()
        k = 1
        string_backwards = ''
        try:
            while k <= len(clear_string):
                string_backwards += clear_string[-k]
                k += 1
            if clear_string == string_backwards:
                print('Yes! String \"' + string + '\" is a palindrome!')
            elif clear_string != string_backwards:
                print('No, unfortunately string \"' + string + '\" is not a palindrome =(')
            else:
                print('Master, you gave me a string! Now Dobby is free! Hurray!')
        except Exception as e:
            print(e)
    else:
        print('String should have type str, not ', type(string))


# is_palindrome('Dog ees!,"?:;e" se egod')


def split_function(string: str, split_char: str):
    """ ### Task 4.3
        # Implement a function which works the same as `str.split` method
        # (without using `str.split` itself, of course)."""
    if isinstance(string, str) and isinstance(split_char, str):
        string = string + split_char
        newborn_list = []
        string_x = ''
        for char in string:
            if char != split_char:
                string_x += char
            elif char == split_char:
                newborn_list.append(string_x)
                string_x = ''
        return newborn_list
    else:
        print('String should have type str, not ', type(string))


# split_function('maesfafasd,asdasfsdf,asdasfewrfsd,asdasd', ',')


def split_by_index(string, ind_lst):
    """ ### Task 4.4
        # Implement a function `split_by_index(s: str, indexes: List[int]) -> List[str]`
        # which splits the `s` string by indexes specified in `indexes`. Wrong indexes
        # must be ignored."""
    ind_lst.append(len(string))
    split_list = []
    for ind in ind_lst:
        if ind <= len(string):
            if ind == ind_lst[0]:
                string_part = string[:ind]
            else:
                string_part = string[ind_lst[ind_lst.index(ind) - 1]:ind]
            split_list.append(string_part)
        elif ind > len(string) and len(ind_lst) == 2:
            split_list.append(string)
    if '' in split_list:
        split_list.remove('')
    if len(ind_lst) == 2 and ind_lst[0] == ind_lst[1]:
        split_list.pop(1)
    return split_list


# print(split_by_index("pythoniscool,isn'tit?", [6, 8, 12, 13, 18]))


def get_digits(number: int):
    """ ### Task 4.5
        # Implement a function `get_digits(num: int) -> Tuple[int]` which returns a tuple
        # of a given integer's digits."""
    if isinstance(number, int):
        number = str(number)
        digit_list = []
        for digit in number:
            digit = int(digit)
            digit_list.append(digit)
        digit_tuple = tuple(digit_list)
        return digit_tuple
    else:
        print('Number should have type int, not ', type(number))


# print(get_digits(213124))


def get_shortest_word(string: str):
    """ ### Task 4.6
        # Implement a function `get_shortest_word(s: str) -> str` which returns the
        # longest word in the given string. The word can contain any symbols except
        # whitespaces (` `, `\n`, `\t` and so on). If there are multiple longest words in
        # the string with a same length return the word that occures first."""
    if isinstance(string, str):
        chars = '.,!?:;-()" \n\t\''
        clear_string = string
        whitespace = ' '
        for char in chars:
            clear_string = clear_string.replace(char, whitespace)
        word_list = clear_string.split()
        word_len_dict = {}
        for word in word_list:
            word_len_dict[word] = len(word)
        shortest_word_list = []
        for k, v in word_len_dict.items():
            if v == max(word_len_dict.values()):
                shortest_word_list.append(k)
        return f'{shortest_word_list[0]!r}'
    else:
        print('String should have type str, not ', type(string))


# get_shortest_word('Any pythonista like namespaces a lot.')


def foo(int_list: list[int]):
    """ ### Task 4.7
        # Implement a function `foo(List[int]) -> List[int]` which, given a list of
        # integers, return a new list such that each element at index `i` of the new list
        # is the product of all the numbers in the original array except the one at `i`."""
    new_int_list = []
    for i, number in enumerate(int_list):
        if isinstance(number, int):
            int_list_exc_num = int_list.copy()
            del int_list_exc_num[i]
            new_int = 1
            for rem_num in int_list_exc_num:
                new_int *= rem_num
            new_int_list.append(new_int)
    return new_int_list


# print(foo([1, 2, 3, 4, 5]))


def get_pairs(some_list: list):
    """ ### Task 4.8
        # Implement a function `get_pairs(lst: List) -> List[Tuple]` which returns a list
        # of tuples containing pairs of elements. Pairs should be formed as in the
        # example. If there is only one element in the list return `None` instead."""
    if isinstance(some_list, list) and len(some_list) > 1:
        paired_list = []
        for i, el in enumerate(some_list):
            k = i + 1
            if k < len(some_list):
                pair_tuple = (el, some_list[k])
                paired_list.append(pair_tuple)
        return paired_list
    elif isinstance(some_list, list) and len(some_list) == 1:
        return None
    else:
        print('List should have type list, not ', type(some_list))


# lst = ['sus', 'mus', 'gus', 'asd']
# print(get_pairs(lst))


def char_funcs(func_num: int, *strings: str):
    """
    ### Task 4.9
    # Implement a bunch of functions which receive a changeable number of strings and return next parameters:
    """
    def repeatable_char(some_strings):
        """
        # 1) characters that appear in all strings
        """
        main_char_set = set()
        for string in some_strings:
            char_set = set(string)
            if not main_char_set:
                main_char_set = main_char_set | char_set
            main_char_set = main_char_set.intersection(char_set)
        return main_char_set

    def appearing_chars(some_strings):
        """
        # 2) characters that appear in at least one string
        """
        main_char_set = set()
        for string in some_strings:
            char_set = set(string)
            main_char_set = main_char_set | char_set
        return main_char_set

    def appearing_two_times_chars(some_strings):
        """
        # 3) characters that appear at least in two strings
        """
        main_char_set = set()
        for string in range(len(some_strings) - 1):
            for char in range(string + 1, len(some_strings)):
                main_char_set.update(set(some_strings[string]) & set(some_strings[char]))
        return main_char_set

    def not_used_chars(some_strings):
        """
        # 4) characters of alphabet, that were not used in any string
        """
        main_char_set = set()
        alphabet_set = set(asc_low)
        for string in some_strings:
            char_set = set(string)
            main_char_set = main_char_set | char_set
        main_char_set = alphabet_set.difference(main_char_set)
        return main_char_set

    if func_num == 1:
        return repeatable_char(strings)
    elif func_num == 2:
        return appearing_chars(strings)
    elif func_num == 3:
        return appearing_two_times_chars(strings)
    elif func_num == 4:
        return not_used_chars(strings)
    else:
        print('There is no such function')
        return None


# print(char_funcs(1, "hello", "world", "python"))
# print(char_funcs(2, "hello", "world", "python"))
# print(char_funcs(3, "hello", "world", "python", 'assn'))
# print(char_funcs(4, "hello", "world", "python"))


def generate_squares(number: int):
    """ ### Task 4.10
        # Implement a function that takes a number as an argument and returns a dictionary, where the key is a number and the value is the square of that number."""
    num_list = []
    num_sqrt_list = []
    while number > 0:
        num_list.append(number)
        num_sqrt_list.append(number * number)
        number -= 1
    sqrt_dict = dict(zip(num_list, num_sqrt_list))
    return sqrt_dict


# print(generate_squares(55555))


def combine_dicts(*args: dict):
    """ ### Task 4.11
        # Implement a function, that receives changeable number of dictionaries (keys - letters, values - numbers) and combines them into one dictionary.
        # Dict values ​​should be summarized in case of identical keys"""
    full_dct = {}
    for dct in args:
        full_dct_set = set(full_dct)
        dct_set = set(dct)
        dct_set_intersec = full_dct_set.intersection(dct_set)
        if dct_set_intersec:
            for el in dct_set_intersec:
                new_num = full_dct[el] + dct[el]
                dct = dct | {el: new_num}
        full_dct = full_dct | dct
    return full_dct


# print(combine_dicts(dict_1, dict_2, dict_3))
