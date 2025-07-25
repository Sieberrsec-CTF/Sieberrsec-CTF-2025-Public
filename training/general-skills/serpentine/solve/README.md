# picoMini 2022 - Serpentine (modified)

1. Download the provided file

```bash
# download the provided file
ctfplayer@enxgmatic:~$ wget X

# verify it is present using "ls"
ctfplayer@enxgmatic:~$ ls
serpentine.zip
```

2. Unzip the file

```bash
# unzip the file
ctfplayer@enxgmatic:~$ unzip serpentine.zip
Archive:  serpentine.zip
 extracting: flag_enc.txt
  inflating: serpentine.py

# verify the zip file was unzipped
ctfplayer@enxgmatic:~$ ls
flag_enc.txt  serpentine.py  serpentine.zip
```

3. Run the python script

```bash
ctfplayer@enxgmatic:~$ python3 serpentine.py

    Y
  .-^-.
 /     \      .- ~ ~ -.
()     ()    /   _ _   `.                     _ _ _
 \_   _/    /  /     \   \                . ~  _ _  ~ .
   | |     /  /       \   \             .' .~       ~-. `.
   | |    /  /         )   )           /  /             `.`.
   \ \_ _/  /         /   /           /  /                `'
    \_ _ _.'         /   /           (  (
                    /   /             \  \
                   /   /               \  \
                  /   /                 )  )
                 (   (                 /  /
                  `.  `.             .'  /
                    `.   ~ - - - - ~   .'
                       ~ . _ _ _ _ . ~

Welcome to the serpentine encourager!


a) Print encouragement
b) Print flag
c) Quit

What would you like to do? (a/b/c) b

Oops! I must have misplaced the print_flag function! Check my source code!
```

4. Check the source code of `serpentine.py` by running `cat serpentine.py`

```python
ctfplayer@enxgmatic:~$ cat serpentine.py
import random
import sys

def str_xor(secret, key):
    #extend key to secret length
    new_key = key
    i = 0
    while len(new_key) < len(secret):
        new_key = new_key + key[i]
        i = (i + 1) % len(key)
    return "".join([chr(ord(secret_c) ^ ord(new_key_c)) for (secret_c,new_key_c) in zip(secret,new_key)])



def print_flag():
  with open('flag_enc.txt','r') as f:
    flag_enc = f.read()

  flag = str_xor(flag_enc, 'sieberr')
  print(flag)



def print_encouragement():
  encouragements = ['You can do it!', 'Keep it up!',
                    'Look how far you\'ve come!']
  choice = random.choice(range(0, len(encouragements)))
  print('\n-----------------------------------------------------')
  print(encouragements[choice])
  print('-----------------------------------------------------\n\n')



def main():

  print(
'''
    Y
  .-^-.
 /     \      .- ~ ~ -.
()     ()    /   _ _   `.                     _ _ _
 \_   _/    /  /     \   \                . ~  _ _  ~ .
   | |     /  /       \   \             .' .~       ~-. `.
   | |    /  /         )   )           /  /             `.`.
   \ \_ _/  /         /   /           /  /                `'
    \_ _ _.'         /   /           (  (
                    /   /             \  \\
                   /   /               \  \\
                  /   /                 )  )
                 (   (                 /  /
                  `.  `.             .'  /
                    `.   ~ - - - - ~   .'
                       ~ . _ _ _ _ . ~
'''
  )
  print('Welcome to the serpentine encourager!\n\n')

  while True:
    print('a) Print encouragement')
    print('b) Print flag')
    print('c) Quit\n')
    choice = input('What would you like to do? (a/b/c) ')

    if choice == 'a':
      print_encouragement()

    elif choice == 'b':
      print('\nOops! I must have misplaced the print_flag function! Check my source code!\n\n')

    elif choice == 'c':
      sys.exit(0)

    else:
      print('\nI did not understand "' + choice + '", input only "a", "b" or "c"\n\n')



if __name__ == "__main__":
  main()
```

5. We can simply edit `serpentine.py` such that when we select choice `b`, the `print_flag()` function will run.
    - To edit the file in the command line, we can use a text editor like vim or nano. In this case, I will use vim.
    - For an introduction to vim: https://youtu.be/-txKSRn0qeA
    - Your edited file should look like [`solved-serpentine.py`](solved-serpentine.py)

> [!NOTE]
> It is highly encouraged for you to play around with vim/nano to become more comfortable with their commands!

```bash
# edit the 
vim serpentine.py

# run the edited file
ctfplayer@enxgmatic:~$ python3 serpentine.py

    Y
  .-^-.
 /     \      .- ~ ~ -.
()     ()    /   _ _   `.                     _ _ _
 \_   _/    /  /     \   \                . ~  _ _  ~ .
   | |     /  /       \   \             .' .~       ~-. `.
   | |    /  /         )   )           /  /             `.`.
   \ \_ _/  /         /   /           /  /                `'
    \_ _ _.'         /   /           (  (
                    /   /             \  \
                   /   /               \  \
                  /   /                 )  )
                 (   (                 /  /
                  `.  `.             .'  /
                    `.   ~ - - - - ~   .'
                       ~ . _ _ _ _ . ~

Welcome to the serpentine encourager!


a) Print encouragement
b) Print flag
c) Quit

What would you like to do? (a/b/c) b
sctf{7h3_r04d_k1nd4_l355_7r4v3l3d_hM}
```


