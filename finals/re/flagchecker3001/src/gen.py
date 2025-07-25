import random

def assemble(indices, signs, op, constant):
    parts = [f"{'+' if s == 1 else '-'} s[{i}]"
             for s, i in zip(signs, indices)]
    expr  = ' '.join(parts).lstrip('+ ').replace('+ -', '- ')
    return f"{expr} {op} {constant}"

def _balanced_combo(s1, s2, terms, max_tries):
    n = len(s1)
    diff = [ord(a) - ord(b) for a, b in zip(s1, s2)]
    for _ in range(max_tries):
        idx  = [random.randrange(n) for _ in range(terms)]
        sign = [random.choice((1, -1)) for _ in range(terms)]
        if sum(s * diff[i] for s, i in zip(sign, idx)) == 0:
            return idx, sign
    raise RuntimeError("pmo")


def unbalanced(s1, s2, terms, max_tries):
    n = len(s1)
    for _ in range(max_tries):
        idx  = [random.randrange(n) for _ in range(terms)]
        sign = [random.choice((1, -1)) for _ in range(terms)]
        v1   = sum(s * ord(s1[i]) for s, i in zip(sign, idx))
        v2   = sum(s * ord(s2[i]) for s, i in zip(sign, idx))
        if v1 != v2:
            return idx, sign, v1, v2
    raise RuntimeError("pmo")

def generate_eq_both(s1, s2, terms=5, max_tries=10000):
    idx, sign   = _balanced_combo(s1, s2, terms, max_tries)
    constant    = sum(s * ord(s1[i]) for s, i in zip(sign, idx))
    return assemble(idx, sign, '==', constant)


def generate_ne_both(s1, s2, terms=5, max_tries=10000):
    idx, sign   = _balanced_combo(s1, s2, terms, max_tries)
    value       = sum(s * ord(s1[i]) for s, i in zip(sign, idx))
    offset      = random.choice([i for i in range(-5, 6) if i != 0])
    constant    = value + offset
    return assemble(idx, sign, '!=', constant)


def generate_eq_s1(s1, s2, terms=5, max_tries=10000):
    idx, sign, v1, _ = unbalanced(s1, s2, terms, max_tries)
    return assemble(idx, sign, '==', v1)


def generate_ne_s2(s1, s2, terms=5, max_tries=10000):
    idx, sign, v1, v2 = unbalanced(s1, s2, terms, max_tries)
    constant = v2 
    return assemble(idx, sign, '!=', constant)


def gen(s1, s2, terms, tries, lines):
    assert len(s1) == len(s2)
    funcs = [
        generate_eq_both,
        generate_ne_both,
        generate_eq_s1,
        generate_ne_s2,
        
    ]
    random.seed(1751440047)
    stuff = [random.getrandbits(1) for i in range(lines)]
    random.seed(1337)
    res = []
    for i in stuff:
        f = funcs[i * 2 + random.getrandbits(1)]
        res.append(f(s1, s2, terms, tries))
    return res

s1 = "The friends we made along the way"
s2 = "sctf{4dv4nc3d_py_m0nk3y_p4tch1ng}"

lines = 100
a = gen(s1, s2, 20, 10000, lines)
random.seed(1751440047)
stuff = [random.getrandbits(1) for i in range(lines)]

for i in range(lines):    
    line = a[i]
    s = s1.encode()
    # print(eval(line), end=' ')

    s = s2.encode()
    if stuff[i]:
        if "!=" in line:
            line = line.replace("!=", "==")
        elif "==" in line:
            line = line.replace("==", "!=")
        print(f"solver.add({line})")
        # print(not eval(line))
    else:
        print(f"solver.add({line})")
        # print(eval(line))