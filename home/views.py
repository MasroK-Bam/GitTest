from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home/index.html')

from .models import movie








#여기부턴 로그인






from django.shortcuts import render
from django.views.generic import View
from .models import Member
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# Create your views here.
from hashlib import sha512
from hashlib import md5
import os, sys
import hashlib
 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def index(request):
    return render(request, 'home/home.html')


class Join(View):
    def get(self,request):
        return render(request, 'home/join.html')

    def post(self,request):
        
        userid = request.POST.get('userid')
        userpw = request.POST.get('userpw')
        userpw2 = request.POST.get('userpw2')
        username = request.POST.get('username')
        birth = request.POST.get('birth')
        userphone = request.POST.get('userphone')
        useremail = request.POST.get('useremail')
        try:
            if len(Member.objects.filter(userid=userid)) != 0:
                msg = '이미 사용중인 ID입니다'  # 팝업 메시지
                page = '/join/'              # 이동할 대상 페이지
            elif userpw == userpw2:
                nb = Member()
                nb.userid = userid
                nb.userpw = getHash(userid, userpw)
                nb.username = username
                nb.birth = birth
                nb.phonenum = userphone
                nb.useremail = useremail
                nb.save()
                request.session['userid'] = nb.userid
                request.session['username'] = nb.username
                msg = '회원가입을 축하합니다'  # 팝업 메시지
                page = '/'                    # 이동할 대상 페이지
            else:
                msg = '비밀번호가 일치하지 않습니다'  # 팝업 메시지
                page = '/join/'                    # 이동할 대상 페이지
            
        except Member.DoesNotExist:
            pass

        jsres = '<script>alert("{}");location.href="{}";</script>'.format(msg, page)
        return HttpResponse(jsres)

class Login(View):
    def get(self,request):
        return render(request, 'home/login.html')

    def post(self,request):
        userid = request.POST.get('userid')
        userpw = request.POST.get('userpw')
        try:
            q = Member.objects.get(userid=userid)
            #if q.userpw == userpw:
            if q.userpw == getHash(userid, userpw):
                request.session['userid'] = q.userid
                request.session['username'] = q.username
                msg = "{}님, 환영합니다.".format(userid)
                jsres = '<script>alert("{}");location.href="/";</script>'.format(msg)
                return HttpResponse(jsres)
            else:
                msg = '비밀번호가 일치하지 않습니다'  # 팝업 메시지
                page = '/login/'                    # 이동할 대상 페이지
        
        except Member.DoesNotExist:
            # 출력할 팝업 메시지
            msg = '계정을 찾을 수 없습니다'
            page = '/login/'    # 이동할 대상 페이지

        jsres = '<script>alert("{}");location.href="{}";</script>'.format(msg, page)
        return HttpResponse(jsres)

def getHash(userid, userpw):
    enc = md5()
    enc.update(userid.encode('utf-8'))
    salt = enc.hexdigest()
    salt = '$6$' + salt[:6] + '$'
    hashValue = salt + sha512(str(userpw).encode('utf-8')).hexdigest()
    return hashValue

class ChangePassword(View):
    def get(self,request):
        return render(request, 'home/changePassword.html')

    def post(self, request):
        oldpw = request.POST.get('oldpw')
        newpw1 = request.POST.get('newpw1')
        newpw2 = request.POST.get('newpw2')
        userid = request.session.get('userid')

        try:
            user = Member.objects.get(userid=userid)
            if getHash(userid, oldpw) == user.userpw:
                if newpw1 == newpw2:
                    user.userpw = getHash(userid, newpw1)
                    user.save()
                    msg = '비밀번호가 정상적으로 변경되었습니다'
                    page = '/'
                else:
                    msg = '신규 비밀번호가 일치하지 않습니다'
                    page = '/changePassword/'
            else:
                msg = '기존 비밀번호가 일치하지 않습니다'
                page = '/changePassword/'
        except Member.DoesNotExist:
            msg = '잘못된 접근입니다'  # 팝업 메시지
            page = '/'                    # 이동할 대상 페이지

        jsres = '<script>alert("{}");location.href="{}";</script>'.format(msg, page)
        return HttpResponse(jsres)

def logout(request):
    msg = '{}님 로그아웃 되었습니다'.format(request.session['userid'])
    page = '/'
    jsres = '<script>alert("{}");location.href="{}";</script>'.format(msg, page)
    del request.session['userid']
    del request.session['username']
    return HttpResponse(jsres)

class MyInfo(View):
    def get(self, request):
        
        userid = request.session.get('userid')
    
        if userid is None:
            msg = '잘못된 접근입니다'  # 팝업 메시지
            page = '/'                # 이동할 대상 페이지
            jsres = '<script>alert("{}");location.href="{}";</script>'.format(msg, page)
            return HttpResponse(jsres)
        

        return render(request, 'home/myinfo.html')






# 여기부턴 리뷰 페이지





from .models import Review

def reviewlist(request):
    return render(request, 'home/reviewlist.html')

def reviewpage(request, pk):
    query = Review.objects.get(pk=pk)
    context = {
        'query' : query,
    }

    return render(request, 'home/reviewpage.html', context)
    
class Newwrite(View):
    def get(self, request, code):
        context = {
            'code' :code,
        }
        return render(request, 'home/newwrite.html', context)

    def post(self, request, code):
        print("POST")
        writer = request.POST.get('writer')
        post_title = request.POST.get('post_title')
        post_contents = request.POST.get('post_contents')

        n = Review()
        n.category=code
        n.writer=writer
        n.post_title=post_title
        n.post_contents=post_contents

        n.save()

        return HttpResponseRedirect('/review/' + str(code))


def review(request, param):
    page = int(request.GET.get('page', 1))
    qs=Review.objects.filter(category=param)
    # Review.category = param
    # category = Review.category
    perPage = 10                            
    totalCnt = qs.count()    
    category=param

    pageCnt = (totalCnt // perPage)                 
    add = totalCnt % perPage != 0 and 1 or 0       
    pageCnt += add
    startId = perPage * (page - 1)     
    endId = perPage * page 
    qs = qs.order_by('-id')[startId:endId]

    print('{} ~ {}'.format(startId, endId))

    context={
        'movie' : movie.objects.get(movie_code=param),
        'qs': qs,
        'startId':startId,
        'endId':endId,
        'page' : page,
        'pageList' : [i for i in range(1, pageCnt + 1)],
        'category' : category,
    }
    
    return render(request, 'home/review.html',context)
    