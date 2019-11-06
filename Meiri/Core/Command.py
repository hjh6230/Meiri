# -*- coding: utf-8 -*-

class Command:
    callee = None
    finish = False
    def __init__(self):
        self.callee = None
        self.finish = False

    def Execute(self, session, message):
        raise 'You must override this method.'
    
    def Parse(self, message):
        raise 'You must override this method.'
