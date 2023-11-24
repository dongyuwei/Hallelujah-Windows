import re
from unidecode import unidecode

from ..utils import check_str, check_empty
from .phonetic_algorithm import PhoneticAlgorithm


class Metaphone(PhoneticAlgorithm):
    """
    The metaphone algorithm.

    [Reference]: https://en.wikipedia.org/wiki/Metaphone
    [Author]: Lawrence Philips, 1990
    """
    def __init__(self):
        super().__init__()

        self.rules = [
            (r'[^a-z]', r''),
            (r'([bcdfhjklmnpqrstvwxyz])\1+', r'\1'),
            (r'^ae', r'E'),
            (r'^[gkp]n', r'N'),
            (r'^wr', r'R'),
            (r'^x', r'S'),
            (r'^wh', r'W'),
            (r'mb$', r'M'),
            (r'(?!^)sch', r'SK'),
            (r'th', r'0'),
            (r't?ch|sh', r'X'),
            (r'c(?=ia)', r'X'),
            (r'[st](?=i[ao])', r'X'),
            (r's?c(?=[iey])', r'S'),
            (r'[cq]', r'K'),
            (r'dg(?=[iey])', r'J'),
            (r'd', r'T'),
            (r'g(?=h[^aeiou])', r''),
            (r'gn(ed)?', r'N'),
            (r'([^g]|^)g(?=[iey])', r'\1J'),
            (r'g+', r'K'),
            (r'ph', r'F'),
            (r'([aeiou])h(?=\b|[^aeiou])', r'\1'),
            (r'[wy](?![aeiou])', r''),
            (r'z', r'S'),
            (r'v', r'F'),
            (r'(?!^)[aeiou]+', r'')
        ]

    def phonetics(self, word):
        check_str(word)
        check_empty(word)

        code = unidecode(word).lower()
        for item in self.rules:
            code = re.sub(item[0], item[1], code)
        return code.upper()
