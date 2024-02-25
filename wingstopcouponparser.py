from bs4 import BeautifulSoup
import re
from datetime import datetime
import pytz

pacific_tz = pytz.timezone('America/Los_Angeles')

def wingstopemailparse(email):
    contents = email




# Find the element containing the code
    soup = BeautifulSoup(contents, 'html.parser')

# Find all <td> elements with class="main-content"
    td_main_content = soup.find_all('td', class_='main-content')
    td_tag = soup.find('td', class_='main-content', align='center', style='font-family: Arial, sans-serif; font-size: 17px; font-weight: bold; color: #454545; line-height: 140%;')
    if td_tag:
        td_content = td_tag.text.strip()
        code_part = td_content.split('Code: ')[1].split()[0]
        print(code_part)
    #print(td_tag)
    return code_part


    
def main():
    email ='''<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"><head><meta name="ROBOTS" content="NOINDEX, NOFOLLOW"><meta name="referrer" content="no-referrer">
              <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"> <!-- utf-8 works for most cases -->
              <meta name="viewport" content="width=device-width"> <!-- Forcing initial-scale shouldn't be necessary -->
              <meta http-equiv="X-UA-Compatible" content="IE=edge"> <!-- Use the latest (edge) version of IE rendering engine -->
              <meta name="x-apple-disable-message-reformatting" content="width=device-width, initial-scale=1.0">  <!-- Disable auto-scale in iOS 10 Mail entirely -->
              <meta name="format-detection" content="telephone=no"> <!-- Disable auto-detection/styling of telephone numbers iOS -->
              <title>Wingstop</title> <!-- The title tag shows in email notifications, like Android 4.4. -->
              <link rel="Shortcut Icon" type="image/x-icon" href="https://mywingstopsurvey.com/Projects/WINGS_CSI/images/emailer/ws-apple-touch.png"><!-- Add a favicon for web version -->

              <!-- Web Font / @font-face : BEGIN -->
              <!-- Desktop Outlook chokes on web font references and defaults to Times New Roman, so we force a safe fallback font. -->
              <!-- Windows 10 ignores inline "text-decoration: none;" - note the forced xy-reset here. -->
              <!--[if mso]>
                  <style>
                      body, table, tr, td, div, h1, h2, h3, h4, h5, h6, p, a {
                          font-family: sans-serif !important;
                      }
                      .title-black {
                        font-family: Arial Black, Arial, sans-serif !important;
                      }
                      .nav-item a,
                      .button a,
                      .preheader {
                        text-decoration: none !important;
                      }
                      ol, ul {
                        Margin-left: 20px !important;
                      }
                      li {
                        text-align:-webkit-match-parent;
                        display:list-item;text-indent: -1em;
                      }
                      .inherit {
                        text-decoration: none !important;
                        color: inherit !important;
                      }

                  </style>
              <![endif]-->
              <!-- Makes background images in 72ppi Outlook render at correct size. -->
              <!--[if gte mso 9]>
              <xml>
                  <o:OfficeDocumentSettings>
                      <o:AllowPNG/>
                      <o:PixelsPerInch>96</o:PixelsPerInch>
                  </o:OfficeDocumentSettings>
              </xml>
              <![endif]-->

              <!-- CSS : BEGIN -->

              <!--[if !mso]><!-->
              <style type="text/css">
                @media screen {
                  @font-face {
                    font-family: 'Open Sans';
                    font-style: normal;
                    font-weight: 400;
                    src: local('Open Sans Regular'), local('OpenSans-Regular'), url(https://fonts.gstatic.com/s/opensans/v15/mem8YaGs126MiZpBA-UFVZ0bf8pkAg.woff2) format('woff2');
                    unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
                  }
                  @font-face {
                    font-family: 'Open Sans Bold Italic';
                    font-style: italic;
                    font-weight: 800;
                    src: local('Open Sans ExtraBold Italic'), local('OpenSans-ExtraBoldItalic'), url(https://fonts.gstatic.com/s/opensans/v15/memnYaGs126MiZpBA-UFUKW-U9hrIqOxjaPX.woff2) format('woff2');
                    unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
                  }
                  .openSansReg {
                    font-family: 'Open Sans', Helvetica, Arial, sans-serif;
                  }
                  .openSansBoldIt {
                    font-family: 'Open Sans Bold Italic', Helvetica, Arial, sans-serif;
                  }
                }
              </style>
              <!--<![endif]-->

              <style type="text/css">
                /* Remove spaces around the email design added by some email clients. */
                /* Beware: It can remove the padding / Margin and add a background color to the compose a reply window. */
                html,
                body {
                  Margin: 0 auto !important;
                  padding: 0 !important;
                  height: 100% !important;
                  width: 100% !important;
                  -webkit-font-smoothing: antialiased;
                  -moz-osx-font-smoothing: grayscale;
                }
                /* Stops email clients resizing small text. */
                * {
                  -ms-text-size-adjust: 100%;
                  -webkit-text-size-adjust: 100%;
                  box-sizing: border-box;
                }

                /* Resets styles rules applied by Outlook/Hotmail adding .ExternalClass */

                .ExternalClass {
                  width: 100%;
                }

                .ExternalClass,
                .ExternalClass p,
                .ExternalClass span,
                .ExternalClass font,
                .ExternalClass td,
                .ExternalClass div {
                  mso-line-height-rule: exactly;
                  line-height: 100%;
                }
                /* Stops Outlook from adding extra spacing to tables. */
                table,
                td {
                  mso-table-lspace: 0pt !important;
                  mso-table-rspace: 0pt !important;
                  box-sizing: border-box !important;
                }
                /* Fixes webkit padding issue. Fix for Yahoo mail table alignment bug. Applies table-layout to the first 2 tables then removes for anything nested deeper. */
                table {
                  border-spacing: 0 !important;
                  border-collapse: collapse !important;
                  table-layout: fixed !important;
                  Margin: 0 auto !important;
                }
                table table table {
                  table-layout: auto;
                }
                /* Uses a better rendering method when resizing images in IE. */
                img {
                  -ms-interpolation-mode: bicubic;
                }
                /* A work-around for email clients meddling in triggered links. */
                *[x-apple-data-detectors], /* iOS */
                .x-gmail-data-detectors,/* Gmail */
                .x-gmail-data-detectors *,
                .aBn {
                  border-bottom: 0 !important;
                  cursor: default !important;
                  color: inherit !important;
                  text-decoration: none !important;
                  font-size: inherit !important;
                  font-family: inherit !important;
                  font-weight: inherit !important;
                  line-height: inherit !important;
                }
                /* Prevents Gmail from displaying download button on large, non-linked images. */
                .a6S {
                  display: none !important;
                  opacity: 0.01 !important;
                }
                /* If the above doesn't work, add a .g-img class to any image in question. */
                img.g-img + div {
                  display: none !important;
                }
                /* Prevents underlining the button text in Windows 10 */
                .button-link {
                  text-decoration: none !important;
                }

                /* Thwart google's plan to turn links (address) blue */
                u + #body a {
                  color: inherit !important;
                  text-decoration: none;
                  font-size: inherit;
                  font-family: inherit;
                  font-weight: inherit;
                  line-height: inherit;
                }

                #MessageViewBody a {
                  color: inherit !important;
                  text-decoration: none !important;
                }

                li {
                  text-align:-webkit-match-parent;
                  display:list-item;
                }

                 .ios-link a {
                    text-decoration: underline !important;
                    color: inherit !important;
                }

                  .spec-disc {
                    width: 0 !important;
                    display: none !important;
                    height: 0 !important;
                    font-size: 0 !important;
                    line-height: 0 !important;
                  }

                #preheader {
                  font-family: sans-serif;
                  font-size: 1px;
                  color: #ffffff;
                  line-height: 1px;
                  mso-line-height-rule: exactly;
                  display: none;
                  max-width: 0px;
                  max-height: 0px;
                  opacity: 0;
                  overflow: hidden;
                  mso-hide: all;
                }

                /* Media Queries */
                @media screen and (max-width: 639px) {
                  .email-container,
                  .email-container table {
                    width: 100% !important;
                    min-width: 100% !important;
                    Margin: 0 auto !important;
                    float: none !important; /** the align attribute on a table is similar to float on a div**/
                  }
                  .mobile-off {
                    width: 0 !important;
                    display: none !important;
                    height: 0 !important;
                    font-size: 0 !important;
                    line-height: 0 !important;
                  }
                  .mobile-on {
                    display: block !important;
                    height: auto !important;
                    line-height: inherit !important;
                    font-size: inherit !important;
                    max-height: inherit !important;
                  }

                  .spec-disc {
                    width: auto !important;
                    display: block !important;
                    height: auto !important;
                    line-height: inherit !important;
                    font-size: inherit !important;
                    max-height: inherit !important;
                  }
                  .mobile-padding {
                    padding: 0 20px !important;
                  }
                  .mobile-center,
                  .mobile-center img {
                    text-align: center;
                    Margin: 0 auto;
                  }
                  .mobile-left {
                    text-align: left !important;
                  }
                  .mobile-left .button {
                    float: none !important;
                    text-align: left !important;
                    Margin: 0 !important;
                  }
                  .mobile-img {
                    display: block !important;
                    width: 100% !important;
                    max-width: 100% !important;
                    height: auto !important;
                  }
                  .mobile-logo {
                    display: block !important;
                    width: 100% !important;
                    max-width: 325px !important;
                    height: auto !important;
                    text-align: center !important;
                  }
                  .email-container .button {
                    width: auto !important;
                  }
                  .xy-reset {
                    height: auto !important;
                    width: auto !important;
                    border: 0 !important;
                  }
                  .padding-reset {
                    padding: 0 !important;
                  }
                  .mobile-response {
                    text-align: left !important;
                    display: block;
                    padding: 14px 0 !important;
                    font-size: 18px !important;
                    font-weight: 400;
                  }
                  .mobile-response span {
                    font-size: 14px;
                    color: #898989;
                    padding-left: 20px;
                  }
                  .mobile-response-icon {
                    display: inline-block !important;
                    height: 32px !important;
                    width: 32px !important;
                    line-height: 100% !important;
                    font-size: 16px !important;
                    float: none;
                  }
                  .mobile-logo img {
                    width: 160px !important;
                  }
                  .line-break {
                    display: block !important;
                  }
                  .mobile-legal {
                    line-height: 120% !important;
                    text-transform: uppercase !important;
                    margin: 0 0 14px 0 !important;
                  }
                  .mobile-sub {
                    font-size: 18px !important;
                  }
                  .mobile-huge {
                    font-size: 60px !important;
                  }
                  .main-content {
                    text-align: left;
                    padding: 0 7% 15px;
                    background-color: #ffffff;
                  }
                  .header-top {
                    font-size: 29px !important;
                    text-align: center;
                    padding: 30px 7% 5px !important;
                    background-color: #ffffff;
                  }
                  .header-btm {
                    text-align: center;
                    padding: 0px 7% 35px !important;
                    background-color: #ffffff;
                  }
                  .footer-content {
                    text-align: left;
                    padding: 30px 7% 5px;
                    background-color: #e5e5e5;
                    color: #696969 !important;
                  }
                  .main-content a {
                    color: #696969 !important;
                  }
                  .green a {
                      color: #006939 !important;
                  }
                  .btn-col a {
                    color: #ffffff !important;
                  }
                  .nc-footer {
                    background-color: #373737;
                  }
                  .nc-footer .white a {
                    color: #696969 !important;
                    text-decoration: underline !important;
                  }
                  .center {
                    text-align: center !important;
                    Margin: 0 auto !important;
                    float: none !important;
                  }
                  .left {
                    text-align: left !important;
                    float: left !important;
                    padding: 0 10% !important;
                  }
                  .email-container .social-table {
                    width: 280px !important;
                    min-width: auto !important;
                    Margin: 0 auto !important;
                    float: none !important;
                    text-align: center !important;
                  }
                  .email-container .survey-responses-desktop {
                    width: 90% !important;
                    min-width: auto !important;
                    Margin: 0 auto !important;
                    float: none !important;
                    text-align: center !important;
                  }

                  .email-container .survey-responses-mobile {
                    min-width: auto !important;
                    Margin: 0 auto !important;
                    float: none !important;
                    text-align: center !important;
                  }

                  .email-container .survey-responses-mobile td {
                    padding: 10px 10% !important;
                    min-width: auto !important;
                    Margin: 0 auto !important;
                    float: none !important;
                    text-align: left !important;
                  }

                  .header-wrapper,
                  .header-container {
                    width: 100% !important;
                    min-width: 100!important;
                    float: none !important;
                  }
                  .header-wrapper td {
                    background-image: none !important;
                  }
                  .header-logo {
                    width: 40% !important;
                  }
                  .header-menu {
                    width: 40% !important;
                    float: right !important;
                  }
                  .mobile-spacer {
                    display: block !important;
                    width: 100% !important;
                    height: 20px !important;
                    font-size: 20px !important;
                    mso-line-height-rule: exactly;
                    line-height: 20px !important;
                  }
                  .email-container .store-locator {
                    max-width: 380px !important;
                    min-width: 300px !important;
                    Margin: 0 auto !important;
                  }
                  .store-locator .sl-title {
                    display: block !important;
                    width: 100% !important;
                    max-width: 275px !important;
                    height: auto !important;
                    Margin: 0 auto;
                  }
                  .offer-header {
                    font-size: 29px !important;
                    padding-bottom: 0px !important;
                    padding-right: 0px !important;
                  }
                }

             @media screen and (max-width: 320px) {
              .offer-header {
                  font-size: 25px !important;
              }

             }

              </style>
              <!-- CSS : END -->
            </head><body id="body" bgcolor="#e5e5e5" style="Margin: 0; background-color: #e5e5e5;">
              <!-- START PREHEADER -->
              <div id="preheader" style="font-family:sans-serif, sans-serif;font-size:1px;color:#e5e5e5;line-height:1px;mso-line-height-rule:exactly;display:none;max-width:0px;max-height:0px;opacity:0;overflow:hidden;mso-hide:all;">
                Thanks for your feedback. Here’s a free fry on us. To redeem, add the regular seasoned fry to your order and then enter the coupon code on the payment page, using our mobile app or wingstop.com. Valid at participating locations only. Offer is redeemable on wingstop.com or in the Wingstop mobile app only. Offer expires 14 days after survey completion. Limit one per customer. Offer not valid with any other offers or promotions. Other restrictions may apply. Thanks for choosing Wingstop.
             </div>
             <!-- END PREHEADER -->
              <center style="background-color: #e5e5e5;">

          <!-- Preheader : BEGIN -->
          <table class="mobile-off" role="presentation" bgcolor="#e5e5e5" cellspacing="0" cellpadding="0" border="0" align="center" width="550" style="Margin: auto; width: 550px; border-collapse: collapse;">
            <tbody><tr>
              <td align="center" style="padding: 10px 0 5px;"><table class="mobile-off" role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" width="550" style="Margin: auto; width: 550px; border-collapse: collapse;">
                  <tbody><tr>
                    <td width="275" align="left" valign="top" style="padding-right: 20px; color: #696969; font-family: Arial, sans-serif; font-size: 12px; line-height: 130%;">

                       </td>
                    <td width="275" align="right" valign="top" style="color: #696969; font-family: Arial, sans-serif; font-size: 12px; line-height: 130%;"><p style="Margin: 0;"> <a href="#browser" target="_blank" style="color: #696969; text-decoration: underline;">View in browser</a> </p></td>
                  </tr>
                </tbody></table></td>
            </tr>
          </tbody></table>
          <!-- Preheader : END -->

          <!-- Hero Image / Responsive : BEGIN -->
          <table role="presentation" bgcolor="#ffffff" cellspacing="0" cellpadding="0" border="0" align="center" width="550" style="Margin: auto; width: 550px; border-collapse: collapse;" class="email-container">
            <!-- Desktop Image -->
            <tbody><tr>
              <td align="center" class="mobile-off" style="font-family: sans-serif; font-size: 24px; font-weight: bold;">
                <a href="#" target="_blank" style="color: #000000; text-decoration: none;">
                  <img class="mobile-off" src="https://mywingstopsurvey.com/Projects/WINGS_CSI/images/emailer/smg-wingstop-invite-header.png" alt="WINGSTOP" border="0" width="550" height="103" style="width: 550px; display: block; color: #ffffff; background-color: #006939;font-family: sans-serif; font-size: 21px;"></a>
              </td>
            </tr>
            <!-- Mobile Image -->
            <!--[if !mso]><!-->
            <tr>
              <td valign="top" align="center">
                <div class="mobile-on" style="display: none; font-family: Arial, sans-serif; color: #ffffff; font-size: 0; height: 0; mso-line-height-rule: exactly; line-height: 0;padding: 0; mso-hide: all; text-align: center;">
                  <a href="#" target="_blank" style="color: #000000; text-decoration: none;">
                    <img class="mobile-img" src="https://mywingstopsurvey.com/Projects/WINGS_CSI/images/emailer/smg-wingstop-invite-header.png" alt="" border="0" width="0" style="display: none; color: #000000; background-color: #ffffff;">
                  </a>
                </div>
              </td>
            </tr>
            <!--<![endif]-->
          </tbody></table>
          <!-- Hero Image / Responsive : END -->

                <!-- Wingstop Intro -->
                <table role="presentation" bgcolor="#ededed" cellspacing="0" cellpadding="0" border="0" align="center" width="550" style="Margin: auto; width: 550px; border-collapse: collapse;" class="email-container">      
                  <tbody>
                    <tr>
                      <td align="center">
                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" width="550" style="Margin: auto; width: 550px; border-collapse: collapse;">
                          <tbody>
                            <tr>
                              <td align="left">
                                <!-- Left Column : BEGIN -->
                                <table align="left" role="presentation" cellspacing="0" cellpadding="0" border="0" width="275" style="width: 275px; border-collapse: collapse;">
                                  <tbody>
                                    <tr>
                                      <td class="" align="left" style="">
                                        <table class="" align="left" cellspacing="0" cellpadding="0" border="0" style="Margin: 0; border-collapse: collapse;">
                                          <tbody>
                                            <tr>
                                              <td class="header-top" align="center" width="100%" style="padding: 40px 0px 0px 40px; font-family: Arial, sans-serif; font-size: 33px; font-weight: bold; font-style: italic; color: #000000; line-height: 100%;">
                                                <span class="OpenSansBoldIt" style="font-weight: 800;">THANK YOU FOR YOUR FEEDBACK</span></td>
                                            </tr>
                                            <tr>
                                              <td class="header-btm" align="center" width="100%" style="padding: 5px 0px 40px 40px; font-family: Arial, sans-serif; font-size: 27px; font-weight: 400; color: #000000; line-height: 100%;">
                                                <span class="OpenSansReg" style="color: #898989; font-size: 27px; line-height: 100%;">Here’s a free fry&nbsp;on&nbsp;us.</span></td>
                                            </tr>
                                          </tbody>
                                        </table></td>
                                    </tr>
                                  </tbody>
                                </table>
                                <!-- Left Column : END -->
                                <!-- Right Column : BEGIN -->
                                <!--[if mso]></td><td><![endif]-->

                                  <!-- Hero Image / Responsive : BEGIN -->
                                  <table role="presentation" bgcolor="#ffffff" cellspacing="0" cellpadding="0" border="0" align="center" width="275" style="Margin: auto; width: 275px; border-collapse: collapse;" class="email-container">
                                    <!-- Desktop Image -->
                                    <tbody><tr>
                                      <td align="center" class="mobile-off" style="font-family: sans-serif; font-size: 24px; font-weight: bold;">
                                        <a href="#" target="_blank" style="color: #000000; text-decoration: none;">
                                          <img class="mobile-off" src="https://mywingstopsurvey.com/Projects/WINGS_CSI/images/emailer/smg-wingstop-incentive-03-bg.png" alt="" border="0" width="275" style="width: 275px; display: block; color: #ffffff; background-color: #ededed;font-family: sans-serif; font-size: 21px;"></a>
                                      </td>
                                    </tr>
                                    <!-- Mobile Image -->
                                    <!--[if !mso]><!-->
                                    <tr>
                                      <td valign="top" align="center">
                                        <div class="mobile-on" style="display: none; font-family: Arial, sans-serif; color: #ffffff; font-size: 0; height: 0; mso-line-height-rule: exactly; line-height: 0;padding: 0; mso-hide: all; text-align: center;">
                                          <a href="#" target="_blank" style="color: #000000; text-decoration: none;">
                                            <img class="mobile-img" src="https://mywingstopsurvey.com/Projects/WINGS_CSI/images/emailer/smg-wingstop-incentive-03-mobile.png" alt="" border="0" width="0" style="display: none; color: #000000; background-color: #e5e5e5;">
                                          </a>
                                        </div>
                                      </td>
                                    </tr>
                                    <!--<![endif]-->
                                  </tbody></table>
                                  <!-- Hero Image / Responsive : END -->

                                <!-- Right Column : END -->
                              </td>
                            </tr>
                          </tbody>
                        </table></td>
                    </tr>
                  </tbody>
                </table>
                <!-- Wingstop Outro -->

              <!-- Horizontal Spacer : BEGIN -->
                <table role="presentation" bgcolor="#ffffff" cellspacing="0" cellpadding="0" border="0" align="center" width="550" style="Margin: auto; width: 550px; border-collapse: collapse;" class="email-container">      
                  <tbody><tr>
                    <td height="10" style="font-size: 20px; mso-line-height-rule: exactly; line-height: 10px;">&nbsp;</td>
                  </tr>
                </tbody></table>
                <!-- Horizontal Spacer : END -->

          <!-- --------------------------- -->
          <!-- --------------------------- -->
          <!-- Survey Body Content : BEGIN -->
          <!-- --------------------------- -->
          <!-- --------------------------- -->

          <table role="presentation" bgcolor="#ffffff" cellspacing="0" cellpadding="0" border="0" align="center" width="550" style="Margin: auto; width: 550px; border-collapse: collapse;" class="email-container">
            <tbody>
            <tr>
              <td class="" width="30" style="font-size: 30px; line-height: 30px;">&nbsp;</td>
            </tr>
            <tr>
              <td align="center"><table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" width="465" style="Margin: auto; width: 465px; border-collapse: collapse;">
                  <tbody><tr>
                    <td align="left"><!-- BODY GREETING -->

                      <table align="left" role="presentation" cellspacing="0" cellpadding="0" border="0" width="465" style="width: 465; border-collapse: collapse;">
                        <tbody><tr>
                          <td class="main-content offer-header" align="center" style="font-family: Arial, sans-serif; font-size: 32px; font-weight: bold; font-style: italic; color: #006939; line-height: 100%;">
                            <p style="Margin: 0;"><span class="OpenSansBoldIt" style="font-weight: 800;">FREE REGULAR&#8209;SIZE,<br />
                              SEASONED FRY</span></p></td>
                        </tr>
                      </tbody></table>
                    </td>
                  </tr>
                </tbody></table></td>
            </tr>
            <tr>
              <td align="center"><table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" width="465" style="Margin: auto; width: 465px; border-collapse: collapse;">
                  <tbody><tr>
                    <td align="left"><!-- BODY INTRO -->

                      <table align="left" role="presentation" cellspacing="0" cellpadding="0" border="0" width="465" style="width: 465; border-collapse: collapse;">
                        <tbody><tr>
                          <td class="main-content" align="center" style="font-family: Arial, sans-serif; font-size: 16px; font-weight: normal; color: #b59958; line-height: 140%;"><p style="Margin: 0;">
                            with your next <span style="font-weight: bold; text-decoration: underline;">online purchase</span> of&nbsp;wings&nbsp;or&nbsp;tenders.</p></td>
                        </tr>
                      </tbody></table>
                    </td>
                  </tr>
                </tbody>
              </table>
              </td>
            </tr>
            <tr>
              <td class="mobile-off" width="15" style="font-size: 15px; line-height: 15px;">&nbsp;</td>
            </tr>
            <tr>
              <td align="center"><table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" width="465" style="Margin: auto; width: 465px; border-collapse: collapse;">
                  <tbody><tr>
                    <td align="left"><!-- BODY INTRO -->

                      <table align="left" role="presentation" cellspacing="0" cellpadding="0" border="0" width="465" style="width: 465; border-collapse: collapse;">
                        <tbody><tr>
                          <td class="main-content" align="center" style="font-family: Arial, sans-serif; font-size: 16px; font-weight: normal; color: #b59958; line-height: 150%;">
                            <img class="mobile-on" src="https://mywingstopsurvey.com/Projects/WINGS_CSI/images/emailer/smg-wingstop-incentive-hr-top.png" alt="" border="0" width="465" style="width: 100%; display: block; color: #ffffff; font-family: sans-serif; font-size: 1px;">
                          </td>
                        </tr>
                      </tbody></table>
                    </td>
                  </tr>
                </tbody>
              </table>
              </td>
            </tr>
            <tr>
              <td class="mobile-off" width="20" style="font-size: 20px; line-height: 20px;">&nbsp;</td>
            </tr>
            <tr>
              <td align="center"><table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" width="465" style="Margin: auto; width: 465px; border-collapse: collapse;">
                  <tbody><tr>
                    <td align="left"><!-- BODY INTRO -->

                      <table align="left" role="presentation" cellspacing="0" cellpadding="0" border="0" width="465" style="width: 465; border-collapse: collapse;">
                        <tbody><tr>
                          <td class="main-content green" align="center" style="font-family: Arial, sans-serif; font-size: 17px; font-weight: bold; color: #006939; line-height: 140%;"><p style="Margin: 0;">
                            To redeem, add the regular seasoned fry to your order and then enter the coupon code on the payment page when you order using our mobile app or <a href="http://www.wingstop.com" style="color: #006939; text-decoration: none;">wingstop.com.</a></p></td>
                        </tr>
                      </tbody></table>
                    </td>
                  </tr>
                </tbody>
              </table>
              </td>
            </tr>
            <tr>
              <td class="mobile-off" width="15" style="font-size: 15px; line-height: 15px;">&nbsp;</td>
            </tr>
            <tr>
              <td align="center"><table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" width="465" style="Margin: auto; width: 465px; border-collapse: collapse;">
                  <tbody><tr>
                    <td align="left"><!-- BODY INTRO -->

                      <table align="left" role="presentation" cellspacing="0" cellpadding="0" border="0" width="465" style="width: 465; border-collapse: collapse;">
                        <tbody><tr>
                          <td class="main-content" align="center" style="font-family: Arial, sans-serif; font-size: 14px; font-weight: 300; color: #5c5c5c; line-height: 140%;"><p style="Margin: 0;">
                            Valid at participating locations only. <span style="font-weight: bold; text-decoration: underline;">Offer is redeemable on </span><a href="http://www.wingstop.com" target="_blank" style="color: #5c5c5c !important; font-weight: bold; text-decoration: underline;"><span style="color: #5c5c5c; font-weight: bold; text-decoration: underline;">wingstop.com</span></a><span style="font-weight: bold; text-decoration: underline;"> or in the Wingstop mobile app only.</span> Offer&nbsp;expires 14&nbsp;days after survey completion. Limit&nbsp;one per&nbsp;customer. Offer not valid with any other offers or promotions. Other&nbsp;restrictions may&nbsp;apply.</p></td>
                        </tr>
                      </tbody></table>
                    </td>
                  </tr>
                </tbody>
              </table>
              </td>
            </tr>
            <tr>
                <td class="mobile-off" width="15" style="font-size: 15px; line-height: 15px;">&nbsp;</td>
              </tr>
              <tr>
                <td align="center"><table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" width="465" style="Margin: auto; width: 465px; border-collapse: collapse;">
                    <tbody><tr>
                      <td align="left"><!-- BODY INTRO -->

                        <table align="left" role="presentation" cellspacing="0" cellpadding="0" border="0" width="465" style="width: 465; border-collapse: collapse;">
                          <tbody><tr>
                            <td class="main-content" align="center" style="font-family: Arial, sans-serif; font-size: 17px; font-weight: bold; color: #454545; line-height: 140%;"><p style="Margin: 0;">
                             Code: DS2403D7DTMWVHWZV4 &nbsp;&nbsp;&nbsp;<br style="display: none;" class="mobile-on">Expires 14 days after issue</p></td>
                          </tr>
                        </tbody></table>
                      </td>
                    </tr>
                  </tbody>
                </table>
                </td>
              </tr>
              <tr>
                <td class="mobile-off" width="15" style="font-size: 15px; line-height: 15px;">&nbsp;</td>
              </tr>
              <tr>
                <td align="center"><table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" width="465" style="Margin: auto; width: 465px; border-collapse: collapse;">
                    <tbody><tr>
                      <td align="left"><!-- BODY INTRO -->

                        <table align="left" role="presentation" cellspacing="0" cellpadding="0" border="0" width="465" style="width: 465; border-collapse: collapse;">
                          <tbody><tr>
                            <td class="main-content" align="center" style="font-family: Arial, sans-serif; font-size: 16px; font-weight: normal; color: #b59958; line-height: 150%;">
                              <img class="mobile-off" src="https://mywingstopsurvey.com/Projects/WINGS_CSI/images/emailer/smg-wingstop-incentive-hr-btm.png" alt="WHERE FLAVOR GETS ITS WINGS" border="0" width="465" style="width: 100%; display: block; color: #000000; font-family: Helvetica, Arial, sans-serif; font-weight: bold; font-size: 14px !important;">
                            </td>
                          </tr>
                          <!-- Mobile Image -->
                          <!--[if !mso]><!-->
                            <tr>
                              <td valign="top" align="center">
                                <div class="mobile-on" style="display: none; font-family: Arial, sans-serif; color: #ffffff; font-size: 0; height: 0; mso-line-height-rule: exactly; line-height: 0;padding: 0; mso-hide: all; text-align: center;">
                                  <img class="mobile-img" src="https://mywingstopsurvey.com/Projects/WINGS_CSI/images/emailer/smg-wingstop-incentive-hr-btm-mobile.png" alt="WHERE FLAVOR GETS ITS WINGS" border="0" width="0" style="display: none; color: #000000; background-color: #ffffff; padding: 0 7%; font-family: Arial, Helvetica, sans-serif; font-weight: bold;">
                                </div>
                              </td>
                            </tr>
                            <!--<![endif]-->
                        </tbody></table>
                      </td>
                    </tr>
                  </tbody>
                </table>
                </td>
              </tr>

          </tbody></table>
          <!-- Survey Body Content : END -->

                <!-- Horizontal Spacer : BEGIN -->
                <table role="presentation" bgcolor="#ffffff" cellspacing="0" cellpadding="0" border="0" align="center" width="550" style="Margin: auto; width: 550px; border-collapse: collapse;" class="email-container">      
                  <tbody><tr>
                    <td height="30" style="font-size: 30px; mso-line-height-rule: exactly; line-height: 30px;">&nbsp;</td>
                  </tr>
                </tbody></table>
                <!-- Horizontal Spacer : END -->

          <!-- PJ Boiler : Begin -->
          <table role="presentation" bgcolor="#e5e5e5" cellspacing="0" cellpadding="0" border="0" align="center" width="550" style="Margin: auto; width: 550px; border-collapse: collapse;" class="email-container">
            <tbody>
            <tr>
              <td class="mobile-off" width="30" style="font-size: 30px; line-height: 30px;">&nbsp;</td>
            </tr>
            <tr>
              <td align="center"><table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" width="550" style="Margin: auto; width: 550px; border-collapse: collapse;">
                  <tbody><tr>
                    <td align="left" class="footer-content">

                      <table align="left" role="presentation" cellspacing="0" cellpadding="0" border="0" width="550" style="width: 550; border-collapse: collapse;">
                        <tbody><tr>
                          <td class="ios-link" align="left" style="font-family: Arial, sans-serif; font-size: 12px; font-weight: normal; color: #5c5c5c; line-height: 150%;"><p style="Margin: 0;">
                          This is an unmonitored email box. Please do not reply to this email. This email was sent on behalf of Wingstop Restaurants, Inc. by SMG. ©2019 Service Management Group, Inc. All rights reserved. 1737&nbsp;McGee Street, Kansas City, MO 64108. You are receiving this email because of your recent survey completion. <a href="http://www.smg.com" target="_blank" style="color: #696969; text-decoration: underline;">Click here to unsubscribe.</a> Please note that you will continue to receive offers, promotions and updates from Wingstop if you unsubscribe from this survey reward&nbsp;email.
                          </p></td>
                        </tr><tr>
                          <td class="mobile-spacer" style="height: 0; width: 0; font-size: 0; line-height: 0;">&nbsp;</td>
                        </tr>
                      </tbody></table>
                    </td>
                  </tr>
                </tbody></table></td>
            </tr>
            <tr>
              <td class="mobile-off" width="30" style="font-size: 30px; line-height: 30px;">&nbsp;</td>
            </tr>
          </tbody></table>
          <!-- PJ Boiler : End -->

                <!-- Gmail Fix : START (Forces Desktop view on Android and Gmail Apps where responsive design is not supported.) -->
                <table class="mobile-off" cellpadding="0" cellspacing="0" border="0" align="center" width="550" style="width: 550px; Margin: 0; border-collapse: collapse;">
                  <tbody><tr>
                    <td class="mobile-off" height="1" style="mso-line-height-rule: exactly; line-height: 1px; min-width: 550px;">
                      <img class="mobile-off" src="https://mywingstopsurvey.com/Projects/WINGS_CSI/images/emailer/itsy-spacer.gif" alt="" width="550" height="1" style="display: block; max-height: 1px; min-height: 1px; min-width: 550px; width: 550px;">
                    </td>
                  </tr>
                </tbody></table>
                <!-- Gmail Fix : END -->

              </center>

          <img src="https://mywingstopsurvey.com/Projects/WINGS_CSI/images/emailer/itsy-spacer.gif" width="1" height="1">
          </body></html>'''

    code = wingstopemailparse(email)
    print(code)
    

if __name__ == "__main__":
    main()