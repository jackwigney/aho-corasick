class DictNode {
    letter: string;                     // The character this DictNode represents
    children: { [key: string]: DictNode };  // Dictionary of child DictNodes
    isEndOfPattern: boolean;            // Flag to mark if this DictNode is the end of a pattern
    fail: DictNode | null;                  // Failure link for Aho-Corasick automaton
    prefix: string;                     // The prefix leading to this DictNode (useful for debugging)
    output: string[];                   // List to store patterns that end at this DictNode

    constructor(letter: string, prefix: string) {
        this.letter = letter;
        this.children = {};
        this.isEndOfPattern = false;
        this.fail = null;
        this.prefix = prefix;
        this.output = [];
    }

    toString(): string {
        const letter = this.letter === "" ? "[EMPTY]" : this.letter;
        if (Object.keys(this.children).length === 0) {
            return letter;
        } else if (Object.keys(this.children).length === 1) {
            return letter + " -> " + Object.values(this.children)[0].toString();
        } else {
            return letter + " -> (" + Object.values(this.children).map(child => child.toString()).join(", ") + ")";
        }
    }
}

function ahoPreprocessStringsAsTrie(strings: string[]): DictNode {
    const root = new DictNode("", "");  // Initialize the root of the trie

    // Add all the strings to the trie
    for (const string of strings) {
        let current = root;
        for (let j = 0; j < string.length; j++) {
            const letter = string[j];
            // Add the letter to the trie if it doesn't exist
            if (!(letter in current.children)) {
                const node = new DictNode(letter, string.substring(0, j + 1));
                current.children[letter] = node;
            }
            current = current.children[letter];
        }
        current.isEndOfPattern = true;     // Mark the end of a pattern
        current.output.push(string);        // Add the pattern to the output list
    }

    // Add failure links using BFS
    const queue: DictNode[] = [];
    // Initialize the queue with the root's children
    for (const child of Object.values(root.children)) {
        child.fail = root;
        queue.push(child);
    }

    // Process each DictNode in the queue
    while (queue.length > 0) {
        const current = queue.shift()!;
        for (const [letter, child] of Object.entries(current.children)) {
            queue.push(child);
            let fail = current.fail;
            // Find the fail link for the current child DictNode
            while (fail !== null && !(letter in fail.children)) {
                fail = fail.fail;
            }
            if (fail === null) {
                child.fail = root;
            } else {
                child.fail = fail.children[letter];
                child.output.push(...child.fail.output);  // Merge output lists
            }
        }
    }

    return root;
}

function ahoSearchPatternsInString(string: string, trie: DictNode | null): void {
    const n = string.length;
    let current = trie;
    // Traverse the string character by character
    for (let i = 0; i < n; i++) {
        const letter = string[i];
        // Follow the fail links if there is no matching child DictNode
        while (current !== null && !(letter in current.children)) {
            current = current.fail;
        }
        if (current === null) {
            current = trie;
            continue;
        }
        current = current.children[letter];
        // Print all patterns that end at the current DictNode
        if (current.output.length > 0) {
            for (const pattern of current.output) {
                console.log(`Pattern ${pattern} found at index ${i - pattern.length + 1}`);
            }
        }
    }
}

function findFailLinks(patterns: string[], trie: DictNode): { [key: string]: string } {
    const failLinks: { [key: string]: string } = {};
    for (const pattern of patterns) {
        let current = trie;
        for (let i = 0; i < pattern.length; i++) {
            const letter = pattern[i];
            if (letter in current.children) {
                current = current.children[letter];
                failLinks[pattern.substring(0, i + 1)] = current.fail ? current.fail.prefix : "";
            } else {
                break;
            }
        }
    }
    return failLinks;
}

function run(patterns: string[], string: string): void {
    console.log("\nRunning Aho-Corasick on the following patterns and string:");
    console.log("Patterns: ", patterns);
    console.log("String: ", string);
    console.log("...");

    const trie = ahoPreprocessStringsAsTrie(patterns);
    console.log("Pattern trie: ", trie.toString());
    const failLinks = findFailLinks(patterns, trie);
    console.log("Fail links: ", failLinks);
    ahoSearchPatternsInString(string, trie);
}

function main(): void {
    // Some patterns that work without dictionary links:
    const patterns1 = ["ACC", "ATC", "CAT", "GCG"];
    const string1 = "GATTACCATCAT";
    run(patterns1, string1);

    // Some patterns that don't work without dictionary links:
    const patterns2 = ["A", "AG", "C", "CAA", "GAG", "GC", "GCA"];
    const string2 = "GCAA";
    run(patterns2, string2);
}

main();
