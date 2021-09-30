import functools
import math
import time
from forex_python.converter import CurrencyRates

# Python Practice - Session 4


# Custom decors
def func_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f"Function time, sec: {round(end - start, 5)}")

    return wrapper


# ### Task 4.1
class Counter:
    """ # ### Task 4.1
        # Implement a Counter class which optionally accepts the start value and the counter stop value.
        # If the start value is not specified the counter should begin with 0.
        # If the stop value is not specified it should be counting up infinitely.
        # If the counter reaches the stop value, print "Maximal value is reached."""

    def __init__(self, start=0, stop=float('inf')):
        self.start = start
        self.stop = stop

    def increment(self):
        if self.start < self.stop:
            self.start += 1
        elif self.start >= self.stop:
            print("Maximal value is reached")

    def get(self):
        print(self.start)

    @func_time
    def count(self):
        if not self.start:
            self.start = 0
        if self.stop:
            while self.start < self.stop:
                self.start += 1
                print(self.start)
                if self.start == self.stop:
                    print("Maximal value is reached")
        elif not self.stop:
            while self.start < self.stop:
                self.start += 1
                print(self.start)

#
# c = Counter(57, 60)
# c.get()
# c.count()
# c.increment()
# c.increment()
# c.increment()
# c.increment()


# #### Task 4.2
class HistoryDict:
    """ # #### Task 4.2
        # Implement custom dictionary that will memorize 10 latest changed keys.
        # Using method "get_history" return this keys."""
    dict_history = []

    def __init__(self, some_dict):
        self.some_dict = dict(some_dict)

    def set_value(self, key, value, dict_history=dict_history):
        self.key = key
        self.value = value
        self.some_dict[self.key] = self.value
        if len(dict_history) >= 10:
            del dict_history[0]
        dict_history.append(self.key)

    def get(self):
        print(self.some_dict)

    def get_history(self, dict_history=dict_history):
        print(dict_history)


# hd = HistoryDict({42: '33'})
# hd.get()
# hd.set_value(44, "22")
# hd.set_value(42, "12")
# hd.set_value(44, "22")
# hd.set_value(42, "12")
# hd.set_value(44, "22")
# hd.set_value(42, "12")
# hd.set_value(44, "22")
# hd.set_value(42, "12")
# hd.set_value(44, "22")
# hd.set_value(42, "12")
# hd.set_value(44, "22")
# hd.set_value(42, "12")
# hd.set_value(44, "22")
# hd.set_value(42, "12")
#
# hd.get()
# hd.get_history()


# ### Task 4.3
class Cipher:
    """ # ### Task 4.3
        # Implement The Keyword encoding and decoding for latin alphabet.
        # The Keyword Cipher uses a Keyword to rearrange the letters in the alphabet.
        # Add the provided keyword at the begining of the alphabet.
        # A keyword is used as the key, and it determines the letter matchings of the cipher alphabet to the plain alphabet.
        # Repeats of letters in the word are removed, then the cipher alphabet is generated with the keyword matching to A, B, C etc. until the keyword is used up, whereupon the rest of the ciphertext letters are used in alphabetical order, excluding those already used in the key.
        """
    alphabet = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.lower().split()

    def __init__(self, keyword):
        self.keyword = keyword

    def encode(self, words: str, alphabet=alphabet, decoded_alph=alphabet.copy(), decoded_word=''):
        self.word = words
        for n_l in range(len(self.keyword)):
            for alph_n in range(len(decoded_alph)):
                if decoded_alph[alph_n] == self.keyword[n_l]:
                    del decoded_alph[alph_n]
                    decoded_alph.insert(n_l, self.keyword[n_l])
        decode_dict = dict(zip(decoded_alph, alphabet))
        for letter in words:
            if letter in decode_dict.keys():
                decoded_word += decode_dict[letter]
            elif letter in (i.upper() for i in decode_dict.keys()):
                decode_dict_upper = dict(
                    zip(list(let.upper() for let in decoded_alph), list(let.upper() for let in alphabet)))
                decoded_word += decode_dict_upper[letter.upper()]
            else:
                decoded_word += letter
        print(decoded_word)


# Cipher('crypto').encode('Fjedhc dn atIDsn')


# ### Task 4.4
class Bird(object):
    """ # ### Task 4.4
        # Create hierarchy out of birds.
        # Implement 4 classes:
        # * class `Bird` with an attribute `name` and methods `fly` and `walk`."""

    def __init__(self, name: str):
        self.name = name

    def walk(self):
        print(self.name, 'bird can walk!')

    def __str__(self):
        description = f'{self.name} is a bird.'
        print(description)
        return description


class FlyingBird(Bird):
    """ # * class `FlyingBird` with attributes `name`, `ration`, and with the same methods. `ration` must have default value.
        # Implement the method `eat` which will describe its typical ration."""

    def fly(self):
        print(self.name, 'bird can fly!')

    def eat(self, ration=None):
        if ration is None:
            ration = ['fish', 'rodents', 'worms', 'bugs']
        print(self.name, 'eats:', ', '.join(ration) + '.')

    def __str__(self):
        description = f'{self.name} can fly and walk.'
        print(description)
        return description


class NonFlyingBird(Bird):
    """ # * class `NonFlyingBird` with same characteristics but which obviously without attribute `fly`.
        # Add same "eat" method but with other implementation regarding the swimming bird tastes."""

    def eat(self, ration=None):
        if ration is None:
            ration = ['fish', 'seaweed']
        print(self.name, 'eats:', ', '.join(ration) + '.')

    def swim(self):
        print(self.name, 'is swimming!')

    def __str__(self):
        description = f'{self.name} can swim and walk.'
        print(description)
        return description


class SuperBird(FlyingBird, NonFlyingBird):
    """ # * class `SuperBird` which can do all of it: walk, fly, swim and eat.
        # But be careful which "eat" method you inherit.
        #
        # Implement str() function call for each class."""

    def __str__(self):
        description = f'{self.name} can fly, swim and walk.'
        print(description)
        return description


# b = Bird('Any')
# b.walk()
#
# c = FlyingBird('Duck')
# c.fly()
# c.eat()
# str(c)
#
# d = NonFlyingBird('Pinga')
# d.swim()
# d.eat()
#
# f = SuperBird('Pingaduck')
# str(f)
# f.name
# f.fly()
# f.swim()
# f.walk()
# f.eat()
# print(SuperBird.__mro__)


# ### Task 4.6
class Me:
    """ # ### Task 4.6
        #
        # A singleton is a class that allows only a single instance of itself to be created and gives access to that created instance.
        # Implement singleton logic inside your custom class using a method to initialize class instance."""
    inst_val = None

    @staticmethod
    def inst():
        if Me.inst_val is None:
            Me.inst_val = Me()

        return Me.inst_val


# me = Me.inst()
# you = Me.inst()
# print(me is you)


# ### Task 4.7
@functools.total_ordering
class Money:
    """ # ### Task 4.7
        # Implement a class Money to represent value and currency.
        # You need to implement methods to use all basic arithmetics expressions (comparison, division, multiplication, addition and subtraction).
        # Tip: use class attribute exchange rate which is dictionary and stores information about exchange rates to your default currency:"""
    rates = CurrencyRates()

    def __init__(self, amount: float, rates=rates, currency: str = 'USD'):
        self.amount = amount
        self.currency = currency
        self.rates = rates

    def exchange(self, currency_to='USD'):
        self.currency_to = currency_to
        if self.currency_to != 'BYN':
            self.amount = self.amount * self.rates.get_rate(self.currency, currency_to)
        elif self.currency_to == 'BYN':
            self.amount = self.amount * 2.50
        self.currency = self.currency_to
        return self.amount

    def __add__(self, other):
        self.amount += other.exchange(self.currency)
        return self

    def __sub__(self, other):
        self.amount - other.exchange(self.currency)
        return self

    def __mul__(self, other):
        self.amount *= other
        return self

    def __truediv__(self, other):
        self.amount /= other
        return self

    def __floordiv__(self, other):
        self.amount //= other
        return self

    def __lt__(self, other):
        return round(self.amount, 2) < round(other.exchange(self.currency), 2)

    def get(self):
        print(f'Amount: {round(self.amount, 3)} | Currency: {self.currency}')

    def __repr__(self):
        return str(f'{round(self.amount, 3)} {self.currency}')


# d20 = Money(20)
# d15 = Money(15)
# print(d15+d20)
# d20.exchange('EUR')
# d20.get()
# d20.exchange('EUR')
# d20.get()
# print(d20)
# print(d15)
# d5 = Money(5)
# print(d15 < d20)
# print((d15 + d5) == d20)
# dsum = (d15+d5+Money(5))
# print(dsum)
# d20 *= 2.5
# print(d20)


# ### Task 4.8
class Pagination:
    """ # ### Task 4.8
        # Implement a Pagination class helpful to arrange text on pages and list content on given page.
        # The class should take in a text and a positive integer which indicate how many symbols will be allowed per each page (take spaces into account as well).
        # You need to be able to get the amount of whole symbols in text, get a number of pages that came out and method that accepts the page number and return quantity of symbols on this page.
        # If the provided number of the page is missing print the warning message "Invalid index. Page is missing". If you're familliar with using of Excpetions in Python display the error message in this way.
        # Pages indexing starts with 0.
        # Optional: implement searching/filtering pages by symblos/words and displaying pages with all the symbols on it.
        # If you're querying by symbol that appears on many pages or if you are querying by the word that is splitted in two return an array of all the occurences."""
    pages_dict = {}

    def __init__(self, text, s_per_page, pages_dict=pages_dict):
        self.text = text
        self.s_per_page = s_per_page
        pages_num = int(math.ceil(len(self.text) / self.s_per_page))
        for page in range(pages_num):
            pages_dict[page] = text[page*s_per_page:(page+1)*s_per_page]

    def item_count(self):
        print(len(self.text))

    @staticmethod
    def display_page(page_num, pages_dict=pages_dict):
        print(f'{pages_dict[page_num]!r}')

    @staticmethod
    def show_pages(pages_dict=pages_dict):
        print(pages_dict)

    @staticmethod
    def page_count(pages_dict=pages_dict):
        print(max(pages_dict.keys()))

    @staticmethod
    def count_items_on_page(page_num, pages_dict=pages_dict):
        try:
            print(len(pages_dict[page_num]))
        except Exception:
            raise Exception('Invalid index. Page is missing.')

    def find_page(self, word):
        letr_pos_list = []
        try:
            word_pos = self.text.find(word)
            for letr in word:
                letr_pos = word_pos
                letr_pos_list.append(letr_pos+1)
                word_pos += 1
        except Exception:
            raise Exception(f'\'{word}\' is missing on the pages')
        pages_num = int(math.ceil(len(self.text) / self.s_per_page))
        list_pos_list = []
        letr = 1
        for page in range(pages_num):
            pos_list = []
            list_pos_list.append(pos_list)
            for _ in range(self.s_per_page):
                pos_list.append(letr)
                letr += 1
        res_pages = set()
        for lst in list_pos_list:
            for letr_pos in letr_pos_list:
                if letr_pos in lst:
                    res_pages.add(list_pos_list.index(lst)+1)
        res_pages = list(res_pages)
        print(res_pages)


# pages = Pagination('Your beautiful text', 5)
# pages.display_page(1)
# pages.show_pages()
# pages.find_page('beautiful t')
# pages.count_items_on_page(3)
# pages.page_count()
# pages.item_count()
