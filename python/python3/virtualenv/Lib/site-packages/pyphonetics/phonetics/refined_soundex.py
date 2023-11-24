import re
from unidecode import unidecode

from ..utils import translation, squeeze, check_str, check_empty
from .phonetic_algorithm import PhoneticAlgorithm


class RefinedSoundex(PhoneticAlgorithm):
    """
    The Refined Soundex algorithm.

    [Reference]: https://en.wikipedia.org/wiki/Soundex
    [Authors]: Robert C. Russel, Margaret King Odell
    """
    def __init__(self):
        super().__init__()

        self.translations = translation(
            'AEIOUYWHBPFVCKSGJQXZDTLMNR',
            '000000DD112233344555667889'
        )

    def phonetics(self, word):
        check_str(word)
        check_empty(word)

        word = unidecode(word).upper()
        word = re.sub(r'[^A-Z]', r'', word)

        first_letter = word[0]
        tail = ''.join(self.translations[char] for char in word
                       if self.translations[char] != 'D')

        return first_letter + squeeze(tail)
