# ############################################################################
#
# Copyright (C) 2016 Minzhang Cheng
# Contact: minzhangcheng@gmail.com
#
# GNU Lesser General Public License Usage
# This file may be used under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation and
# appearing in the file LICENSE included in the packaging of this file.
# Please review the following information to ensure the GNU Lesser
# General Public License version 3 requirements will be met:
# http://www.gnu.org/licenses/gpl-3.0.html
#
# ############################################################################

import __future__
import hashlib
import json
import requests

configFile = '/Users/minzhang/Coding/THUNet/API/Usereg.json'


def _md5(text):
    h = hashlib.md5(text)
    return h.hexdigest()


def _getCookies(username, password, hashed=False, timeout=0):
    rf = open(configFile, 'r')
    config = json.load(rf)
    rf.close()
    conf = config['cookies']
    url = conf['url']
    parameters = conf['parameters']['fixed']
    if not hashed:
        password = '{MD5_HEX}%s' % _md5(password)
    extraParameters = {'username': username, 'password': password}
    if not timeout:
        timeout = config['timeout']
    for i in extraParameters:
        if i in conf['parameters']['variable']:
            parameters.setdefault(conf['parameters']['variable'][i],
                                  extraParameters[i])
    try:
        r = requests.post(url, parameters, timeout=timeout)
        cookies = r.cookies
        r.close()
    except Exception as e:
        print(e)
        return False
    return cookies


def _userParse(text):
    pass


def user(cookies, timeout=0):
    return


def _onlineParse(text):
    pass


def online(cookies, timeout=0):
    return


def loginIP(cookies, ip, timeout=0):
    return


def dropIP(cookies, id, timeout=0):
    return