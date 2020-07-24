import hashlib
import time
import random
import string
from urllib.parse import quote
import requests
import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
from awesome import cmd_list
from awesome import logger_s
import re
import datetime
from awesome import get_info_from_txt

bot = nonebot.get_bot()
# 获取特定指令列表
CMD_LIST = cmd_list.CMD_LIST
# 获取 logger 对象
logger = logger_s.get_logger()
# 获取好友清单
FRIENDS_IN_ATUO_REPLY = []
FRIENDS_IN_LIST = get_info_from_txt.get_user_id_from_txt()
for FRIEND_IN_LIST in FRIENDS_IN_LIST:
    FRIEND_IN_LIST_INSERT_MSG = [FRIEND_IN_LIST[0], 0]
    FRIENDS_IN_ATUO_REPLY.append(FRIEND_IN_LIST_INSERT_MSG)


# 监听所有通话
# @bot.on_message("private")  私聊
# @bot.on_message("group")    群发
@bot.on_message()
async def _(msg):
    print(f"time: {datetime.datetime.now()} -- auto_replay start!")
    # 去掉消息首尾的空白符
    msg_recv_text = str(msg['message']).strip()
    msg_recv_id = msg['sender']['user_id']
    logger_msg = f"From: {str(msg['user_id'])}, " \
                 f"NickName: {str(msg['sender']['nickname'])}, "
    response_msg = ''
    # 互通消息将 user_id 的 未互通消息时间 置0
    for friend_in_list in FRIENDS_IN_ATUO_REPLY:
        if (friend_in_list[0] == str(msg_recv_id))\
                and (friend_in_list[1] < 1):
            await get_info_from_txt.change_friend_info(friend_in_list[0], 3, -1)
            friend_in_list[1] = friend_in_list[1] + 1
    # 获得发送消息
    if msg_recv_text[0] == '[' and msg_recv_text[-1] == ']':
        response_msg = '我只能识别纯文字嗷，请不要发表情、图片、语音给我了 QAQ [CQ:face,id=34]!'
        logger_msg = logger_msg + f"错误：发送表情、图片、语音"
    else:
        if msg_recv_text.split(' ')[0] not in CMD_LIST:
            msg_search_msg = re.sub(r'\[.*\]', "", msg_recv_text)
            response_msg = get_content(msg_search_msg)
            if response_msg == '':
                response_msg = '识别不了该指令额[CQ:face,id=34]'
            logger_msg = logger_msg + f"Say: {msg_recv_text}"
        else:
            logger_msg = logger_msg + f"执行指令：{msg_recv_text}"
    # logger
    logger.debug(logger_msg)
    try:
        await bot.send_private_msg(user_id=msg_recv_id,
                                   message=response_msg)
    except CQHttpError:
        pass
    print(f"time: {datetime.datetime.now()} -- auto_replay stop!")


@nonebot.scheduler.scheduled_job('cron', id='auto_relay_init_FRIENDS', hour='7')
async def _():
    global FRIENDS_IN_ATUO_REPLY
    friends_in_list = get_info_from_txt.get_user_id_from_txt()
    for friend_in_list in friends_in_list:
        friend_in_list_insert_msg = [friend_in_list[0], 0]
        FRIENDS_IN_ATUO_REPLY.append(friend_in_list_insert_msg)


def curlmd5(src):
    m = hashlib.md5(src.encode('UTF-8'))
    # 将得到的MD5值所有字符转换成大写
    return m.hexdigest().upper()


def get_params(plus_item):
    global params
    # 请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效）
    t = time.time()
    time_stamp = str(int(t))
    # 请求随机字符串，用于保证签名不可预测
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    # 应用标志，这里修改成自己的id和key
    app_id = '2149760897'
    app_key = 'qZj8qBeaZix4lmwv'
    params = {'app_id': app_id,
              'question': plus_item,
              'time_stamp': time_stamp,
              'nonce_str': nonce_str,
              'session': '10000'
              }
    sign_before = ''
    # 要对key排序再拼接
    for key in sorted(params):
        # 键值拼接过程value部分需要URL编码，URL编码算法用大写字母，例如%E8。quote默认大写。
        sign_before += '{}={}&'.format(key, quote(params[key], safe=''))
    # 将应用密钥以app_key为键名，拼接到字符串sign_before末尾
    sign_before += 'app_key={}'.format(app_key)
    # 对字符串sign_before进行MD5运算，得到接口请求签名
    sign = curlmd5(sign_before)
    params['sign'] = sign
    return params


def get_content(plus_item):
    global payload, r
    # 聊天的API地址
    url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat"
    # 获取请求参数
    plus_item = plus_item.encode('utf-8')
    payload = get_params(plus_item)
    # r = requests.get(url,params=payload)
    r = requests.post(url, data=payload)
    return r.json()["data"]["answer"]
