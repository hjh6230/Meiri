# -*- coding: utf-8 -*-

from aiocqhttp import CQHttp

from Meiri import User, Session, SessionType, Message
from Meiri import meiri

CQBot = CQHttp(api_root='http://127.0.0.1:5700/', access_token='AmeyaMeiri', secret='AmeyaMeiri')

@CQBot.on_message()
async def handle_msg(context):
    sender = MyUser(context['sender']['user_id'], name=context['sender']['nickname'])
    session = MySession(context)
    data = context['message']
    message = Message(session, data, sender=sender, extra=context)
    meiri.Shell(message)

class MyUser(User):
    def __init__(self, uid, name='unknown', sex='female', age=17):
        super().__init__(uid, name)
        self.sex = sex
        self.age = age
    
class MySession(Session):
    def __init__(self, kwargs):
        stype = kwargs.get('message_type')
        handle = None
        if stype == 'group':
            stype = SessionType.GROUP
            handle = kwargs.get('group_id')
        elif stype == 'discuss':
            stype = SessionType.GROUP
            handle = kwargs.get('discuss_id')
        elif stype == 'private':
            stype = SessionType.FRIEND
            handle = kwargs.get('user_id')
        super().__init__(stype, handle)
    
    async def Send(self, message):
        context = message.extra
        session = message.session
        
        if session.stype == SessionType.GROUP:
            context['message_type'] = 'group'
            context['group_id'] = session.handle
        elif session.stype == SessionType.FRIEND or session.stype == SessionType.TEMPORARY:
            context['message_type'] = 'private'
            context['user_id'] = message.sender.uid
        await CQBot.Send(context, message=message.data)

CQBot.run(host='127.0.0.1', port=8080)