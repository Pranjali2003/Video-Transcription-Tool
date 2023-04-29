from django.shortcuts import render
import requests
from video_transcription_app.models import Video
from django.core.exceptions import ValidationError
from pydub import AudioSegment
import speech_recognition as sr
import uuid
# Create your views here.
def index(request):
    # Video.objects.all().delete()
    return render(request,'transcribe_video.html')

def transcribe_video(request):
    try:
        print(len(Video.objects.all()))
        if request.method=='POST':
            url=request.POST.get('video_url')
            response=requests.get(url,stream=True)
            #path to save video
            video_path='./downloaded_video/video_file/video'+str(uuid.uuid4())+'.mp4'

            if response.ok:
                #video model instance
                url_exist=Video.objects.filter(video_url=url)
                if not url_exist:
                    video_object=Video()
                    video_object.video_url=url
                    video_object.save()
                #downloading and saving video 

                with open(video_path,'wb') as f:
                    if response.content:
                        f.write(response.content)
                #function which return transcript after processing audio file
                transcript=extracting_transcript_from_video(video_path)
                update_transcript=Video.objects.filter(video_url=url).update(transcript=transcript)
                return render(request,'transcription_result.html',{'url':transcript})
            else:
                return render(request,'transcription_result.html',{'url':'Something Went wrong please try after sometime!'})
    except ValidationError as e:
        return render(request,'transcription_result.html',{url:'Passed url does not contain the complete information!'})

        



def extracting_transcript_from_video(video):
    try:
        #video file
        video_file=AudioSegment.from_file(video,"mp4")
        #export audio
        audio_file_path="./downloaded_video/audio_file/audio"+str(uuid.uuid4())+".wav"
        audio_file=video_file.export(audio_file_path,format="wav")
        #speech recognition object
        recognizer=sr.Recognizer()
        #read the audio file
        transcribe_audio=sr.AudioFile(audio_file_path)
        #transcribing text from audio file
        with transcribe_audio as audio:
            transcript=recognizer.record(audio)
        transcript_text=recognizer.recognize_google(transcript)
        print(transcript_text)
        return transcript_text
    except FileNotFoundError:
        return "Something Went wrong requested file not found!"