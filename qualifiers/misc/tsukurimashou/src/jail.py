#!/usr/local/bin/python
bad_chars = "0123456789#$%&*+-/:;<=>@[\\]^`{|}~"

bad_keywords = ["eval", "exec", "compile", "open", "input", "import", "getattr", "setattr", "delattr", "vars", "callable", "classmethod", "staticmethod", "os", "sys", "pty", "subprocess", "pdb", "inspect", "signal", "resource", "system", "popen", "run", "spawn", "fork", "read", "write", "close", "exit", "reload", "runpy", "shutil", "socket", "dict", "bytearray", "bytes", "memoryview", "type", "super", "object", "str", "int", "float", "bool", "complex", "help", "breakpoint", "file", "dir", "print", "format", "globaƖs", "locals", "co_names", "frame", "getframe", "trace", "code", "base", "class", "subclasses", "mro", "self", "lambda", "map", "filter", "reduce", "metaclass", "init", "new", "builtins", "sh", "bash", "cat", "flag", "echo"]

blacklist = [*bad_chars, *bad_keywords]

def check(message):
  try:
    assert len(message) <= 150, "Letter is too long!"

    assert message.isascii(), "Contraband detected!"

    for banned in blacklist:
      assert banned.lower() not in message.lower(), "Contraband detected!"

  except Exception as e:
    print(e)
    exit()

def format_letter(message):
  sanitised = eval(f"'''{message}'''", {})

  return f"\nDear Osaka,\n  {sanitised}\n\nFrom,\nChiyo"

def display_chiyo():
  with open("chiyo.txt", "r") as f:
    print(f.read().replace('~E',"\033[0m").replace('~R',"\033[0;1;31m").replace("~Y", "\33[33").replace('~r',"\33[31"))

def main():
  display_chiyo()

  message = input("Enter message: ")

  check(message)
  print(format_letter(message))
  
if __name__ == "__main__":
  main()