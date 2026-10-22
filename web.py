from helpers import log #type: ignore

@app.route("/hello")
def hello():
    log("hello called")
    return "Hello from lpdc-document-to-html-service"