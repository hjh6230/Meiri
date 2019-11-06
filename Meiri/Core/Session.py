# -*- coding: utf-8 -*-

from Meiri.Core import asyncfunction, UserManager, Context
from enum import Enum, unique

@unique
class SessionType(Enum):
    TEMPORARY = 0
    FRIEND = 1
    GROUP = 2

class Session:
    def __init__(self, stype, handle):
        self.stype = stype
        self.handle = handle
        self.SetActive()
        self.sid = Session._GetSessionId(self.stype, self.handle)
        self.context = Context()
        self.userManager = UserManager()

    @asyncfunction
    def Execute(self, message):
        command = self.context.GetCommand()
        self.sender = self.userManager.GetUser(message.sender)
        message.sender = self.sender
        command.Execute(message)
        if command.callee:
            self.context.Push(command.callee)
        if command.finish:
            self.context.Pop()

    def SetActive(self, level=10):
        self._activity = level
    
    def GetActive(self) -> bool:
        return self._activity > 0
    
    @classmethod
    def _GetSessionId(cls, stype, handle) -> str:
        sid = None
        if stype == SessionType.TEMPORARY:
            sid = 'Temporary@'
        elif stype == SessionType.FRIEND:
            sid = 'Friend@'
        elif stype == SessionType.GROUP:
            sid = 'Group@'
        else:
            sid = 'Unknown@'
        sid += str(handle)
        return sid