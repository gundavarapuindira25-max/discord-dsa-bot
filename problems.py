PROBLEMS = [
    # Week 1 - Arrays & Hashing
    {
        "week": 1,
        "topic": "Arrays & Hashing",
        "easy": {
            "title": "Contains Duplicate",
            "url": "https://leetcode.com/problems/contains-duplicate/",
            "pattern": "HashSet — check if element already seen",
        },
        "medium": {
            "title": "Group Anagrams",
            "url": "https://leetcode.com/problems/group-anagrams/",
            "pattern": "HashMap — sort each word as key",
        },
    },
    # Week 2 - Two Pointers
    {
        "week": 2,
        "topic": "Two Pointers",
        "easy": {
            "title": "Valid Palindrome",
            "url": "https://leetcode.com/problems/valid-palindrome/",
            "pattern": "Two pointers — left and right moving inward",
        },
        "medium": {
            "title": "3Sum",
            "url": "https://leetcode.com/problems/3sum/",
            "pattern": "Sort + two pointers inside a loop",
        },
    },
    # Week 3 - Sliding Window
    {
        "week": 3,
        "topic": "Sliding Window",
        "easy": {
            "title": "Best Time to Buy and Sell Stock",
            "url": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/",
            "pattern": "Track min price, update max profit",
        },
        "medium": {
            "title": "Longest Substring Without Repeating Characters",
            "url": "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
            "pattern": "Sliding window + HashSet",
        },
    },
    # Week 4 - Stack
    {
        "week": 4,
        "topic": "Stack",
        "easy": {
            "title": "Valid Parentheses",
            "url": "https://leetcode.com/problems/valid-parentheses/",
            "pattern": "Push open, pop and match on close",
        },
        "medium": {
            "title": "Min Stack",
            "url": "https://leetcode.com/problems/min-stack/",
            "pattern": "Stack of (value, current_min) pairs",
        },
    },
    # Week 5 - Binary Search
    {
        "week": 5,
        "topic": "Binary Search",
        "easy": {
            "title": "Binary Search",
            "url": "https://leetcode.com/problems/binary-search/",
            "pattern": "Classic left/right/mid — know this cold",
        },
        "medium": {
            "title": "Search in Rotated Sorted Array",
            "url": "https://leetcode.com/problems/search-in-rotated-sorted-array/",
            "pattern": "Binary search — determine which half is sorted",
        },
    },
    # Week 6 - Linked List
    {
        "week": 6,
        "topic": "Linked List",
        "easy": {
            "title": "Reverse Linked List",
            "url": "https://leetcode.com/problems/reverse-linked-list/",
            "pattern": "Three pointers: prev, curr, next",
        },
        "medium": {
            "title": "Add Two Numbers",
            "url": "https://leetcode.com/problems/add-two-numbers/",
            "pattern": "Traverse both lists, carry the remainder",
        },
    },
    # Week 7 - Trees
    {
        "week": 7,
        "topic": "Trees",
        "easy": {
            "title": "Invert Binary Tree",
            "url": "https://leetcode.com/problems/invert-binary-tree/",
            "pattern": "Recursive swap left and right subtrees",
        },
        "medium": {
            "title": "Validate Binary Search Tree",
            "url": "https://leetcode.com/problems/validate-binary-search-tree/",
            "pattern": "Pass min/max bounds through recursion",
        },
    },
    # Week 8 - Heap / Priority Queue
    {
        "week": 8,
        "topic": "Heap / Priority Queue",
        "easy": {
            "title": "Kth Largest Element in a Stream",
            "url": "https://leetcode.com/problems/kth-largest-element-in-a-stream/",
            "pattern": "Min-heap of size k",
        },
        "medium": {
            "title": "K Closest Points to Origin",
            "url": "https://leetcode.com/problems/k-closest-points-to-origin/",
            "pattern": "Max-heap of size k, or sort by distance",
        },
    },
    # Week 9 - Backtracking
    {
        "week": 9,
        "topic": "Backtracking",
        "easy": {
            "title": "Letter Case Permutation",
            "url": "https://leetcode.com/problems/letter-case-permutation/",
            "pattern": "Recurse on each char — two branches for letters",
        },
        "medium": {
            "title": "Combination Sum",
            "url": "https://leetcode.com/problems/combination-sum/",
            "pattern": "DFS — include or skip each candidate",
        },
    },
    # Week 10 - Graphs
    {
        "week": 10,
        "topic": "Graphs",
        "easy": {
            "title": "Find if Path Exists in Graph",
            "url": "https://leetcode.com/problems/find-if-path-exists-in-graph/",
            "pattern": "BFS or DFS from source to target",
        },
        "medium": {
            "title": "Number of Islands",
            "url": "https://leetcode.com/problems/number-of-islands/",
            "pattern": "DFS/BFS flood-fill on each unvisited '1'",
        },
    },
    # Week 11 - Dynamic Programming
    {
        "week": 11,
        "topic": "Dynamic Programming",
        "easy": {
            "title": "Climbing Stairs",
            "url": "https://leetcode.com/problems/climbing-stairs/",
            "pattern": "dp[i] = dp[i-1] + dp[i-2]",
        },
        "medium": {
            "title": "House Robber",
            "url": "https://leetcode.com/problems/house-robber/",
            "pattern": "dp[i] = max(dp[i-1], dp[i-2] + nums[i])",
        },
    },
    # Week 12 - Greedy
    {
        "week": 12,
        "topic": "Greedy",
        "easy": {
            "title": "Lemonade Change",
            "url": "https://leetcode.com/problems/lemonade-change/",
            "pattern": "Track bills, always use largest first",
        },
        "medium": {
            "title": "Jump Game",
            "url": "https://leetcode.com/problems/jump-game/",
            "pattern": "Track max reachable index as you go",
        },
    },
]
