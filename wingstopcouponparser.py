from bs4 import BeautifulSoup
import re
from datetime import datetime
import pytz

pacific_tz = pytz.timezone('America/Los_Angeles')

def wingstopemailparse(email):
    contents = email




# Find the element containing the code
    soup = BeautifulSoup(contents, 'html.parser')

# new wingstop update: Find all <td> elements with class="main-content"
    code_td = soup.find('td', class_=re.compile(r'code'))

    if code_td:
        code_part = code_td.text.strip()
        print(code_part)
        return code_part

    return None


    
def main(): #new wingstop html format as of 2026-02-19, code is in a <td> element with class "code"
    email ='''<table role="presentation" bgcolor="#ffffff" cellspacing="0" cellpadding="0" border="0" align="center" width="600" style="Margin:auto;width:600px;border-collapse:collapse" class="m_8889941269534792171email-container">
                                            <tbody>
                                              
                                              <tr>
                                                <td align="center" class="m_8889941269534792171px-mobile-padding">
                                                  <table role="presentation" cellspacing="0" cellpadding="0" bgcolor="#ffffff" border="0" align="center" width="560" style="Margin:auto;width:520px;max-width:520px;border-collapse:collapse;border:4px dashed #006938">
                                                    <tbody>
                                                      <tr>
                                                        <td width="28" style="font-size:28px;line-height:28px">&nbsp;</td>
                                                      </tr>
                                                      <tr>
                                                        <td width="260" valign="top" align="center" style="font-family:Arial,sans-serif;font-size:14px;font-weight:normal;color:#000000;line-height:22px">
                                                          <img src="https://ci3.googleusercontent.com/meips/ADKq_NZdKjTRK6zncZiyWNOGUU07xAHGDg3ScpAvqt02Yn3cPaCv2YzmVY6BMUn0kIs_HXKWqJyIUKJnbup05koM-ntV0dEjNLyIdL4t8V9YHEwnJw5Mp5RLkh5RUXAnLhA4LEc1KPHKQetlgN_a=s0-d-e1-ft#https://mywingstopsurvey.com/Projects/WINGS_CSI/images/emailer/smg-wingstop-fries.png" alt="photo of Wingstop fry basket" style="color:#000000;font-weight:bold;width:260px;height:auto" width="260" height="auto" class="CToWUd a6T" data-bit="iit" tabindex="0"><div class="a6S" dir="ltr" style="opacity: 0.01; left: 559.2px; top: 803.013px;"><span data-is-tooltip-wrapper="true" class="a5q" jsaction="JIbuQc:.CLIENT"><button class="VYBDae-JX-I VYBDae-JX-I-ql-ay5-ays CgzRE" jscontroller="PIVayb" jsaction="click:h5M12e;clickmod:h5M12e;pointerdown:FEiYhc;pointerup:mF5Elf;pointerenter:EX0mI;pointerleave:vpvbp;pointercancel:xyn4sd;contextmenu:xexox;focus:h06R8; blur:zjh6rb;mlnRJb:fLiPzd;" data-idom-class="CgzRE" data-use-native-focus-logic="true" jsname="hRZeKc" aria-label="Download attachment " data-tooltip-enabled="true" data-tooltip-id="tt-c46" data-tooltip-classes="AZPksf" id="" jslog="91252; u014N:cOuCgd,Kr2w4b,xr6bB; 4:WyIjbXNnLWY6MTg1NzYwNDUxMDU0NDUyODEzMyJd; 43:WyJpbWFnZS9qcGVnIl0."><span class="XjoK4b VYBDae-JX-UHGRz"></span><span class="UTNHae" jscontroller="LBaJxb" jsname="m9ZlFb" soy-skip="" ssk="6:RWVI5c"></span><span class="VYBDae-JX-ank-Rtc0Jf" jsname="S5tZuc" aria-hidden="true"><span class="notranslate bzc-ank" aria-hidden="true"><svg viewBox="0 -960 960 960" height="20" width="20" focusable="false" class=" aoH"><path d="M480-336L288-528l51-51L444-474V-816h72v342L621-579l51,51L480-336ZM263.72-192Q234-192 213-213.15T192-264v-72h72v72H696v-72h72v72q0,29.7-21.16,50.85T695.96-192H263.72Z"></path></svg></span></span><div class="VYBDae-JX-ano"></div></button><div class="ne2Ple-oshW8e-J9" id="tt-c46" role="tooltip" aria-hidden="true">Download</div></span></div>
                                                        </td>
                                                      </tr>
                                                      <tr>
                                                        <td width="30" style="font-size:30px;line-height:30px">&nbsp;</td>
                                                      </tr>
                                                      <tr>
                                                        <td align="left" valign="top" style="background-color:#ffffff">
                                                          <table align="center" border="0" cellspacing="0" cellpadding="0">
                                                            <tbody><tr>
                                                              <td align="center" valign="top" style="padding-left:28px;padding-right:28px;color:#006938;font-size:24px;line-height:24px;font-weight:bold;font-family:Arial,Helvetica,sans-serif" class="m_8889941269534792171body-mobile-padding">
                                                                Code:
                                                              </td>
                                                            </tr>
                                                          </tbody></table>
                                                        </td>
                                                      </tr>
                                                      <tr>
                                                        <td width="5" style="font-size:5px;line-height:5px">&nbsp;</td>
                                                      </tr>
                                                      <tr>
                                                        <td align="left" valign="top" style="background-color:#ffffff">
                                                          <table align="center" border="0" cellspacing="0" cellpadding="0">
                                                            <tbody><tr>
                                                              <td align="center" valign="top" style="padding-left:28px;padding-right:28px;color:#006938;font-size:24px;line-height:24px;font-weight:bold;font-family:Arial,Helvetica,sans-serif" class="m_8889941269534792171body-mobile-padding m_8889941269534792171code">
                                                                DS2602FHRMRFAMPCBB6MH2
                                                              </td>
                                                            </tr>
                                                          </tbody></table>
                                                        </td>
                                                      </tr>
                                                      <tr>
                                                        <td width="30" style="font-size:30px;line-height:30px">&nbsp;</td>
                                                      </tr>
                                                      <tr>
                                                        <td align="left" valign="top" style="background-color:#ffffff">
                                                          <table align="left" border="0" cellspacing="0" cellpadding="0">
                                                            <tbody><tr>
                                                              <td align="left" valign="top" style="padding-left:28px;padding-right:28px;color:#000000;font-size:11px;line-height:18px;font-weight:normal;font-family:Arial,Helvetica,sans-serif;text-align:center" class="m_8889941269534792171body-mobile-padding">
                                                                * FOR FREE REGULAR SEASONED FRIES: Valid only for fourteen (14) days from the date of this email at participating locations in the US on carryout or delivery orders placed via <a href="https://www.wingstop.com/" style="color:#000000;text-decoration:underline" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.wingstop.com/&amp;source=gmail&amp;ust=1771636652636000&amp;usg=AOvVaw0InSJGct2GacMIUDNTC7UF">Wingstop.com</a> or the Wingstop App. Minimum purchase required. Any chicken item and one (1) regular seasoned fries must be in basket and the promo code from this email used to receive promotional item. Does not include applicable Delivery Fee, Service Fee, Government-imposed Fees, Taxes, or Gratuities. Limited to one (1) regular seasoned fries per promo code. Not available on third party marketplaces. Wingstop Restaurants Inc. reserves the right to cancel, suspend and/or modify this offer for any reason or if any fraud, technical failures, human error, or any other factor impairs the integrity or proper performance of the offer, as determined by it in its sole discretion. ©&nbsp;2025&nbsp;WF&nbsp;LLC.
                                                              </td>
                                                            </tr>
                                                          </tbody></table>
                                                        </td>
                                                      </tr>
                                                      <tr>
                                                        <td width="28" style="font-size:28px;line-height:28px">&nbsp;</td>
                                                      </tr>
                                                      
                                                    </tbody>
                                                  </table>
                                                </td>
                                              </tr>
                                            </tbody>
                                          </table>'''

    code = wingstopemailparse(email)
    print(code)
    

if __name__ == "__main__":
    main()