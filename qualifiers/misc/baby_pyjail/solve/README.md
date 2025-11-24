# Solution writeup here

```python
vars(print.__self__)['break''point']()
```

We can easily access `builtins` through `print.__self__`.  
  
Anything afterwards should be pretty trivial given the minimal filters implemented.

## References

