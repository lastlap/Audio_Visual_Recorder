# Audio Visual Recorder

Records Audio and Video simultaneously using Python3

## Requirements

System packages:

	ffmpeg == 4.2.4
	python == 3.8.5
	
Python packages:

	opencv-python == 4.5.2.52
	SpeechRecognition == 3.8.1
	pyaudio == 0.2.11
	
## Project Structure

`AV_Recorder1.py` - Records Audio and Video simultaneously until Ctrl+C is called. Saves the video file as test1.mp4, the audio file as test1.wav and the merged output as output1.mp4

`AV_Recorder2.py` - Records Audio and Video upto given time(5 seconds here). Saves the video file as test2.mp4, the audio file as test2.wav and the merged output as output2.mp4

`AV_Recorder3.py` - Records Audio and Video simultaneously until speaker stops speaking. Saves the video file as test.mp4, the audio file as test.wav and the merged output as output.mp4
