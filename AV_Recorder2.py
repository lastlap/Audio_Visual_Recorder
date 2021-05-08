import time
# import numpy as np
import cv2
import speech_recognition as sr
import threading
import subprocess, os
# from Video_Rec import VideoRecorder
# from Audio_Rec import AudioRecorder

import cv2
import threading

import pyaudio
import wave
import sys

class VideoRecorder:

    def __init__(self):
        self.vid_capture = None
        self.output = []
        self.video = None
        self.read = True
        self.filename = 'test2.mp4'

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
        self.video = cv2.VideoWriter(self.filename, vid_cod, 16.0, (width,height))
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
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.record_seconds = 5
        self.audio = None
        self.filename = 'test2.wav'
        self.p = pyaudio.PyAudio()
        self.all = []

    def record(self):        
        stream = self.p.open(format = self.format, 
                        channels = self.channels, 
                        rate = self.rate, 
                        input = True, 
                        frames_per_buffer = self.chunk)
        print('Listening')
        for i in range(0, int(self.rate/self.chunk * self.record_seconds)):
            data = stream.read(self.chunk)
            self.all.append(data)
    
        stream.close()
        self.p.terminate()
    
    def save_output(self):
        data = b''.join(self.all)
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(data)
        wf.close()


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
    if os.path.isfile('test2.wav'): os.remove('test2.wav') 
    if os.path.isfile('test2.mp4'): os.remove('test2.mp4') 
    if os.path.isfile('output2.mp4'): os.remove('output2.mp4')

    video_thread.save_output()
    audio_thread.save_output()
    
    # merging audio and video
    cmd = 'ffmpeg -i test2.mp4 -i test2.wav -c:v copy -c:a aac output2.mp4'
    subprocess.call(cmd,shell=True)

def main():
    av_record()

if __name__ =='__main__':
    main()