# coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
from models import WebUser
from models import Words
import hashlib
from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect

import OP_RETURN

from OP_RETURN import OP_RETURN_getnewaddress
from OP_RETURN import OP_RETURN_send
from OP_RETURN import OP_RETURN_getmessage

# Create your views here.
def regist(request):
    if request.method == 'GET':
        return render(request, 'web/Regist.html')
    elif request.method == 'POST':
        uname = request.POST['name']
        email = request.POST['email']
        passwd = request.POST['password']
        if uname == '' or email == '' or passwd == '':
            return HttpResponse('input erron')
        passwd = hashlib.sha1(str(passwd)).hexdigest()
        try:
            user = WebUser.objects.get(email=email)
            if user:
                return HttpResponse('error')
        except:
            try:
                addr = OP_RETURN_getnewaddress()
                user = WebUser()
                user.user_name = uname
                user.password = passwd
                user.email = email
                user.addr = addr
                user.save()
                request.session['username'] = user.user_name
                request.session['id'] = user.id
                return HttpResponseRedirect('/display')
            except:
                return HttpResponse("blockchain service is not running")



def login(request):
    try:
        id = request.session['id']
        return HttpResponseRedirect('/display')
    except:
        if request.method == 'GET':
            return render(request, 'web/Login.html')
        elif request.method == 'POST':
            email = request.POST['email']
            passwd = request.POST['password']
            passwd = hashlib.sha1(str(passwd)).hexdigest()
            print email
            print passwd
            try:
                user  = WebUser.objects.get(email=email)
                if user.password == passwd:
                    request.session['username'] = user.user_name
                    request.session['id'] = user.id
                    return HttpResponseRedirect('/display')
                else:
                    return HttpResponse('wrong passwd')
            except:
                return HttpResponse('error')



def input(request):
    if request.method == 'GET':
        return render(request, 'web/Input.html')
    elif request.method == 'POST':
        word = request.POST['word']
        id = request.session['id']
        addr = WebUser.objects.get(id = id).addr
        txid = OP_RETURN_send(addr, 0.001, word)
        try:
            w = Words()
            w.txid = txid['txid']
            w.user_id = id
            w.save()
            return HttpResponseRedirect('/display')
        except:
            return HttpResponse('blockchain error')


def display(request):
    try:
        words = Words.objects.filter(user_id=request.session['id'])
        user = request.session['username']
        words = {'user': user, 'words':words}
        return render(request, 'web/Display.html', words)
    except:
        return HttpResponseRedirect('/login')


def index(request):
    return render(request, 'web/Index.html')

def detail(request):
    txid = request.GET['txid']
    res = OP_RETURN_getmessage(txid)

    return HttpResponse(res)

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
