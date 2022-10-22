
# from pyexpat import model
# from flask import Flask, request, url_for, session, render_template, redirect, send_file
# from pytube import YouTube
# from io import BytesIO
# import openai

# # import pixellib
# # from pixellib.instance import instance_segmentation
# import os
# import whisper

# import pytube
# from moviepy.editor import VideoFileClip
# import os

# import static_ffmpeg

# openai.api_key = os.getenv("OPENAI_API_KEY")


# url = input("Insert a Youtube Link: ")

# def download_video(url):
#     video = pytube.YouTube(url)
#     stream = video.streams.get_by_itag(18)
#     stream.download()
#     return stream.default_filename

# def convert_to_mp3(filename):
#     clip = VideoFileClip(filename)
#     clip.audio.write_audiofile(filename[:-4] + ".mp3")
#     clip.close()

# def AudiotoText(filename):
#     model = whisper.load_model("base")
#     result = model.transcribe(filename)
#     print(result["text"])
#     sonuc = result["text"]
#     return sonuc

# def main(link, model):
#     print('''
#     This tool will convert Youtube videos to mp3 files and then transcribe them to text using Whisper.
#     ''')
#     print("URL: " + link)
#     print("MODEL: " + model)
#     # FFMPEG installed on first use.
#     print("Initializing FFMPEG...")
#     static_ffmpeg.add_paths()

#     print("Downloading video... Please wait.")
#     try:
#         filename = download_video(link)
#         print("Downloaded video as " + filename)
#     except:
#         print("Not a valid link..")
#         return
#     try:
#         convert_to_mp3(filename)
#         print("Converted video to mp3")
#     except:
#         print("Error converting video to mp3")
#         return
#     try:
#         mymodel = pywhisper.load_model(model)
#         global result 
#         result = mymodel.transcribe(filename[:-4] + ".mp3")
#         print(result["text"])
#         result = result["text"]
#         os.remove(filename)
#         os.remove(filename[:-4] + ".mp3")
#         print("Removed video and audio files")
#         print("Done!")
        
#         return result
#     except Exception as e:
#         print("Error transcribing audio to text")
#         print(e)
#         return



# def gpt3(ai_prompt):
#     entity = openai.Completion.create(
#         input=result,
#         model="text-davinci-002",
#         prompt="Extract cosmetic brands from this text",
#         temperature=0.3,
#         max_tokens=60,
#         top_p=1,
#         frequency_penalty=0.8,
#         presence_penalty=0
#         )
#     return entity

# def match_product(entity):
#   matches = {x for x in brand_products if x in entity} #entity is the object been parsed
#   return list(matches) 

# if __name__ == "__main__":
#     main()
