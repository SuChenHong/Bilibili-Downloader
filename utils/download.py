# -*- coding: utf-8 -*-
import requests
from .type import Any, MODE, FILETYPE
from .progressbar import ProgressBar


class Download:

    def __init__(self):
        self.__name__ = 'download'

    @classmethod
    @ProgressBar
    def download(
            cls,
            file: Any,
            filename: str,
            file_size: int,
            mode: MODE,
            type: FILETYPE,
            chunk_size: int = 1,
            bar=None,
            unit: str = 'it',
            unit_scale: bool = False,
            encoding: str = None
    ):
        if type == 'stream':
            try:
                with open(filename, mode=mode, encoding=encoding) as fw:
                    for data in file.iter_content(chunk_size=chunk_size):
                        size = fw.write(data)
                        bar.update(size)
            except Exception as e:
                raise Exception(e, '下载失败')
        elif type == 'text':
            try:
                with open(filename, mode=mode, encoding=encoding) as fw:
                    for data in file:
                        size = fw.write(data)
                        bar.update(size)
            except Exception as e:
                raise Exception(e, '下载失败')
        else:
            raise ValueError('download type 必须是stream或者text类型')
        bar.close()

    @staticmethod
    def create_file_name(filename: str | None) -> str:

        if filename is None:
            import os
            suffix: int = 1
            filename = 'Unknown.mp4'
            while True:
                if os.path.exists(filename):
                    filename = f'Unknown_{suffix}.mp4'
                    suffix += 1
                    continue
                break
        return filename

    def download_stream(
            self,
            file: requests.Response,
            filename: str | None,
            unit: str = 'it',
            unit_scale: bool = False,
            chunk_size: int = 1,
    ):
        """ 下载流文件 """

        filename = self.create_file_name(filename)

        file_size = int(file.headers.get('content-length'))
        self.download(
            file=file, filename=filename, file_size=file_size, mode='wb',
            chunk_size=chunk_size, unit=unit, unit_scale=unit_scale, type='stream'
        )

    def download_text(
            self,
            file: Any,
            filename: str | None,
            mode: MODE = 'w',
            encoding: str = 'utf8',
            unit: str = 'it',
            unit_scale: bool = False,
            chunk_size: int = 1
    ):
        """ 下载文本文件 """

        filename = self.create_file_name(filename)

        file_size = len(file)
        self.download(
            file=file, filename=filename, chunk_size=chunk_size, file_size=file_size,
            mode=mode, unit=unit, unit_scale=unit_scale, type='text', encoding=encoding
        )

