import sys, traceback 

def dump_error(fn):
    '''tries to run function, if there's an error it re-submits the exception, but dumps it to standard error
    usefull when debuging ajax requests'''

    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception, e:
            et, ei, tb = sys.exc_info()
            traceback.print_exc(tb,file=sys.stderr)
            raise et, ei, tb
    return wrapped
