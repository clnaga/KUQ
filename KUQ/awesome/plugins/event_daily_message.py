from awesome import get_info_from_txt
from nonebot import on_command, CommandSession
import nonebot
import requests
import json
from aiocqhttp.exceptions import Error as CQHttpError
import time
import datetime

bot = nonebot.get_bot()


@on_command('set_friend_city', aliases=('我的位置', '记住我的位置'))
async def set_friend_city(session: CommandSession):
    print(f"time: {datetime.datetime.now()} -- on_command set_friend_city start!")
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.state['city'] = stripped_arg
        city = session.get('city')
        await get_info_from_txt.change_friend_info(session.ctx["user_id"], 1, city)
        try:
            await session.send(f"记住了，以后每天晚上23点会向你汇报第二天{city}天气[CQ:face,id=30]")
        except CQHttpError:
            pass
    else:
        try:
            await session.send("指令错误额，要像这样\n\n我的位置 北京\n（注意中间的一个空格）\n\n"
                               "要关闭的话输出\n\n我的位置 error")
        except CQHttpError:
            pass
    print(f"time: {datetime.datetime.now()} -- on_command set_friend_city stop!")

# # 晚上 23 点发送晚安
# @nonebot.scheduler.scheduled_job('cron', hour='23')
# async def _():
#     print(f"time: {datetime.datetime.now()} -- scheduler send_goodnight start!")
#     try:
#         FRIENDS_LIST.remove(['767862831', '南通'])
#         for friend_list in FRIENDS_LIST:
#             time.sleep(0.1)
#             await bot.send_private_msg(user_id=friend_list[0], message="晚安[CQ:face,id=75]")
#     except CQHttpError:
#         pass
#     print(f"time: {datetime.datetime.now()} -- scheduler send_goodnight stop!")

# 晚上 23 点给好友发送天气
@nonebot.scheduler.scheduled_job('cron', id='send_weather_to_friend', hour='23', minute='0', second='3')
async def _():
    print(f"time: {datetime.datetime.now()} -- scheduler send_weather_info_to_friends start!")
    # 获取好友qq号
    for friend_in_list in get_info_from_txt.FRIENDS:
        # == 用于判断内容是否相同
        # is 用于判断引用是否相同
        if friend_in_list[1] != 'error':
            if friend_in_list[2] == '1':
                # 睡眠导致任务过期，不睡眠又容易卡死
                # time.sleep(0.1)
                send_msg = get_city_weather(friend_in_list[1])
                try:
                    await bot.send_private_msg(user_id=friend_in_list[0], message=send_msg)
                except CQHttpError:
                    pass
    print(f"time: {datetime.datetime.now()} -- scheduler send_weather_info_to_friends stop!")


@nonebot.scheduler.scheduled_job('cron', id='refresh_friend_connectivity_index', hour='8', minute='10')
async def _():
    print(f"time: {datetime.datetime.now()} -- scheduler refresh_friend_connectivity_index start!")
    # 获取好友qq号
    for friend_in_list in get_info_from_txt.FRIENDS:
        friend_connectivity_index = int(friend_in_list[3]) + 1
        if friend_connectivity_index < 3:
            friend_in_list[2] = str(1)
        elif friend_connectivity_index == 3:
            friend_in_list[2] = str(0)
            await bot.send_private_msg(user_id=friend_in_list[0], message='咱俩太久没有交流了，我自闭去了，别回复我，不然我又骚扰你啦')
        else:
            friend_connectivity_index = 5
            friend_in_list[2] = str(0)
        friend_in_list[3] = str(friend_connectivity_index)
    await get_info_from_txt.change_friend_info()
    print(f"time: {datetime.datetime.now()} -- scheduler refresh_friend_connectivity_index stop!")


# 获取每日天气推送
def get_city_weather(city: str) -> str:
    url = "http://api.tianapi.com/txapi/tianqi/index?key=13dd4e08419c5a88cda9e095a325db1b&city=" + city
    ret = requests.get(url=url)
    res_text = json.loads(ret.text)
    if res_text['code'] == 200:
        send_msg = f"查询地：{res_text['newslist'][0]['area']} \n" \
                   f"明天天气：{res_text['newslist'][1]['weather']} \n" \
                   f"明天温度：{res_text['newslist'][1]['real']} \n" \
                   f"明日降雨概率：{res_text['newslist'][1]['pop']}"
        if '雨' in res_text['newslist'][1]['weather']:
            send_msg = send_msg + "\n"
            send_msg += "提示：下雨，记得带伞！[CQ:face,id=66]"
    else:
        send_msg = '您的地址有问题啊，请指令重新输入您的地址'
    return send_msg
