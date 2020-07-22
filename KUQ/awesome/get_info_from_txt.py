# -*- coding: UTF-8 -*-
import json

# user_id.txt
# 姓名, 地址, 是否每晚发送天气信息, 未互通消息天数

import nonebot


FRIENDS = []
FLAG = []


bot = nonebot.get_bot()


def add_friend(user_id):
    # 在写入 QQ 号前先读取 txt 中的 QQ 号
    # 直接调用函数 friend_read_pre = get_user_id_from_txt()
    # 两个变量公用一个地址，friend_read_pre 值会随着 FRIENDS 的值改变而改变
    friend_id_pre = [item[0] for item in FRIENDS]
    if str(user_id) not in friend_id_pre:
        insert_info_to_FRIENDS = [str(user_id), 'error', '0', '9']
        FRIENDS.append(insert_info_to_FRIENDS)
    with open('awesome/user_id.txt', 'wb') as f:
        for line in FRIENDS:
            insert_msg = str(line[0]) + ' ' + str(line[1]) + ' ' + str(line[2]) + ' ' + str(line[3]) + '\n'
            insert_msg_bytes = bytes(insert_msg, encoding="utf-8")
            # writelines expects an iterable, so it will iterate on your bytes object
            # and each item it iterates on is an int.
            # 用 writelines 写 bytes 类型会出错，因为 writelines 会遍历对象，可以写 str 类型的
            # 用 write 是整个写进去，可以写 bytes 的
            f.write(insert_msg_bytes)
    get_user_id_from_txt()


async def change_friend_info(self_id=None, para_num=None, para=1):
    if self_id is not None:
        friends_id = [item[0] for item in FRIENDS]
        if str(self_id) in friends_id:
            user_id = friends_id.index(str(self_id))
            if para_num == 1:
                FRIENDS[user_id][para_num] = para
            elif para_num == 3:
                if para > 0:
                    FRIENDS[user_id][para_num] = str(int(FRIENDS[user_id][para_num]) + para)
                    if int(FRIENDS[user_id][para_num]) < 4:
                        FRIENDS[user_id][2] = str(1)
                    else:
                        FRIENDS[user_id][2] = str(0)
                        FRIENDS[user_id][para_num] = str(5)
                        await bot.send_private_msg(user_id=self_id, message='咱俩太久没有交流了，我自闭去了')
                else:
                    FRIENDS[user_id][2] = str(1)
                    FRIENDS[user_id][para_num] = str(0)
    with open('awesome/user_id.txt', 'wb') as f:
        for line in FRIENDS:
            insert_msg = str(line[0]) + ' ' + str(line[1]) + ' ' + str(line[2]) + ' ' + str(line[3]) + '\n'
            insert_msg_bytes = bytes(insert_msg, encoding="utf-8")
            # writelines expects an iterable, so it will iterate on your bytes object
            # and each item it iterates on is an int.
            # 用 writelines 写 bytes 类型会出错，因为 writelines 会遍历对象，可以写 str 类型的
            # 用 write 是整个写进去，可以写 bytes 的
            f.write(insert_msg_bytes)
    get_user_id_from_txt()


def get_user_id_from_txt():
    with open('awesome/user_id.txt', 'rb') as f:
        for line in f.readlines():
            line = line.decode('utf-8')
            line = line.strip('\n').strip()
            line_context = line.split(' ')
            if line_context not in FRIENDS:
                FRIENDS.append(line_context)
    # print(f"user is: {FRIENDS}")
    return FRIENDS


def get_flag_from_txt():
    with open('awesome/flag.txt', 'rb') as f:
        for line in f.readlines():
            line = line.decode('utf-8')
            line = line.strip('\n').strip()
            line_context = line.split(' ')
            if line_context not in FLAG:
                FLAG.append(line_context)
    # print(f"user is: {FLAG}")
    return FLAG


def refresh_flag(self_name, state):
    flag_name = [item[0] for item in FLAG]
    if self_name in flag_name:
        name_index = flag_name.index(self_name)
        FLAG[name_index][1] = state
    with open('awesome/flag.txt', 'wb') as f:
        for line in FLAG:
            insert_msg = line[0] + ' ' + line[1] + '\n'
            insert_msg_bytes = bytes(insert_msg, encoding="utf-8")
            # writelines expects an iterable, so it will iterate on your bytes object
            # and each item it iterates on is an int.
            # 用 writelines 写 bytes 类型会出错，因为 writelines 会遍历对象，可以写 str 类型的
            # 用 write 是整个写进去，可以写 bytes 的
            f.write(insert_msg_bytes)


