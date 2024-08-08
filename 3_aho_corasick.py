
"""
Definition of a trie node for Aho-Corasick. This is pretty much the same as the KMP trie node,
but with a prefix field, which helps for debugging.
"""
class Node:
    def __init__(self, letter, prefix):
        self.letter = letter
        self.children = {}
        self.is_end_of_pattern = False
        self.fail = None
        self.prefix = prefix
    
    def __str__(self):
        letter = "[EMPTY]" if self.letter == "" else self.letter

        if len(self.children) == 0:
            return letter
        elif len(self.children) == 1:
            return letter + " -> " + str(list(self.children.values())[0])
        else:
            return letter + " -> (" + ", ".join([str(child) for child in self.children.values()]) + ")"


"""
Processes a set of pattern strings into a trie. This is just a tree that contains all the possible
prefixes. It also contains "fail" nodes that get traversed if the search fails. Well, technically
it's a graph not a tree, due to the fail links (which can be cyclic). Because we traverse it similarly
to executing a program graph (AST) or matching a regex, it can also be thought of as an automaton.

If you're interested in automata in general, this YouTube channel has a good series of videos
that explain them: youtube.com/watch?v=Qa6csfkK7_I

For the Aho-Corasick automaton specifically, see https://www.youtube.com/watch?v=O7_w001f58c
for a video explanation (highly recommended).
"""
def aho_preprocess_strings_as_trie(strings):
    root = Node("", "")
    # Add all the strings to the trie.
    for string in strings:
        current = root
        
        for (j, letter) in enumerate(string):
            # Add the letter to the trie.
            if letter not in current.children:
                node = Node(letter, string[:j + 1])
                current.children[letter] = node
            else:
                node = current.children[letter]
            current = node
        current.is_end_of_pattern = True


    # Add failure links. This has to be done after the trie is created, because
    # we have to know about *all* the strings before we can determine the right failure link for each node.
    for string in strings:
        current = root

        for (j, letter) in enumerate(string):
            node = current.children[letter]

            # Add the failure link. The failure link is the longest proper suffix of the current
            # string that is also a prefix of the pattern.
            # Key insight: *THIS IS THE SAME AS KMP*. Aho-Corasick is just a generalisation of KMP to multiple patterns.
            current_string = string[:j + 1]
            suffixes = []
            for k in range(1, len(current_string)): # Skip the first suffix, which is the whole string.
                suffixes.append(current_string[k:])
            
            search = root
            for suffix in reversed(suffixes):
                search = search_trie(root, suffix)
                if search is None:
                    search = root
                else:
                    break
            node.fail = search
            current = node
            
    return root


# Helper to search a trie for a given string. Returns the node that matches, or None if there is no match.
def search_trie(root, string):
    current = root
    for letter in string:
        if letter in current.children:
            current = current.children[letter]
        else:
            return None
    return current


# Runs Aho-Corasick! The actual traversal of the trie is really simple.
def aho_search_patterns_in_string(string, trie):
    n = len(string)
    current = trie
    for i in range(n):
        letter = string[i]
        if letter in current.children:
            current = current.children[letter]
            if current.is_end_of_pattern:
                print("Pattern ", current.prefix, " found at index", i - len(current.prefix) + 1)
                current = current.fail
        elif current.fail is not None:
                current = current.fail
                i -= 1
        else:
            current = trie


# Returns fail links for printing.
def find_fail_links(patterns, trie):
    fail_links = {}
    for pattern in patterns:
        current = trie
        for (i, letter) in enumerate(pattern):
            if letter in current.children:
                current = current.children[letter]
                fail_links[pattern[:i+1]] = current.fail.prefix
            else:
                break
    return fail_links

def run(patterns, string):
    print()
    print("Running Aho-Corasick on the following patterns and string:")
    print("Patterns: ", str(patterns))
    print("String: ", string)
    print("...")

    trie = aho_preprocess_strings_as_trie(patterns)
    print("Pattern trie: ", str(trie))
    fail_links = find_fail_links(patterns, trie)
    print("Fail links: ", str(fail_links))
    aho_search_patterns_in_string(string, trie)


def main():
    # Some patterns that work without dictionary links:
    patterns_1 = ["ACC", "ATC", "CAT", "GCG"]
    string_1 = "GATTACCATCAT"
    run(patterns_1, string_1)

    # Some patterns that don't work without dictionary links.
    # The substring patterns get missed by the algorithm!
    # Watch this video about dictionary links: https://www.youtube.com/watch?v=OFKxWFew_L0
    # Then your homework is to get this working :)
    # Hint: Draw it out on paper first, then when coding make liberal use of the python debugger!
    patterns_2 = ["A", "AG", "C", "CAA", "GAG", "GC", "GCA"]
    string_2 = "GCAA"
    run(patterns_2, string_2)

if __name__ == "__main__":
    main()
