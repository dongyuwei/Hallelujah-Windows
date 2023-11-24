import re
from unidecode import unidecode

from ..utils import squeeze, check_empty, check_str
from .phonetic_algorithm import PhoneticAlgorithm


class MatchingRatingApproach(PhoneticAlgorithm):
    """
    Functions related to the computation of the Match Rating Approach codex.

    [Reference]: https://en.wikipedia.org/wiki/Match_rating_approach
    [Article]: Moore, G B.; Kuhns, J L.; Treffzs, J L.; Montgomery, C A. (Feb 1, 1977).
        Accessing Individual Records from Personal Data Files Using Nonunique Identifiers.
        US National Institute of Standards and Technology. p. 17. NIST SP - 500-2.
    """
    def __init__(self):
        super().__init__()

    def phonetics(self, word):
        check_str(word)
        check_empty(word)

        codex = unidecode(word).upper()
        codex = re.sub(r'[^A-Z]', r'', codex)

        # Dropping non - leading vowels
        codex = codex[0] + re.sub(r'[AEIOU]', r'', codex[1:])

        # Dropping consecutive consonants
        codex = squeeze(codex)

        # Returning the codex
        offset = min(3, len(codex) - 3)
        return codex[:3] + codex[len(codex) - offset:offset + len(codex)]
