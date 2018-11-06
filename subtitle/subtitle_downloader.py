# -*- coding: utf-8 -*-
# __author__ = 'ihciah'
# cid_hash_file function from https://github.com/binux/lixian.xunlei/blob/master/libs/tools.py
# Original Gist: https://gist.github.com/ihciah/30eda05ca36ee9f9f190067538b0ae04
# Github Repo: https://github.com/ihciah/subtitle

import hashlib
import os
import sys
import urllib3
import re
import logging
from urllib3.util import parse_url, Url
from subtitle import config
from subtitle.http_dns import dns_hijack
dns_hijack(http_dns=config.http_dns)


class SubtitleDownloader:
    @staticmethod
    def version():
        return u'VERSION %s.\n\r' \
               u'Subtitle downloader by ihciah >_< \n\r' \
               u'https://github.com/ihciah/subtitle' % config.__version__

    @staticmethod
    def url_get(url):
        url_part = parse_url(url)
        UrlObj = Url(url_part.scheme, url_part.auth, url_part.host, url_part.port,
                     url_part.path or None, url_part.query or None, url_part.fragment or None)
        conn = urllib3.connection_from_url(url)
        response = conn.request('GET', UrlObj.request_uri)
        return response

    @staticmethod
    def download_srt(subtitle_url, video_base_path, video_name, num):
        dot = subtitle_url.rfind(u'.')
        if dot < 0:
            return
        subtitle_type = subtitle_url[dot + 1:].lower()
        if subtitle_type not in config.subtitle_types:
            return
        srt_file = os.path.join(video_base_path, video_name + u'.%d.' % num + subtitle_type)
        if os.path.isfile(srt_file):
            return
        response = SubtitleDownloader.url_get(subtitle_url)
        if response.status == 200:
            with open(os.path.join(video_base_path, video_name + u'.%d.' % num + subtitle_type), 'wb') as f:
                f.write(response.data)

    @staticmethod
    def cid_hash_file(path):
        h = hashlib.sha1()
        size = os.path.getsize(path)
        with open(path, 'rb') as stream:
            if size < 0xF000:
                h.update(stream.read())
            else:
                h.update(stream.read(0x5000))
                stream.seek(size//3)
                h.update(stream.read(0x5000))
                stream.seek(size-0x5000)
                h.update(stream.read(0x5000))
        return h.hexdigest().upper()

    @staticmethod
    def fetch_subtitle_list(cid):
        patten = re.compile(b'surl="(.*?)"')
        url_base = u'http://subtitle.kankan.xunlei.com:8000/submatch/%s/%s/%s.lua'
        r = SubtitleDownloader.url_get(url_base % (cid[:2], cid[-2:], cid)).data
        srt_urls = patten.findall(r)[:config.download_count]
        return list(map(lambda url: url.decode(u'utf-8'), srt_urls))

    @staticmethod
    def download_subtitle(video):
        logging.info(u"Processing: {}".format(video))
        if not video:
            logging.error(u"Video file or dir does not exist: %s".format(video))
            return -1
        if os.path.isdir(video):
            if sys.version_info.major == 2:
                code = sys.getfilesystemencoding()
                map(lambda path: SubtitleDownloader.download_subtitle(os.path.join(video, path.decode(code))),
                    os.listdir(video))
            else:
                list(map(lambda path: SubtitleDownloader.download_subtitle(os.path.join(video, path)),
                         os.listdir(video)))
            return
        if not os.path.isfile(video):
            logging.error(u"Video file does not exist: {}".format(video))
            return -1
        video_base_path, video_filename = os.path.split(os.path.abspath(video))
        if not video_base_path or not video_filename:
            logging.error(u"Something error: {}".format(video))
            return -1
        dot = video_filename.rfind(u'.')
        if dot <= 0:
            logging.info(u"File doesn't have a suffix or without a name: {}".format(video_filename))
            return -1
        video_name = video_filename[:dot]
        video_type = video_filename[dot+1:]
        if video_type.lower() not in config.video_types:
            logging.info(u"Not a video file: {}".format(video_filename))
            return -2
        cid = SubtitleDownloader.cid_hash_file(video)
        subtitle_list = SubtitleDownloader.fetch_subtitle_list(cid)
        if not subtitle_list:
            logging.info(u"No subtitle available on the server.")
        else:
            logging.info(u"Fetching {} subtitles for: {}".format(len(subtitle_list), video_filename))
        for num, subtitle in enumerate(subtitle_list):
            SubtitleDownloader.download_srt(subtitle, video_base_path, video_name, num)
        logging.info(u"Done.")

    @staticmethod
    def inotify_loop(watch_dir):
        if not isinstance(watch_dir, bytes):
            watch_dir = str.encode(watch_dir)
        import inotify.adapters, inotify.constants
        try:
            i = inotify.adapters.InotifyTree(watch_dir, mask=inotify.constants.IN_DELETE)
            for event in i.event_gen():
                if event is not None:
                    try:
                        (header, type_names, watch_path, filename) = event
                        filename = filename.decode('utf-8')
                        watch_path = watch_path.decode('utf-8')
                        if 'IN_DELETE' in type_names and filename.endswith(u'.aria2'):
                            video_filename = filename[:filename.rfind(u'.')]  # But this maybe a folder!
                            SubtitleDownloader.download_subtitle(os.path.join(watch_path, video_filename))
                    except:
                        pass
        except:
            pass
