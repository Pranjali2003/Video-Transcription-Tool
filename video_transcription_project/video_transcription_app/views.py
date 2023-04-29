from django.shortcuts import render
import requests
from video_transcription_app.models import Video
from pydub import AudioSegment
import speech_recognition as sr
#for downloading video from google drive with the file id
import gdown
# Create your views here.
def index(request):
    return render(request,'transcribe_video.html')

def transcribe_video(request):
    if request.method=='POST':
        url=request.POST.get('video_url')
        
        #to download using google drive link
        # gdown.download(url,'video.mp4',quiet=False)
        # video_object=Video()
        # video_object.video_url=url
        # video_object.save()

        # response=requests.get(url,stream=True)
        # if response.ok:
        #     with open('./downloaded_video/test_video.mp4','wb') as f:
        #         f.write(response.content)
        # else:
        #     print('Somethings went wrong try after some time!')

        video_path='./downloaded_video/test_video.mp4'
        transcript=extracting_transcript_from_video(video_path)
        print(transcript)
        return render(request,'transcription_result.html',{'url':transcript})



def extracting_transcript_from_video(video):
    try:
        #video file
        
        video_file=AudioSegment.from_file(video,"mp4")
        #export audio
        audio_file=video_file.export("./downloaded_video/audio.wav",format="wav")

        #speech recognition object
        recognizer=sr.Recognizer()
        #read the audio file
        transcribe_audio=sr.AudioFile('./downloaded_video/audio.wav')

        #transcribing text from audio file
        with transcribe_audio as audio:
            transcript=recognizer.record(audio)

        transcript_text=recognizer.recognize_google(transcript)
        print(transcript_text)
        return transcript_text
    except FileNotFoundError:
        return "Something Went wrong requested file not found!"