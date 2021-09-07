import discord
import cv2

thres = 0.5 
classNames= []
classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def scan(img):
    classIds, confs, bbox = net.detect(img,confThreshold=thres)
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            i = classNames[classId-1]
            if i == "pizza":
                return True
    return

client = discord.Client()

async def check_pizza(content,attachemnts):
    for img in attachemnts:
        if img.content_type == "image/jpeg" or img.content_type == "image/png":
            await img.save(f"temp.{img.content_type[6:]}")
            print(f"temp.{img.content_type[6:]}")
            if scan(cv2.imread(f"/Users/erykhalicki/Desktop/projects/chatbot/temp.{img.content_type[6:]}")):
                return True
    if "pi" in content.lower() and "za" in content.lower():
        return True
    return 

global offenses
offenses=0

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global offenses
    if message.author.id == 741252538497630302:
        if await check_pizza(message.content, message.attachments):
            await message.delete()
            offenses+=1
            print(f"Offenses: {offenses}")
            await message.channel.send(f"Offenses: {offenses}")

client.run('NTM3NzMxODU5MjUwMTUxNDI3.XEjP0Q.aCnHiqswz0GSireZyjzKBW0QcK8')