# -*- coding: utf-8 -*-
import nonebot

if __name__ == '__main__':
    nonebot.init()
    nonebot.load_builtin_plugins()
    nonebot.run(host='172.17.0.1', port=8080)
