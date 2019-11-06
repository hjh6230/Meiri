# -*- coding: utf-8 -*-

from aiocqhttp import CQHttp

bot = CQHttp(api_root='http://127.0.0.1:5700/', access_token='AmeyaMeiri', secret='AmeyaMeiri')


@bot.on_message()
async def handle_msg(context):
    await bot.send(context, '你好呀，下面一条是你刚刚发的：')
    print(context['message'])
    return {'reply': context['message']}

@bot.on_notice('group_increase')
async def handle_group_increase(context):
    await bot.send(context, message='欢迎新人～', at_sender=True, auto_escape=True)

@bot.on_request('group', 'friend')
async def handle_request(context):
    return {'approve': True}

@bot.on_meta_event('heartbeat')
async def _(ctx):
    print(ctx)

bot.run(host='127.0.0.1', port=8080)
