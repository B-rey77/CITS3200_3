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

Installation (deployment)
-------------------------

1. Create a Docker Hub account, and create an access token for GitHub actions to use.
2. Add the access token (username / token) as GitHub Repository secrets `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` for the repository (under Settings -> Security -> Secrets -> Actions).
3. Create an AWS account (or use an existing one) and access the CodePipeline console.
4. Under Settings -> Connections, create a connection and point it to the GitHub repository (it will ask you to login). Once this is done, copy the ARN corresponding to the created GitHub connection.
5. ...

References
----------

AWS/Docker Hub deployment courtesy of https://github.com/BluCloudEngineer/UWA-Git-Good-Presentation (under the MIT license)
