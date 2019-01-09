# """ baidu OCR API with location information """

# coding:utf-8
import requests
import base64
from generate_key import gen_key
import os
import sys
import constants


sys.path.append(os.getcwd())

# input_file = '/Users/ally/Documents/python/baidu_ocr/'+str(file_number)+'.png'
# output_file = '/Users/ally/Documents/python/baidu_ocr/output'+str(file_number)+'.txt'

def baidu_ocr():
    access_token=gen_key(constants.API_KEY,constants.SECRET_KEY)
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate?access_token=' + access_token
    # read image files in current directory
    for entry in os.scandir():
        if entry.name.endswith('.png') and entry.is_file():
            input_file = entry.name
            output_file = entry.name + '.txt'

        # 二进制方式打开图文件
            f = open(input_file, 'rb')
            # 参数image：图像base64编码
            img = base64.b64encode(f.read())
            body = {"image":img, "image_type":"BASE64","group_id":"0001", "user_id":"00001" }
            r=requests.post(url,data=body)
            contents = r.json()
            locations = [] # location to store the identified location
            words = []
            top=[]
            left =[]
            new_word=()

            if (contents):
                # print(content)
                raw_content = contents["words_result"]
                for item in raw_content:
                    location = item['location']
                    locations.append(location["top"])
                    top.append(location['top'])
                    left.append(location['left'])
                    words.append(item['words'])
                    tmp_tulip = (location['top'], location['left'],item['words']),
                    # sum_height_width.append(location['top']+location['left'])
                    new_word = new_word + tmp_tulip
                # new_word_1=sorted(new_word, key=lambda item: item[0])
                # new_sum = sorted(sum_height_width)
                # print(sum_height_width)
                # print(new_sum)
                f = open(output_file,"w")
                for item in words:
                    f.write(item)
                    f.write("\n")
                f.close()


baidu_ocr()