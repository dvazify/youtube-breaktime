from flask import Flask, request, flash, render_template, url_for
from api import ReturnVideos
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/handle_data', methods=['POST'])
def handle_data():
        topic = request.form['topic']
        maxmins = int(request.form['maxmins'])
        videolist = ReturnVideos(topic,maxmins)
        return render_template('results.html', videos=videolist)
    
if __name__ == "__main__":
    app.run(debug=True)