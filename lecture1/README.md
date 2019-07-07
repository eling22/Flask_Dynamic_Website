# Flask_Dynamic_Website
to make a dynamic website by flask
## Day1
This is the first day, I learn flask.
today, we build enviroment, make a simple example.

First step, let's build enviroment.

please install following tool:

* Visual Studio Code
* Anaconda(Python)
* Flask(pip install flask)

Second, make a python file.
I create app.py .And,write the following text to app.py .

	from flask import Flask
	print('success')

push run(commond line input :python app.py).  
if you get

`success`

Congratulation~  
It prove your enviroment is fine, and you seccess to import flask to your app.py. You could ready to go next step. 

Third, write the following text to app.py.

	#import flask
	from flask import Flask
	# define app
	app = Flask(__name__)
	
	# define home page route /
	@app.route("/")
	def home():
		return "Home"
	app.run()

after run, you could see :

	 * Serving Flask app "test" (lazy loading)
	 * Environment: production
	   WARNING: Do not use the development
	server in a production environment.
	   Use a production WSGI server instead.
	 * Debug mode: off
	 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`

this time enter `http://127.0.0.1:5000/` to browser, you will see

![image](https://github.com/eling22/Flask_Dynamic_Website/blob/try/picture/lecture1_1.PNG)