# -*- coding: utf-8 -*-
import random
import os
import urllib.parse
import time
import json
import datetime
import requests
import re

from functools import reduce
from hashlib import md5
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from rich.table import Table
from rich import box
from rich.live import Live
from fake_useragent import UserAgent, FakeUserAgentError
from utils.type import quality_type, Any, MODE
from utils.overloading import overload
# from utils.download import Download, requests
from utils.driver import Driver, Download


class BilibiliApi(object):
    def __init__(self):
        """构建母体"""
        """
            解决动态加载
        """
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--log-level=3')
        # chrome_options.add_argument('--silent')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()

        """
            av2bv & bv2av
        """
        self.XOR_CODE = 23442827791579
        self.MASK_CODE = 2251799813685247
        self.MAX_AID = 1 << 51

        self.data = [b'F', b'c', b'w', b'A', b'P', b'N', b'K', b'T', b'M', b'u', b'g', b'3', b'G', b'V', b'5', b'L',
                     b'j', b'7', b'E', b'J', b'n', b'H', b'p', b'W', b's', b'x', b'4', b't', b'b', b'8', b'h', b'a',
                     b'Y', b'e', b'v', b'i', b'q', b'B', b'z', b'6', b'r', b'k', b'C', b'y', b'1', b'2', b'm', b'U',
                     b'S', b'D', b'Q', b'X', b'9', b'R', b'd', b'o', b'Z', b'f']

        self.BASE = 58
        self.BV_LEN = 12
        self.PREFIX = "BV1"

        """
            构建请求头
        """
        self.headers = {
            'User-Agent': random.choice(self.__getFakeUa__),
            'Referer': 'https://www.bilibili.com/',
        }
        self.session = requests.session()

        """
            用于Wbi签名
        """
        self.mixinKeyEncTab = [
            46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
            33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
            61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
            36, 20, 34, 44, 52
        ]

    def __del__(self):
        self.session.close()

    @classmethod
    def downloader(cls):
        """ 下载器 """
        return Download()

    @property
    def __name__(self):
        return self.__class__.__name__

    @staticmethod
    def __createDir__(filepath: str) -> str:
        """ 创建文件夹 """

        if not os.path.exists(filepath):
            os.makedirs(filepath)
        return filepath

    """
        api
    """
    @staticmethod
    def video_view_api(aid: str = None, bvid: str = None) -> str:
        """ 视频详情 """
        if aid is None and bvid is None:
            raise ValueError('Aid and bvid cannot be empty at the same time')
        elif aid:
            return f"https://api.bilibili.com/x/web-interface/view?aid={aid}"
        elif bvid:
            return f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"

    @staticmethod
    def get_cid_api(bvid: str) -> str:
        """ 获取cid的api """
        return f'https://api.bilibili.com/x/player/pagelist?bvid={bvid}&jsonp=jsonp'

    @staticmethod
    def getTime() -> str:
        """ 获取当前时间 """
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @property
    def get_wbi_img_api(self) -> str:
        return 'https://api.bilibili.com/x/web-interface/nav'

    @staticmethod
    def video_download_api(qn: int, fnver: int, bvid: str, cid: str, fnval: int) -> str:
        """ 视频下载地址api """
        return f"https://api.bilibili.com/x/player/wbi/playurl?qn={qn}&fnver={fnver}&bvid={bvid}" \
               f"&cid={cid}&fnval={fnval}&gaia_source=pre-load"

    @staticmethod
    def video_ai_summary_api(query: str) -> str:
        """ 获取视频AI摘要api """
        return f'https://api.bilibili.com/x/web-interface/view/conclusion/get?{query}'

    @staticmethod
    def free_bangumi_download_api(cid: str = None, ep_id: str = None):
        """ 番剧下载地址api """
        if cid:
            return f'https://api.bilibili.com/pgc/player/web/playurl?cid={cid}'
        elif ep_id:
            return f'https://api.bilibili.com/pgc/player/web/playurl?ep_id={ep_id}'

    @staticmethod
    def bangumi_play_page(ep_id: str = None, bvid: str = None):
        """ 番剧播放页 """
        if ep_id:
            ep_id = ep_id.lower()
            if 'ep' in ep_id:
                ep_id = ep_id.split('ep')[1]
            return f'https://www.bilibili.com/bangumi/play/ep{ep_id}?'
        elif bvid:
            return f'https://www.bilibili.com/video/{bvid}/'

    @property
    def bangumi_playlist_free(self):
        return 'https://www.bilibili.com/anime/index/#st=1&page=1&season_status=1&season_version=-1'

    @property
    def __getFakeUa__(self) -> list:
        """ 获取伪装头 """
        ue = UserAgent(verify_ssl=False)
        try:
            return [ue.random for _ in range(5)]
        except FakeUserAgentError as e:
            raise e

    def get_cid(self, bvid: str) -> str:
        # url = f'https://api.bilibili.com/x/player/pagelist?bvid={bvid}&jsonp=jsonp'
        url = self.get_cid_api(bvid)
        try:
            req = self.session.get(url, headers=self.headers)
        except Exception as e:
            raise e
        return str(req.json()["data"][0]["cid"])

    def get_video_view(self, aid: str | None = None, bvid: str | None = None) -> dict:
        """
        获取视频详细信息 (av号和bv号任填其一)
        :param aid: av号
        :param bvid: bv号
        :return: 视频详细信息
        """
        if aid is None and bvid is None:
            raise ValueError('avid和bvid不能同时为空')
        url = ''
        if aid:
            # url = f"https://api.bilibili.com/x/web-interface/view?aid={aid}"
            url = self.video_view_api(aid=aid)
        elif bvid:
            # url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
            url = self.video_view_api(bvid=bvid)
        # print(url)
        try:
            req = self.session.get(url=url, headers=self.headers)
        except Exception as e:
            raise e
        return req.json()

    def get_video_view_details(self):
        pass

    def avid2bvid(self, aid: str) -> str:
        """
        avid转成bvid
        :param aid: 视频avid
        :return: bvid
        """
        bytes = [b'B', b'V', b'1', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0']
        bv_idx = self.BV_LEN - 1
        tmp = (self.MAX_AID | int(aid)) ^ self.XOR_CODE
        while int(tmp) != 0:
            bytes[bv_idx] = self.data[int(tmp % self.BASE)]
            tmp /= self.BASE
            bv_idx -= 1
        bytes[3], bytes[9] = bytes[9], bytes[3]
        bytes[4], bytes[7] = bytes[7], bytes[4]
        return "".join([i.decode() for i in bytes])

    def bvid2aid(self, bvid: str) -> str:
        """
        bvid转成avid
        :param bvid: 视频bvid
        :return: avid
        """
        bvid = list(bvid)
        bvid[3], bvid[9] = bvid[9], bvid[3]
        bvid[4], bvid[7] = bvid[7], bvid[4]
        bvid = bvid[3:]
        tmp = 0
        for i in bvid:
            idx = self.data.index(i.encode())
            tmp = tmp * self.BASE + idx
        return (tmp & self.MASK_CODE) ^ self.XOR_CODE

    """
    ——————————————————————————————————————————————————————————————————————————————————————————————————
    |自 2023 年 3 月起，Bilibili Web 端部分接口开始采用 WBI 签名鉴权，表现在 REST API 请求时在 Query param 中 |
    |添加了 w_rid 和 wts 字段。WBI 签名鉴权独立于 APP 鉴权 与其他 Cookie 鉴权，目前被认为是一种 Web 端风控手段。 |
    ——————————————————————————————————————————————————————————————————————————————————————————————————
    """
    def getMixinKey(self, orig: str) -> str:
        """
        对 imgKey 和 subKey 进行字符顺序打乱编码
        :param orig: img_key + sub_key
        :return: 新编码
        """
        return reduce(lambda s, i: s + orig[i], self.mixinKeyEncTab, '')[:32]

    def encWbi(self, params: dict, img_key: str, sub_key: str) -> dict:
        """
        为请求参数进行 wbi 签名
        :param params: 请求参数
        :param img_key: wbi image key
        :param sub_key: wbi sub key
        :return: 参数列表
        """
        mixin_key = self.getMixinKey(img_key + sub_key)
        curr_time = round(time.time())
        params['wts'] = curr_time  # 添加 wts 字段
        params = dict(sorted(params.items()))  # 按照 key 重排参数
        # 过滤 value 中的 "!'()*" 字符
        params = {
            k: ''.join(filter(lambda ch: ch not in "!'()*", str(v)))
            for k, v
            in params.items()
        }
        query = urllib.parse.urlencode(params)  # 序列化参数
        wbi_sign = md5((query + mixin_key).encode()).hexdigest()  # 计算 w_rid
        params['w_rid'] = wbi_sign
        return params

    def getWbiKeys(self) -> tuple[str, str]:
        """
        获取最新的 img_key 和 sub_key
        :return: [img_key, sub_key]
        """
        try:
            resp = self.session.get(self.get_wbi_img_api, headers=self.headers)
            resp.raise_for_status()
        except Exception as e:
            raise e
        json_content = resp.json()
        img_url: str = json_content['data']['wbi_img']['img_url']
        sub_url: str = json_content['data']['wbi_img']['sub_url']
        img_key = img_url.rsplit('/', 1)[1].split('.')[0]
        sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
        return img_key, sub_key

    @classmethod
    @overload
    def save(cls,
             file: requests.Response,
             filename: str,
             chunk_size: int = 1,
             unit: str = 'it',
             unit_scale: bool = False) -> bool:
        """
        保存流文件
        :param file: 文件内容
        :param filename: 文件名
        :param chunk_size: 下载块大小
        :param unit: 进度条的单位，例如 "B"、"KB"、"MB" 等。
        :param unit_scale: 如果设置为 True，将自动缩放单位，以便更易读地显示。
        :return: 保存状态
        """
        downloader = cls.downloader()
        # chunk_size: int = 1024
        downloader.download_stream(
            file=file, filename=filename, chunk_size=chunk_size, unit=unit, unit_scale=unit_scale
        )
        return True

    @classmethod
    @overload
    def save(cls,
             file: Any,
             filename: str,
             mode: MODE = 'w',
             encoding: str = 'uft8',
             chunk_size: int = 1,
             unit: str = 'it',
             unit_scale: bool = False
             ) -> bool:
        """
        保存文本文件
        :param file: 文件内容
        :param filename: 文件名
        :param mode: 文件打开方式
        :param encoding: 编码格式
        :param chunk_size: 下载块大小
        :param unit: 进度条的单位，例如 "B"、"KB"、"MB" 等。
        :param unit_scale: 如果设置为 True，将自动缩放单位，以便更易读地显示。
        :return: 保存状态
        """

        downloader = cls.downloader()
        downloader.download_text(
            file=file, filename=filename, encoding=encoding,
            unit_scale=unit_scale, unit=unit, mode=mode, chunk_size=chunk_size
        )
        return True


class DownLoadVideo(BilibiliApi):
    """ 视频下载api """

    from utils.type import select_type

    def __init__(self, token=None):
        super(DownLoadVideo, self).__init__()
        self.fnver = 0
        self.fourk = 1
        self.video_suffix = '.mp4'
        self.audio_suffix = '.mp3'
        self.__base_url__ = "https://api.bilibili.com/x/player/wbi/playurl?"
        self.__path__ = 'src'
        if token is not None:
            self.headers['Cookie'] = token

    def download(self,
                 bvid: str | None = None,
                 aid: str | None = None,
                 qn: quality_type = 64,
                 fnval: int = 1,
                 audio: bool = False,
                 summary: bool = False,
                 restriction: select_type = None,
                 path: str = None) -> None:
        """
        下载视频
        :param bvid: 视频bv号, 与aid二选一
        :param aid: 视频av号, 与bvid二选一
        :param qn: 视频清晰度标识, 默认64; 若没有登陆账号, 则该值最大只能为64
        :param fnval: 视频流格式, 默认为mp4(1)
        :param audio: 视频的音频
        :param summary: 是否生成AI视频摘要, 默认否
        :param restriction: 选择指定内容保存
        :param path: 保存路径
        """
        if path is None:
            path = self.__path__

        onlyAudio: bool = False
        onlySummary: bool = False
        if restriction:
            if restriction not in ['ONLY_AUDIO', 'ONLY_SUMMARY']:
                raise ValueError('如果restriction不为空, '
                                 '则应该为["ONLY_AUDIO", "ONLY_SUMMARY"]中的某个值')

            if restriction == 'ONLY_AUDIO':
                # 只保存音频
                if not audio:
                    raise ValueError('audio必须为true')
                elif summary:
                    raise ValueError('summary应该为false')
                onlyAudio = True

            elif restriction == 'ONLY_SUMMARY':
                # 只保存摘要
                if not summary:
                    raise ValueError('summary必须为true')
                elif audio:
                    raise ValueError('audio应该为false')
                onlySummary = True

        if bvid is None and aid is None:
            raise ValueError('avid和bvid不能同时为空!')
        if bvid:
            aid = self.bvid2aid(bvid)
        elif aid:
            bvid = self.avid2bvid(aid)
        cid = self.get_cid(bvid)
        # base_request_url = self.__base_url__ + f"qn={qn}&fnver={self.fnver}" \
        #                                        f"&bvid={bvid}&cid={cid}" + "&fnval={}"

        forbidden_chars = r'[\\/:*?"<>|]'
        # title: str = self.get_video_view(aid)['data']['title']
        title: str = re.sub(forbidden_chars, '', self.get_video_view(aid)['data']['title'])
        path: str = self.__createDir__(os.path.join(path, bvid))

        if audio:
            # 保存音频
            a_fnval = 16
            audio_request_url = self.video_download_api(qn, self.fnver, bvid, cid, a_fnval)
            # print(audio_request_url)
            try:
                req = self.session.get(url=audio_request_url, headers=self.headers)
            except Exception as e:
                raise e
            audio_stream = req.json()["data"]["dash"]["audio"][0]["base_url"]
            filename = os.path.normpath(os.path.join(path, f'{title}{self.audio_suffix}'))
            self.save(
                requests.get(audio_stream, headers=self.headers, stream=True),
                filename,
                1024,
                'B',
                True
            )
        if onlyAudio:
            # 只保存音频
            return

        if summary:
            # 需要生成AI视频摘要
            img_key, sub_key = self.getWbiKeys()
            signed_params = self.encWbi(
                params={
                    'bvid': bvid,
                    'cid': cid,
                    'up_mid': self.get_video_view(aid)['data']['owner']['mid']
                },
                img_key=img_key,
                sub_key=sub_key
            )
            query = urllib.parse.urlencode(signed_params)
            # url = f'https://api.bilibili.com/x/web-interface/view/conclusion/get?{query}'
            url = self.video_ai_summary_api(query)
            try:
                req = self.session.get(url=url, stream=True, headers=self.headers)
            except Exception as e:
                raise e
            summary_name = os.path.join(path, f'【AI摘要】{bvid}.json')
            if int(req.json()["data"]["code"]) == -1:
                print(f'{bvid}不支持生成AI视频摘要')
            else:
                content = json.loads(req.text)
                file = json.dumps(content, indent=4, ensure_ascii=False)
                self.save(file, summary_name, 'w', 'gbk', 1, 'B', True)

        if onlySummary:
            # 只保存摘要
            return

        # 保存视频
        request_url = self.video_download_api(qn, self.fnver, bvid, cid, fnval)
        try:
            req = self.session.get(url=request_url, headers=self.headers)
        except Exception as e:
            raise e
        video_stream = req.json()['data']['durl'][0]['url']
        filename = os.path.normpath(os.path.join(path, f'{title}{self.video_suffix}'))

        # ### 获取文件的总大小 ### #
        file_stream = requests.get(video_stream, headers=self.headers, stream=True)
        file_size = int(file_stream.headers['content-length'])
        self.headers['Range'] = f'bytes={0}-{file_size}'

        self.save(
            requests.get(video_stream, headers=self.headers, stream=True),
            filename,
            1024,
            'B',
            True
        )


class DownloadBangumi(BilibiliApi):
    # https://api.bilibili.com/pgc/player/web/playurl?cid=456486205
    """ 下载番剧 """

    """
    Tips: 下载会员番剧时, 需要登录账号的cookie(token)
    """

    """
    免费番剧: 任意某集的bvid(ep_id)
    """

    def __init__(self, token=None):
        super(DownloadBangumi, self).__init__()
        self.__path__ = 'src'
        if token is not None:
            self.headers['Cookie'] = token

    def playlist(self):
        """ 用来下载全集 """

        table = Table(box=box.HORIZONTALS, show_edge=False)
        table.add_column('[green]id', justify='center')
        table.add_column('[red]title', justify='center')
        table.add_column('[blue]episode', justify='center')
        table.add_column('[yellow]link', justify='center')

        playlist_free_url = self.bangumi_playlist_free
        self.driver.get(playlist_free_url)
        time.sleep(0.5)
        uls = self.driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[1]/ul[2]')
        lis = uls.find_elements(By.XPATH, './/li')
        with Live(table, refresh_per_second=4):
            for idx, li in enumerate(lis):
                href = li.find_element(By.XPATH, './/a[1]').get_attribute('href')
                title = li.find_element(By.XPATH, './/a[2]').text
                total_episodes = li.find_element(By.XPATH, './p').text
                table.add_row(f"[green]{idx+1}",
                              f"[red]{title}",
                              f"[blue]{total_episodes}",
                              f"[yellow]{href}",
                              end_section=True)
                time.sleep(0.4)
        # 这里的
        # choice: str = input(f'[{self.getTime()}]输入你想下载的id:')

    def get_bangumi_episodes_bvid(self, url: str, bvid: str = None) -> tuple[int, str, str, str]:
        """  通过ep_id获取番剧的总集数和bvid """

        if not url:
            raise ValueError("url cannot be empty")

        # from selenium import webdriver
        # from selenium.webdriver.chrome.options import Options
        # from selenium.webdriver.common.by import By
        # from selenium.webdriver.support.ui import WebDriverWait
        # from selenium.webdriver.support import expected_conditions as ec

        # 检查chrome驱动
        chromedriver = Driver()
        chromedriver.check_update_chromedriver()

        # 获取总集数和bvid
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--log-level=3')
        # chrome_options.add_argument('--silent')
        # driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(url)
        time.sleep(1)
        episode_title = self.driver.find_element(By.XPATH, '//*[@id="player-title"]').text
        print(episode_title)
        bangumi_title: str = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/'
                                                                'div/div[2]/div/a[1]').text

        total_episodes: int = len(self.driver.find_elements(By.XPATH, "//*[@id='__next']/div/div"
                                                                      "/div[3]/div[3]/div[3]/div"))

        bvid: str = self.driver.find_element(By.XPATH, "//*[@id='__next']/div/div/div[2]/div/div[2]/div/"
                                                       "div[2]/span[4]/span/a").text if bvid is None else bvid

        # episode_title = WebDriverWait(self.driver, 30).until(
        #     ec.presence_of_all_elements_located((By.XPATH, '//*[@id="player-title"]'))
        # )
        # print(episode_title[0].text)
        # total_episodes = WebDriverWait(driver, 10).until(
        #     ec.presence_of_all_elements_located((By.XPATH, '//*[@id="__next"]/div/div/div[3]/div[3]/div[3]/div'))
        # )
        # bvid = WebDriverWait(driver, 10).until(
        #     ec.presence_of_all_elements_located(
        #         (By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/div[2]/div/div[2]/span[4]/span/a'))
        # )
        self.driver.quit()
        # print(len(total_episodes), bvid[0].text)
        # return len(total_episodes), bvid[0].text
        # print(total_episodes, bvid)
        return total_episodes, bvid, episode_title, bangumi_title

    def download(self, bvid: str = None, ep_id: str = None, aid: str = None, episode: int = 1, path: str = None):
        """
        下载番剧
        :param bvid: 视频的bv号, 和ep_id二选一
        :param ep_id: 视频的ep_id, 和bvid二选一
        :param aid: 视频的av号, 可以为空
        :param episode: 下载的集数
        :param path: 保存路径
        :return:
        """
        if path is None:
            path = self.__path__

        download_url = None
        if not bvid and not ep_id and not aid:
            raise ValueError("bvid and ep_id cannot be empty at the same time")
        if aid:
            bvid = bvid if not bvid else self.avid2bvid(aid)
        """
        ep_id只对下载视频和访问番剧播放页有用, 而bvid可以获取video的详情
        因此:如果在ep_id存在, 而bvid为空的情况下,我们需要通过ep_id访问
        播放页从而获得bvid, 由此获取视频详情
        """
        episode_title: str = ''
        bangumi_title: str = ''

        if bvid:
            cid = self.get_cid(bvid)
            download_url = self.free_bangumi_download_api(cid=cid)
            play_page = self.bangumi_play_page(bvid=bvid)
            print(f'[{self.getTime()}]{bvid}, 正在获取剧集总数...')
            total_episodes, _, episode_title, bangumi_title = self.get_bangumi_episodes_bvid(play_page, bvid)
            # return

        elif ep_id:
            download_url = self.free_bangumi_download_api(ep_id=ep_id)
            play_page = self.bangumi_play_page(ep_id=ep_id)
            print(f'[{self.getTime()}]ep{ep_id}, 正在获取bvid和剧集总数...')
            total_episodes, bvid, episode_title, bangumi_title = self.get_bangumi_episodes_bvid(play_page)

        # # 获取番剧详情
        bangumi_view: dict = self.get_video_view(bvid=bvid)
        # print(bangumi_view)
        # # raise ValueError
        bangumi_view_clean = {}.fromkeys(['bvid', 'aid', 'cid', 'ep_id', 'title', 'tname', 'duration', 'desc', 'pic'])
        bangumi_view_clean['tname'] = bangumi_view['data']['tname']  # 类型
        episode_title = bangumi_view['data']['title'] if episode_title is None else episode_title
        bangumi_view_clean['title'] = episode_title  # 剧集标题
        bangumi_view_clean['bvid'] = bvid
        bangumi_view_clean['aid'] = aid if aid else bangumi_view['data']['aid']
        bangumi_view_clean['cid'] = bangumi_view['data']['cid']
        bangumi_view_clean['ep_id'] = bangumi_view['data']['redirect_url'].split('ep')[1]
        total_time = bangumi_view['data']['duration']  # 以秒为单位
        hour: int = total_time // 3600
        minute: int = (total_time - hour*3600) // 60
        second: int = total_time - hour*3600 - minute*60
        formal_time: str = f'{str(hour).zfill(2)}:{str(minute).zfill(2)}:{str(second).zfill(2)}'
        if bangumi_view['data']['videos'] != 1:
            total_episodes = bangumi_view['data']['videos']
            formal_time = f'{formal_time}(total bangumi duration)'
        bangumi_view_clean['duration'] = formal_time
        bangumi_view_clean['desc'] = bangumi_view['data']['desc']
        bangumi_view_clean['pic'] = bangumi_view['data']['pic']
        # return bangumi_view_clean

        # 番剧下载
        try:
            req = self.session.get(url=download_url, headers=self.headers)
        except Exception as e:
            raise e
        # --------------[多集下载]----------------- #
        # if episode >= 1:
        #     pass
        # --------------[多集下载]----------------- #
        forbidden_chars = r'[\/:*?"<>|]'
        bangumi_title = re.sub(forbidden_chars, '', bangumi_title)
        episode_title = re.sub(forbidden_chars, '', episode_title).rstrip('\u3002').replace('\uFF0C', ',')
        filepath: str = self.__createDir__(os.path.join(path, f"{bangumi_title}", f"{episode_title}"))
        video_file = os.path.join(filepath, f'{episode_title}.mp4')
        text_file = os.path.join(filepath, f"{episode_title}.json")

        # 下载番剧简单介绍
        self.save(
            json.dumps(bangumi_view_clean, indent=4, ensure_ascii=False),
            text_file,
            'w',
            'gbk',
            1,
            'it',
            True
        )

        # 下载番剧
        # ### 获取文件的总大小 ### #
        bangumi_stream = req.json()['result']['durl'][0]['url']
        file_stream = requests.get(bangumi_stream, headers=self.headers, stream=True)
        file_size = int(file_stream.headers['content-length'])
        self.headers['Range'] = f'bytes={0}-{file_size}'
        self.save(
            requests.get(bangumi_stream, stream=True, headers=self.headers),
            video_file,
            1024,
            'B',
            True
        )


class DownloadMusic(BilibiliApi):

    def __init__(self):
        super(DownloadMusic, self).__init__()

    def download(self):
        pass


if __name__ == "__main__":
    # test
    # bilibili_api = BilibiliApi()
    # print(bilibili_api.__name__)
    # print(bilibili_api.avid2bvid('623118235'))
    # print(bilibili_api.bvid2avid('BV1mt4y1o7Rh'))
    # print(bilibili_api.get_cid('BV1mt4y1o7Rh'))

    # download = DownLoadVideo()
    # download.download(bvid='BV1Ux4y1179J', audio=True)

    # download.download(bvid='BV15F4m13775', summary=True, audio=True)
    # _aid = download.bvid2aid('BV1vF411h7uv')
    # print(download.video_view_api(_aid))

    bangumi = DownloadBangumi()
    bangumi.download(bvid='BV1fx411B7xj')
