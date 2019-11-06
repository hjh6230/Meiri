# -*- coding: utf-8 -*-

from Meiri.Core import asyncfunction

class Meiri:
    def __init__(self):
        self.sessions = {}
        self.runing = True
        self.interval = 3600
        self.Update()
    
    def GetSession(self, message):
        sid = message.session.sid
        if sid not in self.sessions:
            self.sessions[sid] = message.session
        self.sessions[sid].SetActive()
        return self.sessions[sid]

    def Shell(self, message):
        session = self.GetSession(message)
        session.Execute(message)
    
    def Stop(self):
        self.runing = False
    
    @asyncfunction
    def Update(self):
        from time import sleep
        while self.runing:
            for sid in self.sessions:
                for uid, user in self.sessions[sid].userManager.users.items():
                    if not user.GetActive():
                        self.sessions[sid].userManager.users.pop(uid)
                self.sessions[sid].active -= 1
                if not self.sessions[sid].GetActive():
                    self.sessions.pop(sid)
            sleep(self.interval)

meiri = Meiri()