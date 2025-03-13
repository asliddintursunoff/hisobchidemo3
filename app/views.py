from django.shortcuts import render,HttpResponse,redirect
from .forms import *
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .decorators import *
from .models import *
import json
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Value
from django.db.models.functions import Concat
from calendar import month_name
from django.db.models import Sum,F,Q
from .extra import *
from django.core.serializers.json import DjangoJSONEncoder
from datetime import date
from datetime import datetime
import datetime as dt
from .to_excel import *
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
now = datetime.now()

@admin_or_worker
def homepage(request):
    return render(request,"index.html")


@is_user_authenticated
def register(request):
    
   
    companyForm = CompanyForm()
    userCreationForm = UserCreation()
    workerCreationForm = UserCreationWorker() 
    CompanyCode = CompanyID()
    workerform= WorkerForm()
    if request.method=="POST":
        user_type = request.POST.get("user_type")
        if user_type == "admin":
            companyForm = CompanyForm(request.POST)
            userCreationForm = UserCreation(request.POST)

            if companyForm.is_valid() and userCreationForm.is_valid():
                try:
                    company = companyForm.save()
                    user = userCreationForm.save(commit=False)
                    user.company = company
                    user.save()

                    group = Group.objects.get(name="admin")
                    user.groups.add(group)

                    username = userCreationForm.cleaned_data["phone_number"]
                    password = userCreationForm.cleaned_data["password1"]
                    check = authenticate(request, phone_number=username, password=password)

                    if check is not None:
                        login(request, check)
                        messages.success(request, "Siz muvaffaqiyatli ro'yxatdan o'tdingiz!")
                        return redirect("adminpage")
                    else:
                        messages.error(request, "Noto‘g‘ri telefon raqam yoki parol. Qayta urinib ko’ring!")

                except IntegrityError:  # ✅ Handle duplicate phone number case
                    messages.error(request, "Bu telefon raqam allaqachon ro'yxatdan o'tgan!")
                    return redirect("register")

                except ValidationError as e:
                    messages.error(request, f"Xatolik: {str(e)}")
                    return redirect("register")

                except Exception:
                    messages.error(request, "Ro'yxatdan o'tishda xatolik yuz berdi. Qayta urinib ko’ring!")
                    return redirect("register")
        
            
        # elif user_type == "worker":   #it is for workers
        #     workerCreationForm = UserCreationWorker(request.POST) 
        #     CompanyCode = CompanyID(request.POST)
        #     workerform= WorkerForm(request.POST)
        #     if workerCreationForm.is_valid() and CompanyCode.is_valid() and workerform.is_valid():   
        #         company_id = CompanyCode.cleaned_data["code"]
        #         id = Company.objects.get(unique_id = company_id)
            
        #         if id is not None:        
        #             worker =  workerCreationForm.save(commit=False)
        #             worker.company = id
        #             worker.save()
        #             group = Group.objects.get(name = "worker")
        #             worker.groups.add(group)
        #             worker_name = workerform.cleaned_data["name"]
        #             worker_family = workerform.cleaned_data["last_name"]
        #             Worker.objects.create(user = worker,name = worker_name,last_name = worker_family,company = id )
                   
        #             username1 = workerCreationForm.cleaned_data["phone_number"]
        #             password1 = workerCreationForm.cleaned_data["password1"]
        #             checking = authenticate(request,username =username1 , password = password1 )
        #             if checking is not None:
        #                 login(request,checking)
        #                 return HttpResponse("registered")
        #             else:
        #                 return HttpResponse("something went wrong")
        #         else:
        #             return HttpResponse("error code")
           
        #     return HttpResponse("not valid")
            
            
            
    context = {
        "companyForm":companyForm,
        "userCreationForm": userCreationForm,
        "worker":workerCreationForm,
        "company": CompanyCode, 
        "workerform":workerform,       
    }
    return render(request, "register.html",context)


@is_user_authenticated
def userlogin(request):
    if request.method=="POST":
       
        username123 = request.POST.get("phone_number")
        password = request.POST.get("password")
        user = authenticate(request,phone_number = username123,password=password)
        if user is not None:
            login(request, user)
            gr = user.groups.first()
      
            if gr and gr.name == "admin":
                return redirect("adminpage")
            elif gr and gr.name == "worker":
                return redirect("homepage")
            else:
                messages.info(request, "Sizda bu sahifani ko'rish uchun ruhsat yo'q!")
                return redirect("login")
        else:
            messages.info(request,"Telefon raqam yoki parol noto'g'ri")
    return render(request, "login.html")


def userlogout(request):
    logout(request)
    return redirect("homepage")



@allowed_pages("admin")
def adminpagedates(request):
    
    company= request.user.company
    date_list = []
    dates = DateforProgress.objects.filter(company = company)
    date_list = [{"date": date , "types": Progresstype.objects.filter(date = date) ,"month":date.date.month,"year":date.date.year} for date in dates  ][::-1]
 
    context = {
        "dates":date_list
    }
    return render(request, "admin/adminpagedate.html", context)

@allowed_pages("admin")
def adminpagedates_add_date(request):
    company = request.user.company
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            year = data.get("year")
            month = data.get("month")
            copy_date_id = data.get("copy_value_id")
       
            new_type = data.get("productname")
            date_form = date(year=year,month=month,day=1)
            d = DateforProgress(date = date_form,company=company)
            if new_type is None and copy_date_id is None:
                return     JsonResponse({"success": False, "error": "Mahsulot nomini kiritng"})
            if new_type is not None:
                d.save()
                pro1=Progresstype.objects.create(date = d,type = new_type)
                
            
            
            if copy_date_id is not None:
                d.save()
                date_data = DateforProgress.objects.get(id = copy_date_id)
                types = Progresstype.objects.filter(date = date_data)
                for type1 in types:
                    
                    a_type = Progresstype.objects.create(type = type1.type,date = d) 
                
                    for progress in Progress.objects.filter(work__types = type1):
                        
                        try:
                            is_exist = Work.objects.get(work_name = progress.work.work_name,company=company,price = progress.work.price,types = a_type)
                        except Work.DoesNotExist:
                            is_exist=None
                        if is_exist is not None:
                            work = Work.objects.get(work_name = progress.work.work_name,company=company,price = progress.work.price,types = a_type) 
                        else:
                            work = Work.objects.create(work_name = progress.work.work_name,company=company,price = progress.work.price,types = a_type )
                    
                        p = Progress.objects.create(worker = progress.worker,work = work,updated_at = d,is_active=True)
                      
                        ProgressItem.objects.create(progress = p,number = 0,date = date_form)
                 
                return  JsonResponse({"success":True})
            
                       
                
            return JsonResponse({"succes":True})
        except Exception as e:
            return JsonResponse({"succes":False,"error":str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})
        
        
@allowed_pages("admin")
@csrf_exempt
def adminpagedates_delete_full(request,pk):
    element = get_object_or_404(DateforProgress,id = pk)
    if  request.method == "DELETE":
        element.delete()
        return JsonResponse({"success": True, "worker_id": pk})
    return JsonResponse({"error": "Invalid request"}, status=400)
        
@allowed_pages("admin")
def adminpage(request,year,month,typeid):  
    company = request.user.company
    
    worker = Worker.objects.filter(company = company)
    types = Progresstype.objects.filter(
        Q(date__date__year = year) ,
        Q(date__date__month = month),
        date__company = company,)
    t = types.get(id = typeid)
    works = Work.objects.filter(company = company,types = t)
    progress_filtered = Progress.objects.filter(
        Q(items__date__year = year) ,
        Q(items__date__month = month),
        worker__company = company,
        work__types = t,
        
        )
    progress = progress_filtered.annotate(
        total_work_done = Sum("items__number")
    )
    works1 = progress_filtered.values("work__id", "work__work_name", "work__price").distinct()
    worker1 = progress_filtered.values("worker__id", "worker__name", "worker__last_name","is_active").distinct()
    
    name_of_month=int_to_month_string_uz(month)
    #calculating total work done
    sum_info = calculating_total_sum(worker,progress,ProgressItem)
    works_json = json.dumps([{"id": w.id, "name": w.work_name, "price": w.price} for w in works])
    #calculating total work
    total_work = total_work_number(works=works,progress=progress)
    #total_money
    total_sum = total_sum_money(sum_info)
    active_progress = progress_filtered.filter(is_active=True)
    active_worker_ids = list(active_progress.values_list('worker__id', flat=True))
    mon = int_to_month_string_uz(month)
    context = {
        "stringmonth":mon,
        "progress":progress,
        "year":year,
        "month_name":month,
        "sum_info":sum_info,
        "types":types,
        "t":t,
        "name_of_month":name_of_month,
        "works1":works1,
        "worker1":worker1,
        "works":works,
        "works_json": works_json,
        "total_work":total_work,
        "total_sum":total_sum,
        "worker":worker,
        'active_worker_ids': active_worker_ids,
    }    
    return render(request, "admin/adminindex.html",context)



@allowed_pages("admin")
def admin_add_work(request):
    company = request.user.company
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            work_name = data.get("work_name")
            price = data.get("price")
            product_id = data.get("types")
            progresses = Progress.objects.filter(work__types = product_id)
            worker_ids = progresses.values_list('worker__id', flat=True).distinct()
            product = Progresstype.objects.get(id = product_id)
            date_m = datetime(year = product.date.date.year,month=product.date.date.month,day=now.day, hour=now.hour, minute=now.minute, second=now.second)
            
            
            
            if not isinstance(price,int):
                return JsonResponse({"success": False, "error": "Narx son qiymatida emas!"})
            w = Work.objects.create(types=product,company=company,work_name=work_name,price=price)
            for worker_id in worker_ids:
                
                worker = Worker.objects.get(id = worker_id)
                p = Progress.objects.create(worker= worker,work = w,updated_at = date_m)
                ProgressItem.objects.create(progress = p,number = 0,date = date_m)
            return JsonResponse({"success":True,"new_work_name":work_name,"new_price":price})
        except Exception as e:
            return JsonResponse({"success":False,"error":str(e)})
        
    return JsonResponse({"success": False, "error": "Invalid request"})
        
@allowed_pages("admin")
@csrf_exempt  
def admin_create_worker(request):
    if request.method == "POST":
        name = request.POST.get("name")
        last_name = request.POST.get("last_name")
        company = request.user.company
        
        type1 = request.POST.get("t_value")
        t = Progresstype.objects.get(id = type1)
        work_ids = Work.objects.filter(company = company,types = t)
        
        worker = Worker.objects.create(company = company,name=name, last_name=last_name)
        workerExpanse = WorkerExpanses.objects.filter(company = company)
        for ex in workerExpanse:
            WorkerExpansesDetail.objects.create(expanse = ex,worker = worker)
        year = int(request.POST.get("year1"))
        month = int(request.POST.get("month1"))

        vaqt = datetime(year=year, month=month, day=now.day, hour=now.hour, minute=now.minute, second=now.second)
        for work_id in work_ids:
            work = work_id
            pro = Progress.objects.create(worker=worker, work=work,updated_at = vaqt,is_active = True)
            ProgressItem.objects.create(progress = pro,number = 0,date=vaqt)

        return JsonResponse({"message": "Worker and Progress objects created!"}, status=201)

    return JsonResponse({"error": "Invalid request"}, status=400)
@allowed_pages("admin")
def admin_createtype(request):
    company = request.user.company
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            type_name = data.get("type_name")
            items_id = data.get("type_id")
            
            type_d = data.get("type_date")
            
            
            type_date = Progresstype.objects.get(id = type_d).date
            
            year3 = type_date.date.year
            month3= type_date.date.month
            exact_date = datetime(year=year3, month=month3, day=now.day, hour=now.hour, minute=now.minute, second=now.second)
            progress_type = Progresstype.objects.create(date = type_date,type = type_name)
            
            
                
            
            if  items_id  != "None":
                a_type = Progresstype.objects.get(id = items_id)
                
                for progress in Progress.objects.filter(work__types = a_type):
                    try:
                        is_exist = Work.objects.get(work_name = progress.work.work_name,company=company,price = progress.work.price,types = progress_type)
                    except Work.DoesNotExist:
                        is_exist=None
                    if is_exist is not None:
                        work = is_exist
                    else:
                        work = Work.objects.create(work_name = progress.work.work_name,company=company,price = progress.work.price,types = progress_type )
                        
                    p = Progress.objects.create(worker = progress.worker,work = work,updated_at = exact_date,is_active =True)
                    ProgressItem.objects.create(progress = p,number = 0,date = exact_date)
                return  JsonResponse({"message": "Yangi mahsulot turi qo'shildi!"}, status=201)
            return  JsonResponse({"message": "Yangi mahsulot turi qo'shildi!"}, status=201)
            
            
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"message": "send POST request not GET"}) 
        
@allowed_pages("admin") 
@csrf_protect  
@require_POST
def progressitemadd(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            progress_id = data.get("progress_id")
            progress_value = data.get("progress_value")
            year2 = int(data.get("year2"))
            month2 = int(data.get("month2"))
            d = datetime(year=year2, month=month2, day=now.day, hour=now.hour, minute=now.minute, second=now.second)
            if not isinstance(progress_value, int):
                return JsonResponse({"success": False, "error": "Invalid input. Must be an integer!"})

            progress = Progress.objects.get(id=progress_id)
            progress_item = ProgressItem.objects.create(progress = progress , number = progress_value,date = d)
            
            return JsonResponse({"success": True, "new_value": progress_item.number})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})
@allowed_pages("admin")
def showworkers(request):
    company = request.user.company
    workers = Worker.objects.filter(company = company)
    expanse=WorkerExpanses.objects.filter(company = company)
    expanse_detail = WorkerExpansesDetail.objects.all()
    context = {
        "workers":workers,
        "workerexpanse":expanse,
        "detail_expanse":expanse_detail
    }
    return render(request,"admin/showworkers.html",context)

@allowed_pages("admin")
@csrf_protect
def add_worker(request):
    
    if request.method == "POST":
        
        name = request.POST.get("worker_name")
        last_name = request.POST.get("worker_last_name")
        if not name or not last_name:
            return JsonResponse({"success": False, "error": "Ism va familiya talab qilinadi!"}, status=400)
        print(last_name)
        worker = Worker.objects.create(name=name, last_name=last_name,company = request.user.company)
        for i in WorkerExpanses.objects.filter(company = request.user.company):
            WorkerExpansesDetail.objects.create(expanse = i,worker = worker)
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Noto‘g‘ri so‘rov!"}, status=400)

@allowed_pages("admin")
def delete_worker(request,pk):
   
    if request.method == "DELETE":
        worker = get_object_or_404(Worker , id = pk)
        worker.delete()
        return JsonResponse({"success": True, "worker_id": pk})
    return JsonResponse({"error": "Invalid request"}, status=400)
    
    
@allowed_pages("admin")
def adminmultipleworkers(request):
    if request.method == "POST":
        try:
            
            data = json.loads(request.body) 
            worker_ids = data.get("workers")
     
            t= data.get("worker2_type")
            type_pro = get_object_or_404(Progresstype,id = t)
            date_m = datetime(year = type_pro.date.date.year,month=type_pro.date.date.month,day=now.day, hour=now.hour, minute=now.minute, second=now.second)
          
            for worker_id in worker_ids:
                
                
                if worker_id["status"]==True:
                    worker = get_object_or_404(Worker,id = worker_id["worker_id"])
                    for wk in Work.objects.filter(company = request.user.company,types = type_pro):
                        if not Progress.objects.filter(worker_id = worker_id["worker_id"],work = wk).exists():
                            p = Progress.objects.create(work=wk,worker = worker,is_active = True,updated_at = date_m)
                            ProgressItem.objects.create(progress = p,number = 0,date=date_m)
                        else:
                            for wk in Work.objects.filter(company = request.user.company,types = type_pro):
                                pro = Progress.objects.filter(worker_id = worker_id["worker_id"],work=wk)
                                for p in pro:
                                    p.is_active=True
                                    p.save()
                        
                        
                elif worker_id["status"]==False:
                    for wk in Work.objects.filter(company = request.user.company,types = type_pro):
                        pro = Progress.objects.filter(worker_id = worker_id["worker_id"],work=wk)
                        for p in pro:
                            p.is_active=False
                            p.save()
           
                
            return JsonResponse({"success":True})
        except DjangoJSONEncoder:
            return JsonResponse({"success":False})




@allowed_pages("admin")
def history(request):
    company = request.user.company
    progress1 = ProgressItem.objects.filter(progress__work__company = company,progress__worker__company = company,number__gt=0)
    progress = progress1.annotate(
        sum_of_work = F("number")*F("progress__work__price")
    )
   
    context = {
        "history":progress[::-1],
       
    }
    return render(request,"admin/history.html",context)

@allowed_pages("admin")
def delete_history(request ,pk):
    progressitem = get_object_or_404(ProgressItem,id = pk)
    if request.method == "DELETE":
        progressitem.delete()
        return JsonResponse({"success": True, "progress_id": pk})
    return JsonResponse({"error": "Invalid request"}, status=400)
@allowed_pages("admin")
def change_history(request,pk):
    progressitem = get_object_or_404(ProgressItem,id = pk)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            number = data.get("number")
            date = data.get("date")
           
            
            if not isinstance(number, int):
                return JsonResponse({"success": False, "error": "Invalid input. Must be an integer!"})
            progressitem.number = number
            progressitem.date = date
            
            progressitem.save()
            return JsonResponse({"success": True, "new_number": progressitem.number,"new_date":progressitem.date,})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Work  # Import your Work model
@allowed_pages("admin")
@csrf_exempt
def update_work(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            work_id = data.get("work_id")
            new_work_name = data.get("new_work_name")
            new_work_price = data.get("new_work_price")

            work = Work.objects.get(id=work_id)
            work.work_name = new_work_name
            work.price = new_work_price  # Make sure `work_price` exists in your model
            work.save()

            return JsonResponse({"success": True, "message": "Work updated successfully"})
        except Work.DoesNotExist:
            return JsonResponse({"success": False, "message": "Work not found"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request method"})

@allowed_pages("admin")
@csrf_exempt
def delete_work(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("😡😡😡",data)
            work_id = data.get("work_id")

            work = Work.objects.get(id=work_id)
            work.delete()

            return JsonResponse({"success": True, "message": "Ish o'chirildi"})
        except Work.DoesNotExist:
            return JsonResponse({"success": False, "message": "Bu nomdagi ish topilmadi"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Noto'g'ri so'rov!"})





