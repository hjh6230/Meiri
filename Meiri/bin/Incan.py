# -*- coding: utf-8 -*-

from Meiri.Core.Command import Command
from enum import Enum, unique
from time import sleep
from datetime import date
from random import randint, choice, shuffle

@unique
class IncanStatus(Enum):
    READY = 0,
    INQUEUE = 1,
    GAMING = 3

class Card:
    def __init__(self, ctype, number=1, value=1, monster=False):
        self.ctype = ctype
        self.number = number
        self.monster = monster
        self.value = value

class CardSet:
    def __init__(self):
        self.cardset = [Card('Sapphire', number=1, value=30)]
        for i in range(2):
            self.cardset.append(Card('Diamond', number=randint(1, 5), value=15))
        for i in range(3):
            self.cardset.append(Card('Ruby', number=randint(3, 10), value=5))
            self.cardset.append(Card('Ruby', number=randint(3, 10), value=5))
            self.cardset.append(Card('Emerald', number=randint(5, 15), value=1))
            self.cardset.append(Card('Emerald', number=randint(5, 20), value=1))
            self.cardset.append(Card('Viper', monster=True))
            self.cardset.append(Card('Spider', monster=True))
            self.cardset.append(Card('Mummy', monster=True))
            self.cardset.append(Card('Flame', monster=True))
            self.cardset.append(Card('Collapse', monster=True))
        shuffle(self.cardset)
    
    def Draw(self):
        card = choice(self.cardset)
        self.cardset.remove(card)
        return card
    
    def DrawJewel(self):
        card = choice(self.cardset)
        while card.monster:
            card = choice(self.cardset)
        self.cardset.remove(card)
        return card

    @classmethod
    def GetValue(cls, ctype, num) -> int:
        if ctype == 'Sapphire':
            return 30 * num
        elif ctype == 'Diamond':
            return 15 * num
        elif ctype == 'Ruby':
            return 5 * num
        elif ctype == 'Emerald':
            return 1 * num

class Incan(Command):
    def __init__(self):
        self.status = IncanStatus.READY
        self.description = [
            '欢迎来到Incan宝藏，是继续探索？还是立刻逃跑？贪婪与勇气，谁会是最后的赢家？\n输入<参加>、<加入>或者<Join>参与这场大冒险吧！', 
            '每一次决定都至关重要，死亡总在不经意间降临。活着带出宝石总价值最高的冒险者才能成为最后的赢家。所有的魔物在攻击前都会警告你们一次，活用魔物对人类最后的怜悯吧！\n来吧！向我们(魔物)展示你们人类的贪婪与勇气吧！']
        self.author = 'Lunex Nocty'
        self.version = '1.0.9.001'
        self.members = {}
        self.turn = 0
        self.camp = {'Sapphire':0,'Diamond':0,'Ruby':0,'Emerald':0}
        self.cardset = CardSet()
        self.monsters = []
        self.venture = 0
        self.lastest = date(2019, 11, 13)
        self.cheer = ['前方是梦想？还是死亡？', '这可没办法平分呢~', '胆小鬼可什么也得不到！', '运气站在有勇气的人一边。', '再挖一颗就回去！']
        self.warning = ['这次就放过你们，不会再有下次了。', '何人扰吾安眠？', '贪婪是人类的原罪。', '这是……人类？', '最珍贵的宝石就在前方，可你逃得掉吗？']
        self.death = ['抱歉呢，此路不通~代价是生命。', '留于此地的宝石，就赐予给下一个来到此地的人类吧~', '为什么呢？明明已经给出了警告，为什么还要前进呢？']
        self.helpdoc = '\n'.join(['规则:', '1. 玩家需要探索洞窟，挖掘宝石，并活着离开', '2. 玩家挖到的宝石会被平分，放弃冒险的玩家无法参与分配宝石，无法平分的宝石会被留在营地', '3. 游戏一共有30张卡牌，其中15张宝石卡，15张怪物卡，怪物卡共5种，每种各3张', '4. 每一回合需要玩家决定前进还是撤退，撤退视为放弃冒险，有权从营地分配宝石并离开洞窟, 选择前进的玩家抽取一张卡牌', '4. 若抽到的是宝石牌，将宝石放入营地，若抽到的是怪物牌，第一次抽到视为警告，第二次抽到同样的牌时，则当前所有正在探险的玩家被怪物杀害', '5. 当前没有玩家继续探险则游戏结束，或者的玩家中获得宝石总价值最高的玩家获胜'])

    def Execute(self, message):
        self.Parse(message)
        if self.context in ['关于', 'about', 'version', '版本']:
            message.session.Send(f'Version: {self.version}\nAuthor: {self.author}\nUpdate Time: {self.lastest}\n')
            self.finish = True
            return
        if self.context in ['帮助', 'help']:
            message.session.Send(f'{self.helpdoc}')
            self.finish = True
            return
        if self.context in ['exit', 'quit', 'end', '退出', '结束']:
            if self.status != IncanStatus.READY:
                message.session.Send('游戏结束，下次再见~')
            self.finish = True
            return
        if self.status == IncanStatus.READY:
            if self.context in ['开始', 'start', 'begin', 'run']:
                self.status = IncanStatus.INQUEUE
                self.members[message.sender.name] = {'status': 0, 'income':'','value':0}
                for desc in self.description:
                    message.session.Send(desc)
                    sleep(1)
        elif self.status == IncanStatus.INQUEUE:
            if self.context in ['参加', '加入', 'join']:
                if message.sender.name in self.members:
                    message.session.Send('你已经在小队中了，无需重复加入')
                else:
                    self.members[message.sender.name] = {'status': 0, 'income':'','value':0}
                    message.session.Send(f'<{message.sender.name}>加入了冒险小队，当前小队共有{len(self.members)}人，输入<开始>或<Go>开始冒险吧！')
            elif self.context in ['开始', 'go', 'start']:
                message.session.Send('游戏开始！')
                self.venture = len(self.members)
                sleep(1)
                message.session.Send('接下来的每一回合，输入<前进>或者<撤退>表示你的行动，待小队全员做出决定之后，进入下一轮')
                self.status = IncanStatus.GAMING
            elif self.context in ['状态', 'status']:
                message.session.Send(f'当前参与的玩家有:<{">, <".join(list(self.members.keys()))}>')
        elif self.status == IncanStatus.GAMING:
            if message.sender.name in self.members:
                if self.context in ['前进', 'go'] and self.members[message.sender.name]["status"] == 0:
                    self.members[message.sender.name]["status"] = 1
                elif self.context in ['撤退', 'escape'] and self.members[message.sender.name]["status"] == 0:
                    self.members[message.sender.name]["status"] = 2
                elif self.context in ['状态', 'status']:
                    status = ''
                    for name, member in self.members.items():
                        status += f'<{name}> '
                        if member['status'] == 0:
                            status += '还在迷茫\n'
                        elif member['status'] == 1:
                            status += '继续冒险\n'
                        elif member['status'] == 2:
                            status += '打算逃跑\n'
                        elif member['status'] == 3:
                            status += '放弃冒险了\n'
                    status += '冒险收获包括: '
                    for name, num in self.camp.items():
                        status += f'<{name}>{num}枚, '
                    status = status[:-2] + '\n'
                    status += f'目前收到了来自<{">, <".join(self.monsters)}>的警告。'
                    message.session.Send(status)
                if self.CheckTurn():
                    cnt = 0 # 撤退人数
                    increse = {}
                    increse['Sapphire'] = self.camp['Sapphire'] // self.venture
                    increse['Diamond'] = self.camp['Diamond'] // self.venture
                    increse['Ruby'] = self.camp['Ruby'] // self.venture
                    increse['Emerald'] = self.camp['Emerald'] // self.venture
                    for name, member in self.members.items():
                        if member["status"] == 2:
                            cnt += 1
                            for campjewel, campnumber in self.camp.items():
                                self.members[name]['value'] += CardSet.GetValue(campjewel, increse[campjewel])
                                self.camp[campjewel] -= increse[campjewel]
                                self.members[name]["income"] += f'{campjewel}: {increse[campjewel]}枚, '
                            self.members[name]["income"] = self.members[name]["income"][:-2]
                            self.members[name]["status"] = 3
                            message.session.Send(f'<{name}>害怕了，决定就此离去，你们平分了营地的宝石，<{name}>最终的收益为{self.members[name]["income"]}')
                            sleep(1)
                        elif member["status"] == 1:
                            self.members[name]["status"] = 0
                    self.turn += 1
                    self.venture -= cnt
                    if self.venture == 0:
                        message.session.Send(self.FindWinner())
                    else:
                        card = self.cardset.Draw() if self.turn > 1 else self.cardset.DrawJewel()
                        if card.monster:
                            if card.ctype in self.monsters:
                                names = "<"
                                for name, member in self.members.items():
                                    if member["status"] == 0:
                                        names += name + ">, <"
                                        member["status"] = -1
                                        self.venture -= 1
                                message.session.Send(f'第{self.turn}轮，{names[:-3]}死于贪婪。\n\n<{card.ctype}>: "{choice(self.death)}"')
                                sleep(1)
                                message.session.Send(self.FindWinner())
                            else:
                                self.monsters.append(card.ctype)
                                message.session.Send(f'第{self.turn}轮，你们发现了来自<{card.ctype}>的警告: "{choice(self.warning)}"')
                        else:
                            self.camp[card.ctype] += card.number
                            message.session.Send(f'第{self.turn}轮，恭喜你们挖到了<{card.ctype}>{card.number}枚！\n<概率女神>: "{choice(self.cheer)}"')

    
    def CheckTurn(self):
        for member in self.members.values():
            if member["status"] == 0:
                return False
        return True
    
    def FindWinner(self):
        winner = []
        income = 0
        alive = False
        self.finish = True
        for name, member in self.members.items():
            if member["status"] == 3:
                alive = True
                if member['value'] > income:
                    income = member['value']
                    winner.clear()
                    winner.append(name)
                elif income > 0 and member['value'] == income:
                    winner.append(name)
        if alive:
            return f'<{">, <".join(winner)}>获得了最后的胜利，收益为{self.members[winner[0]]["income"]}' if winner else '胆小鬼的冒险者哦，没有风险怎么会有回报呢！'
        return '无人生还，做人不要太贪心哦~'


    
    def Parse(self, message):
        self.context = message.data.lower() if message.data else 'run'
