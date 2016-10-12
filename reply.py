#!C:/Pthon27
import requests
import sys
from htmldom import htmldom
import json
import time




# USER INPUTS
threadId='1628542'
messageToPost="Testing with the changes made!"

valuesPassed=sys.argv[1:]
threadId=valuesPassed[1]
msgFile=valuesPassed[0]

with open(msgFile,'r') as mFile:
 messageToPost=mFile.read()


# Global Variables to access across functions
replyUrl="https://bitcointalk.org/index.php?action=post;topic={}".format(threadId)
loginUrl="https://bitcointalk.org/index.php?action=login2";

with open("config.json",'r') as config:
 settings=json.load(config)

# Tooke me few hours to this shit
session=requests.session()

loginData={"user":settings['username'],"passwrd":settings['password'],"cookielength":"60","hash_passwrd":""}
response=session.post("https://bitcointalk.org/index.php?action=login2",{
 "user":settings['username'],
 "passwrd":settings['password'],
 "cookielength":"60",
 "hash_passwrd":""})
if "45 seconds" in response.text:
 print("Try after 45 seconds!")
 sys.exit(2)


response=session.get(replyUrl)

dom=htmldom.HtmlDom().createDom(response.text)
urlToSubmit=dom.find("#postmodify")[0].attr("action")
data={
 "topic":dom.find('input[name="topic"]')[0].attr("value"),
 "subject":dom.find('input[name="subject"]')[0].attr("value"),
 "icon":"xx",
 "message":messageToPost,
 "notify":"1",
 "do_watch":"0",
 "do_watch":"1",
 "goback":"1",
 "post":"Post",
 "num_replies":dom.find('input[name="num_replies"]')[0].attr("value"),
 "additional_options":dom.find('input[name="additional_options"]')[0].attr("value"),
 "sc":dom.find('input[name="sc"]')[0].attr("value"),
 "seqnum":dom.find('input[name="seqnum"]')[0].attr("value")
}

response=session.post(urlToSubmit,data)

html=response.text
dom=htmldom.HtmlDom().createDom(html)
replies=dom.find("table.bordercolor")[1];
repliesC=replies.find(".bordercolor > tr")

todayOnServer=dom.find(".tborder .smalltext")[0].text().split(",")[0] + ",";

lastPost=None

for index in range(repliesC.length()):
 post={}
 userC=repliesC[index].find("td.poster_info > b")[0]
 if userC is None:
  continue
 post['by']=userC.text().strip()
 if 'vino.gcs' not in post["by"]:
  continue
 at=repliesC[index].find(".subject+.smalltext")[0]
 postTime=at.text().replace("Today",todayOnServer)
 postTime=postTime.replace("at","")
 postTime=postTime.replace("\n","")
 perma=repliesC[index].find(".subject > a")[0]
 post["url"]=perma.attr("href")
 post["content"]=repliesC[index].find(".post")[0].text()

 postT=time.strptime(postTime,'%d %B %Y, %H:%M:%S') # format %d %B %Y, %H:%M:%S
 post["at"]=time.mktime(postT)
 if lastPost is None:
  lastPost=post
 else:
  if lastPost["at"]<post["at"]:
   lastPost=post
print ("-----REPLY URL-----")
print(lastPost["url"])
