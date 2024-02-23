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


if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Referer': 'https://www.bilibili.com/',
        'Origin': 'http://bilibili.com'
    }
    req = requests.get(url='https://upos-sz-estgoss.bilivideo.com/upgcxcode/83/86/1387648683/1387648683-1-192.mp4?e=ig8euxZM2rNcNbRVhwdVhwdlhWdVhwdVhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1707067869&gen=playurlv2&os=upos&oi=3062063868&trid=fd19119fbadf4973ab6f27c51f62e403u&mid=11812662&platform=pc&upsig=8d97d89793e858d1f3ecc362fd02bb32&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,3&buvid=B4F774B4-6BF9-DCA9-C649-12237F926EEA64795infoc&build=0&f=u_0_0&agrr=0&bw=35863&logo=80000000', stream=True, headers=headers)
    # print(req.text)
    # download_stream(file=req, filename='deco.mp4', chunk_size=1024)
    download = Download()
    download.download_stream(file=req, filename=None, chunk_size=1024)