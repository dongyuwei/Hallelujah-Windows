def levenshtein_distance(word1, word2):
    """
    Computes the Levenshtein distance.

    [Reference]: https://en.wikipedia.org/wiki/Levenshtein_distance
    [Article]: Levenshtein, Vladimir I. (February 1966). "Binary codes capable of correcting deletions,
        insertions,and reversals". Soviet Physics Doklady 10 (8): 707–710.
    [Implementation]: https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
    """
    if len(word1) < len(word2):
        return levenshtein_distance(word2, word1)

    if len(word2) == 0:
        return len(word1)

    previous_row = list(range(len(word2) + 1))

    for i, char1 in enumerate(word1):
        current_row = [i + 1]

        for j, char2 in enumerate(word2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (char1 != char2)

            current_row.append(min(insertions, deletions, substitutions))

        previous_row = current_row
    return previous_row[-1]
