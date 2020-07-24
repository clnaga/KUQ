import datetime
import nonebot
import random
from nonebot import on_command, CommandSession
from aiocqhttp.exceptions import Error as CQHttpError
from awesome import get_info_from_txt

msg = ['毕老师该去接孩子啦', '小毕同志，快去接孩子', '毕院士，孩子哭啦']
bot = nonebot.get_bot()
flag = get_info_from_txt.get_flag_from_txt()

if flag[0][1] == str('1'):
    curr_time = datetime.datetime.now()
    print(f"time: {curr_time} -- scheduler_xiaobo_start")

    @nonebot.scheduler.scheduled_job('cron', id='start_notice_hui', day_of_week='mon-fri', hour='15', minute="20, 25")
    async def _():
        try:
            await bot.send_private_msg(user_id=67162261, message=msg[random.randint(0, 2)])
        except CQHttpError:
            pass

if flag[1][1] == str('1'):
    curr_time = datetime.datetime.now()
    print(f"time: {curr_time} -- scheduler_xiaoyue_start")

    @nonebot.scheduler.scheduled_job('cron', id='start_notice_yue', hour='23', minute="10")
    async def _():
        try:
            await bot.send_private_msg(user_id=909359100, message="傻逼wy，快去充电，电动牙刷，five！")
        except CQHttpError:
            pass

# @nonebot.scheduler.scheduled_job('interval', minutes=0.1)
# @nonebot.scheduler.scheduled_job('cron', day_of_week='mon-fri', hour='15', minute="20")


@on_command('start_notice_hui', aliases=('开启毕院士提醒', '开启小毕同志提醒', '开启小毕提醒',))
async def _(session: CommandSession):
    print(f"time: {datetime.datetime.now()} -- on_command start_notice_hui start!")
    # 是否是节假日
    # url = 'http://api.tianapi.com/txapi/jiejiari/index?key=13dd4e08419c5a88cda9e095a325db1b&date=2020-07-24'
    # ret = requests.get(url=url)
    # res_text = json.loads(ret.text)
    # print(res_text['newslist'][0]['isnotwork'])
    if nonebot.scheduler.get_job('start_notice_hui'):
        try:
            await session.send('我已经知道了，不要在反复啰嗦了，美丽的小毕女士')
        except CQHttpError:
            pass
    else:
        try:
            await session.send('我知道了, 以后周一到周五会提醒你')
        except CQHttpError:
            pass

        get_info_from_txt.refresh_flag('scheduler_xiaobi_is_open', "1")

        @nonebot.scheduler.scheduled_job('cron', id='start_notice_hui', day_of_week='mon-fri', hour='15', minute="20, 25")
        async def _():
            try:
                await bot.send_private_msg(user_id=67162261, message=msg[random.randint(0, 2)])
            except CQHttpError:
                pass


@on_command('stop_notice_hui', aliases=('关闭毕院士提醒', '关闭小毕同志提醒', '关闭小毕提醒',))
async def _(session: CommandSession):
    print(f"time: {datetime.datetime.now()} -- on_command start_notice_hui stop!")
    print("----------------------------------------------------------------\n")
    try:
        if nonebot.scheduler.get_job('start_notice_hui'):
            nonebot.scheduler.remove_job('start_notice_hui')
            get_info_from_txt.refresh_flag('scheduler_xiaobi_is_open', "0")
            try:
                await session.send('好了好了，不提醒你了')
            except CQHttpError:
                pass
        else:
            try:
                await session.send('你还没让我提醒你呢，四不四傻[CQ:face,id=105]')
            except CQHttpError:
                pass
    except:
        pass


@on_command('start_notice_yue', aliases=('小玥提醒工具开启', 'xx提醒工具开启'))
async def _(session: CommandSession):
    print(f"time: {datetime.datetime.now()} -- on_command start_notice_yue start!")
    # 是否是节假日
    # url = 'http://api.tianapi.com/txapi/jiejiari/index?key=13dd4e08419c5a88cda9e095a325db1b&date=2020-07-24'
    # ret = requests.get(url=url)
    # res_text = json.loads(ret.text)
    # print(res_text['newslist'][0]['isnotwork'])
    if nonebot.scheduler.get_job('start_notice_yue'):
        try:
            await session.send('我已经知道了，不要在反复啰嗦了，傻逼王玥')
        except CQHttpError:
            pass
    else:
        try:
            await session.send('我知道了, 每晚提醒你，five')
        except CQHttpError:
            pass

        get_info_from_txt.refresh_flag('scheduler_xiaoyue_is_open', "1")

        @nonebot.scheduler.scheduled_job('cron', id='start_notice_yue', hour='23', minute="10")
        async def _():
            try:
                await bot.send_private_msg(user_id=909359100, message="傻逼wy，快去充电，电动牙刷，five！")
            except CQHttpError:
                pass


@on_command('stop_notice_yue', aliases=('小玥提醒工具关闭', 'xx提醒工具关闭'))
async def _(session: CommandSession):
    print(f"time: {datetime.datetime.now()} -- on_command start_notice_yue stop!")
    print("----------------------------------------------------------------\n")
    try:
        if nonebot.scheduler.get_job('start_notice_yue'):
            nonebot.scheduler.remove_job('start_notice_yue')
            get_info_from_txt.refresh_flag('scheduler_xiaoyue_is_open', "0")
            try:
                await session.send('好了好了，不提醒你了')
            except CQHttpError:
                pass
        else:
            try:
                await session.send('你还没让我提醒你呢，四不四傻[CQ:face,id=105]')
            except CQHttpError:
                pass
    except:
        pass
