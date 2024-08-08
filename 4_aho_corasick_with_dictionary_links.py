class Node:
    def __init__(self, letter, prefix):
        self.letter = letter                # The character this node represents
        self.children = {}                  # Dictionary of child nodes
        self.is_end_of_pattern = False      # Flag to mark if this node is the end of a pattern
        self.fail = None                    # Failure link for Aho-Corasick automaton
        self.prefix = prefix                # The prefix leading to this node (useful for debugging)
        self.output = []                    # List to store patterns that end at this node

    def __str__(self):
        letter = "[EMPTY]" if self.letter == "" else self.letter
        if len(self.children) == 0:
            return letter
        elif len(self.children) == 1:
            return letter + " -> " + str(list(self.children.values())[0])
        else:
            return letter + " -> (" + ", ".join([str(child) for child in self.children.values()]) + ")"


def aho_preprocess_strings_as_trie(strings):
    root = Node("", "")  # Initialize the root of the trie

    # Add all the strings to the trie
    for string in strings:
        current = root
        for (j, letter) in enumerate(string):
            # Add the letter to the trie if it doesn't exist
            if letter not in current.children:
                node = Node(letter, string[:j + 1])
                current.children[letter] = node
            else:
                node = current.children[letter]
            current = node
        current.is_end_of_pattern = True     # Mark the end of a pattern
        current.output.append(string)        # Add the pattern to the output list

    # Add failure links using BFS
    from collections import deque
    queue = deque()
    # Initialize the queue with the root's children
    for child in root.children.values():
        child.fail = root
        queue.append(child)

    # Process each node in the queue
    while queue:
        current = queue.popleft()
        for letter, child in current.children.items():
            queue.append(child)
            fail = current.fail
            # Find the fail link for the current child node
            while fail is not None and letter not in fail.children:
                fail = fail.fail
            if fail is None:
                child.fail = root
            else:
                child.fail = fail.children[letter]
                child.output.extend(child.fail.output)  # Merge output lists

    return root


def aho_search_patterns_in_string(string, trie):
    n = len(string)
    current = trie
    # Traverse the string character by character
    for i in range(n):
        letter = string[i]
        # Follow the fail links if there is no matching child node
        while current is not None and letter not in current.children:
            current = current.fail
        if current is None:
            current = trie
            continue
        current = current.children[letter]
        # Print all patterns that end at the current node
        if current.output:
            for pattern in current.output:
                print("Pattern ", pattern, " found at index", i - len(pattern) + 1)


def find_fail_links(patterns, trie):
    fail_links = {}
    for pattern in patterns:
        current = trie
        for (i, letter) in enumerate(pattern):
            if letter in current.children:
                current = current.children[letter]
                fail_links[pattern[:i + 1]] = current.fail.prefix if current.fail else ""
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

    # Some patterns that don't work without dictionary links:
    patterns_2 = ["A", "AG", "C", "CAA", "GAG", "GC", "GCA"]
    string_2 = "GCAA"
    run(patterns_2, string_2)


if __name__ == "__main__":
    main()
