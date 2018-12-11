from taubot_logic import respond
from flask import Flask, render_template, request

app = Flask(__name__)
sameInput = 0
isinya =""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    global sameInput
    global isinya
    inputText = request.args.get('msg')
    if (inputText == 'udah'):
        life = False
        return str('Selamat Tinggal kawan:(')
    if(inputText!=isinya):
        isinya = inputText
        sameInput=0
        return str(respond(inputText))
    elif (sameInput>=1):
        return str("Nanya Mulu Beli Kagak!!!")
    elif (inputText==isinya):
        sameInput += 1
        return(respond(inputText))
        # print(sameInput)

if __name__ == "__main__":
    app.run()
