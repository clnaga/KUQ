from nonebot import on_command, CommandSession
import random
from aiocqhttp.exceptions import Error as CQHttpError
import datetime

DINNER_LIST = [
    '饭',
    '面',
    '饺子混沌',
    '包子等小吃'
]

DINNER_ROOM_LIST = [
    '1食堂',
    '2食堂'
]


# on_command 装饰器将函数声明为一个命令处理器
@on_command('choose_dinner', aliases=('吃啥', '吃什么'))
async def choose_dinner(session: CommandSession):
    print(f"time: {datetime.datetime.now()} -- on_command choose_dinner start!")
    dinner_res = get_dinner()
    try:
        await session.send(dinner_res)
    except CQHttpError:
        pass
    print(f"time: {datetime.datetime.now()} -- on_command choose_dinner stop!")
    print("----------------------------------------------------------------\n")


@on_command('choose_dinner_room', aliases=('在哪吃', '在哪里吃'))
async def choose_dinner_room(session: CommandSession):
    print(f"time: {datetime.datetime.now()} -- on_command choose_dinner_room start!")
    dinner_room_res = get_dinner_room()
    try:
        await session.send(dinner_room_res)
    except CQHttpError:
        pass
    print(f"time: {datetime.datetime.now()} -- on_command choose_dinner_room stop!")
    print("----------------------------------------------------------------\n")


def get_dinner():
    return DINNER_LIST[random.randint(0, 3)]


def get_dinner_room():
    return DINNER_ROOM_LIST[random.randint(0, 1)]

