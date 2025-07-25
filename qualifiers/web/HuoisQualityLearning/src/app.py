from flask import Flask, render_template, request, g
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'techniques.db'

FLAG = os.getenv("FLAG")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE techniques (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            notes TEXT
        )
    ''')
    techniques = [
        ('Two Pointers', 'Great for sorted arrays'),
        ('Union Find', f'You win! Here is the flag: {FLAG}'),
        ('Segment Tree', 'Use it for range queries'),
        ('Binary Search', 'Efficient on monotonic functions'),
        ('DFS', 'Recursive, useful for exploring graphs'),
        ('BFS', 'Use a queue, great for shortest path in unweighted graphs'),
        ('Topological Sort', 'Linear ordering of DAGs'),
        ('Dijkstra\'s Algorithm', 'Efficient shortest path in weighted graphs'),
        ('Floyd-Warshall', 'All-pairs shortest paths, O(n^3)'),
        ('Bellman-Ford', 'Handles negative weights'),
        ('Knapsack DP', 'Classic dynamic programming problem'),
        ('Bitmask DP', 'Optimize states with bit manipulation'),
        ('Sliding Window', 'Efficient for subarray problems'),
        ('Trie', 'Prefix trees for efficient word lookups'),
        ('KMP Algorithm', 'Pattern matching in linear time'),
        ('Manacher\'s Algorithm', 'Find longest palindromic substring in linear time'),
        ('Sieve of Eratosthenes', 'Generate primes up to N efficiently'),
        ('Convex Hull Trick', 'Optimize certain dynamic programming transitions'),
        ('Heavy Light Decomposition', 'Advanced tree decomposition for path queries'),
        ('MO\'s Algorithm', 'Offline range queries optimization'),
        ('Fenwick Tree', 'Binary Indexed Tree for prefix sums'),
        ('Tarjan\'s Algorithm', 'Find strongly connected components'),
        ('Kosaraju\'s Algorithm', 'Alternative SCC algorithm using 2 passes'),
        ('Z-Algorithm', 'String matching, computes Z-array'),
        ('Centroid Decomposition', 'Tree decomposition technique for complex queries'),
        ('Matrix Exponentiation', 'Solve recurrences in log(n) time'),
        ('Longest Increasing Subsequence', 'Can be solved in O(n log n)'),
        ('Suffix Array', 'Useful for string processing'),
        ('Rabin-Karp', 'String matching using hashing'),
        ('Binary Lifting', 'LCA in O(log n)'),
        ('Digit DP', 'Dynamic programming on digits'),
        ('Cycle Detection', 'Useful in graph validation'),
        ('Disjoint Set Union with Rollback', 'Used in persistent union find variants'),
        ('Meet in the Middle', 'Divide and conquer approach for hard brute-force problems'),
        ('Game Theory - Grundy Numbers', 'Sprague-Grundy theorem applies to impartial games'),
        ('Greedy with Sorting', 'Common combo for interval problems'),
        ('0-1 BFS', 'Deque-based BFS for graphs with edge weights 0 or 1'),
        ('Persistent Segment Tree', 'Track historical states efficiently'),
        ('Implicit Segment Tree', 'Handles huge coordinate ranges'),
        ('CDQ Divide and Conquer', 'Used for some advanced offline problems'),
    ]
    c.executemany('INSERT INTO techniques (name, notes) VALUES (?, ?)', techniques)
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    error = None
    if request.method == 'POST':
        query = request.form.get('technique')
        db = get_db()
        try:
            # VULNERABLE: UNSAFE STRING FORMATTING
            sql = f"SELECT name FROM techniques WHERE name LIKE '%{query}%'"
            cursor = db.execute(sql)
            results = cursor.fetchall()
        except Exception as e:
            error = str(e)
    return render_template('index.html', results=results, error=error)

if __name__ == '__main__':
    init_db()
    app.run('0.0.0.0', 12958)
