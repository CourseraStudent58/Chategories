import inspect

debug = True

def loggerOut(*args):
    for s in args:
        print(s)
        if inspect.isclass(s):
            print(inspect.getmembers(s))

def log(*args):
    if debug is not True:
        return
    loggerOut(*args)

def error(fname, *args ):
    loggerOut( "ERROR: "+fname, *args )




