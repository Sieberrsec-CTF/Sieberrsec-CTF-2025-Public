#!/usr/local/bin/python
characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '"', '#', '$', '%', '&', "'", '*', '+', ',', '-', '/', ':', ';', '<', '>', '?', '@', '\\', '^', '_', '`', '|', '~', ' ', '\t', '\n']

premium_stuff = ["async", "await", "yield", "assert", "eval", "exec", "compile", "input", "import", "breakpoint", "help", "locals", "globals", "builtins", "exit", "print", "bool", "bytearray", "bytes", "classmethod", "complex", "dict", "enumerate", "filter", 
"float", "frozenset", "int", "list", "map", "memoryview", "object", "property", "range", "reversed", "set", "slice", "staticmethod", "str", "super", "tuple", "type", "zip"]

class MiniVim:
    def __init__(self):
        self.padding = 40
        self.code = ""

    def start(self):
        while True:
            self.display_menu()
            choice = input("Select an option: ")

            if choice == "1":
                self.display_code()
            elif choice == "2":
                self.editor()
            elif choice == "3":
                self.clear_code()
            elif choice == "4":
                self.run_code()
            elif choice == "5":
                self.about()
            elif choice == "6":
                print("Exiting...")
                exit()

    def clear(self):
        import os
        os.system('clear')

    def pause(self):
        input("Press Enter to return to menu...")

    def banner(self, lines):
        print("=" * self.padding)
        
        for line in lines:
            print(line.center(self.padding))

        print("=" * self.padding)

    def display_menu(self):
        self.clear()
        self.banner(["MiniVim 1.0"])

        print("1. Inspect code file")
        print("2. Edit code file")
        print("3. Clear code file")
        print("4. Execute code file")
        print("5. About")
        print("6. Exit")
        print("=" * self.padding)

    def about(self):
        self.clear()
        self.banner(["MiniVim 1.0", "A lightweight text-based Python IDE", "By jeff160"])

        self.pause()

    def display_code(self):
        self.clear()
        self.banner(["Your Code"])
        print(self.code)

        self.pause()

    def clear_code(self):
        self.clear()
        self.banner(["Code file emptied"])
        
        self.code = ""
        self.pause()

    def run_code(self):
        self.clear()
        self.banner(["Execution Results"])

        try:
            import time
            start_time = time.time()

            exec(self.code, {})

            end_time = time.time()

            print(f"\nFinished execution in {round((end_time - start_time) * 1000, 7)}ms")
        except Exception as e:
            print(f"Error: {e}")

        self.pause()

    def editor(self):
        self.clear()
        self.banner(["Enter Python code line by line", "Empty line to finish"])

        while True:
            try:
                line = input("> ")

                if not len(line):
                    break

                for char in line:
                    assert char in characters, "Invalid character!"

                for stuff in premium_stuff:
                    assert stuff not in line, "You don't have access to this feature! Premium subscription coming soon!"

                self.code += line + "\n"

            except Exception as e:
                print(e)

if __name__ == "__main__":
    ide = MiniVim()
    ide.clear()
    ide.start()