from simplegmail import Gmail
from simplegmail.query import construct_query
import os

def delete_coupons(account):
    os.remove("gmail_token.json")
    gmail = Gmail()
    #gmail = Gmail(client_secret_file='/etc/secrets/client_secret.json')

    if account == 2:
        labels = gmail.list_labels()
        #print(labels)

        inbox = list(filter(lambda x: x.name == 'UNUSED: NOT IN DB', labels))[0]
        expired = list(filter(lambda x: x.name == 'EXPIRED', labels))[0]

        month_params = {
            "older_than": (29, "day"),
            "sender": "BlazePizza@smg.com",
            "labels" : ["UNUSED: NOT IN DB"]
        }

        week_params = {
            "older_than": (13, "day"),
            "sender": ["WINGS@smg.com", "PandaExpressFeedback@smg.com", "dunkinbrands@express.medallia.com"],
            "labels" : ["UNUSED: NOT IN DB"]
        }



        messages = gmail.get_messages(query=construct_query(week_params))
        messages += gmail.get_messages(query=construct_query(month_params))
        print(len(messages))

        for message in messages:
            print("From: " + message.sender)
            print("Subject: " + message.subject)
            print("Date: " + message.date)

            message.modify_labels(to_add=expired, to_remove=inbox)

            
        print(len(messages))
    else:
        labels = gmail.list_labels()


        inbox = list(filter(lambda x: x.name == 'INBOX', labels))[0]
        expired = list(filter(lambda x: x.name == 'EXPIRED', labels))[0]

        month_params = {
            "older_than": (29, "day"),
            "sender": "BlazePizza@smg.com",
            "labels" : ["INBOX"]
        }

        week_params = {
            "older_than": (13, "day"),
            "sender": ["WINGS@smg.com", "PandaExpressFeedback@smg.com", "dunkinbrands@express.medallia.com"],
            "labels" : ["INBOX"]
        }



        messages = gmail.get_messages(query=construct_query(week_params))
        messages += gmail.get_messages(query=construct_query(month_params))
        print(len(messages))

        for message in messages:
            print("From: " + message.sender)
            print("Subject: " + message.subject)
            print("Date: " + message.date)

            message.modify_labels(to_add=expired, to_remove=inbox)

            
        print(len(messages))

def main():
    print("Which Account?")
    print("1 - foodsurveycodes")
    print("2 - wff")
    account = int(input("Enter account number: "))
    
    delete_coupons(account)

if __name__ == "__main__":
    main()
