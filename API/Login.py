# ############################################################################
#
# Copyright (C) 2015 Minzhang Cheng
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

from __future__ import *
import hashlib
import json
import requests

configFile = 'Login.json'


def _post(key, extraParameters={}, timeout=0):
    rf = open(configFile, 'r')
    config = json.load(rf)
    rf.close()
    conf = config[key]
    url = conf['url']
    parameters = conf['parameters']['fixed']
    if not timeout:
        timeout = config['timeout']
    for i in extraParameters:
        if i in conf['parameters']['variable']:
            parameters.setdefault(conf['parameters']['variable'][i],
                                  extraParameters[i])
    result = conf['result']
    try:
        r = requests.post(url, parameters, timeout=timeout)
        content = r.text
        r.close()
    except Exception as e:
        print(e)
        return False
    if content in result['others']:
        return result['others'][content]
    elif result['default']:
        return result['default']
    else:
        return content


def _md5(text):
    h = hashlib.md5(text)
    return h.hexdigest()


def login(username, password, hashed=False, timeout=0):
    if not hashed:
        password = '{MD5_HEX}%s' % _md5(password)
    extra = {'username': username, 'password': password}
    return _post('login', extra, timeout=timeout)


def check(timeout=0):
    return _post('check', timeout=timeout)


def logout(timeout=0):
    _post('logout', timeout=timeout)
    return not check(timeout=timeout)