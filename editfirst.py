#!C:/Pthon27
import requests
import sys
from htmldom import htmldom
import json
import time


threadId='1628542'
messageId='16377284'
threadUrl="https://bitcointalk.org/index.php?topic={}.msg{}#msg{}".format(threadId,messageId,messageId)
editUrl="https://bitcointalk.org/index.php?action=post;msg={messageId};topic={threadId};sesc=sesc"

valuesPassed=sys.argv[1:]
messageId=valuesPassed[2]
threadId=valuesPassed[1]
msgFile=valuesPassed[0]

messageToPost="Changed text"
subjectToPost="New Subject to test"

with open(msgFile,'r') as mFile:
 lines=mFile.readlines()
 subjectToPost=lines[0]
 messageToPost="\r\n".join(lines[1:])


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

res=session.get(threadUrl)

with open("sess.html","w") as sFile:
 sFile.write(res.text.encode("utf-8"))

html= res.text
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
 #find Edit Button
 post["edit"]=''
 buttons=repliesC[index].find("td.td_buttons > div > a")
 buttonUrl=buttons[0].attr("href")
 buttonParams=buttonUrl.split("?")[1].split(";")
 sesc=''
 for param in buttonParams:
  if 'sesc' in param:
   sesc=param.split("=")[1].strip()
   break
 post["edit"]="https://bitcointalk.org/index.php?action=post;msg={};topic={};sesc={}".format(messageId,threadId,sesc)
 if post["url"] in threadUrl:
  lastPost=post
  break

res=session.get(lastPost["edit"])
with open("edit.html","w") as eFile:
 eFile.write(res.text)

dom=htmldom.HtmlDom().createDom(res.text)
urlToSubmit=dom.find("#postmodify")[0].attr("action")
data={
 "topic":dom.find('input[name="topic"]')[0].attr("value"),
 "subject":subjectToPost,
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
if response.status_code==200:
 print("Edited")
else:
 print("Try again")
