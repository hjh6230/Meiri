# -*- coding: utf-8 -*-

from Meiri.Core import asyncfunction

class Meiri:
    def __init__(self):
        self.sessions = {}
        self.runing = False
        self.interval = 3600
    
    def GetSession(self, message):
        sid = message.session.sid
        if sid not in self.sessions:
            self.sessions[sid] = message.session
        self.sessions[sid].SetActive()
        print(f'meiri.py getSession(): {self.sessions[sid]}')
        return self.sessions[sid]

    def Shell(self, message):
        session = self.GetSession(message)
        print(f'meiri.py Shell(): {session}')
        session.Execute(message)
    
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
