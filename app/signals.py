from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DateforProgress,Attendence_date,Worker
from datetime import datetime
from datetime import date
now = datetime.now()
from .extra import get_days_in_month
@receiver(post_save,sender = DateforProgress)
def creating_attendance(sender,instance,created,**kwargs):
    if created:
        days = get_days_in_month(year = instance.date.year , month=instance.date.month)
        for day in days:
            
            for w in Worker.objects.filter(company = instance.company):
                Attendence_date.objects.create(month = instance,company = instance.company,worker = w,date =day["day"],day  = day["week"])
@receiver(post_save,sender = Worker)                
def attendance_worker(sender,instance,created,**kwargs):
    if created:
        dates = DateforProgress.objects.filter(date__month = now.month , date__year =now.year)
        
        for dt in dates:
            days = get_days_in_month(year = dt.date.year , month=dt.date.month)
            for day in days:
                Attendence_date.objects.create(month = dt,worker = instance,company = instance.company,date =day["day"],day  = day["week"])
        