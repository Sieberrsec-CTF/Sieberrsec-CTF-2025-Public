# Solution writeup here

```
''' or license.__repr__.__globals__.__getitem__("s""ys").modules.__getitem__("o""s").environ.__setitem__("PYTHONI""NSPECT", "a") or '''
```

To prevent our payload from being evaluated as a string, we have to first escape the triple quotes.  

Some techniques we can use to bypass the keyword filters include
- `__getitem__` to access dictionary keys, since `[]` is blacklisted
- implicit string concatenation, since `+` is blacklisted
  
The next thing we might notice is that in the blacklist, `globals` isn't actually filtered due to one of the letters being in a different font.  
  
We can then exploit `license` to access the global namespace, where we can then fetch the `sys` module, which contains a reference to the `os` module.  

Due to the blacklist preventing access to object attributes, common methods of executing system commands like `system` and `popen` aren't available. However, we can modify the environment variables to spawn an interactive console when the script finishes executing, where we can then use Python to read `flag.txt`.

## References

- https://www.elttam.com/blog/env/#python