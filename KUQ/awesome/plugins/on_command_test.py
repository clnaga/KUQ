from nonebot import on_command, CommandSession
from awesome import logger_s
from aiocqhttp.exceptions import Error as CQHttpError
import nonebot
import datetime
from awesome import get_info_from_txt
import time
import requests
from bs4 import BeautifulSoup

bot = nonebot.get_bot()
logger = logger_s.get_logger()
logger_suggestions = logger_s.get_logger_suggestions()


@on_command('test1', aliases=('test1', 'tests1'))
async def test1(session: CommandSession):
    print(f"time: {datetime.datetime.now()} -- on_command test1 start!")
    ret = requests.get(
        url="https://chp.shadiao.app/api.php",
    )
    soup = BeautifulSoup(ret.text, 'html.parser')  # 使用 lxml 则速度更快
    if soup is not None:
        print("ss")
    print(f"time: {datetime.datetime.now()} -- on_command test1 stop!")
    print("----------------------------------------------------------------\n")


@on_command('test2', aliases=('test2', 'tests2'))
async def test2(session: CommandSession):
    print(f"time: {datetime.datetime.now()} -- on_command test2 start!")
    print(nonebot.scheduler.get_jobs())
    print(get_info_from_txt.FRIENDS)
    print(f"time: {datetime.datetime.now()} -- on_command test2 stop!")
    print("----------------------------------------------------------------\n")
    pass


@on_command('suggestion', aliases=('提议', '建议'))
async def suggestion(session: CommandSession):
    print(f"time: {datetime.datetime.now()} -- on_command suggestion start!")
    # 命令会话当前参数。实际上是 酷 Q 收到的消息去掉命令名的剩下部分
    stripped_arg = session.current_arg_text.strip()
    logger_msg = "建议内容：" + stripped_arg
    logger_suggestions.debug(logger_msg)
    try:
        await session.send("谢谢你的建议 [CQ:face,id=126]")
    except CQHttpError:
        pass
    print(f"time: {datetime.datetime.now()} -- on_command suggestion stop!")
    print("----------------------------------------------------------------\n")
