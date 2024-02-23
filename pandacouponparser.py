from bs4 import BeautifulSoup
import re
from datetime import datetime
import pytz

pacific_tz = pytz.timezone('America/Los_Angeles')

def pandamailparse(email):
    contents = email

    # Find elements with inline styles containing !important
    soup = BeautifulSoup(contents, 'html.parser')

# Find the element containing the code
    code_elements = soup.find_all('span', style=lambda value: value and 'important' in value)

# Extract the text from each element
    codes = []
    for code_element in code_elements:
        code = code_element.text.strip()
        codes.append(code)

    # Print the extracted codes
    if codes:
        #print("Codes found:")
        #print(codes[2])
        #print(codes[3])

        date_pattern = r'\d{2}/\d{2}/\d{4}'

        dates = re.findall(date_pattern, codes[3])
        first_date = dates[0] if dates else None
        #print(first_date)

        return codes[2], first_date
        # date_format = "%m/%d/%Y"

        # Parse the date string into a datetime object
        # date_object = datetime.strptime(first_date, date_format)
        # localized_date_object = pacific_tz.localize(date_object)

        # Convert the datetime object to a Unix timestamp
        # unix_timestamp = int(date_object.timestamp())

        # Print the Unix timestamp
        # print(unix_timestamp)

        # expiredate = unix_timestamp - 24 * 60 * 60
        # print(expiredate)

        # formatted_date = datetime.fromtimestamp(expiredate, tz=pytz.utc).astimezone(pytz.timezone('America/Los_Angeles')).strftime("%m/%d/%Y")
        # print(formatted_date)

        # unix_time_pacific = int(datetime.now(pacific_tz).timestamp())
        # print(unix_time_pacific)
        # current_date = datetime.fromtimestamp(unix_time_pacific, tz=pytz.utc).astimezone(pytz.timezone('America/Los_Angeles')).strftime("%m/%d/%Y")
        # print(current_date)
    else:
        print("pandamailparse(): Codes not found")
        return "NO CODE", "NO DATE"
    
def main():
    email = """<div id="mail"><div>
<table align="center" border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse" width="100%">
<tbody><tr>
<td align="center" bgcolor="#f8f7ee" style="background-color: rgba(248, 247, 238, 1); padding-bottom: 40px" valign="top">
<table bgcolor="#f8f7ee" border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse" width="600">
<tbody><tr>
<td align="left" style="background-color: rgba(248, 247, 238, 1)">
<table align="left" border="0" cellpadding="0" cellspacing="0" style="width: 100%">
<tbody><tr>
<td style="display: none !important; visibility: hidden; font-size: 1px; color: rgba(255, 255, 255, 1); line-height: 1px; max-height: 0; max-width: 0; opacity: 0; overflow: hidden">
<font></font>
</td>
</tr>
<tr>
<td align="left" style="padding: 10px 0; font-size: 10px; line-height: 120%; font-family: Arial, Helvetica, sans-serif; text-align: left" valign="top" width="350">
<span align="left" style="color: rgba(112, 111, 111, 1); display: block; text-align: left"></span>
</td>
<td align="right" style="padding: 10px 0; font-size: 10px; line-height: 120%; font-family: Arial, Helvetica, sans-serif; text-align: right; width: 250px" valign="top" width="250">
<a align="right" href="#browser" style="color: rgba(112, 111, 111, 1); display: block; text-align: right; font-family: Arial, sans-serif" target="_blank">
<span style='font-family: "Montserrat", Arial, sans-serif !important'>View in browser</span>
</a>
</td>
</tr>
</tbody></table>
</td>
</tr>
<tr>
<td align="left" style="line-height: 0; font-size: 0; background-color: rgba(255, 255, 255, 1)" valign="top">
<table align="left" border="0" cellpadding="0" cellspacing="0" style="display: inline-table; border-collapse: collapse" width="100%">
<tbody><tr>
<td align="left" style="line-height: 0; font-size: 0" valign="top">
<table align="left" border="0" cellpadding="0" cellspacing="0" style="display: inline-table; border-collapse: collapse" width="100%">
<tbody><tr>
<td>
<a border="0" href="https://www.pandaexpress.com" style="border: 0; text-decoration: none; color: rgba(209, 40, 46, 1)">
<img alt="THANK YOU for your feedback!" border="0" height="160" src="https://www.pandaguestexperience.com/Projects/PRG2_CSI/images/emailer/smg-px-hero-ty-01.png" style="text-align: center; color: rgba(209, 40, 46, 1); font-family: Arial, sans-serif; font-weight: bold; font-size: 20px; line-height: 150%; max-width: 600px; max-height: 160px; display: block; background-color: rgba(255, 255, 255, 1)" width="600"/>
</a>
</td>
</tr>
<tr>
<td height="0">
<div style="background-color: rgba(255, 255, 255, 1); display: none; font-family: Arial, Helvetica, sans-serif; color: rgba(255, 255, 255, 1); font-size: 0; height: 0; line-height: 0; padding: 0; text-align: center">
<a border="0" href="#" style="border: 0; text-decoration: none; color: rgba(209, 40, 46, 1)">
<img alt="THANK YOU for your feedback!" border="0" height="auto" src="https://www.pandaguestexperience.com/Projects/PRG2_CSI/images/emailer/smg-px-hero-ty-02.png" style="text-align: center; color: rgba(209, 40, 46, 1); font-weight: bold; font-family: Arial, sans-serif; font-size: 20px; line-height: 150%; width: 100%; height: 160px; display: block !important; background-color: rgba(255, 255, 255, 1)" width="320"/>
</a>
</div>
</td>
</tr>
<tr>
<td>
<table bgcolor="#ffffff" border="0" cellpadding="0" cellspacing="0" style="" width="100%">
<tbody><tr>
<td style="font-size: 40px; line-height: 40px" width="40"> </td>
</tr>
<tr>
<td align="left" style="background-color: rgba(255, 255, 255, 1)" valign="top">
<table align="left" border="0" cellpadding="0" cellspacing="0">
<tbody><tr>
<td align="left" style="padding-left: 40px; padding-right: 40px; color: rgba(45, 41, 38, 1); font-size: 14px; line-height: 25px; font-weight: normal; font-family: Arial, Helvetica, sans-serif" valign="top">
<span style='font-family: "Gotham", "Montserrat", Arial, sans-serif !important'>Here’s a little something you can use on your next visit.</span>
</td>
</tr>
</tbody></table>
</td>
</tr>
<tr>
<td style="font-size: 30px; line-height: 30px" width="30"> </td>
</tr>
<tr>
</tr></tbody></table><table align="center" bgcolor="#ffffff" border="0" cellpadding="0" cellspacing="0" style="margin: auto; width: 600px; border-collapse: collapse" width="600">
<tbody>
<tr>
<td align="center">
<table align="center" bgcolor="#ffffff" border="0" cellpadding="0" cellspacing="0" style="margin: auto; width: 520px; max-width: 520px; border-collapse: collapse; border: 3px dashed rgba(209, 40, 46, 1)" width="520">
<tbody>
<tr>
<td align="left" style="padding: 0">
<table align="" border="0" cellpadding="0" cellspacing="0" style="width: 50%; border-collapse: collapse" width="50%">
<tbody>
<tr>
<td>
<table align="" border="0" cellpadding="0" cellspacing="0" style="width: 100%; border-collapse: collapse" width="100%">
<tbody><tr>
<td height="0" style="padding: 0">
<div style="background-color: rgba(255, 255, 255, 1); display: none; font-family: Arial, Helvetica, sans-serif; color: rgba(255, 255, 255, 1); font-size: 0; height: 0; line-height: 0; padding: 0; text-align: center">
<a border="0" href="#" style="border: 0; text-decoration: none; color: rgba(209, 40, 46, 1)">
<img alt="THANK YOU for your feedback!" border="0" height="auto" src="https://www.pandaguestexperience.com/Projects/PRG2_CSI/images/emailer/smg-px-coupon-m.png" style="text-align: center; color: rgba(209, 40, 46, 1); font-weight: bold; font-family: Arial, sans-serif; font-size: 20px; line-height: 150%; width: 100%; height: 160px; display: block !important; background-color: rgba(255, 255, 255, 1)" width="320"/>
</a>
</div>
</td>
</tr>
<tr>
<td style="font-size: 18px; line-height: 18px" width="18"> </td>
</tr>
<tr>
<td align="left" style="font-family: Arial, sans-serif; font-size: 14px; font-weight: normal; color: rgba(209, 40, 46, 1); line-height: 22px; padding: 0 18px" valign="top" width="200">
<img alt="Present this barcode at your next in-store purchase" height="auto" src="https://www.pandaguestexperience.com/Common/controls/IDAutomation/Barcode.aspx?D=CIIFPM0C4&amp;LM=.25&amp;TM=0&amp;ST=F" style="color: rgba(209, 40, 46, 1); font-weight: bold; width: 200px; height: auto" width="200"/>
</td>
</tr>
<tr>
<td style="font-size: 20px; line-height: 20px" width="20"> </td>
</tr>
<tr>
<td align="center" style="font-family: Arial, Helvetica, sans-serif; font-size: 14px; font-weight: bold; color: rgba(21, 21, 21, 1); line-height: 22px; padding: 0 18px 18px" valign="top" width="200">
<span style='font-family: "Montserrat", Arial, sans-serif !important'>CIIFPM0C4</span>
</td>
</tr>
</tbody></table>
</td>
<td>
<table align="" border="0" cellpadding="0" cellspacing="0" style="width: 100%; border-collapse: collapse" width="100%">
<tbody><tr>
<td align="left" style="font-family: Arial, sans-serif; font-size: 14px; font-weight: normal; color: rgba(209, 40, 46, 1); line-height: 22px; padding: 0; margin: 0" valign="top" width="263">
<img alt="" src="https://www.pandaguestexperience.com/Projects/PRG2_CSI/images/emailer/smg-px-coupon-d.png" style="color: rgba(209, 40, 46, 1); font-weight: bold; width: 263px; height: auto; margin: 0; padding: 0" width="263"/>
</td>
</tr>
</tbody></table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
</td></tr>
<tr>
<td style="font-size: 10px; line-height: 10px" width="10"> </td>
</tr>
<tr>
<td align="left" style="background-color: rgba(255, 255, 255, 1)" valign="top">
<table align="center" border="0" cellpadding="0" cellspacing="0">
<tbody><tr>
<td align="left" style="padding-left: 40px; padding-right: 40px; color: rgba(45, 41, 38, 1); font-size: 10px; line-height: 18px; font-weight: normal; font-family: Arial, Helvetica, sans-serif" valign="top">
<span style='font-family: "Gotham", "Montserrat", Arial, sans-serif !important'>
                                                      Offer will expire on 03/07/2024. This coupon code is good for one-time use only and is limited to one coupon code per order. Valid only at participating locations and online at PandaExpress.com or on the Panda Express app.  No additional charge for premium entrée. Delivery, tax and other fees still apply. Cannot be combined with any other offer, discount, or promotion. Cash value of 1/100 cent. Panda Restaurant Group, Inc. reserves the right to modify or discontinue the offer at any time and additional restrictions may apply.
                                                    </span>
</td>
</tr>
</tbody></table>
</td>
</tr>
<tr>
<td style="font-size: 20px; line-height: 20px" width="20"> </td>
</tr>
</tbody></table>
</td>
</tr>
</tbody></table>
<table align="center" bgcolor="#f8f7ee" border="0" cellpadding="0" cellspacing="0" style="margin: auto; width: 600px; border-collapse: collapse" width="600">
<tbody>
<tr>
<td style="font-size: 20px; line-height: 20px" width="20"> </td>
</tr>
<tr>
<td align="center">
<table align="center" border="0" cellpadding="0" cellspacing="0" style="margin: auto; width: 600px; border-collapse: collapse" width="600">
<tbody>
<tr>
<td align="left">
<table align="left" border="0" cellpadding="0" cellspacing="0" style="width: 600px; border-collapse: collapse" width="600">
<tbody>
<tr>
<td align="left" style="font-family: Arial, sans-serif; font-size: 10px; font-weight: normal; color: rgba(112, 111, 111, 1); line-height: 16px">
<span style='font-family: "Montserrat", Arial, sans-serif !important'>
                                                            Copyright © 2022. Panda Express, P.O. Box 1159, Rosemead, CA 91770. All rights reserved. <a href="https://www.pandaexpress.com/" style="text-decoration: underline; color: rgba(112, 111, 111, 1)" target="_blank">www.pandaexpress.com</a>
</span>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
<tr>
<td style="font-size: 20px; line-height: 20px" width="20"> </td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody></table>
</td>
</tr>
</tbody></table>
</div></div>"""

    code, expiredate = pandamailparse(email)
    print(code)
    print(expiredate)

if __name__ == "__main__":
    main()