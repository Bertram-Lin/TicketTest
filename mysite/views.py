from cgitb import enable
from email import message
from django.shortcuts import render
from mysite import models, forms
# _*_ encoding:utf-8_*_
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMessage, send_mail
import json
import urllib
from django.conf import settings
from django.shortcuts import render, redirect
# Create your views here.

# def index(request):
#     years = range(1960, 2021)
#     urfcolor = request.GET.getlist('fcolor')
#     try:
#         urid = request.GET['user_id']
#         urpass = request.GET['user_pass']
#     except:
#         urid = None
#     if urid != None and urpass == '123456':
#         verified = True
#     else:
#         verified = False
#     return render(request, 'index.html', locals())

def index(request, pid=None, del_pass=None):
    posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:30]
    moods = models.Mood.objects.all()
    try:
        user_id = request.GET['user_id']
        user_pass = request.GET['user_pass']
        user_post = request.GET['user_post']
        user_mood = request.GET['mood']
    except:
        user_id = None
        message = '如要張貼訊息，則每一個欄位都要填...'

    if del_pass and pid:
        try:
            post = models.Post.objects.get(id=pid)
        except:
            post = None
        if post:
            if post.del_pass == del_pass:
                post.delete()
                message = "資料刪除成功"
            else:
                message = "密碼錯誤"
    elif user_id != None:
        mood = models.Mood.objects.get(status=user_mood)
        post = models.Post.objects.create(mood=mood, nickname=user_id, del_pass=user_pass, message=user_post)
        post.save()
        message = '成功儲存!請記得你的編輯密碼[{}]!,訊息需經審查後才會顯示。'.format(user_pass)

    return render(request, 'index.html', locals())

def listing(request):
    posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:150]
    moods = models.Mood.objects.all()
    return render(request, 'listing.html', locals())

def posting(request):
    moods = models.Mood.objects.all()
    try:
        user_id = request.POST['user_id']
        user_pass = request.POST['user_pass']
        user_post = request.POST['user_post']
        user_mood = request.POST['mood']
    except:
        user_id = None
        message = '如要張貼訊息，則每一個欄位都要填...'

    # if del_pass and pid:
    #     try:
    #         post = models.Post.objects.get(id=pid)
    #     except:
    #         post = None
    #     if post:
    #         if post.del_pass == del_pass:
    #             post.delete()
    #             message = "資料刪除成功"
    #         else:
    #             message = "密碼錯誤"
    if user_id != None:
        mood = models.Mood.objects.get(status=user_mood)
        post = models.Post.objects.create(mood=mood, nickname=user_id, del_pass=user_pass, message=user_post)
        post.save()
        message = '成功儲存!請記得你的編輯密碼[{}]!,訊息需經審查後才會顯示。'.format(user_pass)
    return render(request, 'posting.html', locals())

def contact(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            message = '感謝您的來信。'



            user_name = form.cleaned_data['user_name']
            user_city = form.cleaned_data['user_city']
            user_school = form.cleaned_data['user_school']
            user_email = form.cleaned_data['user_email']
            user_message = form.cleaned_data['user_message']


          
            mail_body = u'''
網友姓名：{}
居住城市：{}
是否在學：{}
反應意見：如下
{}'''.format(user_name, user_city, user_school, user_message)
            send_mail("來自【不吐不快】網站的網友意見", 
                    mail_body,
                    user_email, 
                    ['t105568004@ntut.org.tw'])
            # email = EmailMessage( '來自【不吐不快】網站的網友意見',
            #                     mail_body,
            #                     user_email,
            #                     ['t105568004@ntut.org.tw'])
        else:
            message = '請檢查您輸入的資訊是否正確!'
    else:
        form = forms.ContactForm()

    return render(request, 'contact.html', locals())

def post2db(request):
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            if result['success']:
                message = '您的訊息已儲存，要等管理者啟用後才看得到喔。'
                post_form.save()
                return HttpResponseRedirect('/list/')
            else:
                message = 'reCAPTCHA驗證失敗，請在確認.'
        else:
            message = '如要張貼訊息，則每一個欄位都要填...'
    else:
        post_form = forms.PostForm()
        # moods = models.Mood.objects.all()
        message = '如要張貼訊息，則每一個欄位都要填...'
    return render(request, 'post2db.html', locals())


def login(request):
    try:
        user_id = request.GET['user_id']
        user_pass = request.GET['user_pass']
    except:
        user_id = None
        message = '請輸入帳密!'
    if user_id != None:
        try:
            login_check = models.login.objects.get(user_id=user_id)
            if login_check.password == user_pass:
                message = "帳密正確"
                Role = str(login_check.PermissionRole)
                request.session['PermissionRole'] = Role
                return HttpResponseRedirect('/ticket_list/')
            else:
                message = "密碼錯誤"
        except:
            message = '帳號不存在'

    return render(request, 'login.html', locals())

def ticket_list(request):
    PermissionRole = request.session['PermissionRole']
    tickets = models.ticket.objects.order_by('-tid')
    return render(request, 'ticket_list.html', locals())

def ticket_edit(request, tid):
    PermissionRole = request.session['PermissionRole']
    if request.method == 'POST':
        tid = request.POST['tid']
        if PermissionRole == 'QA':
            Summary = request.POST['Summary']
            description = request.POST['description']
        elif PermissionRole == 'RD':
            isResolve = request.POST['isResolve']
        elif PermissionRole == 'PM':
            severity = request.POST['severity']   
            priority = request.POST['priority']

        #try:
        edit_obj = models.ticket.objects.filter(tid=tid).first()
        if edit_obj != None:
            if PermissionRole == 'QA':
                edit_obj.Summary = Summary
                edit_obj.Description = description
            elif PermissionRole == 'RD':
                edit_obj.isResolve = isResolve
            elif PermissionRole == 'PM':
                if severity != '':
                    if severity == '不嚴重':
                        severity_id = 1
                    elif severity == '嚴重':
                        severity_id = 2
                    edit_obj.Severity_id = severity_id
                if priority != '':
                    if priority == '不急':
                        priority_id = 1
                    elif priority == '緊急':
                        priority_id = 2
                    edit_obj.Priority_id = priority_id
            edit_obj.save()
        return HttpResponseRedirect('/ticket_list')
        # except:
        #     return redirect('/')
    else:
        PermissionRole = request.session['PermissionRole']
        isRD = ""
        isPM = ""
        if PermissionRole == 'RD':
            isRD = "disabled"
        elif PermissionRole == 'PM':
            isPM = "disabled"
        try:
            tid = tid
            severitys = models.Severitys.objects.all
            prioritys = models.Prioritys.objects.all
            ticket_data = models.ticket.objects.get(tid = tid)
            severity = str(ticket_data.Severity)
            priority = str(ticket_data.Priority)
            if ticket_data != None:
                return render(request, 'ticket_edit.html', locals())
        except:
            return redirect('/')

def ticket_add(request):
    if request.method == 'POST':
        Summary = request.POST['Summary']
        Description = request.POST['description']
        ticket = models.ticket.objects.create(Summary=Summary, Description=Description)
        ticket.save()
        return HttpResponseRedirect('/ticket_list')
    else:
        severitys = models.Severitys.objects.all
        prioritys = models.Prioritys.objects.all
        return render(request, 'ticket_add.html', locals())

def ticket_delete(request, del_id):
    del_obj = models.ticket.objects.filter(tid=del_id).first()
    del_obj.delete()
    return HttpResponseRedirect('/ticket_list')