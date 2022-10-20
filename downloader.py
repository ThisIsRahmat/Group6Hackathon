
# from flask import Flask, request, url_for, session
# from pytube import YouTube
# app = Flask(__name__)
# app.config['SECRET_KEY'] = "your_secret_key"
# @app.route("/", methods = ["GET", "POST"])
# def home():
#     if request.method == "POST":
#         session['link'] = request.form.get('url') # Getting the URL, using sessions
#         try:
#             url = YouTube(session['link'])
#             url.check_availability() # Checking if the URL is valid
#         except:
#             return render_template("error.html") # If the URL is invalid, we display an error page.
#         return render_template("shop.html", url = url)
#     return render_template("index.html")