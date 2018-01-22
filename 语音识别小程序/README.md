## 一、功能概述
实现语音为文字，可以扩展到多种场景进行工作，这里只实现其基本的语言接收及转换功能。
在语言录入时，根据语言内容的多少与停顿时间，自动截取音频进行转换。
工作示例：
![](https://github.com/mxbq/DreamPath/blob/master/%E8%AF%AD%E9%9F%B3%E8%AF%86%E5%88%AB%E5%B0%8F%E7%A8%8B%E5%BA%8F/getImage.png)

## 二、软件环境

 - 操作系统：win10
 - 语言：Python 版本：3.6.0
 - Python库：AipSpeech(百度语音识别SDK客户端），wave，PyAudio，paInt16

###Python库安装：除百度为：pip install baidu-aip，其他直接 pip install *（库名） 即可。
 
## 三、原理概述

利用wave，PyAudio搭建一个wav格式的简易录音机，基于百度API进行wav格式的音频转文本。

 - 简易录音机类（WWAV）有__save_wave_file音频文件保存方法与my_record音频录制方法。在录制音频的方法中，加入了有效音频测试的代码，可以测试一小段时间内是否有有效音频输入，否则退出音频录制。
 - 转换类（Translation）则为__get_file_content方法与get_word音频转换主方法。

## 四、核心代码

### my_record音频录制方法（WWAV类）
录制的音频保存在两个独立的音频源中，一个是my_buf主音频源，一个是buf测试音频源，主音频的最长录制时间为TIME，测试音频源的标准时间为INTERVAL，每录满一个测试音频源即将其进行转文本操作，如果音频源有效，则主音频源继续录入；否则主音频源录制停止。录制时间中，输出“ . ”以检测程序动态。

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
            my_buf.append(string_audio_data) # 将其添加入my_buf列表中
            
            if i < INTERVAL*2: # 判断是否达到间隔时间
                buf.append(string_audio_data)
                i += 1
            elif i == INTERVAL*2:
                self.__save_wave_file('00.wav',buf) # 保存测试音频
                err,a = tr.get_word('00.wav') # 得到测试音频是否有效
                if err == 0:
                    break
                i = 0 # 初始化
                buf = [] # 同上
        
            print('.',end = ' ') # 表示程序进行中
        self.__save_wave_file('01.wav',my_buf)
        stream.close()
        
### get_word音频转换方法（Translation类）
音频转文字，参数filePath为wav音频地址，返回双值：状态(1为转换成功)及转换后文本或错误信息。首先输入音频与参数，得到返回文本word，然后分析word，确定返回值内容。

    def get_word(self,filePath):
        '''音频转文字，参数filePath为wav音频地址，返回双值：状态(1为转换成功)及转换后文本或错误信息'''
        word = self.__client.asr(self.__get_file_content(filePath),'wav',8000,{
            'lan': 'zh'
            }) # 参数：语音对象，文件格式，采样率，语种类型
    
        if word['err_no'] == 0: # 错误值为0（即正确）
            return 1,word['result'][0] # 返回 1 与 文本信息
        else:
            return 0,word['err_no'] # 否则返回 0 与 错误内容
            
## 源码

[GitHub地址](https://github.com/mxbq/DreamPath/tree/master/%E8%AF%AD%E9%9F%B3%E8%AF%86%E5%88%AB%E5%B0%8F%E7%A8%8B%E5%BA%8F)
