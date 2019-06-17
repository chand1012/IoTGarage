# this is a test device that returns 200s and other responses for 
# nothing other than testing purposes

from flask import Flask, Response

app = Flask(__name__)

@app.route("/doAThing")
def doAThing():
    return Response(status=200)

@app.route("/doAThingWrong")
def doAThingWrong():
    return Response(status=404)

if __name__=="__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)