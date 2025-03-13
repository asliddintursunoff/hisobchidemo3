from django.shortcuts import HttpResponse,render,redirect
from .models import Expanse,ExpanseName,Company,User,Worker,DateforExpanse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .decorators import allowed_pages
@allowed_pages("admin")
def usersettings_get(request):
    company = request.user.company
    info = Company.objects.get(id = company.id)
    workers = Worker.objects.filter(company=company).count()
    context = {
        "info":info,
        "workers":workers
    }
    return render(request,"admin/adminsettings.html",context)
@allowed_pages("admin")
@csrf_exempt  # Disable CSRF protection (not recommended for production without proper security setup)
def save_user_info(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = request.user  # Get the logged-in user
            company = Company.objects.get(id = user.company.id)
            # Update user fields
            n= data.get("name")
            user.first_name = data.get("first_name", user.first_name)
            user.last_name = data.get("last_name", user.last_name)
            user.phone_number = data.get("username", user.phone_number)
            company.name = n
            company.save()
            user.save()

            return JsonResponse({"status": "success", "message": "User info updated successfully!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)


from .extra import calculating_expanse_total
@allowed_pages("admin")
def expanse_view(request):
    company = request.user.company
    expanse_names = ExpanseName.objects.filter(company = company)
    expanse = Expanse.objects.all()
    dates = DateforExpanse.objects.filter(company = company)
    total = calculating_expanse_total(company)
    context = {
        "expanse_names":expanse_names,
        "expanse":expanse,
        "dates":dates,
        "total":total
    }
    return render(request,"admin/expanse.html",context)

     
     
     
@csrf_exempt
def update_expanse(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("😡😡", data)  # Debugging line

        try:
            
            date_id = data.get("date_id")
            expanse_id = data.get("expanse_id")
            expanse_key = data.get("expanse_key")
            expanse_value = data.get("expanse_value")
            
            if not date_id:
                return JsonResponse({"success": False, "message": "Iltimos avval sanani kiriting"})

            date = DateforExpanse.objects.get(id=date_id)

            if expanse_id is not None:  # Update existing record
                expanse = Expanse.objects.get(id=expanse_id)
               
                expanse.value = expanse_value
                expanse.date = date
                expanse.save()
                d=calculating_expanse_total(request.user.company)
                return JsonResponse({"success": True, "message":"with id", "expanse_id": expanse.id})

            else:  
                # Create new record
                try:
                    if expanse_key : 
                        a = Expanse.objects.filter(date = date,expanse_key=ExpanseName.objects.get(id=expanse_key))
                        b = a[0]
                        for i in a[1:]:
                            i.delete()
                        b.value = expanse_value
                        b.save()
                        d=calculating_expanse_total(request.user.company)
                        return JsonResponse({"success": True,"message":"with name", "expanse_id": b.id})
                except  :
                   
                        new_expanse = Expanse.objects.create(
                            expanse_key=ExpanseName.objects.get(id=expanse_key),
                            value=expanse_value,
                            date=date
                        )
                        d=calculating_expanse_total(request.user.company)
                        return JsonResponse({"success": True,"expanse_id": new_expanse.id})  # ✅ Return new expanse_id

        except Exception as e:
            return JsonResponse({"success": False, "message": ("big: ",str(e))})  # ✅ Properly return errors

    return JsonResponse({"success": False, "message": "Invalid request"})


@csrf_exempt
def update_date(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("💕", data)
            date_id = data.get("date_id")
            date_value = data.get("date_value")
            
            if date_id:  # ✅ If date_id exists, update the existing record
                date_id = int(date_id)
                dates = DateforExpanse.objects.get(id=date_id)
                dates.date = date_value
                dates.save()
            else:  # ✅ If no date_id, create a new record
                date = DateforExpanse.objects.create(company=request.user.company, date=date_value)
                date_id = date.id

            return JsonResponse({"success": True, "date_id": date_id})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False})


def add_column(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            column_name = data.get("column_name")
            column_type = data.get("column_type")

            if not column_name:
                return JsonResponse({"success": False, "message": "Ustun nomini kiriting!"})

            # Create new column in the database
            new_column = ExpanseName.objects.create(company = request.user.company,expanse_name=column_name, expabse_type=column_type)
            return JsonResponse({"success": True, "column_id": new_column.id})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request"})


def deleting_expanse_name(request,pk):
    
        ex = ExpanseName.objects.get(id = pk)
        ex.delete()
        return redirect("expanse_view")
   
   
def deleting_expanse_date(request,pk):
    
        ex = DateforExpanse.objects.get(id = pk)
        ex.delete()
        return redirect("expanse_view")
   