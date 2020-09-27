from twilio.rest import Client
from typing import Type
account_sid = 'ACfa3ae5e3f45bc3117c8acdb2a746dda5'
auth_token = '5367f96ec73961710eadd7cdcdfbe1a1'
client = Client(account_sid, auth_token)
msg = ""
scheema_object = {'adviser': 'Angel', 'customer_name': 'Brand',
                  'appointment_time': '3:00pm',
                  'adviser_number': '+?????',
                  'customer_number': '+???'}
link = "www.autonation.com"


def send_msg(msg, to):
    message = client.messages.create(
        from_='+?????',
        body=msg,
        to=to
    )
    return message


def appointment_found(service, user):
    msg = f"Greetings {service['advisor_name']}!\n{user['first']} {user['last']} is "\
        f"here for their {service['time']} appointment"
    return send_msg(msg, service['adviser_number'])


def appointment_not_found(user):
    msg = f"Greetings {user['first']}!\nThank you for visiting AutoNation "\
          f"We did not find any appointments for you today.\n\nIf you wish to"\
          f" schedule a drive-in appointment you can do it directly from {link}"
    return send_msg(msg, user['customer_number'])


def appointment_too_early(user, timediff):
    msg = f"Greetings {user['first']} {user['last']}!\nThank you for visiting AutoNation "\
          f"It looks like you are {timediff} minutes early, do"


print(appointment_not_found(scheema_object))
