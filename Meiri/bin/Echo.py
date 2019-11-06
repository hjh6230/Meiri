# -*- coding: utf-8 -*-

from Meiri.Core.Command import Command

class Echo(Command):
    def __init__(self):
        self.context = ''
    
    def Execute(self, message):
        self.Parse(message)
        message.session.Send(message)
        self.finish = True
    
    def Parse(self, message):
        self.context = message.data