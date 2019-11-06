# -*- coding: utf-8 -*-

from Meiri.Core.Command import Command
from Meiri import bin
from Meiri.bin import SysPath

class Syscall(Command):
    def __init__(self):
        self.commands = {}
        for command, value in SysPath.items():
            for name in value:
                self.commands[name] = command
    
    def Execute(self, message):
        self.Parse(message)
        if self.cmd == 'Syscall' and not message.sender.AuthorityCheck():
            message.session.Send('权限不足')
            self.finish = True
            return
        from importlib import import_module
        cmd = import_module(f'Meiri.bin.{self.cmd}')
        self.callee = eval(f'{cmd.__name__[6:]}.{self.cmd}')
        command = self.callee()
        command.Execute(message)
        self.finish = command.finish
    
    def Parse(self, message):
        args = message.data.split(' ', 1)
        self.cmd = self.commands[args[0]]
        self.param = args[1]
        message.data = args[1]