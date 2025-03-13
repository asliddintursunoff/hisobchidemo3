from django.shortcuts import render,HttpResponse,redirect,get_list_or_404
import json
from django.http import JsonResponse
from .decorators import allowed_pages
from .models import WorkerExpansesDetail,WorkerExpanses,Worker,Avans,Premya,Jarima,Attendence_date,DateforProgress,Progress,ProgressItem

def number_of_attendance_days(worker,company,month):
    list = Attendence_date.objects.filter(company = company,worker = worker,month = month)
    counter = 0
    for lst in list:
        if lst.is_attend == True:
            counter+=1
    return counter
def calculating_expanses(worker,company,total_days):
    total = []
    for i in WorkerExpanses.objects.filter(company = company):
        
        a = WorkerExpansesDetail.objects.filter(worker__id = worker,expanse = i)
        if a.exists():
            
            expanse_sum = a[0].cost*total_days
            
        else:
            expanse_sum = 0
        js = {
            "expanse_name":i.expanse,
            "expanse_id":i.id,
            "expanse_sum":expanse_sum
        }
        total.append(js)
    return total
def avans_get(worker,pk):
    
    avans = Avans.objects.filter(worker = worker,date__year =pk.date.year,date__month = pk.date.month)
    total = 0
    for ava in avans:
        total +=ava.number
        
    return total
       
       
def premya_get(worker,pk):
    
    premya = Premya.objects.filter(worker = worker,date__year =pk.date.year,date__month = pk.date.month)
    total = 0
    for pr in premya:
        total +=pr.number
        
    return total

        
        
    

def calculating_total_sum(worker,pk):
    
    progress = Progress.objects.filter(worker = worker,items__date__year = pk.date.year,items__date__month = pk.date.month)
    sum = 0
    for pro in progress:
        item = ProgressItem.objects.filter(progress=pro)
        number = 0
        for i in item:
            number =number+ i.number
        sum =sum+ number*pro.work.price
    
    return sum//2
        
    
    
    
        
def how_much_get(avans,premya,total_sum,expanses):
    f_money = 0
    for ex in expanses:
        money = ex.get("expanse_sum")
        f_money+=money
    total = 0
    
    total = total_sum+avans+premya+f_money
    return total
def salary_logic(pk,cp):
    month = DateforProgress.objects.get(id = pk)
    company = cp
    
    workers = Worker.objects.filter(company=company)
    
    
    worker_list = [{"worker":f"{worker.name} {worker.last_name}",
                        "total_days":number_of_attendance_days(worker,company,month),
                        "calculating_expanses":calculating_expanses(worker.id,company=company,total_days=number_of_attendance_days(worker,company,month)),
                        "done_money":calculating_total_sum(worker=worker,pk=month),
                        "avans":avans_get(worker,month),
                        "premya":premya_get(worker,month),
                        "full_money":how_much_get(avans=avans_get(worker,month),premya=premya_get(worker,month),total_sum=calculating_total_sum(worker=worker,pk=month),expanses=calculating_expanses(worker.id,company=company,total_days=number_of_attendance_days(worker,company,month))),
                        "worker_id":worker.id
                        } for worker in workers] 
    return worker_list
def salary_get(request,pk):
    month = DateforProgress.objects.get(id = pk)
    company = request.user.company
    expanses =  WorkerExpanses.objects.filter(company = company)
    workers = Worker.objects.filter(company=company)
    
    
    worker_list = salary_logic(pk=pk,cp=company)
    
    context= {
        "expanses":expanses,
        "workers":worker_list,
        "date" : month
    }
    return render(request,"admin/salary.html",context)
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def post_premya(request):
    if request.method=="POST":
        try: 
            data = json.loads(request.body)
            print(data,"😊")
            worker_id = data.get("worker_id")
            date_id = data.get("dateid")
            number = data.get("numberpremya")
            print(data,"😊")
            if not isinstance(number,int):
                return JsonResponse({"success":False})
            else:
                worker = Worker.objects.get(id=worker_id)
                date = DateforProgress.objects.get(id = date_id)
                Premya.objects.create(worker = worker,date = date.date,number = number)
                return JsonResponse({"success":True})
        except Exception as ex:
            return JsonResponse({"success":False,"error":str(ex)})
    else:
        return JsonResponse({"not valid response"})
        
@csrf_exempt
def post_avans(request):
    if request.method=="POST":
        try: 
            data = json.loads(request.body)
            print(data)
            worker_id = data.get("worker_id")
            date_id = data.get("dateid")
            number = data.get("numberavans")
            print(data,"🧑🏻‍🎓")
            if not isinstance(number,int):
                return JsonResponse({"success":False})
            else:
                worker = Worker.objects.get(id=worker_id)
                date = DateforProgress.objects.get(id = date_id)
                Avans.objects.create(worker = worker,date = date.date,number = number)
                return JsonResponse({"success":True})
        except Exception as ex:
            return JsonResponse({"success":False,"error":str(ex)})
    else:
        return JsonResponse({"not valid response"})
        
    
@csrf_exempt
def post_workerexpanse(request):
    if request.method=="POST":
        try: 
            workers = Worker.objects.filter(company = request.user.company)
            data = request.POST.get("expanse_name")
            ex = WorkerExpanses.objects.create(company = request.user.company,expanse = data)
            for worker in workers:
                WorkerExpansesDetail.objects.create(worker = worker,expanse = ex)
            return JsonResponse({"success":True})
        except Exception as er:
            return JsonResponse({"success":False})
    return JsonResponse({"success":False})

@csrf_exempt
def update_worker_expanse(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ex_id = data.get("worker_id")
            new_value = data.get("new_expanse_value")
           
            expanse = WorkerExpansesDetail.objects.get(id = ex_id)
        
            expanse.cost = new_value
            expanse.save()
            
            return JsonResponse({"success":True})
        except:
            return JsonResponse({"success":False})
    
    
@csrf_exempt
def update_worker_expansename(request):
    if request.method == "POST":
        data = json.loads(request.body)
        expanse_id = data.get("expanse_id")
        new_value = data.get("new_expanse_value")

        try:
            expanse = WorkerExpanses.objects.get(id=expanse_id)
            expanse.expanse = new_value
            expanse.save()
            return JsonResponse({"success": True, "new_value": new_value})
        except WorkerExpanses.DoesNotExist:
            return JsonResponse({"success": False, "error": "Not found"}, status=404)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)
@csrf_exempt
def delete_worker_expanse_name(request):
    if request.method == "POST":  # Change to DELETE if needed
        try:
            data = json.loads(request.body)
            expanse_id = data.get("expanse_id")

            # Find and delete
            expanse = WorkerExpanses.objects.get(id=expanse_id)
            expanse.delete()

            return JsonResponse({"success": True})
        except WorkerExpanses.DoesNotExist:
            return JsonResponse({"success": False, "error": "Harajat topilmadi"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    
    return JsonResponse({"success": False, "error": "Noto'g'ri so'rov turi"})