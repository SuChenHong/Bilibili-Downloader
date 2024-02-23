# -*- coding: utf-8 -*-
import os
import time

# urls = 'https://www.bilibili.com/video/BV1hk4y1S7PJ/?spm_id_from=333.1007.tianma.1-2-2.click&vd_source=7bd143dfc7ff42621d3b07ad2c79a689'
#
# print(urls.split('/')[4])
#
# path = '.'
# name = 'afgg.mp4'
#
# print(os.path.join(path, name))
#
# # os.makedirs('test')
#
# class Aniaml:
#
#     def __init__(self, type, color, age=12):
#         self.type = type
#         self.color = color
#         self.age = age
#
#     def PrintIn(self):
#         print(self.__class__.__name__)
#
#
# class Cat(Aniaml):
#     def __init__(self, color, age=0, hobby=''):
#         super(Cat, self).__init__('猫科', color, age)
#         self.hobby = hobby
#
#     # def PrintIn(self):
#     #     print(self.__class__.__name__)
#
#     def main(self):
#         # return self.__class__.PrintIn(self)
#         return self.PrintIn()
#     # def getname(self):
#     #     return self.__class__.__name__
#
#
# an1 = Aniaml('犬科', '黄色')
# an2 = Aniaml('犬科', '黄色', 10)
#
#
# cat1 = Cat('白色')
# cat2 = Cat('灰色', 3)
# cat3 = Cat('灰色', hobby='睡觉')
# cat4 = Cat('灰色', 3, '睡觉')
# print(an1.PrintIn())
# print(cat1.main())
# print(cat1.age)
#
# from datetime import datetime
#
# timestamp = 645631
# dt_object = datetime.utcfromtimestamp(timestamp)
#
# print(int(datetime.utcnow().timestamp()))
#
# print(dt_object)
#
# from functools import reduce
# from hashlib import md5
# import urllib.parse
# import time
# import requests
#
# mixinKeyEncTab = [
#     46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
#     33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
#     61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
#     36, 20, 34, 44, 52
# ]
#
# def getMixinKey(orig: str):
#     '对 imgKey 和 subKey 进行字符顺序打乱编码'
#     return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, '')[:32]
# def encWbi(params: dict, img_key: str, sub_key: str):
#     '为请求参数进行 wbi 签名'
#     mixin_key = getMixinKey(img_key + sub_key)
#     curr_time = round(time.time())
#     params['wts'] = curr_time                                   # 添加 wts 字段
#     params = dict(sorted(params.items()))                       # 按照 key 重排参数
#     # 过滤 value 中的 "!'()*" 字符
#     params = {
#         k: ''.join(filter(lambda chr: chr not in "!'()*", str(v)))
#         for k, v
#         in params.items()
#     }
#     query = urllib.parse.urlencode(params)                      # 序列化参数
#     wbi_sign = md5((query + mixin_key).encode()).hexdigest()    # 计算 w_rid
#     params['w_rid'] = wbi_sign
#     return params
#
#
# def getWbiKeys() -> tuple[str, str]:
#     '获取最新的 img_key 和 sub_key'
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#         'Referer': 'https://www.bilibili.com/',
#     }
#     resp = requests.get('https://api.bilibili.com/x/web-interface/nav', headers=headers)
#     resp.raise_for_status()
#     json_content = resp.json()
#     img_url: str = json_content['data']['wbi_img']['img_url']
#     sub_url: str = json_content['data']['wbi_img']['sub_url']
#     img_key = img_url.rsplit('/', 1)[1].split('.')[0]
#     sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
#     return img_key, sub_key
#
# img_key, sub_key = getWbiKeys()
# print(img_key, sub_key)
# # bvid=BV1mt4y1o7Rh&cid=1387648683&up_mid=507373006&
# signed_params = encWbi(
#     params={
#         'bvid': 'BV1QU4y1T7TK',
#         'cid': 456486205,
#         'qn': 112,
#         'fourk': 1,
#         'fnver': 0,
#         'fnval': 4048,
#         'gaia_source': 'pre-load'
#     },
#     img_key=img_key,
#     sub_key=sub_key
# )
# query = urllib.parse.urlencode(signed_params)
# print(signed_params)
# print(query)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.bilibili.com/',
}
# req = requests.get(url='https://api.bilibili.com/x/player/wbi/playurl?bvid=BV1mt4y1o7Rh&cid=1387648683&qn=64&fnver=0&fnval=16&fourk=1', headers=headers)
# print(req.json()["data"]["dash"]["audio"][0]["base_url"])


# from overloading import overload
# from type import Any
#
#
# class test:
#     def __init__(self):
#         pass
#
#     @staticmethod
#     @overload
#     def area(l: Any, b: int) -> int:
#         print(l, b)
#         return l*b
#
#     @staticmethod
#     @overload
#     def area(l: Any, b: int, c: int, d: str) -> int:
#         print(l, b, c, d)
#         return l * b * c
#         # import math
#         # return math.pi * r ** 2
#
# t = test()
# print(t.area(3, 4))
# print(t.area(1, 3, 4, '45'))

# req = requests.get('https://xy118x182x248x66xy.mcdn.bilivideo.cn:4483/upgcxcode/05/62/456486205/'
#                    '456486205_da2-1-16.mp4?e='
#                    'ig8euxZM2rNcNbRVhwdVhwdlhWdVhwdVhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ'
#                    '10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline='
#                    '1706810083&gen=playurlv2&'
#                    'os=mcdn&oi=3062063582&trid='
#                    '000056818b1fd9f147e883f143d6ad987e86p&'
#                    'mid=0&platform=pc&upsig=41daaea8811e59cef1b37ea47d87ae21&'
#                    'uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&'
#                    'mcdnid=1002731&bvc=vod&nettype=0&orderid=0,3&'
#                    'buvid=22DF378F-72EC-EB59-BC28-45C99C6D4D8E99744infoc&build=0&f=p_0_0&agrr=0&bw=48724&logo=A0000001', headers=headers)
# with open('3.mp4', 'wb') as f:
#     f.write(req.content)

# headers['Cookie'] = 'buvid3=B4F774B4-6BF9-DCA9-C649-12237F926EEA64795infoc; b_nut=1680505864; i-wanna-go-back=-1; _uuid=FA32911B-D31A-3FEB-56F7-3EBAAB4BE1AF61507infoc; nostalgia_conf=-1; buvid4=6B730CE7-9FBB-CB08-1038-EB0FF0970FB565646-023040315-HNYvTHSPdBRNML1dEnuXxO0engO05zPTmhhla%2BtesC5K0dgJf%2BxUcg%3D%3D; rpdid=0zbfVGh7SF|cUYMrsaV|4a4|3w1PJemC; b_ut=5; CURRENT_PID=316a7b70-d1f8-11ed-897c-6bf157e3ce02; buvid_fp_plain=undefined; LIVE_BUVID=AUTO8616815283202627; CURRENT_BLACKGAP=0; header_theme_version=CLOSE; hit-new-style-dyn=0; hit-dyn-v2=1; FEED_LIVE_VERSION=V8; DedeUserID=11812662; DedeUserID__ckMd5=86d50fc2cb16b576; enable_web_push=DISABLE; CURRENT_QUALITY=120; home_feed_column=5; browser_resolution=2560-1271; SESSDATA=72350046%2C1722216653%2C841ea%2A12CjBeto18eQH8NVHWhzrmyiehDwBQ7udhEzHU3zupQZRewiLWSIgqCUCpG3DRny2beVgSVnN1MWhISWhQV3NjbG5RR05kM01CY2h5MWIzQTNUbHBERzVFRGZWOE16YXI4cEdQYU14R24yZ1RxWWlFVWZDSVZONmVFMEJkeS0xX2c5bDBjbjZvcXd3IIEC; bili_jct=99baf38d6a73d8b01adde7ebf4bae04e; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDcwMTY1NDIsImlhdCI6MTcwNjc1NzI4MiwicGx0IjotMX0.axGGTdLpHzrfMf2Cdc3W5TkOUWy50BchKpXFhcmvZSY; bili_ticket_expires=1707016482; bp_video_offset_11812662=893026767204253705; fingerprint=6499834177756ee1e60c8faf9c1cc781; buvid_fp=8976009bec71a14d4a6bb711b2e4c91c; sid=7w633ojf; b_lsid=7A677DE9_18D6A77E269; CURRENT_FNVAL=4048; PVID=4'
#
# req = requests.get(url='https://api.bilibili.com/pgc/player/web/playurl?ep_id=409795', headers=headers)
# with open('te.mp4', 'wb') as f:
#     f.write(requests.get(url=req.json()['result']['durl'][0]['url'], headers=headers).content)
# requests.get(url=req.json()['result']['durl'][0]['url'], headers=headers)
# path = './Video'
# bvid = 'BHGONKLN'
# print(os.path.join(path, bvid))

# from utils.driver import Driver
#
# dr = Driver()
# dr.check_update_chromedriver()

import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


def download_video(url):
    req = requests.get(url, headers=headers, stream=True)
    file_size = int(req.headers['content-length'])
    if req.status_code == 200:
        with tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024) as bar:
            with open('video.mp4', 'wb') as file:
                for chunk in req.iter_content(chunk_size=1024):
                    if chunk:
                        size = file.write(chunk)
                        bar.update(size)
            bar.close()
# import aiohttp
# import aiofiles
# import asyncio
# from tqdm import tqdm
#
# async def download_video_chunk(session, url, output_path, chunk_size):
#     async with session.get(url, headers=headers) as response:
#         file_size = int(response.headers.get('Content-Length', 0))
#         print(file_size)
#         bar = tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024)
#
#         async with aiofiles.open(output_path, 'wb') as file:
#             async for chunk in response.content.iter_any():
#                 if chunk:
#                     await file.write(chunk)
#                     bar.update(len(chunk))
#         bar.close()
#
# async def download_video(url, output_path="video.mp4", chunk_size=1024):
#     async with aiohttp.ClientSession() as session:
#         await download_video_chunk(session, url, output_path, chunk_size)
#
# async def main():
#     video_url = 'https://xy218x91x222x135xy.mcdn.bilivideo.cn:4483/upgcxcode/83/86/1387648683/1387648683-1-16.mp4?e=ig8euxZM2rNcNbRVhwdVhwdlhWdVhwdVhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1708185923&gen=playurlv2&os=mcdn&oi=3062769236&trid=0000c86acf46622e452685abc1e17a5b1102u&mid=11812662&platform=pc&upsig=e5fc504df8110f2a2952660fdaff32c3&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&mcdnid=50000333&bvc=vod&nettype=0&orderid=0,3&buvid=B4F774B4-6BF9-DCA9-C649-12237F926EEA64795infoc&build=0&f=u_0_0&agrr=0&bw=15001&logo=A0020000'
#     await download_video(video_url)
#
# if __name__ == "__main__":
#     start = time.time()
#     asyncio.run(main())
#     end = time.time()
#     print(end - start)

url = 'https://xy218x91x222x135xy.mcdn.bilivideo.cn:4483/upgcxcode/83/86/1387648683/1387648683-1-16.mp4?e=ig8euxZM2rNcNbRVhwdVhwdlhWdVhwdVhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1708185923&gen=playurlv2&os=mcdn&oi=3062769236&trid=0000c86acf46622e452685abc1e17a5b1102u&mid=11812662&platform=pc&upsig=e5fc504df8110f2a2952660fdaff32c3&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&mcdnid=50000333&bvc=vod&nettype=0&orderid=0,3&buvid=B4F774B4-6BF9-DCA9-C649-12237F926EEA64795infoc&build=0&f=u_0_0&agrr=0&bw=15001&logo=A0020000'

# start = time.time()
# with ThreadPoolExecutor(max_workers=8) as executor:
#     executor.submit(download_video, url)
# download_video(url)
# end = time.time()
# print(end-start)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from rich.table import Table
from rich import box
from rich.live import Live

table = Table(box=box.HORIZONTALS, show_edge=False)
table.add_column('[green]ep_id', justify='center')
table.add_column('[red]title', justify='center')
table.add_column('[blue]episode', justify='center')
table.add_column('[yellow]link', justify='center')

te = 'https://www.bilibili.com/anime/index/#st=1&page=1&season_status=1&season_version=-1'
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--silent')
driver = webdriver.Chrome(options=chrome_options)
driver.get(te)
time.sleep(0.5)
uls = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[1]/ul[2]')
lis = uls.find_elements(By.XPATH, './/li')
with Live(table, refresh_per_second=4):
    for li in lis:
        href = li.find_element(By.XPATH, './/a[1]').get_attribute('href')
        ep_id = href.split('?')[0].split('ss')[1]
        title = li.find_element(By.XPATH, './/a[2]').text
        total_episodes = li.find_element(By.XPATH, './p').text
        table.add_row(f"[green]{ep_id}",
                      f"[red]{title}",
                      f"[blue]{total_episodes}",
                      f"[yellow]{href}",
                      end_section=True)
        time.sleep(0.4)
        # print(f'{title:^20}:{href}')
import datetime
choice = input(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]输入ep_id:')
if int(choice) == 1672:
    print('龙与虎下载完成')
driver.quit()

# import curses
# import time
#
# menu_items = ["1. Download video", "2. Download anime", "3. Download music", "4. EXIT"]
#
# def download_video(stdscr):
#     stdscr.clear()
#     stdscr.addstr(0, 0, "Downloading video...")
#     stdscr.refresh()
#
#     # 模拟下载操作
#     for i in range(1, 101):
#         progress_bar(stdscr, i)
#         time.sleep(0.1)
#
#     stdscr.clear()
#
# def download_anime(stdscr):
#     stdscr.clear()
#     stdscr.addstr(0, 0, "Downloading anime...")
#     stdscr.refresh()
#
#     # 模拟下载操作
#     for i in range(1, 101):
#         progress_bar(stdscr, i)
#         time.sleep(0.1)
#
#     stdscr.clear()
#
# def download_music(stdscr):
#     stdscr.clear()
#     stdscr.addstr(0, 0, "Downloading music...")
#     stdscr.refresh()
#
#     # 模拟下载操作
#     for i in range(1, 101):
#         progress_bar(stdscr, i)
#         time.sleep(0.1)
#
#     stdscr.clear()
#
# def progress_bar(stdscr, percent):
#     h, w = stdscr.getmaxyx()
#     bar_width = w - 4
#     progress_width = int(bar_width * percent / 100)
#
#     stdscr.addstr(h // 2, 2, f"[{'=' * progress_width}{' ' * (bar_width - progress_width)}] {percent}%")
#     stdscr.refresh()
#
# def print_menu(stdscr, selected_row):
#     stdscr.clear()
#     h, w = stdscr.getmaxyx()
#
#     for i, item in enumerate(menu_items):
#         x = w // 2 - len(item) // 2
#         y = h // 2 - len(menu_items) // 2 + i
#
#         if i == selected_row:
#             stdscr.attron(curses.color_pair(1))
#             stdscr.addstr(y, x, item)
#             stdscr.attroff(curses.color_pair(1))
#         else:
#             stdscr.addstr(y, x, item)
#
#     stdscr.refresh()
#
# def main(stdscr):
#     curses.curs_set(0)
#     curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
#
#     current_row = 0
#     stdscr.timeout(0)  # 设置超时为零，使得getch()不会阻塞
#     stdscr.nodelay(1)  # 使得getch()不会阻塞
#
#     while True:
#         key = stdscr.getch()
#
#         if key == curses.KEY_UP and current_row > 0:
#             current_row -= 1
#         elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
#             current_row += 1
#         elif key == curses.KEY_ENTER or key in [10, 13]:
#             if current_row == 0:
#                 download_video(stdscr)
#             elif current_row == 1:
#                 download_anime(stdscr)
#             elif current_row == 2:
#                 download_music(stdscr)
#             elif current_row == 3:
#                 break  # EXIT
#
#             # 等待用户按任意键返回主菜单
#             while stdscr.getch() == -1:
#                 pass
#
#             stdscr.clear()
#
#         print_menu(stdscr, current_row)
#
# curses.wrapper(main)






