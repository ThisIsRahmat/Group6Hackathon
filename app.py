from glob import glob
from pyexpat import model
from unittest import result
from flask import Flask, request, url_for, session, render_template, redirect, send_file
from pytube import YouTube
from io import BytesIO
import pandas
import os
import whisper
import openai
import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
# from get_shop_link import get_source
import json
import serpapi
from serpapi import GoogleSearch


openai.api_key = os.getenv("OPENAI_API_KEY")
makeup_data = pandas.read_csv("products (1).csv")
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
        # result = main(link,model)
        return render_template("shopper.html")
    return render_template("index.html", errors=errors)

def download_audio():
        buffer = BytesIO() # Declaring the buffer
        print(YouTube(session['link']))
        url = YouTube(session['link']) # Getting the URL
        itag = request.form.get("itag") # Get the video resolution 
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



#Gets Transcript from the YT video audio
def get_text(video_audio):
  result = model.transcribe(video_audio)
  return result['text']

#GPT-3 Prompt that extracts the Makeup producst from the transcript data



def gpt3(transcript):
    entity = openai.Completion.create(
        input=transcript,
        model="text-davinci-002",
        prompt="Extract cosmetic brands from this text",
        temperature=0.3,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0.8,
        presence_penalty=0
        )
    return entity


#function that matches the extratced beauty products with the brand_products dataset we have 

def match_product(entity):
  matches = {x for x in brand_products if x in entity} #entity is the object been parsed
  return list(matches) 


def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

#This function searches google with the beauty products we have extracted

 
def scrape_google(queries):
  for query in queries:
    params = {
    "api_key": os.getenv("GOOGLE_SEARCH_API"),
    "engine": "google",
    "q": query,
    "gl": "us",
    "hl": "en",
    "tbm": "shop"
  }
 
  search = GoogleSearch(params)
  results = search.get_dict()


# This gives the shopping results from the google search
 
  for shopping_result in results['shopping_results']:
      return json.dumps(shopping_result, indent=2, ensure_ascii=False)
 



#video_audio = download_audio()
#transcript = get_text(video_audio)
#gpt3result = gpt3(transcript)
#matches = match_product(gpt3result)
#shop_items = scrape_google(matches)


# @app.route("/shop", methods = ["GET", "POST"])
# def return_shop():
#     if request.method == "GET":
#         video_audio = download_audio()
#         transcript = get_text(video_audio)
#         gpt3result = gpt3(transcript)
#         matches = match_product(gpt3result)
#         shop_items = scrape_google(matches)
#         print(shop_items)
#     return render_template("shop.html", shop_items=shop_items)


#this function runs all the previous functions and returns the data in a .json that is then represented in shop.html file
@app.route("/shop", methods = ["GET", "POST"])
def return_shop():
    if request.method == "GET":
        video_audio = download_audio()
        transcript = get_text(video_audio)
        gpt3result = gpt3(transcript)
        matches = match_product(gpt3result)
        shop_items = scrape_google(matches)
        # print(shop_items)
        with open('file.json', 'w') as f:
            json.dump(shop_items, f)
    return render_template("shop.html", shop_items=shop_items)




# @app.route("/")
# def hello():
#     return "Hello World!"


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
