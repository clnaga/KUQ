from nonebot import on_command, CommandSession
import datetime
from aiocqhttp.exceptions import Error as CQHttpError
import re
import nonebot


@on_command('richeng', aliases=('添加日程', '添加提醒'))
async def richeng(session: CommandSession):
    print(f"time: {datetime.datetime.now()} -- on_command richeng start!")
    try:
        stripped_arg = session.current_arg_text.strip().split(' ')
        if stripped_arg[0] == '明天':
            time_num = 1
        else:
            time_num = 0
        stripped_arg_time = re.split('[点:]', stripped_arg[time_num].strip())
        if stripped_arg_time[1] ==   '':
            stripped_arg_time[1] = '0'
        curr_time = datetime.datetime.now()
        if (time_num * 24 * 60 + int(stripped_arg_time[0]) * 60 + int(stripped_arg_time[1])) \
                > (curr_time.hour * 60 + curr_time.minute):
            insert_time = str(curr_time.year) + '-' + str(curr_time.month) + '-' + str(curr_time.day + time_num) \
                          + ' ' + str(stripped_arg_time[0]) + ':' + str(stripped_arg_time[1]) + ':0'
            insert_info = stripped_arg[1]
            @nonebot.scheduler.scheduled_job('date', id='richeng: '+insert_time, run_date=insert_time)
            async def _():
                try:
                    await session.send(f"嘀嘀嘀，提醒内容：\n\n  {insert_info} ")
                except CQHttpError:
                    pass
            try:
                await session.send(f"OK[CQ:face,id=30]，记住了")
            except CQHttpError:
                pass
        else:
            try:
                await session.send(f"跑到过去提醒你嘛，时间请超过现在的时间！")
            except CQHttpError:
                pass
    except :
        try:
            await session.send("指令错误额，要像这样\n\n添加日程  时间  内容\n\n"
                               "添加日程 8点20 我要上天\n添加提醒 18:20 我要上天\n添加提醒 明天 6点10 我要上天")
        except CQHttpError:
            pass
    print(f"time: {datetime.datetime.now()} -- on_command richeng stop!")


# @on_command('daily_richeng', aliases=('添加每日日程', '添加每日提醒'))
# async def daily_richeng(session: CommandSession):
#     print(f"time: {datetime.datetime.now()} -- on_command daily_richeng start!")
#     try:
#         stripped_arg = session.current_arg_text.strip().split(' ')
#         stripped_arg_time = re.split('[点:]', stripped_arg[0].strip())
#         scheduler_hour = stripped_arg_time[0]
#         scheduler_minute = stripped_arg_time[1]
#         @nonebot.scheduler.scheduled_job('cron', id="daily_richeng：", hour=scheduler_hour, minute=scheduler_minute)
#         async def _():
#             try:
#                 await session.send(f"嘀嘀嘀，提醒内容：\n\n  {stripped_arg[1]} ")
#             except CQHttpError:
#                 pass
#         try:
#             await session.send(f"OK[CQ:face,id=30]，记住了")
#         except CQHttpError:
#             pass
#     except :
#         try:
#             await session.send("指令错误额，要像这样\n\n添加每日日程  时间  内容\n\n"
#                                "添加每日日程 8点20 我要上天\n添加每日提醒 18:20 我要上天")
#         except CQHttpError:
#             pass
#     print(f"time: {datetime.datetime.now()} -- on_command daily_richeng stop!")
