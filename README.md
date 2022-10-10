CITS3200 Project: ASAVI Strep. A. Literature Database
=====================================================

Installation (Development)
--------------------------

Setup virtualenv (using python version 3.8 or later):
```
python3 -m virtualenv pyenv
. ./pyenv/bin/activate
```


First, install the required plugins/programs using pip:
```
pip install -r requirements.txt # or pip3 install -r requirements.txt # *depends on your python version
```
https://www.codegrepper.com/code-examples/shell/how+to+install+packages+from+requirements.txt

Admin:
Username: admin
Password: Password1

Second, initiate local server:
```
python manage.py runserver # *depends on your python version
```

HTML pages:
localserver  - homepage
localserver/login
localserver/signup
localserver/visitor (you wont get in unless youre signed up)
localserver/admin

References
----------

AWS/Docker Hub deployment courtesy of https://github.com/BluCloudEngineer/UWA-Git-Good-Presentation (under the MIT license)
