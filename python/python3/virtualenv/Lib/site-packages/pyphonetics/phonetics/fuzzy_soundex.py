import re
from unidecode import unidecode

from ..utils import squeeze, translation, check_empty, check_str
from .phonetic_algorithm import PhoneticAlgorithm


class FuzzySoundex(PhoneticAlgorithm):
    """
    Implementation of the "Fuzzy Soundex" algorithm.

    [Reference]: http://wayback.archive.org/web/20100629121128/http://www.ir.iit.edu/publications/downloads/IEEESoundexV5.pdf
    [Article]: Holmes, David and M. Catherine McCabe. "Improving Precision and Recall for Soundex Retrieval."
    """
    def __init__(self):
        super().__init__()

        self.translations = translation(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            '0193017-07745501769301-7-9'
        )

        self.rules = [
            (r'CA', r'KA'),
            (r'CC', r'KK'),
            (r'CK', r'KK'),
            (r'CE', r'SE'),
            (r'CHL', r'KL'),
            (r'CL', r'KL'),
            (r'CHR', r'KR'),
            (r'CR', r'KR'),
            (r'CI', r'SI'),
            (r'CO', r'KO'),
            (r'CU', r'KU'),
            (r'CY', r'SY'),
            (r'DG', r'GG'),
            (r'GH', r'HH'),
            (r'MAC', r'MK'),
            (r'MC', r'MK'),
            (r'NST', r'NSS'),
            (r'PF', r'FF'),
            (r'PH', r'FF'),
            (r'SCH', r'SSS'),
            (r'TIO', r'SIO'),
            (r'TIA', r'SIO'),
            (r'TCH', r'CHH'),
        ]

        self.set1 = ['CS', 'CZ', 'TS', 'TZ']
        self.set2 = ['HR', 'WR']
        self.set3 = ['KN', 'NG']
        self.set4 = 'HWY'

    def phonetics(self, word):
        check_str(word)
        check_empty(word)

        word = unidecode(word).upper()

        # Substitutions for beginnings
        first_two, rest = word[:2], word[2:]

        if first_two in self.set1:
            word = 'SS' + rest
        elif first_two == 'GN':
            word = 'NN' + rest
        elif first_two in self.set2:
            word = 'RR' + rest
        elif first_two == 'HW':
            word = 'WW' + rest
        elif first_two in self.set3:
            word = 'NN' + rest

        # Substitutions for endings
        last_two, initial = word[-2:], word[0:-2]

        if last_two == 'CH':
            word = initial + 'KK'
        elif last_two == 'NT':
            word = initial + 'TT'
        elif last_two == 'RT':
            word = initial + 'RR'
        elif word[-3:] == 'RDT':
            word = word[0:-3] + 'RR'

        # Applying the rules
        for rule in self.rules:
            word = re.sub(rule[0], rule[1], word)

        # Catch the first letter
        first_letter = word[0]

        # Translating
        code = ''.join(self.translations.get(char, char) for char in word)

        # Removing hyphens
        code = code.replace('-', '')

        # Squeezing the code
        code = squeeze(code)

        # Dealing with initials
        code = first_letter if code[0] in self.set4 \
            else first_letter + code[1:]

        # Dropping vowels
        code = code.replace('0', '')
        return code
