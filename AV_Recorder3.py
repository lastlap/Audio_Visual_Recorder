import time
# import numpy as np
import cv2
import speech_recognition as sr
import threading
import subprocess, os
# from Video_Rec import VideoRecorder
# from Audio_Rec import AudioRecorder

class VideoRecorder:

    def __init__(self):
        self.vid_capture = None
        self.output = []
        self.video = None
        self.read = True

    def record(self):
        self.vid_capture = cv2.VideoCapture(0)
        # vid_cod = cv2.VideoWriter_fourcc(*'XVID')
        # self.output = cv2.VideoWriter("./cam_video.mp4", vid_cod, 16.0, (640,480))
        # time.sleep(1)
        while(self.read):
            ret, frame = self.vid_capture.read()
            self.output.append(frame)
            # if cv2.waitKey(1) &0XFF == ord('x'):
            #     break
    def save_output(self):
        vid_cod = cv2.VideoWriter_fourcc(*'mp4v')
        height, width, layers = self.output[0].shape
        self.video = cv2.VideoWriter("test.mp4", vid_cod, 16.0, (width,height))
        for image in self.output:
            self.video.write(image)
        self.video.release()

    def start(self):
        video_thread = threading.Thread(target=self.record)
        video_thread.start()

    def stop(self):
        cv2.destroyAllWindows()
        self.vid_capture.release()
        # self.output.release()

class AudioRecorder:

    def __init__(self):
        self.r = sr.Recognizer()
        self.audio = None

    def record(self):
        with sr.Microphone() as source:
            print('Listening...')
            self.r.adjust_for_ambient_noise(source, duration=1)
            self.audio = self.r.listen(source)
    
    def save_output(self):
        with open('test.wav','wb') as file:
            file.write(self.audio.get_wav_data())

    def start(self):
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()


def av_record():
    video_thread = VideoRecorder()
    audio_thread = AudioRecorder()

    video_thread.start()
    time.sleep(1.5)
    audio_thread.record()
    video_thread.read = False
    
    video_thread.stop()

    # removing previous files
    if os.path.isfile('test.wav'): os.remove('test.wav') 
    if os.path.isfile('test.mp4'): os.remove('test.mp4') 
    if os.path.isfile('output.mp4'): os.remove('output.mp4')

    video_thread.save_output()
    audio_thread.save_output()

    # merging audio and video
    cmd = 'ffmpeg -i test.mp4 -i test.wav -c:v copy -c:a aac output.mp4'
    subprocess.call(cmd,shell=True)

def main():
  av_record()

if __name__ =='__main__':
  main()