# -*- coding: utf-8 -*-
import requests
import winreg
import zipfile
import os

from .download import Download


class Driver:
    def __init__(self, driver=None):
        if driver is None:
            driver = 'chrome'
        self.driver = driver

    @classmethod
    def downloader(cls):
        return Download()

    @property
    def __name__(self):
        return self.__class__.__name__

    @property
    def __driver__(self):
        return "chromedriver.zip"

    @property
    def download_url(self):
        return 'https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json'

    @classmethod
    def get_chrome_version(cls):
        """ 获取系统chrome的版本 """

        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'Software\\Google\\Chrome\\BLBeacon')
        version, types = winreg.QueryValueEx(key, 'version')
        return version

    @classmethod
    def get_chromedriver_version(cls):
        """ 获取chromedriver的版本 """

        version = os.popen(r'.\chromedriver.exe --version').read()
        return version.split(' ')[1]

    @classmethod
    def unzip_driver(cls, path: str = None) -> bool:
        """ 解压chromedriver.zip到指定路径 """

        if not path:
            path = os.getcwd()
        try:
            with zipfile.ZipFile(os.path.join(path, cls().__driver__), 'r') as f:
                for file in f.namelist():
                    target_file = os.path.join(path, os.path.basename(file))
                    with f.open(file) as source, open(target_file, 'wb') as fw:
                        fw.write(source.read())
            return True
        except zipfile.error:
            return False

    @classmethod
    def download_driver(cls, version: int) -> bool:
        """下载文件"""

        import platform
        system_info = platform.system()
        if system_info == 'Windows':
            win_info = platform.architecture()
            if '64bit' in win_info:
                sid = 4  # win64
            elif '32bit' in win_info:
                sid = 3  # win32
            else:
                raise ValueError(f'>>>Unknown Windows System: {win_info}')
        elif system_info == 'Linux':
            sid = 0
        elif system_info == 'Darwin':
            mac_info = platform.machine()
            if mac_info == 'x86_64':
                sid = 2
            elif mac_info == 'arm64':
                sid = 1
            else:
                raise ValueError(f'>>>Unknown Mac System {mac_info}')
        else:
            raise ValueError(f'>>>Unknown System {system_info}')

        all_file = requests.get(cls().download_url).json()
        file = None
        for idx in range(len(all_file['versions'])):
            current_version = int(all_file['versions'][idx]['version'].split('.')[0])
            if version == current_version:
                try:
                    file = all_file['versions'][idx]['downloads']['chromedriver'][sid]['url']
                except IndexError as e:
                    raise e
                break
        if file is None:
            raise ValueError('>>> No compatible version ')

        downloader = cls.downloader()
        downloader.download_stream(
            file=requests.get(url=file, stream=True),
            filename=cls().__driver__,
            unit='B',
            unit_scale=True,
            chunk_size=1024
        )
        # with open(cls().__driver__, 'wb') as zip_file:  # 保存文件到脚本所在目录
        #     zip_file.write(requests.get(url=file).content)
        print('>>>Download chromedriver.zip successfully')
        return True

    def check_update_chromedriver(self) -> bool:

        chrome_version = self.get_chrome_version()
        c_main_v_number = int(chrome_version.split('.')[0])
        if not os.path.exists('chromedriver.exe'):
            print('chromedriver.exe: Downloading chromedriver...')
            self.download_driver(c_main_v_number)
            if self.unzip_driver():
                print(f'>>>Current Version: {self.get_chromedriver_version()}')
                os.remove(self.__driver__)
                return True
            return False
        else:
            # 一般地, 保证主要版本号相同即可 => 主.x.x.x
            driver_version = self.get_chromedriver_version()
            d_main_v_number = int(driver_version.split('.')[0])
            if c_main_v_number != d_main_v_number:
                print(f'\033[32m chromedriver.exe: Need to update\033[0m')
                if self.download_driver(c_main_v_number):
                    if not self.unzip_driver():
                        raise f">>>No compatible version, Please open {self.download_url}"
                    os.remove(self.__driver__)
                    print(f'>>>Updated Version: {self.get_chromedriver_version()}')
                    return True
            else:
                print('chromedriver.exe: No need to update')
                return False


if __name__ == '__main__':
    # # 测试
    dr = Driver()
    # print(dr.get_chromedriver_version())
    ver = dr.get_chromedriver_version()
    ver = ver.removesuffix(f'.{ver.split(".")[-1]}')
    print(ver)
    d = dr.get_chrome_version()
    d = d.removesuffix(f'.{d.split(".")[-1]}')
    print(d)
    # print(dr.get_chrome_version())
    re = requests.get('https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json')
    lens = len(re.json()['versions'])
    for i in range(lens):
        print(re.json()['versions'][i]['version'])
