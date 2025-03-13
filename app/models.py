from django.db import models

from django.db import models
from django.contrib.auth.models import User,AbstractUser

from django.utils.timezone import now
from datetime import datetime, timedelta
from django.utils import timezone
import random
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number field must be set")
        extra_fields.setdefault("is_active", True)

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)
def generate_unique_number():
    """Generates a 4-digit unique number."""
    code = str(random.randint(1000, 9999))  # Generates a number between 1000-9999

    # Ensure the code is unique in the database
    while Company.objects.filter(unique_id=code).exists():
        code = str(random.randint(1000, 9999))

    return code

class Company(models.Model):
    name = models.CharField(max_length=255)
    unique_id = models.IntegerField(null=True,blank=True, unique=True, default=generate_unique_number, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(default=timezone.now() + timedelta(days=15)) 
    anneversary = models.BooleanField(null=True,blank = True)
    def is_active(self):
        if self.anneversary == True:
            active = True
        elif self.expiry_date>timezone.now():
            active = True
        else:
            active = False
        return active
    
    def active_time(self):
        if self.anneversary == True:
            active = "always"
        else:
            active = self.expiry_date
        return active
    
    def __str__(self):
        return f"{self.name} | {self.is_active()} | {self.active_time()} | {self.unique_id}" 

class User(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=13, unique=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True,related_name="compnay")
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",  # Add a unique related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",  # Add a unique related_name
        blank=True,
    )
    USERNAME_FIELD = "phone_number"  # Login with phone number
    REQUIRED_FIELDS = [] 
    objects = CustomUserManager()

class Worker(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="worker_profile",null=True,blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(default=user.name ,max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.last_name} {self.name}"


class DateforProgress(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(default=now)
    def __str__(self):
        return f"{ self.company } -- {self.date}"
class Progresstype(models.Model):
    date = models.ForeignKey(DateforProgress,on_delete=models.CASCADE,related_name="dates",null=True, blank=True)
    type = models.CharField(max_length=100,null=True, blank=True)
    def __str__(self):
        return f"{self.date} | {self.type} | {self.id}"
class Work(models.Model):
    types  = models.ForeignKey(Progresstype, on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="works")
    work_name = models.CharField(max_length=100,null=True,blank=True)
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.types} - {self.work_name} - {self.price}   -- {self.company.name}  -- "
class Progress(models.Model):
    
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="progress")
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="progress")
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return f"{self.worker.name} {self.worker.last_name}  | {self.work.work_name} | {self.work.company.name})"

class ProgressItem(models.Model):
    progress = models.ForeignKey(Progress, on_delete=models.CASCADE, related_name="items")
    number = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"Item {self.number} for {self.progress}"


# class Expanses(models.Model): 
#     company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="expanses")
#     worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True, related_name="expanses")
#     description = models.TextField()
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.company.name} - {self.amount} on {self.date}"

class Attendence_date(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)
    worker = models.ForeignKey(Worker,on_delete=models.CASCADE,null=True,blank=True)
    month = models.ForeignKey(DateforProgress,on_delete=models.CASCADE,null=True,blank=True)
    date = models.IntegerField(null=True,blank=True)
    is_attend = models.BooleanField(default=False,null=True,blank=True)
    day = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return f"{self.worker} - {self.company.name} - {self.date}"
    
    
class WorkerExpanses(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)
    expanse = models.CharField(max_length=100,null=True,blank=True)
    
class WorkerExpansesDetail(models.Model):
    expanse = models.ForeignKey(WorkerExpanses,on_delete=models.CASCADE,null=True,blank=True)
    cost = models.IntegerField(default=0)
    worker = models.ForeignKey(Worker,on_delete=models.CASCADE,null=True,blank=True)
    
class Premya(models.Model):
    date = models.DateField(null=True,blank=True)
    worker = models.ForeignKey(Worker,on_delete=models.CASCADE)
    number = models.IntegerField(default=0,null=True,blank=True)
    
class Avans(models.Model):
    date = models.DateField(null=True,blank=True)
    worker = models.ForeignKey(Worker,on_delete=models.CASCADE)
    number = models.IntegerField(default=0,null=True,blank=True)
    
    
class Jarima(models.Model):
    date = models.DateField(null=True,blank=True)
    worker = models.ForeignKey(Worker,on_delete=models.CASCADE)
    number = models.IntegerField(default=0,null=True,blank=True)
    
    

class DateforExpanse(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    date = models.DateField(default=now)
    def __str__(self):
        return f"{self.date} - {self.company}" 
class ExpanseName(models.Model):
    STATUS_CHOICES = [
        ('kirim', 'kirim'),
        ('chiqim', 'chiqim'),
        ('istisno', 'istisno'),
    ]
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)
    expanse_name = models.CharField(max_length=100)
    expabse_type = models.CharField(max_length=10, choices=STATUS_CHOICES, default='istisno')
    
    def __str__(self):
        return f"{self.expanse_name} - {self.expabse_type}"
    
class Expanse(models.Model):
    date = models.ForeignKey(DateforExpanse,on_delete=models.CASCADE,related_name="items")
    expanse_key = models.ForeignKey(ExpanseName,null=True,blank=True,on_delete=models.CASCADE,related_name="items")
    value = models.CharField(max_length=300,null=True,blank=True)
   
    def __str__(self):
        return f"{self.expanse_key} - {self.value}"
    