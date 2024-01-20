import requests
from bs4 import BeautifulSoup
def check(result):
    if "Upon completion of this survey" in result:
        print("Success")

data1 = {
  "JavaScriptEnabled": 1,
  "FIP": "true",
  "OneQuestionLeftUnansweredErrorMessageTemplate": "There is {0} error on the page.",
  "MoreQuestionsLeftUnansweredErrorMessageTemplate": "There are {0} errors on the page.",
  "InputStoreNum": "0175",
  "Index_VisitDateFormattedDate": "20240107",
  "Index_VisitDateDatePicker": "01/07/2024",
  "InputHour": "04",
  "InputMinute": "02",
  "InputMeridian": "PM",
  "InputOrderNum": "154886",
  "NextButton": "Start"
}

headers= {
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
  "Accept-Encoding": "gzip, deflate, br",
  "Accept-Language": "en-US,en;q=0.9",
  "Cache-Control": "max-age=0",
  "Connection": "keep-alive",
  "Content-Length": "240",
  "Content-Type": "application/x-www-form-urlencoded",
  "Cookie": "SN=CH-WEB-WSE03-P; BIGipServerpandaguestexperience.com_pool=254939820.52259.0000; bhtglocalcooksesstest=1; bhtglocalcookperstest=1; DF_Placed=1; ASP.NET_SessionId=xcfp4ctvesqubuvdneoaqsyq; LID=US; CCID=index.aspx; T=SN=CH-WEB-WSE03-P&ST=1/7/2024 8:42:26 AM&FP=/Index.aspx&RA=172.88.39.145&LA=1/7/2024 10:50:02 AM; TS017a8bfa=01af266ec9c56cd4eb9ccfa0329102f34e86544d5818155caf79068fc5dc0266646775648947a47c6949e84d1d0f11dc97bb84af557e168f7f8eefee8cf985fcda686a215f0ecfca0b286b52ab3d806f50fd2acd4c034ff8c3d5745d027d959e157fe6566160d174adc0eb5bfb979e9267a509f9fdb64741796fea6c521087e9d3c2baa519c81bd5cad37d2ae40ea07fcc87e078919a537a74f7c8d1191fd2d133870c350f5bac86da4cff27ff54657cfc455eee9c; TS709abc9c027=TS709abc9c027=084b59c7b6ab2000f5d5628b0463888072fa22faee182305868f331e848d29c8a40921d67c7a433708c85771ed113000008370339bda2b1c7c59d0fd80885c8bce1564ac56bdd86961e22e5934c23d980029d4518786a3e28adfc7bff63e30b4",
  "Host": "www.pandaguestexperience.com",
  "Origin": "https://www.pandaguestexperience.com",
  "Referer": "https://www.pandaguestexperience.com/Index.aspx?c=523304",
  "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
  "Sec-Ch-Ua-Mobile": "?0",
  "Sec-Ch-Ua-Platform": "\"Windows\"",
  "Sec-Fetch-Dest": "document",
  "Sec-Fetch-Mode": "navigate",
  "Sec-Fetch-Site": "same-origin",
  "Sec-Fetch-User": "?1",
  "Upgrade-Insecure-Requests": "1",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

url = "https://www.pandaguestexperience.com/Survey.aspx?c=523304"

# while not url.startswith("https://www.pandaguestexperience.com/Survey.aspx?"):
#   response = requests.post(url, data=data1, headers=headers )
#   print(response.url)
#   print("cookies: ", response.cookies)

for range in range(1, 3):
  response = requests.post(url, data=data1, headers=headers)
  print(response.url)
  print("request headers: ", response.request.headers)
  print("response headers: ", response.headers)

# newurl = response.url
# print(response.url)
# check(response.text)
# response = requests.post(newurl, data = data1)
# print(response.url)
# # soup = BeautifulSoup(response.text, features='html.parser')
# # print(soup.prettify())
# check(response.text)
# newurl = response.url
# print(response.url)
# response = requests.post(newurl, data = data1)
# check(response.text)
# print(response.url)
