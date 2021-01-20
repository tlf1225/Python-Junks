def test(*dargs, **dkwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            nargs = dargs + args
            nkwargs = dkwargs.copy()
            nkwargs.update(kwargs)
            func(*nargs, **nkwargs)

        return wrapper

    return decorator


@test("a", test=True)
def work(*args, **kwargs):
    print("Test")


if __name__ == '__main__':
    work("a", "b", "c", test2=True, work=True)
