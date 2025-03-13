from django.shortcuts import render,HttpResponse,redirect,get_list_or_404
import json
from django.http import JsonResponse
from .models import DateforProgress,Attendence_date,Worker
from .decorators import allowed_pages
@allowed_pages("admin")
def attendance_get(request,pk):
    attendance = Attendence_date.objects.filter(company = request.user.company,month = DateforProgress.objects.get(id=pk))   
    workers = Worker.objects.filter(company = request.user.company)
    attendance_list = [{"worker":f"{worker.name} {worker.last_name}",
                        "data":attendance.filter(worker = worker)} for worker in workers]      
    context = {
        "attendance":attendance_list,
        "for_days":attendance_list[0]
    }
   
    return render(request,"admin/attendance.html",context)
@allowed_pages("admin")
def attendance_post(request):
    if request.method=="POST":
        try:
            data = json.loads(request.body)
            print("👌",data)
            attendance_id = data.get("id")
            status = data.get("status")
            attendance = Attendence_date.objects.get(id = attendance_id)
            attendance.is_attend = status
            attendance.save()
            return JsonResponse({"success": "yo'qlama muvaffaqqiyatli amalga oshdi", "status": status}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)



