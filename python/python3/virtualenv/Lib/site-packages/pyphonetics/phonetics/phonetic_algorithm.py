from ..distance_metrics import levenshtein_distance, hamming_distance
from ..exceptions import DistanceMetricError


class PhoneticAlgorithm:
    """
    The main Phonetic Algorithm class, to ensure a unified API
    for all the included algorithms.
    """
    def __init__(self):
        self.distances = {
            'levenshtein': levenshtein_distance,
            'hamming': hamming_distance,
        }

    def phonetics(self, word):
        """Get the phonetic representation of the word."""
        pass

    def sounds_like(self, word1, word2):
        """Compare the phonetic representations of 2 words, and return a boolean value."""
        return self.phonetics(word1) == self.phonetics(word2)

    def distance(self, word1, word2, metric='levenshtein'):
        """Get the similarity of the words, using the supported distance metrics."""
        if metric in self.distances:
            distance_func = self.distances[metric]
            return distance_func(self.phonetics(word1), self.phonetics(word2))
        else:
            raise DistanceMetricError('Distance metric not supported! Choose from levenshtein, hamming.')
