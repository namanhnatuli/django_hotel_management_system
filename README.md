# Django hotel management system

Hotel Manager system made you don’t have to sit and manage the entire activities on paper. And at the same time Owner of the Hotel will feel comfortable to keep a check on. Hotel easily from anywhere around the world.This System will give them power and flexibility to manage the entire system from a single online portal. Hotel management System provides room management, reservation, room booking, staff management, checkin, checkout, bill generation, profit management features.

# Technology Used
 - HTML/CSS
 - Javascript( particularly AJAX, DOM)
 - Git
 - Django
 - Bootstrap 4

# How to run the project
 Clone this repo in your system:
 ```
 git clone https://github.com/namanhnatuli/django_hotel_management_system.git
 ```
 Get inside the repo, type this is terminal:
 ```
 cd django_hotel_management_system
 ```
 Create a virtual environment inside the repo:
 ```
 python -m venv .venv
 ```
 After that activate the virtual environment by typing:
 ```
 source .venv/bin/activate
 ```
 Next step is to install all the dependencies into your virtual environment:
 ```
pip install -r requirements.txt
 python3 manage.py makemigrations
 python3 manage.py migrate
 ```
 Now to access the admin page before running the server create a superuser:
 ```
 python manage.py createsuperuser
 fill the details:
 username: <ur choice>
 email: <optional>
 password: <password>
 confirm password: <confirm the password>
 ```
 After filling all these to run the project:
 ```
 python manage.py runserver
 ```
the app runs in the development mode.
Open http://127.0.0.1:8000/ to view it in the browser.

# Demo
The demo is updated whenever the demo branch code is updated.
```bash
username: admin
password: admin
```

# Features of the project
 - Superuser can create staff object with id, staff can use that id to register account
 - Staff can Login, Signup, Logout, Update profile, Change password, Reset forgotten password
 - Customers can make reservations
 - Facility to add, delete, update rooms.
 - Service, room class to add, delete, update.
 - Room to add, delete, set maintenance, availability.
 - Handle Reservation, Booking, Check in, Check out, update, cancel the transaction. 
 - Calculate the cost of transaction, Statistics compared with the previous month, shown on the chart 
 - Create, Update, Store customer information
 - View the details of user that has booked one of his rooms.
 - Superuser have access to all the functionality listed above.
