from itertools import groupby

from .exceptions import WrongLengthException, UnicodeException, \
    EmptyStringError


def translation(first, second):
    """Create an index of mapped letters (zip to dict)."""
    if len(first) != len(second):
        raise WrongLengthException('The lists are not of the same length!')
    return dict(zip(first, second))


def squeeze(word):
    """Squeeze the given sequence by dropping consecutive duplicates."""
    return ''.join(x[0] for x in groupby(word))


def check_str(word):
    """Throw exception at non-string input."""
    if not isinstance(word, str):
        raise UnicodeException('Expected a unicode string!')


def check_empty(word):
    """Throw exception at empty string input."""
    if not len(word):
        raise EmptyStringError('The given string is empty.')
