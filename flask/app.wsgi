from api import api as application

activate_this = '/home/brettbissey/anaconda3/envs/flask/bin/activate.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))



