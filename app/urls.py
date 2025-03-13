from django.contrib import admin
from django.urls import path,include
from .views import *
from .attendance_view import *
from .views_salary import *
from .views_settingsandexpanses import *

urlpatterns = [

    path("", homepage,name='homepage'),
    path("register/", register,name='register'),
    path("login/", userlogin,name='login'),
    path("logout/", userlogout,name='logout'),
    path("adminpage/",adminpagedates,name = "adminpage"),
    path("adminpage/deletedate/<int:pk>/",adminpagedates_delete_full,name="adminpage_delete_date"),
    path("adminpage/<int:year>/<int:month>/<int:typeid>/" , adminpage ,name = "adminpaging"),
    path("adminpage/createdate/",adminpagedates_add_date,name = "adminpagedates_add_date"),
    path("adminpage/addworker/",admin_add_work,name="admin_add_worker"),
    path("adminpage/createtype/",admin_createtype,name = "admincreatetype"),
    path("adminpage/create_worker/",admin_create_worker,name="adminpage_create_worker"),
    path("update-progress-item/", progressitemadd, name="update-progress-item"),
    path("showworkers/",showworkers,name="showworkers"),
    path("showworkers/delete/<int:pk>/" , delete_worker , name = "delete_worker"),
    path("history/",history , name = "history"),
    path("history/<int:pk>/" , delete_history ),
    path("history/change/<int:pk>/",change_history),
    path("createworker/",add_worker,name="createworker"),
    path("proworkers/",adminmultipleworkers,name="adminmultipleworkers"),
    path("attendance/<int:pk>/",attendance_get,name="attendance"),
    path("attendance/add",attendance_post,name="attendance_post"),
    path("adminpage/salary/<int:pk>/",salary_get,name="salary-get"),
    path("post-premya/",post_premya,name = "post_premya"),
    path("post-avans/",post_avans,name = "post_avans"),
    path("post-workerexpanse/",post_workerexpanse, name="post-workerexpanse"),
    path("update-workerexpanse",update_worker_expanse , name="update-workerexpanse"),
    #excell
    path("mainexcel/<int:month>/<int:year>/<int:typeid>",main_to_excell,name = "main-excell"),
    path("salaryexcel/<int:pk>",salaries_to_excell,name = "salary-excell"),
    path("admindatemaintoexcel/<int:pk>",admindate_main_to_excel, name="admindate_main_to_excel"),
    #admin settings
    path("adminsettings/",usersettings_get,name = "adminsettings"),
    #expanse 
    path("expanse/",expanse_view,name="expanse_view"),
 
    path("update-expanse/",update_expanse,name = "expanse-post"),
    path("save-user-info/", save_user_info, name="save-user-info"),
    
    #deleting and updaind
    path("update-workerexpansename/",update_worker_expansename , name="update-workerexpansename"),
    path('delete-expanse/', delete_worker_expanse_name, name='delete-workerexpansename'),
    path('update-work/', update_work, name='update-work'),  # Update URL
    path('delete-work/', delete_work, name='delete-work'),  # Delete URL
    path('update-date/', update_date, name='delete-work'), 
    path('add-column/', add_column, name='add-column'), 
    path('delete-column/<int:pk>/', deleting_expanse_name, name='delete_expanse_name'),
    path('delete-date/<int:pk>/', deleting_expanse_date, name='delete_expanse_date'),
]
