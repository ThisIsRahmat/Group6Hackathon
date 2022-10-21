
from pyexpat import model
from unittest import result
from flask import Flask, request, url_for, session, render_template, redirect, send_file
from pytube import YouTube
from io import BytesIO
import pandas as pd
import os
import whisper
import openai
from audio import main

openai.api_key = os.getenv("OPENAI_API_KEY")


makeup_data = pd.read_csv("products (1).csv")
brand_products = list(makeup_data['brand_product'].unique())

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def home():
    errors = ""
    if request.method == "POST":
        session['link'] = request.form.get('url') # Getting the URL, using sessions
            # we need to validate if model is empty or not if empty then we need to set it to base
        try:     
            url = YouTube(session['link'])
            url.check_availability() # Checking if the URL is valid
        except:
            return render_template("error.html") # If the URL is invalid, we display an error page.
        result = main(link,model)

        return render_template("download.html", url = url)
    return render_template("index.html", errors=errors)


@app.route("/download", methods = ["GET", "POST"])
def download_audio():
    if request.method == "POST":
        buffer = BytesIO() # Declaring the buffer
        url = YouTube(session['link']) # Getting the URL
        itag = request.form.get("itag") # Get the video resolution 
        global video
        video = url.streams.get_by_itag(itag) # Store the video into a variable

        #get the video audio 
        video_audio = video.streams.filter(only_audio=True).first()
        out_file=video.download(output_path=".")
        base, ext = os.path.splitext(out_file)
        new_file = base+'.mp3'
        os.rename(out_file, new_file)
        a = new_file
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name="Video - YT2Video.mp4", mimetype="video/mp4")
    return redirect(url_for("home"))

def get_audio():
  yt = YouTube(session['link'])
  video = yt.streams.filter(only_audio=True).first()
  out_file=video.download(output_path=".")
  base, ext = os.path.splitext(out_file)
  new_file = base+'.mp3'
  os.rename(out_file, new_file)
  a = new_file
  return a

def get_text(url):
  result = model.transcribe(get_audio(url))
  return result['text']


# ai_prompt ="Extract cosmetic brands from this text"

def gpt3(ai_prompt):
    entity = openai.Completion.create(
        input=result,
        model="text-davinci-002",
        prompt="Extract cosmetic brands from this text",
        temperature=0.3,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0.8,
        presence_penalty=0
        )
    return entity

def match_product(entity):
  matches = {x for x in brand_products if x in entity} #entity is the object been parsed
  return list(matches) 

if __name__ == "__main__":
    app.run(debug=True)
