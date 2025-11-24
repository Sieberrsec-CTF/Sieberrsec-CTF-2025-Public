# Solution writeup here

```python
for x in lambda _: "flag\56txt",:
    @quit
    @next
    @open
    @x
    class C: 0
```

To bypass the parentheses filter, we can invoke builtin functions by chaining decorators to a dummy class.  
  
To pass a string into `open`, we can iterate through a collection that contains a single lambda that returns our flag path, then include it in our decorator chain. Since parentheses are blocked, we can simply append a comma at the end to declare a tuple.  

Although periods are not included in the whitelist, this can easily be bypassed through octal encoding.  
  
We then use `next` to get the string contents of the file, before finally passing it into `quit` to output our flag.  

## References
