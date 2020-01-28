

def func(*args, **kwargs) :
    print(type(args)) # tuple
    print(type(kwargs)) # dict
    print(args)
    print(*args)
    print("name={name}, d={d}".format(**kwargs))
    print(kwargs)


func(1, 2, 4, name="me", d="2")