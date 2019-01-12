# text_recognition
text recognition and paragraph analysis

## what the project does:
1. scan input image and recognize the texts in the image
2. based on input text pattern to split the image into small images and store the texts in each small image to separate text files

## input and output examples:

### input image
 
![alt text](https://github.com/yaliqin/text_recognition/blob/master/data/input/amc8.png?raw=true)

### output image
![alt text](https://github.com/yaliqin/text_recognition/blob/master/data/output/split_image_amc8_0.png?raw=true)
![alt text](https://github.com/yaliqin/text_recognition/blob/master/data/output/split_image_amc8_1.png?raw=true)
![alt text](https://github.com/yaliqin/text_recognition/blob/master/data/output/split_image_amc8_2.png?raw=true)
![alt text](https://github.com/yaliqin/text_recognition/blob/master/data/output/split_image_amc8_3.png?raw=true)
![alt text](https://github.com/yaliqin/text_recognition/blob/master/data/output/split_image_amc8_4.png?raw=true)
![alt text](https://github.com/yaliqin/text_recognition/blob/master/data/output/split_image_amc8_5.png?raw=true)
![alt text](https://github.com/yaliqin/text_recognition/blob/master/data/output/split_image_amc8_6.png?raw=true)
### output text files
you can see the output files in  
https://github.com/yaliqin/text_recognition/blob/master/data/output/split_amc8.png0.txt
https://github.com/yaliqin/text_recognition/blob/master/data/output/split_amc8.png1.txt
https://github.com/yaliqin/text_recognition/blob/master/data/output/split_amc8.png2txt
https://github.com/yaliqin/text_recognition/blob/master/data/output/split_amc8.png3.txt
https://github.com/yaliqin/text_recognition/blob/master/data/output/split_amc8.png4.txt
https://github.com/yaliqin/text_recognition/blob/master/data/output/split_amc8.png5.txt
https://github.com/yaliqin/text_recognition/blob/master/data/output/split_amc8.png6.txt

## how to use the project
AioOcr.py is the main file. Change the input file name and split image pattern in the main function of AioOcr.py
