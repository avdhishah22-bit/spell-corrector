"""
Edit distance = minimum number of single-character operations needed to turn
word1 into word2, where the allowed operations (each with cost 1) are:
    - insertion
    - deletion
    - substitution

Notes:
    - The functions are case-sensitive. Normalisation (lower-casing, stripping)
    - No external libraries are used; the DP is written by hand.
"""

# Costs are named constants so the recurrence is easy to read / adjust.
INSERT_COST = 1
DELETE_COST = 1
SUBSTITUTE_COST = 1


def _validate(word1, word2):
    if not isinstance(word1, str) or not isinstance(word2, str):
        raise TypeError("levenshtein_distance expects two strings")


# --------------------------------------------------------------------------
# 1. Standard 2D DP matrix  -  O(m*n) time, O(m*n) space
# --------------------------------------------------------------------------
def levenshtein_distance_matrix(word1, word2, return_matrix=False):
    """
    Standard dynamic-programming solution using the full (m+1) x (n+1) matrix.

    Definition:
        dp[i][j] = edit distance between the first i characters of word1
                   and the first j characters of word2.

    Base cases:
        dp[i][0] = i * DELETE_COST   (delete all i chars to reach "")
        dp[0][j] = j * INSERT_COST   (insert all j chars starting from "")

    Recurrence (for i, j >= 1):
        if word1[i-1] == word2[j-1]:
            dp[i][j] = dp[i-1][j-1]                       # no cost, characters match
        else:
            dp[i][j] = min(
                dp[i-1][j]   + DELETE_COST,               # delete word1[i-1]
                dp[i][j-1]   + INSERT_COST,               # insert word2[j-1]
                dp[i-1][j-1] + SUBSTITUTE_COST,           # substitute word1[i-1] -> word2[j-1]
            )

    Answer: dp[m][n].

    If return_matrix is True, returns (distance, dp) so the table can be
    printed / explained in a viva.
    """
    _validate(word1, word2)
    m, n = len(word1), len(word2)

    # Build the table.
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases.
    for i in range(m + 1):
        dp[i][0] = i * DELETE_COST
    for j in range(n + 1):
        dp[0][j] = j * INSERT_COST

    # Fill the table row by row.
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                delete = dp[i - 1][j] + DELETE_COST
                insert = dp[i][j - 1] + INSERT_COST
                substitute = dp[i - 1][j - 1] + SUBSTITUTE_COST
                dp[i][j] = min(delete, insert, substitute)

    if return_matrix:
        return dp[m][n], dp
    return dp[m][n]


# --------------------------------------------------------------------------
# 2. Memory-optimised version  -  O(m*n) time, O(min(m, n)) space
# --------------------------------------------------------------------------
def levenshtein_distance_optimized(word1, word2):
    """
    Same recurrence, but only the previous row and the current row are kept.

    Why this is valid:
        dp[i][j] depends only on dp[i-1][j-1], dp[i-1][j] (previous row) and
        dp[i][j-1] (current row). Rows older than i-1 are never read again,
        so they can be discarded.

    Why O(min(m, n)) space:
        The distance is symmetric (distance(a, b) == distance(b, a) because an
        insertion in one direction is a deletion in the other, both cost 1),
        so we make the row run along the SHORTER word.
    """
    _validate(word1, word2)

    # Make word2 the shorter one so each row has min(m, n) + 1 entries.
    if len(word2) > len(word1):
        word1, word2 = word2, word1
    m, n = len(word1), len(word2)

    # Row 0 of the full matrix: dp[0][j] = j.
    previous = list(range(n + 1))

    for i in range(1, m + 1):
        current = [0] * (n + 1)
        current[0] = i  # dp[i][0] = i
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                current[j] = previous[j - 1]
            else:
                current[j] = 1 + min(
                    previous[j],       # delete
                    current[j - 1],    # insert
                    previous[j - 1],   # substitute
                )
        previous = current  # current row becomes the previous row

    return previous[n]


# --------------------------------------------------------------------------
# 3. Public interface (agreed with B2 and B4)
# --------------------------------------------------------------------------
def levenshtein_distance(word1, word2):
    """
    Return the Levenshtein edit distance between word1 and word2 as an int.

    Uses the memory-optimised implementation, with quick exits for trivial
    cases (these are just shortcuts; the DP gives the same answers).
    """
    _validate(word1, word2)

    if word1 == word2:
        return 0
    if not word1:
        return len(word2)
    if not word2:
        return len(word1)

    return levenshtein_distance_optimized(word1, word2)


if __name__ == "__main__":
    # Small demo: print the DP table for a classic example.
    a, b = "kitten", "sitting"
    dist, table = levenshtein_distance_matrix(a, b, return_matrix=True)
    print(f"distance({a!r}, {b!r}) = {dist}\n")
    header = "      " + "  ".join(["''"] + list(b))
    print(header)
    for i, row in enumerate(table):
        label = "''" if i == 0 else a[i - 1]
        print(f"{label:>3}  " + "  ".join(f"{v:>2}" for v in row))
