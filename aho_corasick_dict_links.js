var DictNode = /** @class */ (function () {
    function DictNode(letter, prefix) {
        this.letter = letter;
        this.children = {};
        this.isEndOfPattern = false;
        this.fail = null;
        this.prefix = prefix;
        this.output = [];
    }
    DictNode.prototype.toString = function () {
        var letter = this.letter === "" ? "[EMPTY]" : this.letter;
        if (Object.keys(this.children).length === 0) {
            return letter;
        }
        else if (Object.keys(this.children).length === 1) {
            return letter + " -> " + Object.values(this.children)[0].toString();
        }
        else {
            return letter + " -> (" + Object.values(this.children).map(function (child) { return child.toString(); }).join(", ") + ")";
        }
    };
    return DictNode;
}());
function ahoPreprocessStringsAsTrie(strings) {
    var _a;
    var root = new DictNode("", ""); // Initialize the root of the trie
    // Add all the strings to the trie
    for (var _i = 0, strings_1 = strings; _i < strings_1.length; _i++) {
        var string = strings_1[_i];
        var current = root;
        for (var j = 0; j < string.length; j++) {
            var letter = string[j];
            // Add the letter to the trie if it doesn't exist
            if (!(letter in current.children)) {
                var node = new DictNode(letter, string.substring(0, j + 1));
                current.children[letter] = node;
            }
            current = current.children[letter];
        }
        current.isEndOfPattern = true; // Mark the end of a pattern
        current.output.push(string); // Add the pattern to the output list
    }
    // Add failure links using BFS
    var queue = [];
    // Initialize the queue with the root's children
    for (var _b = 0, _c = Object.values(root.children); _b < _c.length; _b++) {
        var child = _c[_b];
        child.fail = root;
        queue.push(child);
    }
    // Process each DictNode in the queue
    while (queue.length > 0) {
        var current = queue.shift();
        for (var _d = 0, _e = Object.entries(current.children); _d < _e.length; _d++) {
            var _f = _e[_d], letter = _f[0], child = _f[1];
            queue.push(child);
            var fail = current.fail;
            // Find the fail link for the current child DictNode
            while (fail !== null && !(letter in fail.children)) {
                fail = fail.fail;
            }
            if (fail === null) {
                child.fail = root;
            }
            else {
                child.fail = fail.children[letter];
                (_a = child.output).push.apply(_a, child.fail.output); // Merge output lists
            }
        }
    }
    return root;
}
function ahoSearchPatternsInString(string, trie) {
    var n = string.length;
    var current = trie;
    // Traverse the string character by character
    for (var i = 0; i < n; i++) {
        var letter = string[i];
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
            for (var _i = 0, _a = current.output; _i < _a.length; _i++) {
                var pattern = _a[_i];
                console.log("Pattern ".concat(pattern, " found at index ").concat(i - pattern.length + 1));
            }
        }
    }
}
function findFailLinks(patterns, trie) {
    var failLinks = {};
    for (var _i = 0, patterns_1 = patterns; _i < patterns_1.length; _i++) {
        var pattern = patterns_1[_i];
        var current = trie;
        for (var i = 0; i < pattern.length; i++) {
            var letter = pattern[i];
            if (letter in current.children) {
                current = current.children[letter];
                failLinks[pattern.substring(0, i + 1)] = current.fail ? current.fail.prefix : "";
            }
            else {
                break;
            }
        }
    }
    return failLinks;
}
function run(patterns, string) {
    console.log("\nRunning Aho-Corasick on the following patterns and string:");
    console.log("Patterns: ", patterns);
    console.log("String: ", string);
    console.log("...");
    var trie = ahoPreprocessStringsAsTrie(patterns);
    console.log("Pattern trie: ", trie.toString());
    var failLinks = findFailLinks(patterns, trie);
    console.log("Fail links: ", failLinks);
    ahoSearchPatternsInString(string, trie);
}
function main() {
    // Some patterns that work without dictionary links:
    var patterns1 = ["ACC", "ATC", "CAT", "GCG"];
    var string1 = "GATTACCATCAT";
    run(patterns1, string1);
    // Some patterns that don't work without dictionary links:
    var patterns2 = ["A", "AG", "C", "CAA", "GAG", "GC", "GCA"];
    var string2 = "GCAA";
    run(patterns2, string2);
}
main();
