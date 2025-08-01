import time
from multiprocessing import Process
import yaml
import os
import threading
import ffmpeg
from picamera2 import Picamera2
from picamera2.encoders import Quality, H264Encoder
from picamera2.outputs import CircularOutput

import RPi.GPIO as GPIO

import queue




class eventRecorder:

    def __init__(self, settingsFile):
        self.picamera = Picamera2()

        self.captureQueue = queue.Queue(10)
        self.convertQueue = queue.Queue(10)
        settings = self.Settings(settingsFile)
        #check if folders exist
        captureFolder = os.path.isdir(settings.captureFolder)
        
        if(not captureFolder):
            os.mkdir(settings.captureFolder)
            
        self.settings = settings

    class Settings:
        def __init__(self, file: str):
            with open(file, 'r') as stream:
                self.settings = yaml.safe_load(stream)

            self.captureFolder = self.settings["project"]["capture_Location"]
            self.id = self.settings["project"]["id"]

    def record(self, buffersize : int, additionalRecording : int = 0):
        
        
        vconfig = self.picamera.create_video_configuration()
        self.picamera.configure(vconfig)
    
        
        while True: 
            encoder = H264Encoder(10000000)
            encoder.output = CircularOutput(buffersize = buffersize, outputtofile=False)  
            
            self.picamera.start()
            self.picamera.start_encoder(encoder)
            
            #wait for event
            t=self.captureQueue.get(block=True)

            filename = self.settings.id+"_"+str(int(t)) + ".h264"
            file = os.path.join(self.settings.captureFolder, filename)
            encoder.output.fileoutput = file
            time.sleep(0.1)
            #start_and record
            encoder.output.start()
            
            #record for n more seconds
            if(additionalRecording > 0):
                time.sleep(additionalRecording)
                
            #stop recording
            encoder.output.stop()
            print("end recording")
            self.picamera.stop_encoder()
            self.picamera.stop()


    def saveEventHW(self,pin, afterCapture = None ):
       
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.IN, pull_up_down=20)

        while True:
            #button press: wait till falling edge
            GPIO.wait_for_edge(pin, GPIO.FALLING)
            
            t = time.time()
            self.captureQueue.put(t)

            #execute in parallel
            if(afterCapture != None):
                afterCapture(t)
            
            
        
    def saveEventSW(self, trigger: queue.Queue, afterCapture = None):
        while True:
            trigger.get(block= True)
            t = time.time()
            self.captureQueue.put(t)

            #execute in parallel
            if(afterCapture != None):
                afterCapture(t)

     def createSaveEventHW(self, pin , afterCapture = None, triggerQueue: queue.Queue = None):
        #triggerQueue unused, added to support faster switching between HW and SW saveEvent
        thread = threading.Thread(target=self.saveEventHW , args= (pin, afterCapture))
        thread.start()

    def createSaveEventSW(self, triggerQueue: queue.Queue, afterCapture = None, pin = None):
        #pin unused, added to support faster switching between HW and SW saveEvent
        thread = threading.Thread(target=self.saveEventSW , args= (triggerQueue, afterCapture))
        thread.start()

    def start(self, buffersizeFrames, additionalRecording):
        thread = threading.Thread(target=self.convert)
        thread.start()
        self.record(buffersize=buffersizeFrames, additionalRecording= additionalRecording)

def main():
#replace with your setup
    modeSwitch = 38
    statusLED = 33
    
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(modeSwitch, GPIO.IN)
    GPIO.setup(statusLED, GPIO.OUT)
    
    if(False): # The following lines are disabled for publishing purposes. Reactivate them for usage
        #replace for your setup
        
        if(GPIO.input(modeSwitch)==0):
            recorder = eventRecorder("Desktop/ChronoVAult/config.yaml")
        
            GPIO.output(statusLED,1)
            recorder.createSaveEventHW(pin = 40, afterCapture= timestamp )
            try:
                recorder.start(buffersizeFrames=500, additionalRecording= 3)
                while(True):
                    pass
            except:
                GPIO.output(statusLED,0)#deactivate led if an error occours

        else:
            print("Fileserver")
            os.system("sudo nmcli con up FileServer")
            while(True):
            	pass
        
        
        
def timestamp(time):
    print("trigger")
    f = open("time.csv", "a")
    #write in csv
    f.write(str(time))
    f.write(",\n")
    f.flush()

if __name__ == '__main__':
    main()
