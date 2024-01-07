import requests

url = "https://www.pandaguestexperience.com/Survey.aspx?c=353204"

# Original form data
original_data = {
    "S000057":"foo.dsurveycodes@gmail.com",
    "S000064":"foo.dsurveycodes@gmail.com",
    "IoNF": "229",
    "PostedFNS": "S000057|S000064",
    "OneQuestionLeftUnansweredErrorMessageTemplate": "There is {0} error on the page.",
    "MoreQuestionsLeftUnansweredErrorMessageTemplate": "There are {0} errors on the page."
}
headers={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "en-US,en;q=0.9",
"Cache-Control": "max-age=0",
"Connection": "keep-alive",
"Content-Length": "272",
"Content-Type": "application/x-www-form-urlencoded",
"Cookie": "AspxAutoDetectCookieSupport=1; BIGipServerpandaguestexperience.com_pool=1580339884.52259.0000; ASP.NET_SessionId=3geh44tsjyj3yfhq2pfm0xw2; LID=US; CCID=index.aspx; SN=CH-WEB-WSE07-P; bhtglocalcooksesstest=1; bhtglocalcookperstest=1; DF_Placed=1; T=SN=CH-WEB-WSE07-P&ST=1/5/2024 10:28:45 AM&FP=/Index.aspx&RA=172.88.39.145&LA=1/5/2024 10:32:36 AM; TS017a8bfa=01af266ec9d592a1278ac590f68aa970d743ccb325719ee02f7ddadf4086755121b9c03eb86f0bb5fdd884c5277b675d08a7ef2856c2d34340054cad37169e07050b279b862f17c2ea5e8937ad8f5157be1351e10c5925eb2788b0dd20fa4c07092ab5f33731cdac4459350c479349844bec3992510b49fb209a8682000597644018be446d30c3b4f74c20d3d8aec95951a5db806cd60ca4b693d64eafe2eee94fe3332fa39cbb68ebb83a802d89909057f46eaf7a; TS709abc9c027=084b59c7b6ab200034e7d1fe961ca6d47146b3d125218ea770ae1c1b42eaa12051dbbe6c07bbac8e08bdb2ace11130004c2b35345935dc5134669684d9fb5ef3713e159f1f68ef79e4ab2c9900f426b0855c8ba8e8b16be24183567ccfc946d9",
"Host": "www.pandaguestexperience.com",
"Origin": "https://www.pandaguestexperience.com",
"Referer": "https://www.pandaguestexperience.com/Survey.aspx?c=262904",
"Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
"Sec-Ch-Ua-Mobile": "?0",
"Sec-Ch-Ua-Platform": '"Windows"',
"Sec-Fetch-Dest": "document",


}


# Send the POST request with the modified payload

response = requests.post(url, headers= headers,data=original_data)
print(response)


