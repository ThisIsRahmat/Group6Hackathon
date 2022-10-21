
from pyexpat import model
from flask import Flask, request, url_for, session, render_template, redirect, send_file
from pytube import YouTube
from io import BytesIO
import 

# import pixellib
# from pixellib.instance import instance_segmentation
import os
import whisper

model = whisper.load_model("base")
# summarizer = pipeline("summarization")


url = input("paste a youtube link: ")

def get_audio(url):
  yt = YouTube(url)
  video = yt.streams.filter(only_audio=True).first()
  out_file=video.download(output_path=".")
  base, ext = os.path.splitext(out_file)
  new_file = base+'.mp3'
  os.rename(out_file, new_file)
  a = new_file
  return a


result = model.transcribe(get_audio(url))
# return(result['text'])

print(result['text'])
