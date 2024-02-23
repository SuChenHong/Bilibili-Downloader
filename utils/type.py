# -*- coding: utf-8 -*-
from typing import (
    Literal,
    Any
)

"""
    视频分辨率
"""
quality_type = Literal[120, 112, 80, 64, 32, 16]

"""
    选择需要保存的内容
"""
select_type = Literal['ONLY_AUDIO', 'ONLY_SUMMARY']

"""
    文件打开模式
"""
MODE = Literal['w', 'wb', 'r+', 'a', 'wt', 'a+']

"""
    文件下载类型
"""
FILETYPE = Literal['stream', 'text']
