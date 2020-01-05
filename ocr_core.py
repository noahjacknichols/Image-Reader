from lxml import html, etree
from pathlib import Path
import cv2
import requests
import os
import pytesseract
try:
    from PIL import Image
except:
    print("error occured")

if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

'''
TODO:
-> Look for some kind of multipurpose classification model, or try to build my own..
-> Documenting and saving functions (implement tagging if possible)
'''

# print(ocr_core('images/ocr_example_1.jpg'))

def getImageLinks(website):
    page = requests.get(website)
    extractedHtml = html.fromstring(page.content)
    imageSrc = extractedHtml.xpath("//img/@src")
    # print(imageSrc)

    imageDomain = website.rsplit('/',1)
    imageLinks = []
    for image in range(len(imageSrc)):
        if imageSrc[0].startswith("http"):
            imageLink = imageSrc[image]
        else:
            imageLink = str(imageDomain[image]) + str(imageSrc[image])

        imageLinks.append(imageLink)
    return imageLinks

'''
will scan a directory or by default images/scrapedImages for files.
check if file contains popular image extensions, and then
returns a list of strings of possible image filenames.
'''
def getLocalImages(directory = 'images/scrapedImages/'):
    fileTypes = ['.png', '.jpg', '.jpeg', '.tif']
    localFiles = [str(file) for file in os.listdir(directory)]
    images = []
    for file in localFiles:
        if any(fileType in file for fileType in fileTypes):
            images.append(file)
    localImages = [directory + str(image) for image in images]
    return localImages 
    
def downloadImage(imageLink):
    # print("image:",imageLink)
    try:
        filename = imageLink.split("/")[-1]
        rawImage = requests.get(imageLink, stream=True)
        folder = "images/scrapedImages/" 
        writeLocation = folder+filename
        with open(writeLocation,'wb') as fd:
            for chunk in rawImage.iter_content(chunk_size=1024):
                fd.write(chunk)
    except:
        print("Issue occured while getting image {}".format(filename))
    return

def grayscaleImage(image):
    img = cv2.imread(image)
    grayScaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(grayScaled, 127, 255, cv2.THRESH_BINARY)
    cv2.imshow('thresh',thresh)
    cv2.imshow('Original image', img)
    cv2.imshow('Gray image', grayScaled)
    cv2.waitKey(0)
    
    return Image.fromarray(grayScaled)

#image must be a PIL image
def getImageText(image):
    text = pytesseract.image_to_string(image)
    return text

def saveText(title, text, location = '/text/',attachment = '.txt'):
    location = os.getcwd() + location + attachment
    Path(location).mkdir(parents=True, exist_ok=True)
    with open(location+title, 'w', encoding='UTF-8') as file:
        file.write(text)
    return

def main():
    imageLinks = getImageLinks("https://twitter.com/imgur?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor")
    for link in imageLinks:
        print("link:", link)
    try:
        for image in imageLinks[:10]:
            downloadImage(image)
    except:
        print("Seems to be an issue downloading images from the website.")
# downloadImage("https://scontent.fykz1-2.fna.fbcdn.net/v/t1.0-1/p720x720/37761468_10157914956042588_4029176324378591232_n.jpg")

# print(os.getcwd())
saveText('title',getImageText('images/text.png'))

