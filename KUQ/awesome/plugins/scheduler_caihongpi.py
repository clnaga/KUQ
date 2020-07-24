from bs4 import BeautifulSoup
from awesome import get_info_from_txt
import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
from awesome import functions
import requests
import time
import datetime


bot = nonebot.get_bot()
chp_times = functions.get_random_time_to_send_message(2, 9, 22)


@nonebot.scheduler.scheduled_job('cron', id='daily_chp_create', hour='8', minute='30')
def _():
    global chp_times
    chp_times = functions.get_random_time_to_send_message(2, 9, 22)
    create_chp(chp_times)


def create_chp(create_chp_times):
    for chp_time in create_chp_times:
        @nonebot.scheduler.scheduled_job('date', id='chp: '+chp_time, run_date=chp_time)
        async def _():
            print(f"time: {datetime.datetime.now()} -- scheduler {chp_time} start!")
            try:
                # 获取彩虹屁内容
                msg = get_text()
                # await bot.send_private_msg(user_id=707598245, message=msg)
                for friendlist in get_info_from_txt.FRIENDS:
                    if friendlist[2] == '1':
                        # time.sleep(0.1)
                        try:
                            await bot.send_private_msg(user_id=friendlist[0], message=msg)
                        except CQHttpError:
                            pass
            except CQHttpError:
                pass
            print(f"time: {datetime.datetime.now()} -- scheduler {chp_time} stop!\n")


create_chp(chp_times)


def get_text():
    # 请求头
    ret = requests.get(
        url="https://chp.shadiao.app/api.php",
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36', }
    )
    soup = BeautifulSoup(ret.text, 'html.parser')  # 使用 lxml 则速度更快
    return soup.text
