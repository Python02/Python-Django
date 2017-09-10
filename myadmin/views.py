from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import Users
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
import time,json
def index(request):
    return render(request,'myadmin/index.html')

def login(request):
	return render(request,'myadmin/login.html')

def verify(request):
	#引入随机函数模块
    import random
    from PIL import Image, ImageDraw, ImageFont
    #定义变量，用于画面的背景色、宽、高
    #bgcolor = (random.randrange(20, 100), random.randrange(
    #    20, 100),100)
    bgcolor = (242,164,247)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    #str1 = '0123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('static/STXIHEI.TTF', 21)
    #font = ImageFont.load_default().font
    #构造字体颜色
    fontcolor1 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor2 = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 0), rand_str[0], font=font, fill=fontcolor1)
    draw.text((25, 0), rand_str[1], font=font, fill=fontcolor2)
    draw.text((50, 0), rand_str[2], font=font, fill=fontcolor1)
    draw.text((75, 0), rand_str[3], font=font, fill=fontcolor2)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

def dologin(request):
	verifycode = request.session['verifycode']
	code = request.POST['code']
	if verifycode != code:
		context = {'info':'验证码错误!'}
		return render(request,"myadmin/login.html",context)
	try:
		user = Users.objects.get(username=request.POST['username'])
		if user.state == 0:
			#import hashlib
			#m = hashlib.md5()
			#m.update(bytes(request.POST['passa'],encoding="utf8"))
			if user.passa == request.POST['passa']:
				request.session['myadminuser'] = user.name
				return redirect(reverse('myadmin_index'))
			else:
				context = {'info':'登录密码错误!'}
		else:
			context = {'info':'此用户非后台管理用户!'}
	except:
		context = {'info':'登录账号错误!'}
	return render(request,"myadmin/login.html",context)

def logout(request):
	del request.session['myadminuser']
	return redirect(reverse('myadmin_login'))

def usersindex(request):
    list = Users.objects.all()
    context = {"userslist":list}
    return render(request,'myadmin/users/index.html',context)
def usersadd(request):
	return render(request,'myadmin/users/add.html')


def usersinsert(request):
	try:
		ob =Users()
		ob.username=request.POST['username']
		ob.name=request.POST['name']
		import hashlib
		m = hashlib.md5()
		m.update(bytes(request.POST['passa'],encoding="utf8"))
		ob.passa = m.hexdigest()
		ob.sex = request.POST['sex']
		ob.address = request.POST['address']
		ob.code = request.POST['code']
		ob.name = request.POST['phone']
		ob.email = request.POST['email']
		ob.state = 1
		ob.addtime = time.time()
		print(ob)
		ob.save()
		context = {'info':'添加成功'}
	except:
	 	context = {'info':'添加失败'}
	return render(request,"myadmin/users/info.html",context)

def usersdel(request,id):
	try:
		ob = Users.objects.get(id=id)
		ob.delete()
		context = {'info':'删除成功!'}
	except:
		context = {'info':'删除失败!'}
	return render(request,"myadmin/users/info.html",context)

def usersedit(request,id):
	try:
		ob = Users.objects.get(id=id)
		context = {'user':ob}
		return render(request,"myadmin/users/edit.html",context)
	except:
		context = {'info':'没有找到要修改的信息！'}
	return render(request,"myadmin/info.html",context)
	
def usersupdate(request,id):
	try:
		ob = Users.objects.get(id=id)
		ob.name = request.POST['name']
		ob.sex = request.POST['sex']
		ob.address = request.POST['address']
		ob.code = request.POST['code']
		ob.phone = request.POST['phone']
		ob.email = request.POST['email']
		ob.state = request.POST['state']
		ob.save()
		context = {'info':'修改成功！'}
	except:
		context = {'info':'修改失败！'}
	return render(request,"myadmin/users/info.html",context)
