"""Typing test implementation"""

from lib2to3.pytree import type_repr
from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


#################
# Part 1  Typing#
#################


def pick(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns True. If there are fewer than K such paragraphs, return
    the empty string.

    Arguments:
        paragraphs: a list of strings
        select: a function that returns True for paragraphs that can be selected
        k: an integer

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> pick(ps, s, 0)
    'hi'
    >>> pick(ps, s, 1)
    'fine'
    >>> pick(ps, s, 2)
    ''
    """
    count = -1
    for s in paragraphs:
        if select(s):
            count += 1
        if count == k:
            return s
    return ''


def about(topic):
    """Return a select function that returns whether
    a paragraph contains one of the words in TOPIC.

    Arguments:
        topic: a list of words related to a subject

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'

    def helper(string_check):
        string_check = split(lower(remove_punctuation(string_check)))
        for s in string_check:
            for s_topic in topic:
                if s_topic == s:
                    return True
        return False
    return helper


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    Arguments:
        typed: a string that may contain typos
        reference: a string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    if len(typed_words) == 0 and len(reference_words) == 0:
        return 100.0
    if len(typed_words) == 0 or len(reference_words) == 0:
        return 0.0
    i = 0
    count = 0
    while i < len(typed_words):
        if i < len(reference_words) and typed_words[i] == reference_words[i]:
            count += 1
        i += 1
    return count/len(typed_words)*100


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.

    Arguments:
        typed: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, 'Elapsed time must be positive'
    return len(typed)/5*60/elapsed

#####################
# Part 2 Autocorrect#
#####################


def autocorrect(typed_word, word_list, diff_function, limit):
    """Returns the element of WORD_LIST that has the smallest difference
    from TYPED_WORD. Instead returns TYPED_WORD if that difference is greater
    than LIMIT.

    Arguments:
        typed_word: a string representing a word that may contain typos
        word_list: a list of strings representing reference words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    lowest = diff_function(typed_word, word_list[0], limit)
    lowest_s = word_list[0]
    i = 1
    while i < len(word_list):
        s = word_list[i]
        if s == typed_word:
            return typed_word
        num = diff_function(typed_word, s, limit)
        if num < lowest:
            lowest = num
            lowest_s = s
        i += 1
    if lowest > limit:
        return typed_word
    return lowest_s


def feline_fixes(typed, reference, limit):
    """A diff function for autocorrect that determines how many letters
    in TYPED need to be substituted to create REFERENCE, then adds the difference in
    their lengths and returns the result.

    Arguments:
        typed: a starting word
        reference: a string representing a desired goal word
        limit: a number representing an upper bound on the number of chars that must change

    >>> big_limit = 10
    >>> feline_fixes("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> feline_fixes("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> feline_fixes("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> feline_fixes("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> feline_fixes("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    """
    if typed == reference:
        return 0
    if limit == 0:
        return 1
    diff = 0
    if typed == '' or reference == '':
        return min(abs(len(typed) - len(reference)), limit + 1)

    if typed[0] != reference[0]:
        diff += 1
    return diff + feline_fixes(typed[1:], reference[1:], limit-diff)


def hidden_kittens(typed, reference, limit):
    """A diff function that returns the number of times REFERENCE appears as a
    (potentially non-continuous) substring of TYPED. If REFERENCE appears 0 or > LIMIT times
    within TYPED, return a number greater than LIMIT.

    Arguments:
        typed: a starting word
        reference: a string representing a desired goal word
        limit: a number representing an upper bound on the number of substrings found

    >>> limit = 5
    >>> hidden_kittens("ccatgts", "cats", limit)
    4
    >>> hidden_kittens("123123123", "123", limit) > limit # 123 appears 10 times in 123123123
    True
    >>> hidden_kittens("hiddnehddi", "hidden", limit) > limit # hidden appears 0 times in hiddnehddi
    True
    """
    numHK = helperHK(typed, reference, limit)
    if numHK == 0 or numHK > limit:
        return limit + 1
    return numHK


def helperHK(typed, reference, limit):
    if reference == typed:
        return 1
    if len(reference) == 0:
        return 1
    if len(typed) == 0:
        return 0
    if typed[0] == reference[0]:
        num = helperHK(typed[1:], reference, limit) + \
            helperHK(typed[1:], reference[1:], limit)
    else:
        num = helperHK(typed[1:], reference, limit)
    return num


def final_diff(typed, reference, limit):
    """A diff function that takes in a string TYPED, a string REFERENCE, and a number LIMIT.
    If you implement this function, it will be used."""
    ...


#####################
# Part 3 Multiplayer#
#####################


def report_progress(typed, prompt, user_id, upload):
    """Upload a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.

    Arguments:
        typed: a list of the words typed so far
        prompt: a list of the words in the typing prompt
        user_id: a number representing the id of the current user
        upload: a function used to upload progress to the multiplayer server

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> typed = ['how', 'are', 'you']
    >>> prompt = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(typed, prompt, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], prompt, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    count_right = 0
    i = 0
    for x in typed:
        if x == prompt[i]:
            i += 1
            count_right += 1
        else:
            print(f'ID: {user_id} Progress: {count_right / len(prompt)}')
            return count_right / len(prompt)
    print(f'ID: {user_id} Progress: {count_right / len(prompt)}')
    return count_right / len(prompt)


def time_per_word(words, times_per_player):
    """Given timing data, return a match dictionary, which contains a
    list of words and the amount of time each player took to type each word.

    Arguments:
        words: a list of words, in the order they are typed.
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> match = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> match["words"]
    ['collar', 'plush', 'blush', 'repute']
    >>> match["times"]
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    big_lst = []
    for x in times_per_player:
        i = 1
        lst = []
        while i < len(x):
            diff_time = x[i]-x[i-1]
            lst.append(diff_time)
            i += 1
        big_lst.append(lst)
    dic = {"words": words, "times": big_lst}
    return dic


def fastest_words(match):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        match: a match dictionary as returned by time_per_word.

    >>> p0 = [5, 1, 3]
    >>> p1 = [4, 1, 6]
    >>> fastest_words(match(['Just', 'have', 'fun'], [p0, p1]))
    [['have', 'fun'], ['Just']]
    >>> p0  # input lists should not be mutated
    [5, 1, 3]
    >>> p1
    [4, 1, 6]
    """
    player_indices = range(
        len(match["times"]))  # contains an *index* for each player
    # contains an *index* for each word
    word_indices = range(len(match["words"]))

    bigList = []
    for _ in player_indices:
        bigList.append([])

    for w in word_indices:
        timelist = []
        for p in player_indices:
            timelist.append(match["times"][p][w])
        m = min(timelist)
        i = timelist.index(m)
        bigList[i].append(match["words"][w])
    return bigList


def match(words, times):
    """A dictionary containing all words typed and their times.

    Arguments:
        words: A list of strings, each string representing a word typed.
        times: A list of lists for how long it took for each player to type
            each word.
            times[i][j] = time it took for player i to type words[j].

    Example input:
        words: ['Hello', 'world']
        times: [[5, 1], [4, 2]]
    """
    assert all([type(w) == str for w in words]
               ), 'words should be a list of strings'
    assert all([type(t) == list for t in times]
               ), 'times should be a list of lists'
    assert all([isinstance(i, (int, float))
               for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]
               ), 'There should be one word per time.'
    return {"words": words, "times": times}


def get_word(match, word_index):
    ...


def time(match, player_num, word_index):
    ...


def match_string(match):
    ...


enable_multiplayer = False

...
