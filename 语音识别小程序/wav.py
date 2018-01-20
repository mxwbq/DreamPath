# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 20:13:29 2017

@author: mxwbq
"""

import wave
from pyaudio import PyAudio,paInt16
from translation import Translation

class WWAV:
    __framerate = 8000 # 帧速率
    __NUM_SAMPLES = 2000 # pyaudio内置缓冲大小
    __channels = 1 # 通道数
    __sampwidth = 2 # 取样宽度
    def __save_wave_file(self,filename,data):
        '''保存wav格式音频文件'''
        wf=wave.open(filename,'wb')
        wf.setnchannels(self.__channels)
        wf.setsampwidth(self.__sampwidth)
        wf.setframerate(self.__framerate)
        wf.writeframes(b"".join(data)) # 字节
        wf.close()
    
    def my_record(self,TIME = 60,INTERVAL = 5):
        '''录制并保存音频文件，TIME录制时间，INTERVAL测试间隔'''
        pa=PyAudio()
        tr = Translation()
        stream=pa.open(format = paInt16,channels=self.__channels,
                       rate=self.__framerate,input=True,
                       frames_per_buffer=self.__NUM_SAMPLES)
        my_buf=[] # 主音频源
        buf=[] # 测试音频源
        i=0
        while i < TIME*2: #控制录音时间
            string_audio_data = stream.read(self.__NUM_SAMPLES)  # 获取音频片段
            my_buf.append(string_audio_data)
            
            if i < INTERVAL*2:
                buf.append(string_audio_data)
                i += 1
            elif i == INTERVAL*2:
                self.__save_wave_file('00.wav',buf) # 保存测试音频
                err,a = tr.get_word('00.wav') # 得到测试音频是否有效
                if err == 0:
                    break
                i = 0 # 初始化
                buf = [] # 同上
        
            print('.',end = ' ')
        self.__save_wave_file('01.wav',my_buf)
        stream.close()
    
    def __init__(self):
        pass