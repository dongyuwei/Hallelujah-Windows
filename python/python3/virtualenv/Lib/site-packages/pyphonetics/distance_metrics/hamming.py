from ..exceptions import WrongLengthException


def hamming_distance(word1, word2):
    """
    Computes the Hamming distance.

    [Reference]: https://en.wikipedia.org/wiki/Hamming_distance
    [Article]: Hamming, Richard W. (1950), "Error detecting and error correcting codes",
        Bell System Technical Journal 29 (2): 147–160
    """
    from operator import ne
    if len(word1) != len(word2):
        raise WrongLengthException('The words need to be of the same length!')

    return sum(map(ne, word1, word2))
