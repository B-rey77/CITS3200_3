CITS3200 Project: ASAVI Strep. A. Literature Database
=====================================================

Online database providing contemporary burden of Strep A infections in Australia.

Installation (Development)
--------------------------


1. Make sure Python is installed on your computer and verify that you can run it in a terminal / powershell / cmd window using a command resembling `python --version` (sometimes `python3 --version`) - this should output something similar to `Python 3.10.2` (version 3 is important, although minor version numbers are less significant)
2. Clone the git repository somewhere suitable - copy the full path name so you can use refer to it via the terminal where you have Python. (substitute this for `$REPO` in the following commands)
3. Set up a virtual Python home environment (this will contain any python packages you install). Run `python -m virtualenv $REPO/pyenv` to create a virtual environment directory in the pyenv folder inside the repository - note that this will be ignored by Git and should not be added to the repository (everyone's virtualenv folder will be slightly different as it is specific to your PC)
4. In the terminal run `. $REPO/pyenv/bin/activate` to activate the virtualenv
5. Run `pip install django` to set up the django module for python.
6. Change to the `$REPO` directory inside the terminal (`cd $REPO`) and run `./manage.py migrate` to get Django to set up the default local database.
7. Run the web server using `./manage.py runserver` and open the link in your browser!


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
