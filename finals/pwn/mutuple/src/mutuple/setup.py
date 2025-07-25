from distutils.core import setup, Extension

def main():
    setup(
        name="mutuple",
        ext_modules=[Extension("mutuple", ["chall.c"])]
    )

if __name__ == "__main__":
    main()
