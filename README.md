# Django hotel management system

Hotel Manager system made you don’t have to sit and manage the entire activities on paper. And at the same time Owner of the Hotel will feel comfortable to keep a check on. Hotel easily from anywhere around the world.This System will give them power and flexibility to manage the entire system from a single online portal. Hotel management System provides room management, reservation, room booking, staff management, checkin, checkout, bill generation, profit management features.

# Technology Used
 - HTML/CSS
 - Javascript (particularly AJAX, DOM)
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

# Features of the project
Page interface
 - Home page introduces hotel information, allowing guests to make reservations
 - Blog contains categories, articles with author information, views, comments 
 - Dashboard display informations, calculate the cost of transaction, statistics compared with the previous month, shown on the chart 

Permission
 - Superuser can create staff object with id, staff can use that id to register account;
add, delete, update room facility, service, room class; add, update, delete, set maintenance, availability of Rooms
 - Staff can Login, Signup, Logout, Update profile, Change password, Reset forgotten password
 - Receptionists can Create, Update customer information; handle Reservation, Booking, Check in, Check out, update, cancel the transaction. 
 - Maketing staff can write, update, public blog article
 - Guests can read article, make comments, make reservations

# Screenshots

Login
![plot](./static/blog image/login.png)

Register
![plot](./static/blog image/register.png)

Homepage
![plot](./static/blog image/homepage.png) 

Blog
![plot](./static/blog image/blog.png)

Proflie
![plot](./static/blog image/profile.png)

Dashboard  
![plot](./static/blog image/dashboard.png)

