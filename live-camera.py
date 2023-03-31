import cv2, os
from PIL import Image, ImageOps, ImageDraw


asciiCharacters = [" ",".",":","-","=","+","*","#","%","@"]

def createImage(text):
    charSize = 5
    newImg = Image.new('RGB', (charSize*len(text[0]), charSize*len(text)), (0,0,0))
    im = ImageDraw.Draw(newImg)
    for y in range(len(text)):
        for x in range(len(text[y])):
            char = text[y][x]
            im.text((charSize*x,charSize*y), char, fill=(255,255,255))
    newImg.save('temp.png')

def imageToAscii(image,inVideo):
    #image = ImageOps.grayscale(Image.open(filename))
    imgData = image.load()

    width, height = image.size[0], image.size[1]

    charBlocks = []
    for yBlock in range(height // pixelNum):
        blockLine = []
        for xBlock in range(width // pixelNum):
            curBlock = []
            for x in range(pixelNum):
                for y in range(pixelNum):
                    curBlock.append(imgData[(xBlock*pixelNum)+x,(yBlock*pixelNum)+y])
            blockLine.append(curBlock)
        charBlocks.append(blockLine)


    text = []
    line = ''
    for blockLine in charBlocks:
        line = ''
        for block in blockLine:
            avg = sum(block)/len(block)
            line += asciiCharacters[int(round((avg/255)*len(asciiCharacters),0))-1]
        text.append(line)
    else:
        return text

def camera():
    try:
        video = cv2.VideoCapture(0)
    except:
        print('Error getting camera input')
  
    while(True):
        ret, frame = video.read() #get current camera frame
        text = imageToAscii(ImageOps.grayscale(Image.fromarray(frame)),True) #get frame in ASCII
        #show(text) #print frame
        createImage(text)
        #break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


pixelNum = int(input('N.Pixels squared per character (1 = one character per pixel): ')) #number of pixels per character squared ; 10 = 10x10
input('Using camera as live input (press enter to start):')
camera()