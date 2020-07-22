from nonebot import on_request, RequestSession
from awesome import get_info_from_txt
from aiocqhttp.exceptions import Error as CQHttpError
import datetime


@on_request()
async def _(session: RequestSession):
    print(f"time: {datetime.datetime.now()} -- request start!")
    try:
        await session.approve()
        await session.send("输出指令\n‘我的位置 地址’\n可以每天获取您所在地的天气额")
    except CQHttpError:
        pass
    send_id = session.ctx['user_id']
    get_info_from_txt.add_friend(send_id)
    print(f"time: {datetime.datetime.now()} -- request stop!")
    # print(type(friend.FRIENDS[0]))
    # print(friend.get_user_id_from_txt())
