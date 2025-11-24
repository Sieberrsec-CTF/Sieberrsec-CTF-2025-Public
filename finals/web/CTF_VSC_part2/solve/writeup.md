# Solution - CTF VSC part 2

The CSV injection vulnerability remains.

However, numerous protections have been added to prevent the use of the webserver function.

- In the Dockerfile, notice that all the configuration to allow automatic updating of WEBSERVER links is now removed.
- In `app.py`, a filter has been added to remove "webser" from input.
- In the macro `Module1.xba`, the command `Wait 3000` is removed. Even if we somehow could get "=WEBSERVER" into the csv opened by libreoffice, there likely isn't enough time for the link to be fetched (this doesn't work all the time).

Thus, we need to get a little creative to solve this. No more copy-pasting online payloads (:

## Solution

The solution is inspired by blind SQL injections. 

We can brute force the flag, one character at a time. We can do so by using a function that checks for a substring in the flag. If the substring is present, we return a valid award category, which leads to our vote being counted. If it isn't present, we return an invalid award category, which leads to an error in our vote.

Let's find a calc function that searches for a substring. Looking at the [list of functions](https://wiki.documentfoundation.org/Documentation/Calc_Functions/List_of_Functions), one suitable function is [`FIND`](https://wiki.documentfoundation.org/Documentation/Calc_Functions/FIND). Another is [SEARCH](https://wiki.documentfoundation.org/Documentation/Calc_Functions/SEARCH) (for case insensitive search).

So, we can check whether the flag includes a substring using this payload:

```
=IF(ISERROR(FIND("sctf{flag_substr_here}",C4)),"no","best")
```

- `FIND(substr, C4)` will check check whether the substring is present in the flag (at cell C4)
    - If the substring is not present, an error occurs. 
    - If the substring is present, it will return the position the substring was found (i.e. `1` in this case).
- `ISERROR(value)` will return True/False, depending on whether `FIND` returns an error
- `IF(condition,"no","best")` will return "no" if substring was not found, and "best" if the substring was found

However, this doesn't actually work. Our payload will always return "no" in this case. Why? C4="NIL" when you first open the csv in libreoffice (as in `app.py`). As such, our payload will initially return "no". Then, when the macro validates our submission, the check will fail, hence writing "N" in C4. Thus, the flag is never written into the csv.

So, we need to adjust our payload to account for C4's initial value. Actual payload:

```
=IF(OR(C4="NIL",IFERROR(FIND("sctf{flag_substr_here}",C4),0)=1),"best","no")
```

- `FIND(substr, C4)` will check check whether the substring is present in the flag (at cell C4)
- `IFERROR(value, 0)` will return 0 if there is an error (i.e. substring not present). Else, returns value of `FIND` (in this case, `1`).
- `OR(C4="NIL",IFERROR(FIND(substr,C4),0)=1)` will return "True" if C4=NIL (i.e. submission was not checked yet) or if the substring was found in the flag.
- `=IF(OR(condition),"best","no")` will return "best" if `OR` is True, else will return "no"

What will occur:
1. When the csv is first opened, C4="NIL", so the `OR` check passes, award_cat = "best"
2. The macro validates our vote, and it passes the check. The flag is written to C4
3. Our payload formula gets re-evaluated. If the substring in `FIND` is present, award_cat = "best". Else, award_cat = "no", which is invalid.
4. When `app.py` tries to analyse the vote, an error will occur if award_cat = "no". Else, if the substring is present, our vote is counted.

We will use this payload to brute force the characters in the flag one by one.

See [`solve.py`](solve.py) for a suggested script.
