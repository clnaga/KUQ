from os import path
import nonebot


# from KUQ import config
# 用 python 解释器运行代码时，不用上面的 import，用下面的 import 方法
import sys
sys.path.extend(['D:\\workspace\\PyCharmDemo\\KUQ\\KUQ\\config'])
import config

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'awesome', 'plugins'),
        'awesome.plugins'
    )

    nonebot.run()
