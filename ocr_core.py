from lxml import html, etree
import requests
import os
import pytesseract
try:
    from PIL import Image
except:
    print("error occured")

if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



def filterImage(image):
    return image


def ocr_core(filename):
    text = pytesseract.image_to_string(Image.open(filename))
    return text

print(ocr_core('images/ocr_example_1.jpg'))

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
    
def downloadImage(imageLink):
    # print("image:",imageLink)
    filename = imageLink.split("/")[-1]
    rawImage = requests.get(imageLink, stream=True)
    folder = "images/scrapedImages/" 
    writeLocation = folder+filename
    with open(writeLocation,'wb') as fd:
        for chunk in rawImage.iter_content(chunk_size=1024):
            fd.write(chunk)
    
    return

imageLinks = getImageLinks("https://twitter.com/imgur?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor")
# print(imageLinks)
for link in imageLinks:
    print("link:", link)
try:
    for image in imageLinks[:10]:
        downloadImage(image)
except:
    print("Seems to be an issue downloading images from the website.")
# downloadImage("https://scontent.fykz1-2.fna.fbcdn.net/v/t1.0-1/p720x720/37761468_10157914956042588_4029176324378591232_n.jpg")