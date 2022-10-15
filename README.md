CITS3200 Project: ASAVI Strep. A. Literature Database
=====================================================

Online database providing contemporary burden of Strep A infections in Australia.

Installation (Development)
--------------------------

1. Make sure Python (version 3.8 or later) is installed on your computer. You can verify this by opening a Command Prompt/Terminal/Powershell window and using the command ```python --version``` (or ```python3 --version```). You can download the latest version of Python from https://www.python.org/downloads/ if necessary. 

2. Copy the full path name of the folder in which you have placed the code. Use this path name instead of ```$REPO``` in the following commands.

3. Set up a virtual Python home environment. If you are a Windows user, run ```python -m venv $REPO/pyenv``` in your Command Prompt/Terminal/Powershell window. For macOS and Linux users, run ```python -m virtualenv $REPO/pyenv```. Next, run ```$REPO/pyenv/Scripts/activate``` for Windows users, or ```. $REPO/pyenv/bin/activate``` for macOS and Linux users. 

4. Run pip install django to set up the Django module for Python. 

5. Install the required plugins/programs. 

```pip install -r requirements.txt```

https://www.codegrepper.com/code-examples/shell/how+to+install+packages+from+requirements.txt

6. Initiate the local server:
```
python manage.py runserver
```
You can access the local server at http://127.0.0.1:8000/


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
