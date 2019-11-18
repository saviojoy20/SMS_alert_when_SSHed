# python program to receive msg when an ssh connection is made
import re
import time
import requests
import json

URL = 'https://www.way2sms.com/api/v1/sendCampaign'

#  request
def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
  req_params = {
  'apikey':apiKey,
  'secret':secretKey,
  'usetype':useType,
  'phone': phoneNo,
  'message':textMessage,
  'senderid':senderId
  }
  return requests.post(reqUrl, req_params)
# ssh log file
Log_File= "/var/log/secure"

#startting log scanner
with open (Log_File,'r') as f:
    while 1:
        where = f.tell()
        line = f.readline()
        f_line = str(line)
        if "Acc" in f_line:
            print(f_line)
            user = re.search(r"for(.*)from",f_line).group(1)
            time = re.findall("[0-9]{,2}:[0-9]{,2}:[0-9]{,2}",f_line)
            time=str(time)
            time = time.rstrip("]").lstrip("[")
            ip = re.findall("[0-9]{0,3}\.[0-9]{0,3}\.[0-9]{0,3}\.[0-9]{0,3}",f_line)
            ip = str(ip)
            ip = ip.rstrip("]").lstrip("[")
            message = "New connection to account"+ user +"from ip "+ ip + " at "+ time +" IST"
            print(message)
            response = sendPostRequest(URL, 'apiKey' , 'secretKey', 'stage',
                                       'your_mobile_number', 'active-sender-id', message)
            print(response.text)
            if not line:
                print("waiting for new line. position is at".format(where))
                time.sleep(2)
                f.seek(where)
