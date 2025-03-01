# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import json
import os
import re
import time
from datetime import datetime

import requests
import urllib

lfasr_host = 'https://raasr.xfyun.cn/v2/api'
# 请求的接口名
api_upload = '/upload'
api_get_result = '/getResult'


class RequestApi(object):
    def __init__(self, appid, secret_key, upload_file_path):
        self.appid = appid
        self.secret_key = secret_key
        self.upload_file_path = upload_file_path
        self.ts = str(int(time.time()))
        self.signa = self.get_signa()

    def get_signa(self):
        appid = self.appid
        secret_key = self.secret_key
        m2 = hashlib.md5()
        m2.update((appid + self.ts).encode('utf-8'))
        md5 = m2.hexdigest()
        md5 = bytes(md5, encoding='utf-8')
        # 以secret_key为key, 上面的md5为msg， 使用hashlib.sha1加密结果为signa
        signa = hmac.new(secret_key.encode('utf-8'), md5, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        return signa

    def upload(self):
        # print("上传部分：")
        upload_file_path = self.upload_file_path
        file_len = os.path.getsize(upload_file_path)
        file_name = os.path.basename(upload_file_path)

        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict["fileSize"] = file_len
        param_dict["fileName"] = file_name
        param_dict["duration"] = "200"
        # print("upload参数：", param_dict)
        data = open(upload_file_path, 'rb').read(file_len)

        response = requests.post(url=lfasr_host + api_upload + "?" + urllib.parse.urlencode(param_dict),
                                 headers={"Content-type": "application/json"}, data=data)
        # print("upload_url:",response.request.url)
        result = json.loads(response.text)
        # print("upload resp:", result)
        return result

    def get_result(self):
        uploadresp = self.upload()
        orderId = uploadresp['content']['orderId']
        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict['orderId'] = orderId
        param_dict['resultType'] = "transfer,predict"
        # print("")
        # print("查询部分：")
        # print("get result参数：", param_dict)
        status = 3
        # 建议使用回调的方式查询结果，查询接口有请求频率限制
        while status == 3:
            response = requests.post(url=lfasr_host + api_get_result + "?" + urllib.parse.urlencode(param_dict),
                                     headers={"Content-type": "application/json"})
            # print("get_result_url:",response.request.url)
            result = json.loads(response.text)
            # print(result)
            status = result['content']['orderInfo']['status']
            # print("status=",status)
            if status == 4:
                break
            time.sleep(5)
        # print("get_result resp:",result)
        with open("temp/temp.json", 'w', encoding='utf-8') as f:
            json.dump(result, f)
            f.close()

        return result

def seconds_to_hhmmss(seconds):
    seconds=float(seconds)
    seconds=seconds*0.001
    dt = datetime.utcfromtimestamp(seconds)
    time_str = dt.strftime('%H:%M:%S.%f')[:-3]
    return time_str
def json_analysis(text_file):
    f = open('temp/temp.json', 'r')
    content = f.read()
    all = json.loads(content)
    f.close()
    text = all['content']
    text = json.loads(text['orderResult'])['lattice']
    out_text = []
    out_time_ss = []
    out_time_to = []
    for i in text:
        pattern = re.compile(r'"w":"(.*?)"')
        pattern_list = pattern.findall(i['json_1best'])
        sentence = ''
        for letter in pattern_list:
            sentence += letter
        out_text.append(sentence)
        pattern_ss = re.compile(r'"bg":"(.*?)"')
        pattern_list_ss = pattern_ss.findall(i['json_1best'])
        for temp in pattern_list_ss:
            out_time_ss.append(seconds_to_hhmmss(temp))
            # out_time_ss.append(seconds_to_hhmmss(temp)[:-4])
        pattern_to = re.compile(r'"ed":"(.*?)"')
        pattern_list_to = pattern_to.findall(i['json_1best'])
        for temp in pattern_list_to:
            out_time_to.append(seconds_to_hhmmss(temp))
            # out_time_to.append(seconds_to_hhmmss(temp)[:-4])

    # print(len(out_text),len(out_time_to),len(out_time_ss))
    # for i in range(len(out_text)):
    #     print(out_time_ss[i],out_time_to[i],out_text[i])

    with open(text_file, 'w') as f:
        for i in range(len(out_text)):
            f.write(f'{out_time_ss[i]},{out_time_to[i]},{out_text[i]}\n')
    return out_time_ss, out_time_to, out_text


def my_xunfei(upload_file_path=r"audio/test.wav", out_text_file='tet.txt'):
    try:
        api = RequestApi(appid="60f4d417",
                         secret_key="7a3e2c6efd3e489fee0528dcfe1d4519",
                         upload_file_path=upload_file_path)
    except:
        print("上传失败")
    print('上传成功，请等待！(10分钟内视频，处理时间在3分钟内)')
    try:
        api.get_result()
    except:
        print('提取失败')
    print('提取成功，解析保存中！')

    try:
        out_time_ss, out_time_to, out_text=json_analysis(out_text_file)
    except:
        print('解析失败')
    print('提取保存成功！')
    return out_time_ss, out_time_to, out_text


# 输入讯飞开放平台的appid，secret_key和待转写的文件路径
if __name__ == '__main__':
    # api = RequestApi(appid="60f4d417",
    #                  secret_key="7a3e2c6efd3e489fee0528dcfe1d4519",
    #                  upload_file_path=r"audio/test.wav")
    #
    # api.get_result()
    my_xunfei(upload_file_path=r"test.wav", out_text_file='tet.txt')
