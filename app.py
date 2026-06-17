from flask import Flask, request
from gtts import gTTS
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os


app = Flask(__name__)


FOLDER_ID = "1RPWcXCCUSAfRv0CPJE5tnOp_MZPuYbeN"


SCOPES = [
    "https://www.googleapis.com/auth/drive"
]


credentials = service_account.Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)


drive = build(
    "drive",
    "v3",
    credentials=credentials
)



@app.route("/")
def home():

    return "Hindi TTS Bot Running"



@app.route("/tts", methods=["POST"])
def tts():

    text = request.json["text"]


    filename = "final.mp3"



    voice = gTTS(
        text=text,
        lang="hi"
    )


    voice.save(filename)



    file_metadata = {

        "name": filename,

        "parents": [
            FOLDER_ID
        ]

    }



    media = MediaFileUpload(
        filename,
        mimetype="audio/mpeg"
    )



    upload = drive.files().create(

        body=file_metadata,

        media_body=media,

        fields="id"

    ).execute()



    return {

        "status":"success",

        "drive_file_id": upload["id"]

    }




if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
