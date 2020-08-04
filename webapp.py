from flask import Flask, render_template

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():

    news = dict()
    with open('collected_data.txt', 'r') as f:
        collected_data = f.readlines()

    for line in collected_data:
        if line[:4] == 'http':
            title = line
            news[title] = list()
        else:
            news[title].append(line)

    return render_template('index.html', news=news)

if __name__ == '__main__':
    app.run(debug=True)