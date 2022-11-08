# SoftDesk_API
***
##Introduction:

Softdesk_API is an API which allows to track and follow technical issues.(ITS)
This software is developped for B2B firms.

This back-end system deliver a strong and secure interface for creating projects and followissues and share comments and solutions.

***
## Table of content
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Installing Environment](#Installing-Environment)
4. [Configuring Environment](#Configuring-Environment)
5. [Starting Softdesk_API](#Starting-Softdesk_API)
6. [PEP8 reports](#PEP8-reports)
7. [FAQs](#faqs)
***
***
## General Info
***
This program is in version 1.0 and aimed the purpose why it has been created.
I wait the result of the meeting with the askers to see if there was some modifications to bring to this version.

***
## Technologies
***
List of technologies used within this project : 
* [Windows 10](https://www.microsoft.com/fr-fr/software-download/windows10): version 21H2
* [Python](https://www.python.org/downloads/release/python-3100/):  version 3.10.0
* [PyCharm](https://www.jetbrains.com/fr-fr/pycharm/): version 2021.2.3
* [git](https://git-scm.com/download/win): version 2.35.1.windows.2
* [Django](https://www.djangoproject.com/): version 4.1
* [djangorestframework](https://www.django-rest-framework.org): version 3.14.0
* [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/): version 5.2.1
* [flake8](https://pypi.org/project/flake8/): Version 4.0.0
* [flake8-html](https://pypi.org/project/flake8-html/): version 0.4.2

***
## Installing Environment
***
This process suggests that you have admin priviledges on you computer
### Python 3.10.0 installation
***
For installing Python 3.10.0 on your computer go to those adress following the OS you use :

For MacOS :

  Package :
    [Python 3.10.0](https://www.python.org/ftp/python/3.10.0/python-3.10.0post2-macos11.pkg)
    
  Installation guide :
    [Installing Python 3 on MacOS](https://docs.python-guide.org/starting/install3/osx/)

For Linux :

  Package :
    [Python 3.10.0](https://www.python.org/downloads/release/python-3100/)
    [Gzipped source tarball](https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz)
    [XZ compressed source tarball](https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tar.xz)
    
 Installation guide :
    [Installing Python 3.10.0 on Linux](https://docs.python-guide.org/starting/install3/linux/)

For Windows :

  Package : 
    [Python 3.10.0](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)
    
  Installation guide :
    [installing Python 3.1.0 on Windows](https://docs.python.org/fr/3/using/windows.html)

***
### Git 2.35.1 installation
***
For installing Git on your computer go to this adress (all OS contents):

[Git installation guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

***
#### Git configuration 
***
(Even if you did not have done before, create an account on Github at the adress : https://github.com)

1. In order to configure your git IDs , see the following process in GitBash console :
   Type the following command
  
  ``` 
       $ git config --global user.name "your_github_username"
       $ git config --global user.email your_email@your_provider.com
  ```
2. Type the following command to configure the GitBash console interface (optional) :
  
  ```
       $ git config --global color.diff auto
       $ git config --global color.status auto 
       $ git config --global color.branch auto
  ```
***
### Clone the distant repository with Gitbash
***
You have now to clone the distant repository on your computer.
1. type the following command in Gitbash console :
  
  ```
        $ git clone https://github.com/SGauthier2Pro/P10_SoftDesk_API.git
  ```
***
## Configuring environment
***
***
### Installation and execution with virtualenv
***
1. Move to Softdesk_API directory with ```$ cd Softedesk_API```
2. Create a virtual environment for the project with ```$ python -m venv env``` on windows or ```$ python3 -m venv env``` on macos or linux.
3. Activate the virtual environment with ```$ env\Scripts\activate.bat``` on windows or ```$ source env/bin/activate``` on macos or linux.
4. Install project dependencies with ```$ pip install -r requirements.txt```
5. Create an admin user for your server with ```$ python manage.py createsuperuser``` on windows or ```$ python3 manage.py createsuperuser``` on macos or linux.
6. Start the server with ```$ python manage.py runserver``` on windows or ```$ python3 manage.py runserver```on macos or linux.

***
## Starting Softdesk_API
***
***
In order to use the API please refere you to the online documentation at thi adress:
https://documenter.getpostman.com/view/21154794/2s8YYPJ1Vu

***
## PEP8 reports
***

In order to generate the flake8-html report, type the following command from the program folder :

```
    flake8 --format=html --htmldir=flake8-report --exclude env ../SoftDesk_API
```  

***
***
## FAQs
***
***
N/A
***