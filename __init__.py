from flask import Flask      

# create an instance of the Flask class
app = Flask(__name__)   # 1. create the name of the single module
# if starts as application, '__main__'    if imports as module, '__name__'

@app.route('/recommendation/<username>')
def recommendation(username):
    return recommendapi()