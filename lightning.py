from yopmail import Yopmail

y = Yopmail('wffwingstop', proxies=None)

mails_ids = y.get_mail_ids(page=1)

for mail_id in mails_ids:
    mail = y.get_mail_body(mail_id, show_image=True)
    print(mail)