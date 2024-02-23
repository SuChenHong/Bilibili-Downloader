# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import argparse
from api import DownLoadVideo, DownloadBangumi


class CIL:
    """ 命令行控制 """

    # ---------------参数----------------- #
    __VERSION__:        str = '1.0.0'
    __DEFAULT_BVID__:   str = 'BV15F4m13775'
    # __

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='bilibili',
            usage='\n\t%(prog)s <command>[options]',
            description='desc:\n\t\033[35mBilibili Video Downloader\033[0m',
            add_help=False,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        subcommand = self.parser.add_subparsers(title='commands',
                                                dest='command',
                                                metavar='  <command>\t\t<function>')
        # 创建 video 子命令
        video_parser = subcommand.add_parser('video', help='下载普通视频')
        video_parser.add_argument('-b', '--bv', help='视频的BV号')
        video_parser.add_argument('-a', '--av', help='视频的AV号')
        video_parser.add_argument('-s', '--summary', type=bool, default=False, help='是否需要AI生成视频摘要')
        video_parser.add_argument('-A', '--Audio', type=bool, default=False, help='是否单独下载音频')
        video_parser.add_argument('--only', choices=['ONLY_SUMMARY', 'ONLY_AUDIO'], default=None,
                                  help='指定内容下载.该项应用时,将只下载选择的内容')
        video_parser.add_argument('-p', '--path', help='视频保存路径')

        # 创建 bangumi 子命令
        bangumi_parser = subcommand.add_parser('bangumi', help='下载番剧, 大会员番剧需要用户的cookie')
        bangumi_parser.add_argument('-b', '--bv', help='番剧BV号')
        bangumi_parser.add_argument('-a', '--av', help='番剧AV号')
        bangumi_parser.add_argument('-e', '--ep', help='番剧某一集的id, 网址上可以看到')
        bangumi_parser.add_argument('-p', '--path', help='保存路径')
        bangumi_parser.add_argument('--playlist', action='store_true', help='显示可以下载的免费番剧')

        self.parser.add_argument('-v', '--version', action='version',
                                 version=f'%(prog)s {self.__VERSION__}',
                                 help='当前版本号')
        self.parser.add_argument('-h', '--help', action='help', help='帮助信息')
        self.parser.add_argument('-t', '--token', help='用户登录token, 在需要大会员认证或进行其他用户行为的时候必须提供该token')

    def __run__(self):
        args = vars(self.parser.parse_args())
        # args = self.parser.parse_args()
        if args['command'] == 'video':
            video = DownLoadVideo()
            bvid = args['bv'] if args['bv'] else self.__DEFAULT_BVID__
            aid = args['av'] if args['av'] else None
            isSummary = args['summary']
            isAudio = args['Audio']
            restriction = args['only']
            path = args['path'] if args['path'] else './src'
            video.download(
                bvid=bvid, aid=aid, audio=isAudio, summary=isSummary, restriction=restriction, path=path
            )
        elif args['command'] == 'bangumi':
            bangumi = DownloadBangumi()
            if args['playlist']:
                bangumi.playlist()
                return
            bvid = args['bv'] if args['bv'] else ''
            aid = args['av'] if args['av'] else None
            eid = args['ep'] if args['ep'] else None
            path = args['path'] if args['path'] else './src'
            bangumi.download(
                bvid=bvid, ep_id=eid, aid=aid, path=path
            )
        else:
            raise ValueError(f'{args["command"]}不存在')


if __name__ == '__main__':
    cli = CIL()
    cli.__run__()


