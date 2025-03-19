Hisobchi Demo
Overview
Hisobchi is a multi-company customer relationship management system built with Django. It helps businesses manage their workers, track the total amount of production parts they complete over a month, and calculate salaries based on their work type. The system includes role-based access control and a time restriction for company usage.

Links
deployed demo version of code Application is under the process!!! https://hisobchi5.pythonanywhere.com/ account(entered some details of one Company) for login: phone: +998937832622 password: Qale/0202

Features
Multi-Company Support – Each company has its own admins and clients.
Worker Management – Track workers' total production output per month and calculate salaries based on their work type.
Attendance Tracking – Record worker attendance and calculate daily expenses based on the number of days worked in a month.
Progress & Expense Tracking – Monitor work progress and expenses.
Excel Export – Export reports and data to Excel files.
Role-Based Access Control – Superadmin, company admins, and clients.
Time-Limited Access – Restrict usage based on the company’s time limit.
Installation
Prerequisites
Python 3.x
Django
pandas
Virtual environment (recommended)
Setup Steps
Clone the repository
git clone https://github.com/asliddintursunoff/hisobchi.git
cd hisobchi
Create a virtual environment and activate it
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies
pip install -r requirements.txt
Apply migrations
python manage.py migrate
Create a superuser
python manage.py createsuperuser
Run the development server
python manage.py runserver
Access the CRM Open your browser and go to http://127.0.0.1:8000/
Usage
Superadmin creates company admins.
Company admins manage workers, clients, and expenses.
Clients can log in, view, and manage their data.
Export reports using the Excel export feature.
Contributing
Feel free to submit pull requests or open issues for improvements.
