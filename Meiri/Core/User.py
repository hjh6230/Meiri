# -*- coding: utf-8 -*-

class User:
    def __init__(self, uid, name='unknown'):
        self.uid = uid
        self.name = name
        self.isAdmin = False
        self.SetActive()
    
    def SetActive(self, level=10):
        self.activity = level
    def GetActive(self) -> bool:
        return self.activity > 0
    def GetUID(self):
        return self.uid
    def GetName(self):
        return self.name
    def AuthorityCheck(self):
        return self.isAdmin

class UserManager:
    def __init__(self):
        self.users = {}
    
    def GetUser(self, user) -> User:
        uid = user.uid
        if uid not in self.users:
            self.users[uid] = user
        self.users[uid].SetActive()
        return self.users[uid]
    
    def SetAdmin(self, uid) -> bool:
        if uid not in self.users:
            return False
        self.users[uid]._isAdmin = True
        return True
    
    def UnsetAdmin(self, uid) -> bool:
        if uid not in self.users:
            return False
        self.users[uid]._isAdmin = False
        return True