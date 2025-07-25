#!/usr/local/bin/python

blacklist = ["eval", "exec", "compile", "open", "import", "help", "breakpoint", "builtins", "locals", "globals", "flag"]

def banner():
    width = 50

    baby = """   ,=""=,
  c , _,{
  /\  @ )                 __
 /  ^~~^\          <=.,__/ '}=
(_/ ,, ,,)          \_ _>_/~
 ~\_(/-\)'-,_,_,_,-'(_)-(_)"""
    
    baby = [*map(lambda x: x.rstrip(), baby.split("\n"))]
    margin = (width - max(map(lambda x: len(x.strip()), baby))) // 2

    print("=" * width)
    for line in baby:
        print(f'{" " * margin}{line}')
    print()
    print("Welcome to Pyjail training!".center(width))
    print("=" * width)

def check(exp):
    try:
        assert exp.isascii()

        for banned in blacklist:
            assert banned not in exp
    except:
        print("bad word detected!!!")
        exit()

if __name__ == "__main__":
    banner()

    exp = input("> ")
    check(exp)

    try:
        eval(exp, {})
    except Exception as e:
        print(f"Error: {e}")