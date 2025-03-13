def int_to_month_string_uz(month):
    months = [
        "Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun",
        "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"
    ]
    return months[month - 1] if 1 <= month <= 12 else "mavjud bo'lmagan sana"


def calculating_total_sum(worker,progress_filtered,ProgressItem):
    sum_info=[]
    for i in worker:     
        worker_total_sum = 0
        for j in progress_filtered.filter(worker = i):
           
            price = j.work.price
            a = 0
            for table in ProgressItem.objects.filter(progress=j):               
                a+=table.number 
            sum = a*price
            worker_total_sum+=sum    
        print("",worker_total_sum)
        content = {
            "people":i,
            "people_id":i.id,
            "sum_money": worker_total_sum,
        }
        sum_info.append(content)
    return sum_info



def total_work_number(works,progress):
        total_work = []
        for w in works:
            actual_progress_items = progress.filter(work = w)
            total= 0
            for a in actual_progress_items:
                
                total+=a.total_work_done
            total_dict = {
                "work_id":w.id,
                "work_n":w,
                "total":total
            }
            total_work.append(total_dict)
        return total_work
    
def total_sum_money(calculating_total_sum):
    sum = 0
    for i in calculating_total_sum:
        sum+=i["sum_money"]
        
    return sum
    
    
import calendar   
def get_days_in_month(year, month):
    num_days = calendar.monthrange(year, month)[1]  # Get number of days in the month
    
    days_list = [
        {"day":day, "week":calendar.day_name[calendar.weekday(year, month, day)]}
        for day in range(1, num_days + 1)
    ]
    return days_list


#for exporting data as exdell
from .models import *
from django.db.models import Q,Sum
def showing_adminpageindex(company,month,year,typeid):
    worker = Worker.objects.filter(company = company)
    
    t = Progresstype.objects.get(id= typeid)
    works = Work.objects.filter(types = t,company = company)
    progress_filtered = Progress.objects.filter(
        Q(items__date__year = year) ,
        Q(items__date__month = month),
        worker__company = company,
        work__types = t,  
        )
    progress = progress_filtered.annotate(
        total_work_done = Sum("items__number")
    )
    worker1 = progress_filtered.values("worker__id", "worker__name", "worker__last_name","is_active").distinct()
    sum_info = calculating_total_sum(worker,progress,ProgressItem)
    #calculating total work
    total_work = total_work_number(works=works,progress=progress)
    #total_money
    total_sum = total_sum_money(sum_info)
    
    result = []
    a = 0
    for j in worker1:
        
        if j["is_active"]==True:
            if a == 0:
                costs = {"Иш номи": "Расенка"}  # First column
                ordered_costs = {f"{new.work_name}": new.price for new in works }
                costs.update(ordered_costs) 
                result.append(costs)
            data = {
                "Иш номи":f"{j["worker__name"]} {j["worker__last_name"]}"
            }
            
            for w in works:
                for pro in progress:
                    if pro.worker.id == j["worker__id"] and pro.work.id == w.id:
                        data.update({f"{w.work_name}":pro.total_work_done})    
            for value in sum_info:
                if value["people_id"] ==j["worker__id"]:
                    data.update({f"Жами":value["sum_money"]})  
            
            result.append(data)
            a+=1
            
    new_values = {"Иш номи":"Жами"}
    new_values.update({f"{new["work_n"].work_name}": new["total"] for new in total_work })
    new_values.update({"Жами":total_sum})
    result.append(new_values)
    
   
    return result  
                    
            
    
    
    
def calculating_expanse_total(company):
    dates = DateforExpanse.objects.filter(company = company)
    expanseNames = ExpanseName.objects.filter(company=company)
    lst = []
    for expanseName in expanseNames:
        expanse = Expanse.objects.filter(expanse_key = expanseName)
        sum = 0
        for ex in expanse:
            try:
                
                i = int(ex.value.replace(" ",""))
            except ValueError:
                i = 0
            sum+=i
        dic = {
            "expanse_name":expanseName,
            "expanse_total":sum,
            "type":expanseName.expabse_type
        }
        lst.append(dic)
    return lst