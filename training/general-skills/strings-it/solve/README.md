# picoCTF 2019 - strings it (modified) [General Skills]

1. Download the file

```bash
# download the provided file
ctfplayer@enxgmatic:~$ wget X

# verify it is present using "ls"
ctfplayer@enxgmatic:~$ ls
strings
```

2. Give the challenge binary executable permissions

```bash
# when you try to run the executable directly, you will get an error
ctfplayer@enxgmatic:~$ ./strings
bash: ./strings: Permission denied

# this is because the binary does not have executable persmissions
# this can be shown by running "ls -la", where you will see that the binary's permissions is "rw-rw-r--", which do not include executable which is "x"
ctfplayer@enxgmatic:~$ ls -la
total 788
drwxrwxr-x 2 ctfplayer ctfplayer   4096 Jul  5 00:39 .
drwxrwxr-x 4 ctfplayer ctfplayer   4096 Jul  2 23:26 ..
-rw-rw-r-- 1 ctfplayer ctfplayer 798648 Jul  5 00:39 strings

# let's give the binary executable permissions using "chmod"
ctfplayer@enxgmatic:~$ chmod +x strings

# now, when you run "ls -la", the binary's permissions are now "rwxrwxr-x", so it is executable
ctfplayer@enxgmatic:~$ ./strings2
total 788
drwxrwxr-x 2 ctfplayer ctfplayer   4096 Jul  5 00:41 .
drwxrwxr-x 4 ctfplayer ctfplayer   4096 Jul  2 23:26 ..
-rwxrwxr-x 1 ctfplayer ctfplayer 798648 Jul  5 00:41 strings

```

3. Run the binary for the first part of the flag

```bash
ctfplayer@enxgmatic:~$ ./strings
Congratulations! You have found the second part of the flag: "5tr1NgS_!?!}"
Maybe try the 'strings' function for the first part of the flag? Take a look at the man page.
The flag starts with the characters "sctf{".
```

4. Run strings on the binary

```bash
ctfplayer@enxgmatic:~$ strings strings
/lib64/ld-linux-x86-64.so.2
__cxa_finalize
__libc_start_main
setvbuf
stdout
puts
... 
...
...
.fini_array
.dynamic
.data
.bss
.comment

# However, there seems to be too much data. How can we find the first part of the flag...?
```

5. Combine strings with grep to get the second part of the flag

```bash
# we can use the command "grep" to search for a specific pattern in the output of strings
# particularly, since we know the flag starts with "sctf{", we can grep for that pattern

# to combine grep with strings, we can use pipes, i.e. "|".
# as mentioned in the training document, pipes transfers the output of the previous command to be the input of the next command

ctfplayer@enxgmatic:~$ strings strings | grep sctf{
The flag starts with the characters "sctf{".
sctf{wUt_d4_

```

6. Combine both parts of the flag to form `sctf{wUt_d4_5tr1NgS_!?!}}`
