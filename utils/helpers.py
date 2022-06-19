from datetime import datetime

def strptime_to_second(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def is_err(err, func, args=(), kwargs={}) -> bool:
    try:
        func(*args, **kwargs)
    except err:
        return True
    return False