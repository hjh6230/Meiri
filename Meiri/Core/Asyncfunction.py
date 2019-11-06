# -*- coding: utf-8 -*-

def asyncfunction(func):
    def wrapper(*args, **kwargs):
        from threading import Thread
        task = Thread(target=func, args=args, kwargs=kwargs)
        task.start()
    return wrapper