# -*- encoding: utf-8 -*-

import urllib
import urllib2
from urllib import urlencode
import json
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

#to get access_token
appid = 'wx2a7aa3771cf62e4a'
secret = '57735b9cf4d44f710eaa662a983c2204'
getToken = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='
					+ appid + '&secret=' + secret
f = urllib2.urlopen(getToken)
getJson = f.read()
access_token = json.loads(getJson)['access_token']

#to create the menus
postUrl = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token='+ access_token

menus = '''{
	"button":[
	{
		"type":"click",
		"name":"发誓",
		"key":"PROMISE"
	},
	{
		"type":"click",
		"name":"回顾",
		"key":"RECALL"
	},
	{
		"name":"关于",
		"sub_button":[
		{
			"type":"click",
			"name":"功能介绍",
			"key":"INTRODUCTION"
		},
		{
			"type":"click",
			"name":"开发团队",
			"key":"TEAM"
		},
		{
			"type":"click",
			"name":"联系方式",
			"key":"CONTACT"
		}]
	}]
}'''

request = urllib2.urlopen(postUrl, menus.encode('utf-8'))
