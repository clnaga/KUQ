from nonebot import on_command, CommandSession
import requests
import json
from aiocqhttp.exceptions import Error as CQHttpError
import datetime


# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('weather', aliases=('天气', '天气预报', '查天气'))
async def weather(session: CommandSession):
    print(f"time: {datetime.datetime.now()} -- on_command weather start!")
    # 命令会话当前参数。实际上是 酷 Q 收到的消息去掉命令名的剩下部分
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
        # 例如用户可能发送了：天气 南京
        session.state['city'] = stripped_arg
        # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
        # city = session.get('city', prompt='你想查询哪个城市的天气呢？')
        city = session.get('city')
        # 获取城市的天气预报
        weather_report = get_weather_of_city(city)
        # 向用户发送天气预报
        try:
            await session.send(weather_report)
        except CQHttpError:
            pass
    else:
        try:
            await session.send("指令错误额，要想这样\n\n天气 北京\n\n（注意中间的一个空格）")
        except CQHttpError:
            pass
    print(f"time: {datetime.datetime.now()} -- on_command weather stop!\n")


# # weather.args_parser 装饰器将函数声明为 weather 命令的参数解析器
# # 命令解析器用于将用户输入的参数解析成命令真正需要的数据
# @weather.args_parser
# async def _(session: CommandSession):
#     # 去掉消息首尾的空白符
#     stripped_arg = session.current_arg_text.strip()
#
#     if session.is_first_run:
#         # 该命令第一次运行（第一次进入命令会话）
#         if stripped_arg:
#             # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
#             # 例如用户可能发送了：天气 南京
#             session.state['city'] = stripped_arg
#         return
#
#     if not stripped_arg:
#         # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
#         # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
#         session.pause('要查询的城市名称不能为空呢，请重新输入')
#
#     # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
#     session.state[session.current_key] = stripped_arg


def get_weather_of_city(city: str) -> str:
    url = "http://api.tianapi.com/txapi/tianqi/index?key=13dd4e08419c5a88cda9e095a325db1b&city=" + city
    ret = requests.get(url=url)
    res_text = json.loads(ret.text)

    send_msg = f"查询地：{res_text['newslist'][0]['area']} \n" \
               f"今天天气：{res_text['newslist'][0]['weather']} \n" \
               f"现在温度：{res_text['newslist'][0]['real']} \n" \
               f"今天降雨概率：{res_text['newslist'][0]['pop']} \n" \
               f"[CQ:face,id=74] [CQ:face,id=74] [CQ:face,id=74] [CQ:face,id=74] " \
               f"[CQ:face,id=74] [CQ:face,id=74] [CQ:face,id=74] [CQ:face,id=74] [CQ:face,id=74] \n" \
               f"明天天气：{res_text['newslist'][1]['weather']} \n" \
               f"明天温度：{res_text['newslist'][1]['real']} \n" \
               f"明天降雨概率：{res_text['newslist'][1]['pop']}\n"
    if '雨' in res_text['newslist'][1]['weather']:
        send_msg += "提示：明天下雨，记得带伞！[CQ:face,id=66]"
    send_msg = send_msg + "\n\n可以使用 '我的位置 地点' 指令，每日获得目的地点天气"
    return send_msg
