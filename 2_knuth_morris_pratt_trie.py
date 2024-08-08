
"""
Definition of a trie node for KMP.
"""
class Node:
    def __init__(self, letter):
        self.letter = letter
        self.children = {}
        self.is_end_of_pattern = False
        self.fail = None
    
    def __str__(self):
        letter = "[EMPTY]" if self.letter == "" else self.letter

        if len(self.children) == 0:
            return letter
        elif len(self.children) == 1:
            return letter + " -> " + str(list(self.children.values())[0])
        else:
            raise Exception("Node has more than one child")


"""
Processes a pattern string into a trie. This is the same data as the table version,
but in a tree format. The tree ends up being effectively a linked list, because there is only
one string. However, we can then generalise the idea to multiple strings to do Aho-Corasick,
and this will be a regular (not a linked list special case) trie.
"""
def kmp_preprocess_string_as_trie(string):
    # Track string prefixes. These are used for creating "fail" links.
    prefixes = []
    for i in range(len(string) + 1):
        prefixes.append(string[:i])
    print("Prefixes: " + str(prefixes))

    root = Node("")
    current = root
    for (i, letter) in enumerate(string):
        # Add the letter to the trie.
        node = Node(letter)
        current.children[letter] = node
        
        # Add the failure link. The failure link is the longest proper suffix of the current
        # string that is also a prefix of the pattern.
        prefix = prefixes[i]
        suffixes = []
        for j in range(len(prefix)):
            suffixes.append(prefix[j:])
        
        # Find the longest suffix of the current prefix.
        # For example, if the string is "BABBAGE" and we are currently up to the fifth letter, then
        # the current prefix is "BABBA", and the longest suffix of that prefix that is also a
        # prefix of the main string, is "BA".
        for suffix in reversed(suffixes):
            current = root
            for letter in suffix:
                if letter in current.children:
                    current = current.children[letter]
                else:
                    break
            if current != root:
                node.fail = current
                break
        
        # Move to the next node.
        current = node

    current.is_end_of_pattern = True
    return root


"""
Searches for a pattern in a string using the KMP algorithm.
This version uses a trie as the format of the preprocessed pattern.
"""
def kmp_search_pattern_in_string(pattern, string, trie):
    m = len(pattern)
    n = len(string)
    trie = kmp_preprocess_string_as_trie(pattern)
    # Perform the search using the KMP algorithm
    current = trie
    for i in range(n):
        while current != None and string[i] not in current.children:
            current = current.fail
        if current == None:
            current = trie
        else:
            current = current.children[string[i]]
            if current.is_end_of_pattern:
                print("Pattern found at index", i - m + 1)


def main():
    pattern = "babbage"
    string = "ababbabagebabbageabab"
    trie = kmp_preprocess_string_as_trie(pattern)
    print("Pattern trie: " + str(trie))
    kmp_search_pattern_in_string(pattern, string, trie)

if __name__ == "__main__":
    main()
