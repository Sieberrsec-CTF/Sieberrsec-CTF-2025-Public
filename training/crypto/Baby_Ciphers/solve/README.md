# Solution writeup here

Include e.g. images, an exploit script.

## Baby Ciphers

In this challenge, the ciphers (other than base64) are mono-alphabetic, meaning each character is replaced by a uniquely corresponding character/string. To recover the plaintext, we simply replace each character/string with it's original character.

For base64, we simply use `base64`'s _b64decode_ function to reverse the encoding, and retrieve the original string.

My solve script:

```python
import string
import codecs
import base64

def from_atbash(part):
    alphabet_lower = string.ascii_lowercase + '_{}' + '123456789'
    alphabet_lower_rev = alphabet_lower[::-1] + '_{}' + '123456789'
    converter = {alphabet_lower_rev[idx] : alphabet_lower[idx] for idx in range(len(alphabet_lower))}

    res = ''.join([converter[char] for char in part])

    return res

def from_morse(part):
    MORSE_CODE = {
        'a': '.-',     'b': '-...',   'c': '-.-.',  'd': '-..',
        'e': '.',      'f': '..-.',   'g': '--.',   'h': '....',
        'i': '..',     'j': '.---',   'k': '-.-',   'l': '.-..',
        'm': '--',     'n': '-.',     'o': '---',   'p': '.--.',
        'q': '--.-',   'r': '.-.',    's': '...',   't': '-',
        'u': '..-',    'v': '...-',   'w': '.--',   'x': '-..-',
        'y': '-.--',   'z': '--..',
        '0': '-----',  '1': '.----',  '2': '..---', '3': '...--',
        '4': '....-',  '5': '.....',  '6': '-....', '7': '--...',
        '8': '---..',  '9': '----.',
        '_': '_', '{' : '{', '}' : '}'
    }

    MORSE_CODE_REV = {
        MORSE_CODE[char] : char for char in MORSE_CODE
    }

    res = ''.join([MORSE_CODE_REV[char] for char in part.split(' ')])

    return res


parts = [0 for _ in range(4)]
parts[0] = 'fpgs{x3ly'
parts[1] = 'geel7iw2g'
parts[2] = 'cnNfNHIzX24w'
parts[3] = '- _ ... ...-- -.-. ..- .-. ...-- }'

# applying rot_13 2 times to any text gives us the original text! 
parts[0] = codecs.decode(parts[0], 'rot_13')
parts[1] = from_atbash(parts[1])
parts[2] = base64.b64decode(parts[2].encode()).decode()
parts[3] = from_morse(parts[3])

flag = ''.join(part for part in parts)

print(f'{flag = }')
```
