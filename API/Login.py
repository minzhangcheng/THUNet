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

import __future__
import json
import requests
import hashlib

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
    try:
        r = requests.post(url, parameters, timeout=timeout)
        content = r.text
        r.close()
    except Exception as e:
        print(e)
        return False
    if 'result' in conf:
        result = conf['result']
        if content in result['others']:
            return result['others'][content]
        elif 'default' in result:
            return result['default']
        else:
            return content
    else:
        return content


def _md5(text):
    h = hashlib.md5(text.encode())
    return h.hexdigest()


def login(username, password, hashed=False, timeout=0):
    if not hashed:
        password = '{MD5_HEX}%s' % _md5(password)
    else:
        password = '{MD5_HEX}%s' % password
    extra = {'username': username, 'password': password}
    return _post('login', extra, timeout=timeout)


def online(timeout=0):
    return _post('online', timeout=timeout)


def info(timeout=0, sep=','):
    rf = open(configFile, 'r')
    config = json.load(rf)
    rf.close()
    conf = config['info_parse']
    r = _post('info', timeout=timeout).split(conf['sep'])
    if len(r) != conf['length']:
        w = "Warning: result from Login.info is not compacat with set."
    username = r[conf['username']]
    lastTime = int(r[conf['time_end']]) - int(r[conf['time_begin']])
    ipAddress = r[conf['ip']]
    usage = int(r[conf['usage']])
    moneyRemain = float(r[conf['money_remain']])
    return {
        'username': username,
        'connected': lastTime,
        'ip': ipAddress,
        'usage': usage,
        'money': moneyRemain
    }


def logout(timeout=0):
    return _post('logout', timeout=timeout)
