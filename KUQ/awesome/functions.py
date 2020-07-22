import random
from nonebot import on_command, CommandSession
import datetime
import math


def create_get_friend_list_task():
    @on_command('get_friend_list', aliases=('好友', '获取好友列表'))
    async def get_friend_list(session: CommandSession):
        # print(await bot.get_stranger_info(user_id='707598333'))
        # print(await bot.get_group_list())
        # print(await bot.send_private_msg(user_id=707598245, message='love'))
        # print(await bot._get_friend_list())

        # # 利用 bot 的 api 获得好友qq号
        # friends_in_changzhou_list = await bot._get_friend_list()
        # print(friends_in_changzhou_list)
        # print(friends_in_changzhou_list[1]['friends'])
        # CQ:face,id=90     CQ:image,file=skin.jpg
        # for i in range(150):
        #    await session.send(f'{i}[CQ:face,id={i}]')
        await session.send('[CQ:face,id=66]')


def get_random_time_to_send_message(num_count, start, end):
    # 获得当前时间
    curr_time = datetime.datetime.now()
    time_list = []
    # 随机获得发送消息时间的 时，分，秒
    # 可以 hour*60*60 + minute*60 + second 懒得改了记录下
    hour_step = (end - start) / num_count
    for i in range(num_count):
        hour_value = random.randint(math.floor(start + i * hour_step), math.floor(start + (i + 1) * hour_step))
        if hour_value > curr_time.hour:
            minute_value = random.randint(0, 59)
            second_value = random.randint(0, 59)
            insert_time = str(curr_time.year) + '-' + str(curr_time.month) + '-' + str(curr_time.day) \
                          + ' ' + str(hour_value) + ':' + str(minute_value) + ':' + str(second_value)
            time_list.append(insert_time)
        else:
            if hour_value == curr_time.hour:
                minute_value = random.randint(0, 59)
                if minute_value > curr_time.minute:
                    second_value = random.randint(0, 59)
                    insert_time = str(curr_time.year) + '-' + str(curr_time.month) + '-' + str(curr_time.day) \
                                  + ' ' + str(hour_value) + ':' + str(minute_value) + ':' + str(second_value)
                    time_list.append(insert_time)
                else:
                    if minute_value == curr_time.minute:
                        second_value = random.randint(0, 59)
                        if second_value > curr_time.second:
                            insert_time = str(curr_time.year) + '-' + str(curr_time.month) + '-' + str(curr_time.day) \
                                          + ' ' + str(hour_value) + ':' + str(minute_value) + ':' + str(second_value)
                            time_list.append(insert_time)
    print(f"生成的时间集为：{time_list}")
    return time_list



# 获取随机的发送时间
# def get_random_nums(num_count, start, end):
#     temp_list = []
#     temp_num_count = 0
#     while temp_num_count < num_count:
#         temp_num = random.randint(start, end)
#         if temp_num not in temp_list:
#             temp_list.append(temp_num)
#             temp_num_count += 1
#     temp_list.sort()
#     # 获取时钟列表
#     minute_list = ''
#     for i in range(num_count):
#         minute_list += str(temp_list[i]) + ','
#     minute_list = minute_list[:-1]
#     print(f"提醒时间为(单位小时)：{minute_list}")
#     return minute_list



