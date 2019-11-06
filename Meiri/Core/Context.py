# -*- coding: utf-8 -*-

from Meiri.bin.Syscall import Syscall

class Context:
    def __init__(self):
        self._commands = [Syscall()]
    
    def GetCommand(self):
        return self._commands[-1]
    
    def Pop(self):
        if len(self._commands) > 1:
            self._commands.pop()
        
    def Push(self, command):
        self._commands.append(command)