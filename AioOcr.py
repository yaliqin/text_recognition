# """ baidu OCR API with location information """

# coding:utf-8
import requests
import base64
from generate_key import gen_key
import os
from os import path
import sys
import constants
import re


sys.path.append(os.getcwd())
sys.path.append(path.abspath('/Users/ally/Documents/python/split_image/'))

from split_image import split_image

# input_file = '/Users/ally/Documents/python/baidu_ocr/'+str(file_number)+'.png'
# output_file = '/Users/ally/Documents/python/baidu_ocr/output'+str(file_number)+'.txt'


def baidu_ocr(img_input_file, output_path):
    access_token=gen_key(constants.API_KEY,constants.SECRET_KEY)
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate?access_token=' + access_token
    # read image files in current directory
    # for entry in os.scandir():
    #     if entry.name.endswith('.png') and entry.is_file():
    #         img_input_file = entry.name
    #         txt_output_file = 'text_'+ entry.name + '.txt'
    #         location_output_file ='location_'+ entry.name + '.txt'
    file = os.path.basename(img_input_file)
    path = os.path.dirname(img_input_file)

    txt_output_file = os.path.join(output_path + 'text_'+ file + '.txt')
    location_output_file =os.path.join(output_path + 'location_'+ file + '.txt')

    f = open(img_input_file, 'rb')
    img = base64.b64encode(f.read())
    body = {"image":img, "image_type":"BASE64","group_id":"0001", "user_id":"00001" }
    r=requests.post(url,data=body)
    contents = r.json()
    words = []
    tops=[]
    lefts =[]
    widths=[]
    heights = []
    locations=()

    if (contents):
        # print(content)
        raw_content = contents["words_result"]
        # organize
        for item in raw_content:
            location = item['location']
            top = location['top']
            left = location['left']
            width = location['width']
            height = location['height']
            # locations.append(top)
            tops.append(top)
            lefts.append(left)
            widths.append(width)
            heights.append(height)
            words.append(item['words'])
            tmp_tulip = (location['top'], location['left'],location['width'],location['height']),
            # output location information
            locations = locations + tmp_tulip

        f = open(txt_output_file,"w")
        for item in words:
            f.write(item)
            f.write("\n")
        f.close()

        f= open(location_output_file,'w')

        # with open(location_output_file, 'w') as fp:
        #     fp.write('\n'.join('{} {} {} {}'.format(x[0],x[1],x[2],x[3]) for x in locations)
        for item in locations:
            for data in item:
                f.write(str(data))
                f.write(',')
            f.write("\n")
        f.close()

    return location_output_file,txt_output_file


def text_block_split(txt_input_file, problem_pattern,output_path):
    line_number = []
    output_file_num = 0

    f1 = open(txt_input_file, 'r')
    lines_1 = f1.readlines()
    f1.close()
    line_count = 0
    block_count = 0
    file = os.path.basename(img_input_file)

    for line in lines_1: #get the problem start line number
        match_result = re.match(problem_pattern,line)
        if match_result:
            line_number.append(line_count)
            if block_count > 0:
                txt_output_file = os.path.join(output_path,'split_'+file+("%d.txt" %output_file_num))
                f2 = open(txt_output_file,'w')
                write_line_number = line_number[block_count] - line_number[block_count-1]
                for i in range(write_line_number):
                    f2.write(lines_1[line_number[block_count-1]+i])
                f2.close()
                output_file_num += 1
            block_count += 1
        line_count += 1

    line_number.append(line_count-1)  #add last line number for end of last block
    if block_count == 1: # only one block, output file should copy all content of input file
        txt_output_file = os.path.join(output_path,'split_'+file+("%d.txt" %output_file_num))
        # txt_output_file = os.path.join('split_'+txt_input_file+("%d.txt" %output_file_num))
        f2 = open(txt_output_file,'w')
        for i in range(line_count-line_number[0]):
            f2.write(lines_1[line_number[0]+i])
        f2.close()
    elif block_count == 0:
        print('input wrong problem pattern')
    else: #output last block
        txt_output_file = os.path.join(output_path,'split_'+file+("%d.txt" %output_file_num))
        f2 = open(txt_output_file,'w')
        for i in range(line_number[block_count]-line_number[block_count-1]):
            f2.write(lines_1[line_number[block_count-1]+i])
        f2.write(lines_1[line_number[block_count]]) #last line of line_number can't be reached in for loop
        f2.close()
    return line_number

# generage box location file based on baidu OCR output location
# baidu OCR location file is organized as [top, left, width, height]
# so input_location_file stores each identified text line location information
# line_number stores text block start line number
# to crop image, the location should be stored as left,up,right,lower
def gen_block_box(line_number, input_location_file,output_path):
    with open(input_location_file, 'r') as ins:
        right_position = []
        lower_position = []
        left_position = []
        top_position = []
        for line in ins:
            low_line = line.split(',')
            lower = int(low_line[0])+int(low_line[3])
            right = int(low_line[1])+ int(low_line[2]) #get the lower and right location
            right_position.append(right)
            lower_position.append(lower)

            top = int(low_line[0])
            left = int(low_line[1])
            top_position.append(top)
            left_position.append(left)
    #         line = lines[line_number[i]] # read out txt block location with start line number
    # up_line = line.split(',')
    # top = up_line[0]
    # left = up_line[1]

    # f1 = open(input_location_file, 'r')
    # lines = f1.readlines()  # in each line contain [top, left, width, height]
    # f1.close()

    file = os.path.basename(input_location_file)
    output_location_file = os.path.join(output_path,'for_crop '+file)
    f2 = open(output_location_file, 'w')

    line_size = len(line_number)#line_number's last element is the last line of text file
    for i in range(line_size-1):
        max_right = max(right_position[line_number[i]:line_number[i+1]])
        max_low = max(lower_position[line_number[i]:line_number[i+1]])
        min_left = min(left_position[line_number[i]:line_number[i+1]])
        min_top = min(top_position[line_number[i]:line_number[i+1]])
        if i == line_size-2: #include last line position
            max_low = max(max_low, lower_position[-1])
            max_right = max(max_right, right_position[-1])
        left = str(min_left)
        top = str(min_top)
        lower = str(max_low)
        right = str(max_right) #get the lower and right location
        string = left+','+top +',' + right +',' + lower
        f2.write(string)
        f2.write('\n')
    f2.close()
    return f2.name


if __name__ == '__main__':

    # current_path = sys.path.append(os.getcwd())
    img_input_file = 'amc8.png'
    concated_input_file = 'data/input/'+img_input_file
    output_path = 'data/output/'
    location_file, txt_file = baidu_ocr(concated_input_file, output_path) # extract whole text and location

    amc_pattern = r'^\s*Problem [1-9][0-9]?'
    normal_pattern = r'^\s*[1-9][0-9]?\.'

    # txt_file = 'text_8.jpg.txt'
    # location_file = 'location_8.jpg.txt'
    line_number = text_block_split(txt_file,amc_pattern,output_path) #gen text block from whole text file
    file_name = gen_block_box(line_number,location_file,output_path)
    pattern = re.compile(r'.[a-z]+$')
    img_out_file_prefix=pattern.sub('', img_input_file)
    n=split_image(file_name,concated_input_file,img_out_file_prefix,output_path ) #split orininal image based on text block information
