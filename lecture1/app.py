from flask import Flask, render_template

# build flask's example

# define app
app = Flask(__name__)

# define home page route /
@app.route("/")
def home():
    # define response of home page
    web_content = {
        "title": 'hello',
        "text": 'Welcome to my home page!'
    }
    lucky_nums = [1,6,9,22,32,36]
    #content = '<a href="/about">link_about</a>'
    #return  '<h1>Welcome</h1> to my home page!!!'+content
    return render_template("home.html", content = web_content, lucky_nums = lucky_nums )

@app.route("/about")
def about():
    #title = '<h1>About</h1>'
    #content = '<a href="/">link</a>'
    #return title+content
    return render_template("about.html")

# start app
if __name__ == '__main__':
    app.run(debug=True)
