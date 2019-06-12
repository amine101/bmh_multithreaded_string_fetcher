from collections import defaultdict
import  global_var
"""
    Functions to run the BOYER MOORE HORSPOOL algorithm
"""


def precalc(pattern):
    """
    Create the precalculation table: a dictionary of the number of characters
    after the last occurrence of a given character. This provides the number of
    characters to shift by in the case of a mismatch. Defaults to the length of
    the string.
    """
    table = defaultdict(lambda: len(pattern))
    for i in range(len(pattern) - 1):
        table[pattern[i]] = len(pattern) - i - 1
    return table


def run_bmh(table, text, pattern, M, compare):
    """
    Using the precalculated table, , making comparisons with the provided compare function and exiting whenever a match is found
    """

    # Currently attempted offset of the pattern in the text
    i = 0

    # Keep going until the pattern overflows the text
    while (i + M <= len(text)) and (not global_var.Match_found):
        # Start matching from the end of the string
        j = M - 1

        # Match each element in the pattern, from the end to the beginning
        while j >= 0 and compare(text, i + j, pattern, j):
            j -= 1

        # If the start of the string has been reached (and so every comparison
        # was successful), then yield the position
        if j < 0:
            #print("PATTERN FOUND")
            return i

        # Shift by the precalculated offset given by the character in the text
        # at the far right of the pattern, so that it lines up with an equal
        # character in the pattern, if posssible. Otherwise the pattern is
        # moved to after this position.
        i += table[text[i + M - 1]]
    if global_var.Match_found:
        return -10
    else:
        return -1