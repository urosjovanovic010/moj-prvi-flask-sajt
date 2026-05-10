from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('pocetna.html')

@app.route('/o-nama')
def onama():
    return "Ovo je stranica o nama!"

if __name__ == '__main__':
    app.run(debug=True)

