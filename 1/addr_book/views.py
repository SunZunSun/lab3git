from django.shortcuts import render, render_to_response
from django.template import Context
from addr_book.models import Author,Book
from django.contrib.auth.models import User
from django.contrib import auth
import re
# Create your views here.
from django.http import HttpResponse
def create(request):
    if request.POST:
        post = request.POST
        if post['code']==post['code2']:
            name =request.POST['name']
            code =request.POST['code']
            try:
                user = User.objects.create_user(username=name,password=code)
                user.save()
            except:
                return render_to_response("register.html",{'judge':True,'judge2':False,})
        else:
            error = Context({'judge':False,'judge2':True,})
            return render_to_response("register.html",error)
    mind = Context({'judge':True,'judge2':True,})
    return render_to_response("register.html",mind)
def login(request):
    if request.POST:
        post=request.POST
        user = auth.authenticate(username=post['name'], password=post['code'])
        if user is not None and user.is_active:
            auth.login(request,user)
            return render_to_response("start.html",{"name":post["name"],})
        else:
            return render_to_response("login.html",{"judge":False})
    return render_to_response("login.html",{"judge":True})
def change(request):
    if request.POST:
        post = request.POST
        if post['code']==post['code2']:
            user = auth.authenticate(username=post['name'], password=post['oldcode'])
        else:
            return render_to_response("change.html",{'judge':True,'judge2':False,})
        if user is not None:
            user.set_password(post['code'])
            user.save()
        else:
            error = Context({'judge':False,'judge2':True,})
            return render_to_response("change.html",error)
    mind = Context({'judge':True,'judge2':True,})
    return render_to_response("change.html",mind)
def hello(request):
    return render_to_response("book_home.html")
def logout(request):
    auth.logout(request)
    return render_to_response("home.html")
def people_list(request):
    if not request.user:
        return render_to_response("home.html")
    if request.POST:
        error = False
        if re.search(r'[^\d]',request.POST['number']) or re.search(r'[^\d]',request.POST['phone']) :
            error = True
        if re.search(r'[^\d]',request.POST['year']) or re.search(r'[^\d]',request.POST['month']) or re.search(r'[^\d]',request.POST['day']) :
            error = True
        try:
            if not error:
                post = request.POST
                if post['name']=="" or post['number']=='' or post['year']=='' or post['month']=='' or post['day']=='':
                    return render_to_response("list.html",{'judge':False,})
                new_people = People(
                    user = request.user,
                    name = post["name"],
                    school_number = post["number"],
                    phone = post["phone"],
                    email = post["email"],
                    year = post["year"],
                    month = post["month"],
                    day = post["day"],
                    QQ = post["QQ"],
                    address = post["address"])    
                if post["sex"] == 'M':
                    new_people.sex = True
                else:
                    new_people.sex = False       
                new_people.save()
            else:
                return render_to_response("list.html",{'judge':False,})
        except:
            return render_to_response("list.html",{'judge':False,})
    return render_to_response("list.html",{'judge':True,})
   
def see_our_list(request):
    if not request.user:
        return render_to_response("home.html")
    people_list = People.objects.filter(user=request.user)
    c = Context({"people_list":people_list,})   
    return render_to_response("list2.html", c)
def delete(request):
    if not request.user:
        return render_to_response("home.html")
    if request.GET:
        it = People.objects.filter(user=request.user,school_number = request.GET["id"])
        it.delete()
        people_list = People.objects.filter(user=request.user)
        c = Context({"people_list":people_list,})   
        return render_to_response("list2.html", c)
def update(request):
    if not request.user:
        return render_to_response("home.html")
    if request.GET:
        id = request.GET["id"]
        it = People.objects.get(user=request.user,school_number = id)
        if request.POST:
            if re.search(r'[^\d]',request.POST['number']) or re.search(r'[^\d]',request.POST['phone']):
                return render_to_response("update.html",{"it":it,"judge":False,})
            if re.search(r'[^\d]',request.POST['year']) or re.search(r'[^\d]',request.POST['month']) or re.search(r'[^\d]',request.POST['day']):
                return render_to_response("update.html",{"it":it,"judge":False,})
            try:
                post = request.POST
                if post['name']=="" or post['number']=='' or post['year']=='' or post['month']=='' or post['day']=='':
                    return render_to_response("update.html",{"it":it,"judge":False,})
                new_people = People(
                    user = request.user,
                    name = post["name"],
                    school_number = post["number"],
                    phone = post["phone"],
                    email = post["email"],
                    year = post["year"],
                    month = post["month"],
                    day = post["day"],
                    QQ = post["QQ"],
                    address = post["address"]) 
                if post["sex"] == 'M':
                    new_people.sex = True
                else:
                    new_people.sex = False       
                new_people.save()
                it.delete()
                return render_to_response("update2.html")
            except:
                return render_to_response("update.html",{"it":it,"judge":False,})
        return render_to_response("update.html",{"it":it,"judge":True,})
def query(request):
    if not request.user:
        return render_to_response("home.html")
    if request.POST:
        try:
            post = request.POST
            query_name = post["query_name"]
            people_list = People.objects.filter(user=request.user,name__icontains = query_name)
            imit = Context({"people_list":people_list,})
            return render_to_response("list2.html",imit)
        except:
            return HttpResponse("Not Found")
    return render_to_response("query.html")

def book_add(request):
    if request.POST:
        try:
            post = request.POST
            pattern = re.compile('[\d]+\.[\d]+')
            error_1 = (post['name']=='')
            error_2 = (post['owner']=='')
            error_3 = (post['price']=='') or not pattern.match(post['price'])
            error_4 = (post['ISBN']=='')
            pub_date=post["selYear"]+'-'+post["selMonth"]+'-'+post["selDay"]
            owner = Author.objects.filter(name=post['owner'])
            try:
                own = owner[0]
                error_5 = False
            except:
                error_5 = True
            error = Context({"error_1":error_1,
                             "error_2":error_2,
                             "error_3":error_3,
                             "error_4":error_4,
                             "error_5":error_5,})
            if error_1 or error_2 or error_3 or error_4 or error_5:
                return render_to_response('book_add.html',error)
            else:
                new_book = Book(name = post['name'],
                                owner = own,
                                price = post['price'],
                                pub_house = post['pub_house'],
                                pub_date = pub_date,
                                ISBN = post['ISBN'])
                new_book.save()
                return render_to_response('book_add.html',error)
        except:
            error = Context({"error_1":True,
                             "error_2":True,
                             "error_3":False,
                             "error_4":False,
                             "error_5":False,})
            return render_to_response('book_add.html',error)
    error = Context({"error_1":False,
                     "error_2":False,
                     "error_3":False,
                     "error_4":False,
                     "error_5":False,})
    return render_to_response('book_add.html',error)
def author_add(request):
    if request.POST:
        error = False
        if re.search(r'[^\d]',request.POST['year']):
            error = True
        try:
            if not error:
                post = request.POST
                if post['name']=="" or post['year']=='' or post['ID']=='':
                    return render_to_response("author_add.html",{'judge':False,})
                new_people = Author(
                    name = post["name"],
                    Age = post["year"],
                    Author_ID = post['ID'],
                    Country = post["Country"],
                    sex = True)    
                if post["sex"] == 'M':
                    new_people.sex = True
                else:
                    new_people.sex = False       
                new_people.save()
            else:
                return render_to_response("author_add.html",{'judge':False,})
        except:
            return render_to_response("author_add.html",{'judge':False,})
    return render_to_response("author_add.html",{'judge':True,})
def book_query_auth(request):
    if request.GET:
        get = request.GET
        my_owner = Author.objects.filter(name__icontains = get["query_name"])
        book_list = Book.objects.all()
        book_set = []
        for author in my_owner:
            book_set.append([author,book_list.filter(owner = author)])
        imit = Context({"book_set":book_set,})
        return render_to_response("book_query_auth.html",imit)
    return render_to_response("book_query_auth.html")
def see_book(request):
    if request.GET:
        it = request.GET["book_name"]
        m_book = Book.objects.get(name = it)
        return render_to_response("book_see.html",{'m_book':m_book,})
def book_delete(request):
    if request.GET:
        m_name = request.GET["d_name"]
        m_book = Book.objects.filter(name = m_name)
        m_book.delete()
        return render_to_response("delete.html")
def book_update(request):
    if request.GET:
        book_name = request.GET["u_name"]
        it = Book.objects.get(name = book_name)
        m_date = ["2015","10","30"]
        m_date= it.pub_date.split("-")
        if request.POST:
            try:
                post = request.POST
                pattern = re.compile('[\d]+\.[\d]+')
                error_1 = (post['name']=='')
                error_2 = (post['owner']=='')
                error_3 = (post['price']=='') or not pattern.match(post['price'])
                error_4 = (post['ISBN']=='')
                pub_date=post["selYear"]+'-'+post["selMonth"]+'-'+post["selDay"]
                owner = Author.objects.filter(name=post['owner'])
                try:
                    own = owner[0]
                    error_5 = False
                except:
                    error_5 = True
                error = Context({"error_1":error_1,
                                 "error_2":error_2,
                                 "error_3":error_3,
                                 "error_4":error_4,
                                 "error_5":error_5,
                                 "success":not(error_1 or error_2 or error_3 or error_4 or error_5),
                                 "it":it,"it_year":m_date[0],"it_month":m_date[1],"it_day":m_date[2],})
                if error_1 or error_2 or error_3 or error_4 or error_5:
                    return render_to_response('book_update.html',error)
                else:
                    new_book = Book(name = post['name'],
                                    owner = own,
                                    price = post['price'],
                                    pub_house = post['pub_house'],
                                    pub_date = pub_date,
                                    ISBN = post['ISBN'])
                    new_book.save()
                    it.delete()
                    return render_to_response('book_update.html',error)
            except:
                error = Context({"error_1":True,
                                 "error_2":True,
                                 "error_3":False,
                                 "error_4":False,
                                 "error_5":False,
                                 "success":False,
                                 "it":it,"it_year":m_date[0],"it_month":m_date[1],"it_day":m_date[2],})
                return render_to_response('book_update.html',error)
        error = Context({"error_1":False,
                         "error_2":False,
                         "error_3":False,
                         "error_4":False,
                         "error_5":False,
                         "success":False,
                         "it":it,"it_year":m_date[0],"it_month":m_date[1],"it_day":m_date[2],})
        return render_to_response('book_update.html',error)
        
            