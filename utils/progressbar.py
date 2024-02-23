# -*- coding: utf-8 -*-
from tqdm import tqdm
from functools import wraps


def ProgressBar(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 获取文件名和总大小
        filename = kwargs.get('filename') if kwargs.get('filename') else 'Unknown'
        # total_size = kwargs.get('file_size', int(req.headers.get('content-length', 0)))
        total_size = kwargs.get('file_size')
        if total_size is None or total_size == 0:
            raise ValueError("File size is EMPTY")
        # print("total size: {}".format(total_size))
        chunk_size = kwargs.get('chunk_size')
        unit = kwargs.get('unit') if kwargs.get('unit') else 'it'
        unit_scale = kwargs.get('unit_scale') if kwargs.get('unit_scale') else True
        # print(chunk_size, unit_scale, unit)

        # 使用 tqdm 进度条包装文件写入操作
        with tqdm(
            desc=filename,
            total=total_size,
            unit=unit,
            unit_scale=unit_scale,
            unit_divisor=chunk_size if chunk_size >= 1000 else 1000
        ) as bar:
            # 调用原函数，并传递 tqdm 进度条对象
            kwargs['bar'] = bar
            result = func(*args, **kwargs)
        return result
    return wrapper


if __name__ == '__main__':
    pass
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    #     'Referer': 'https://www.bilibili.com/',
    #     'Origin': 'http://bilibili.com'
    # }
    # req = requests.get(url='https://upos-sz-estgoss.bilivideo.com/upgcxcode/83/86/1387648683/1387648683-1-192.mp4?e=ig8euxZM2rNcNbRVhwdVhwdlhWdVhwdVhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1707059511&gen=playurlv2&os=upos&oi=3062063868&trid=1dec2b833ccb48f3b3912d03859cebc0u&mid=11812662&platform=pc&upsig=9bfa97ad57c8b433a4078ec1cf2795aa&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,3&buvid=B4F774B4-6BF9-DCA9-C649-12237F926EEA64795infoc&build=0&f=u_0_0&agrr=0&bw=35863&logo=80000000', stream=True, headers=headers)
    # save(file=req, filename='deco.mp4')

