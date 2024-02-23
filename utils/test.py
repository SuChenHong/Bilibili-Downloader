from flask import Flask, redirect

app = Flask(__name__)


@app.route('/')
def open_existing_webpage():
    # 在这里设置你想要打开的网页 URL
    existing_webpage_url = ''
    return redirect(existing_webpage_url)


if __name__ == '__main__':
    app.run(debug=True)
