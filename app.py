
from flask import Flask, request, url_for, session, render_template, redirect, send_file
from pytube import YouTube
from io import BytesIO
import banana_dev as banana
import pixellib
from pixellib.instance import instance_segmentation

#Save it as a secure variable later
api_key={YOUR API KEY}

#Defining the model to run 
model_key="carrot"
model_parameters = {
                    "text":"is this a makeup item?", #text for QA / Similarity
                    "imageURL":video, #image for the model
                    "similarity":False, #whether to return text-image similarity
                    "maxLength":100, #max length of the generation
                    "minLength":30 #min length of the generation
                    }

#To generate captions, only send the image in model_parameters

out = banana.run(api_key, model_key, model_parameters)
print(out)


app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        session['link'] = request.form.get('url') # Getting the URL, using sessions
        try:
            url = YouTube(session['link'])
            url.check_availability() # Checking if the URL is valid
        except:
            return render_template("error.html") # If the URL is invalid, we display an error page.
        return render_template("download.html", url = url)
    return render_template("index.html")

@app.route("/download", methods = ["GET", "POST"])
def download_video():
    if request.method == "POST":
        buffer = BytesIO() # Declaring the buffer
        url = YouTube(session['link']) # Getting the URL
        itag = request.form.get("itag") # Get the video resolution 
        global video
        video = url.streams.get_by_itag(itag) # Store the video into a variable

        #segment the video
        segment_video = instance_segmentation()
        segment_video.load_model

        # Setting the file path for the input video
input_video_file_path = "videos/test_video.mp4"
# Creating an instance_segmentation object
segment_video = instance_segmentation()
# Loading the Mask R-CNN model trained on the COCO dataset
segment_video.load_model("mask_rcnn_coco.h5")
# Processing the video
segment_video.process_video(
    input_video_file_path, 
    show_bboxes=True, 
    extract_segmented_objects=True, 
    save_extracted_objects=False,
    frames_per_second=30,
    output_video_name="videos/instance_segmentation_output.mp4",
)

        



        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name="Video - YT2Video.mp4", mimetype="video/mp4")
    return redirect(url_for("home"))


@app.route(/)

if __name__ == "__main__":
    app.run(debug=True)