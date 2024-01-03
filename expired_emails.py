from simplegmail import Gmail
from simplegmail.query import construct_query

def delete_coupons():
    gmail = Gmail()

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
    delete_coupons()

if __name__ == "__main__":
    main()
