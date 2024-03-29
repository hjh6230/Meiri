# -*- coding: utf-8 -*-

from Meiri.Core import asyncfunction

class Meiri:
    def __init__(self):
        self.sessions = {}
        self.runing = False
        self.interval = 3600
    
    def GetSession(self, message):
        sid = message.session.sid
        if sid in self.sessions:
            self.sessions[sid].SetActive()
            self.sessions[sid].extra = message.session.extra
        else:
            self.sessions[sid] = message.session
        return self.sessions[sid]

    def Shell(self, message):
        session = self.GetSession(message)
        message.session = session
        message.session.Execute(message)
            
    def Run(self):
        self.runing = True
        self.Update()

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
