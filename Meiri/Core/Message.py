# -*- coding: utf-8 -*-

class Message:
    def __init__(self, session, data, reciever=None, sender=None, extra=None):
        self.session = session
        self.data = data
        self.reciever = reciever
        self.sender = sender
        self.extra = extra
    
    