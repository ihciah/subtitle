#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

__author__ = u'ihciah'
__version__ = u'2.3'
__email__ = u'ihciah@gmail.com'
video_types = [u'mkv', u'mp4', u'avi', u'rm', u'rmvb', u'wmv', u'webm', u'mpeg', u'mpe', u'flv', u'3gp', u'mov']
subtitle_types = [u'ass', u'srt', u'sub', u'sst', u'son', u'ssa', u'smi', u'tts', u'psb', u'pjs', u'stl', u'vsf']
download_count = 3

http_dns = os.environ.get('SUBTITLE_HTTP_DNS') # can be one of 'dnspod', 'cf', 'cloudflare', or leave it None
if http_dns not in ('dnspod', 'cf', 'cloudflare'):
    http_dns = None

