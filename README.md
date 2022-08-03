# CITS3200_3
Online database providing contemporary burden of Strep A infections in Australia.

## Setting up Django

1. Make sure Python is installed on your computer and verify that you can run it in a terminal / powershell / cmd window using a command resembling `python --version` (sometimes `python3 --version`) - this should output something similar to `Python 3.10.2` (version 3 is important, although minor version numbers are less significant)
2. Clone the git repository somewhere suitable - copy the full path name so you can use refer to it via the terminal where you have Python. (substitute this for `$REPO` in the following commands)
3. Set up a virtual Python home environment (this will contain any python packages you install). Run `python -m virtualenv $REPO/pyenv` to create a virtual environment directory in the pyenv folder inside the repository - note that this will be ignored by Git and should not be added to the repository (everyone's virtualenv folder will be slightly different as it is specific to your PC)
4. In the terminal run `. $REPO/pyenv/bin/activate` to activate the virtualenv
5. Run `pip install django` to set up the django module for python.
6. Change to the `$REPO` directory inside the terminal (`cd $REPO`) and run `./manage.py migrate` to get Django to set up the default local database.
7. Run the web server using `./manage.py runserver` and open the link in your browser!