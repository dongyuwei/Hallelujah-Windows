import re
from unidecode import unidecode

from ..utils import squeeze, translation, check_str, check_empty
from .phonetic_algorithm import PhoneticAlgorithm


class Lein(PhoneticAlgorithm):
    """
    The Lein name coding procedure.

    [Reference]: http://naldc.nal.usda.gov/download/27833/PDF
    """
    def __init__(self):
        super().__init__()

        self.translations = translation(
            'DTMNLRBFPVCJKGQSXZ',
            '112233444455555555'
        )

        self.pad = lambda code: '{}0000'.format(code)[:4]

    def phonetics(self, word):
        check_str(word)
        check_empty(word)

        word = unidecode(word).upper()
        word = re.sub(r'[^A-Z]\s', r'', word)

        # Keep the 1st letter
        first, code = word[0], word[1:]

        # Drop vowels and Y, W & H
        code = re.sub(r'[AEIOUYWH]', r'', code)

        # Drop consecutive duplicates and truncate to 4 chars
        code = squeeze(code)[0: 4]

        # Translations
        code = ''.join(self.translations.get(char, char) for char in code)

        return self.pad(first + code)
