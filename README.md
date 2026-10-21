# Spell Corrector: Edit Distance Module 

Part of the DSA project **Autocomplete and Spell Corrector using Trie**.
This part implements the **Levenshtein edit distance** using dynamic programming,
written from scratch with no external libraries.

## What it does

`levenshtein_distance(word1, word2)` returns the minimum number of single-character
**insertions, deletions and substitutions** (each costing 1) needed to turn
`word1` into `word2`.

```python
from spell_correction.edit_distance import levenshtein_distance

levenshtein_distance("aple", "apple")   # Returns 1
levenshtein_distance("cat", "cut")      # Returns 1
levenshtein_distance("book", "books")   # Retrurns 1
levenshtein_distance("abc", "xyz")      # Returns 3
levenshtein_distance("apple", "apple")  # Returns 0
```

## Project structure

```
spell-corrector/
├── spell_correction/
│   ├── __init__.py            
│   └── edit_distance.py       
├── tests/
│   ├── __init__.py            
│   └── test_edit_distance.py 
└── README.md
```

## Implementations

| Function | Time | Space | Notes |
|---|---|---|---|
| `levenshtein_distance_matrix` | O(m*n) | O(m*n) | Standard 2D DP table; can return the full matrix |
| `levenshtein_distance_optimized` | O(m*n) | O(min(m, n)) | Keeps only the previous and current rows |
| `levenshtein_distance` | O(m*n) | O(min(m, n)) | Public interface used by B2 and B4 |

## Why dynamic programming?
- **Optimal substructure:** the best way to convert `word1[:i]` into `word2[:j]`
  is built from the best ways to convert slightly shorter prefixes.
- **Overlapping subproblems:** plain recursion recomputes the same `(i, j)` pair
  exponentially many times. A table stores each answer once -> O(m*n).

## How the DP works

`dp[i][j]` is the edit distance between the first `i` characters of `word1`
and the first `j` characters of `word2`.

- Base cases: `dp[i][0] = i` and `dp[0][j] = j`
- If `word1[i-1] == word2[j-1]`: `dp[i][j] = dp[i-1][j-1]`
- Otherwise: `dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`
  (delete, insert, substitute)

The answer is `dp[m][n]`. See `docs/EDIT_DISTANCE_NOTES.md` for a worked example.
### Worked example: `aple` -> `apple`
|   | "" | a | p | p | l | e |
|---|----|---|---|---|---|---|
| "" | 0 | 1 | 2 | 3 | 4 | 5 |
| a  | 1 | 0 | 1 | 2 | 3 | 4 |
| p  | 2 | 1 | 0 | 1 | 2 | 3 |
| l  | 3 | 2 | 1 | 1 | 1 | 2 |
| e  | 4 | 3 | 2 | 2 | 2 | 1 |

Bottom-right cell = **1**.
## Two-row optimisation
`dp[i][j]` only reads `dp[i-1][j-1]`, `dp[i-1][j]` (previous row) and
`dp[i][j-1]` (current row). Older rows are never used again, so we keep just
`previous` and `current`. Because distance is symmetric, we run the row along the
**shorter** word, giving O(min(m, n)) extra space.
## Running the tests

From the repository root:

```
python -m unittest discover -s tests -v
```

Expected result: `Ran 18 tests ... OK`.

To see the DP table demo:

```
python spell_correction/edit_distance.py
```

## Notes 

- **Case-sensitive:** lower-case words before calling.
- **Transpositions cost 2:** plain Levenshtein counts `recieve` -> `receive` as 2 edits, not 1.
- **Safe pruning bound:** `|len(a) - len(b)| <= distance(a, b).
- **Input check:** non-string inputs raise `TypeError`.
- **Interface:** `levenshtein_distance(word1, word2) -> int`


