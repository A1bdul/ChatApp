# ChatApp
A web chatting application with Python Django

# Requirements
    Python, Django
    Django rest framework
    Channels
    Cloudinary

the channel third party app is responsible for socket connection with various users.
Cloudinary handles all images, files and video upload and transformations. You should sign up or login with this [link](https://cloudinary.com/users/login)

# Installation
Run the following commands from your shell

Project cloning and dependent package installation:

    git clone https://github.com/A1bdul/ChatApp
    cd ChatApp
    pip install -r requirements.txt
    
Defining all hidden credentials in your .env file. The CLOUDINARY_URL value is available in the dashboard of your cloudinary account.
Creating a local database and running a web server:
    
    python manage.py migrate --run-syncdb
    python manage.py runserver

Create admin user to login into website and control dashboard

    python manage.py createsuperuser

You can now browse the following [link](http://localhost:8000)

    http://localhost:800/

# Features
    
    You can live chat with other users with active notification system and fast encrypted messages
    You can create or be added to a group chat to chat with multiple users at once
    Upload files(images, documents) to other users
    Alter your profic pic, background picture, deafault themes and chat favourites
    etc ....
    
