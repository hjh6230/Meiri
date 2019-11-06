# -*- coding: utf-8 -*-

from Meiri.Core.Command import Command

class Admin(Command):
    def __init__(self):
        self.userId = None
    
    def Execute(self, message):
        self.Parse(message)
        if not message.sender.isAdmin:
            message.session.Send('权限不足')
        elif message.session.userManager.GetUser(self.userId) is None:
            message.session.Send('用户不存在')
        elif self.action == 'set':
            message.session.userManager.SetAdmin(self.userId)
            message.session.Send(f'已将{self.userId}设置为meiri管理员')
        elif self.action == 'unset':
            message.session.userManager.UnsetAdmin(self.userId)
            message.session.Send(f'已取消{self.userId}的管理员权限')
        self.finish = True
    
    def Parse(self, message):
        args = message.data.split()
        self.action = args[0]
        self.userId = args[1]