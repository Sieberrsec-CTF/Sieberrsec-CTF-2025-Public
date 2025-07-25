import string
import codecs
import base64

def to_atbash(part):
    alphabet_lower = string.ascii_lowercase + '_{}' + '123456789'
    alphabet_lower_rev = alphabet_lower[::-1] + '_{}' + '123456789'
    converter = {alphabet_lower[idx] : alphabet_lower_rev[idx] for idx in range(len(alphabet_lower))}

    res = ''.join([converter[char] for char in part])

    return res

def to_morse(part):
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

    res = ' '.join([MORSE_CODE[char] for char in part])

    return res


# Defining a flag of length 36, all letters are lowercase
flag = 'sctf{redacted}'

# Split the flag into 4 parts, each of equal length
part_length = len(flag) // 4
parts = [flag[part_length * x : part_length * (x + 1)] for x in range(4)]

# Apply different techniques to hide flag
parts[0] = codecs.decode(parts[0], 'rot_13')
parts[1] = to_atbash(parts[1])
parts[2] = base64.b64encode(parts[2].encode()).decode()
parts[3] = to_morse(parts[3])

for idx in range(len(parts)):
    print(f"parts[{idx}] = '{parts[idx]}'")

# Output: 
# parts[0] = 'fpgs{x3ly'
# parts[1] = 'geel7iw2g'
# parts[2] = 'cnNfNHIzX24w'
# parts[3] = '- _ ... ...-- -.-. ..- .-. ...-- }'