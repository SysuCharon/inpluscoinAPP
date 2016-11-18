# -*- coding: utf-8 -*-
# from django.http import HttpResponse
from django.template import RequestContext, Template
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str, smart_unicode

from django.shortcuts import render
from django.http import HttpResponse
import json
import time
import datetime
import OP_RETURN

from OP_RETURN import OP_RETURN_getnewaddress
from OP_RETURN import OP_RETURN_send
from OP_RETURN import OP_RETURN_getmessage

from .models import User, Content
from django.core.exceptions import ObjectDoesNotExist

import xml.etree.ElementTree as ET
import urllib,urllib2,time,hashlib,re


@csrf_exempt
def handleRequest(request):
  if request.META.has_key('HTTP_X_FORWARDED_FOR'):
    ip = request.META['HTTP_X_FORWARDED_FOR']
  else:
    ip = request.META['REMOTE_ADDR']
  print ip
  if request.method == 'GET':
    response = HttpResponse(checkSignature(request),content_type="text/plain")
    return response
  elif request.method == 'POST':
    response = HttpResponse(responseMsg(request),content_type="application/xml")
    return response
  else:
    return None

def checkSignature(request):
  signature = request.GET.get("signature", None)
  timestamp = request.GET.get("timestamp", None)
  nonce = request.GET.get("nonce", None)
  echoStr = request.GET.get("echostr",None)

  token = "inlab"
  hashlist = [token, timestamp, nonce]
  hashlist.sort()

  hashstr = ''.join([s for s in hashlist])

  hashstr = hashlib.sha1(hashstr).hexdigest()

  if hashstr == signature:
    return echoStr
  else:
    return None

submenu = {}

menustr = '回复1：进入注册\n回复2：新增誓言\n回复3：查看誓言列表'
menu1 = '回复1：确认注册\n回复0：返回主菜单'
menu2 = '回复誓言内容发誓\n回复0：返回主菜单'
menu3 = '回复对应誓言数字查看具体誓言\n回复0：返回主菜单'
blockchain_error = '区块链错误\n回复0：返回主菜单'
regist_error = '您尚未注册\n请按照提示注册'
def responseMsg(request):
  print request.body
  str_xml = ET.fromstring(request.body)

  toUser = str_xml.find('ToUserName').text
  fromUser = str_xml.find('FromUserName').text  #用户openid
  msgType = str_xml.find('MsgType').text
  nowtime = str(int(time.time()))
  content = str_xml.find('Content').text


  if msgType == 'text':
    if submenu.has_key(fromUser):
      if submenu[fromUser] == 1:
        replyContent = submenu1(fromUser, content)

      elif submenu[fromUser] == 2:
        replyContent = submenu2(fromUser, content)

      elif submenu[fromUser] == 3:
        replyContent = submenu3(fromUser, content)
    else:
      replyContent = menu(fromUser, content)
      
  else:
    replyContent = '不支持非文本格式输入'
  resMsgType = 'text'

  responseContent = wechatXML(fromUser,toUser,nowtime,resMsgType,replyContent)
  return responseContent

def menu(fromUser, content):
  if content == '1':
    replyContent = menu1
    submenu[fromUser] = 1
  elif content == '2':
    replyContent = menu2
    submenu[fromUser] = 2
  elif content == '3':
    try:
      user = User.objects.get(openID=fromUser)
      txids = Content.objects.filter(user = user.id)
      count = txids.count()
    except:
      replyContent = regist_error
    else:
      if count == 0:
        replyContent = '您未发誓'
      else:
        i = 1
        for item in txids:
          string =  str(i) + ' ' + item + '\n'
          i += 1
        replyContent = '序号 誓言在区块链上的位置' + string + menu3
        submenu[fromUser] = 3
  else:
    replyContent = '回复错误\n' + menustr

  return replyContent

def submenu1(fromUser, content):
  if content == '1':
    try:
      user = User.objects.get(openID=fromUser)
    except:
      try:
        address = OP_RETURN_getnewaddress()
      except:
        replyContent = blockchain_error
      else:
        addUser(fromUser, address)
        replyContent = '注册成功\n您在区块链上的地址为\n' + address
    else:
      replyContent = '您已注册\n回复0：返回主菜单'
  elif content == '0':
    replyContent = menustr
    del submenu[fromUser]
  else:
    replyContent = '回复错误\n' + menu1

  return replyContent

def submenu2(fromUser, content):
  if content == '0':
    replyContent = menustr
  else:
    try:
      user = User.objects.get(openID=fromUser)
    except:
      replyContent = regist_error
    else:
      address = getAddrByOpenID(fromUser)
      txid = OP_RETURN_send(address, 0.001, content)
      if txid.has_key('txid'):
        addContent(address, txid['txid'])
        replyContent = '发誓成功\n' + menustr
      else:
        replyContent = blockchain_error
  del submenu[fromUser]

  return replyContent

def submenu3(fromUser, content):
  if content == '0':
    replyContent = menustr
    del submenu[fromUser]
  else:
    try:
      txid = getTxid(fromUser, content)
    except:
      replyContent = '输入错误，不存在的id，请重新输入'
    else:
      try:
        text = OP_RETURN_getmessage(txid)
      except:
        replyContent = blockchain_error
      else:
        replyContent = text
  return replyContent

def wechatXML(fromUser, toUser, nowtime, msgType, replyContent):
  extTpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content></xml>";
  extTpl = extTpl % (fromUser,toUser,nowtime,msgType,replyContent)
  return extTpl

def addUser(openID, address):
    user = User()
    user.openID = openID
    user.address = address
    user.save()

def addContent(openID, txid):
    c = Content()
    user = User.objects.get(openID = openID)
    c.user = user
    c.count = Content.objects.filter(user = user.id).count() + 1
    c.txid = txid
    c.save()

def getAddrByOpenID(openID):
    return User.objects.get(openID = openID).address

def getTxid(openID, count):
  user = User.objects.get(openID = openID).id
  return Content.objects.get(user = user, count = count).txid

def getCount(openID):
    user = User.objects.get(openID = openID)
    return Content.objects.filter(user = user.id).count()



# Create your views here.

# 你需要在你的代码中引用import OP_RETURN 才能使用下面的接口！！！
# 同时这个接口目前来说只能在嘉辉电脑上运行！！！
# 1.OP_RETURN_getnewaddress() 返回address
# 只有在用户注册的时候需要调用，返回是一个字符串，记得在数据库中把这个跟用户原来的id进行一一匹配
#
#
# 2.OP_RETURN_send('LR62fFecG9j5Y1HfqxTWZ9CMqwHt3GcBu7', 0.001, "这是测试语句")  返回txid
#
# 你需要在你的代码中限制用户输入字数最多60个中文字，120个英文字母
#
#
# 3.OP_RETURN_getmessage(txid) 返回信息



def Main(request):
    return render(request,'wx/web.html')


def fun1():
    new_addr = OP_RETURN_getnewaddress()
    return new_addr


def fun2(addr):
    txid = OP_RETURN_send(addr, 0.001, "for test")
    return txid


def fun3(txid):
    msg = OP_RETURN_getmessage(txid)
    return msg

openID = 0

def Test(request):
    sid = request.GET['sid']
    # print sid
    start_time = datetime.datetime.now()
	# print 'enter'
    sid = str(sid)
    res = {}

    # print '1'
 
    if sid == str(1):
    	# print '1'
        addr = fun1()	
        addUser('temp1', '4', addr)
    elif sid == str(2):
    	# print '2'
        addr = getAddrByOpenID('4')
        print addr
        txid = fun2(addr)
        print txid

        addContent('4', txid['txid'])
        # res['addr'] = addr
        # res['txid'] = txid['txid']
    elif sid == str(3):
    	# print '3'
        # txid = fun2(addr)
        # msg  = fun3(txid['txid'])

        # user = User()

        # openID = 0
        # user.name = 'test' + str(openID)
        # user.openID = openID
        # user.address = addr
        # openID += 1

        # user.save()

        addr = getAddrByOpenID('4')
        user = User.objects.get(openID = '4').id
        # print user

        count = Content.objects.filter(user = user).count()
        txid = getTxid('4', count)
        print fun3(txid)
        # c = Content()
        # temp = User.objects.get(openID=0)
        # c.user = temp
        # c.txid = txid
        # c.save()
        # print temp.name
        # print temp.id


    end_time = datetime.datetime.now()
    cost_time = end_time - start_time
    res['time'] = cost_time.total_seconds()
    # print txid
    # date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return HttpResponse(json.dumps(res), content_type = 'aplication/json')
    

