
"""
Preprocesses a string into a table (list) of the longest proper suffixes that are also prefixes.
Example:

pattern = "babbage"
table = [0, 0, 1, 1, 2, 0, 0]

Imagine each of these values as pointers to the node that should start at if the search fails.
For example, if a string contains "babba", but then diverges from the pattern,
the search should continue from the first "ba", so this value is 2.

Basically:
b -> "" (0)
ba -> "" (0)
bab -> "b" (1)
babb -> "b" (1)
babba -> "ba" (2)
babbag -> "" (0)
babbage -> "" (0)

Hence the result of kmp_preprocess_string_as_table("babbage") is [0, 0, 1, 1, 2, 0, 0].
"""
def kmp_preprocess_string_as_table(string):
    n = len(string)
    table = [0] * n
    i = 1
    j = 0
    while i < n:
        if string[i] == string[j]:
            j += 1
            table[i] = j
            i += 1
        else:
            if j != 0:
                j = table[j - 1]
            else:
                table[i] = 0
                i += 1
    return table


"""
Searches for a pattern in a string using the KMP algorithm.
This allows searching for a pattern in a string in O(n) time, where n is the length of the string.
The preprocessing of the pattern takes O(m) time, where m is the length of the pattern.
"""
def kmp_search_pattern_in_string(pattern, string, table):
    m = len(pattern)
    n = len(string)
    table = kmp_preprocess_string_as_table(pattern)
    i = 0
    j = 0
    while i < n:
        if pattern[j] == string[i]:
            i += 1
            j += 1
        if j == m:
            print("Pattern found at index", i - j)
            j = table[j - 1]
        elif i < n and pattern[j] != string[i]:
            if j != 0:
                j = table[j - 1]
            else:
                i += 1


def main():
    pattern = "babbage"
    string = "ababbabagebabbageabab"
    table = kmp_preprocess_string_as_table(pattern)
    print("Pattern table: " + str(table))
    kmp_search_pattern_in_string(pattern, string, table)

if __name__ == "__main__":
    main()
