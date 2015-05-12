#from nexmomessage import NexmoMessage
from django.conf import settings
from nexmo.libpynexmo.nexmomessage import NexmoMessage


class NexmoClient:

    def send(recipient, path):
        msg = {
            'reqtype': 'json',
            'api_key': settings.NEXMO_KEY,
            'api_secret': settings.NEXMO_SECRET,
            'from': 'Yishai',
            'to': recipient,
            'text': "Hello, please click the link to \
                     complete your call with us: "+path
        }
        sms = NexmoMessage(msg)
        sms.set_text_info(msg['text'])
        response = sms.send_request()
        return response

    def sendMessage(recipient, message):
        msg = {
            'reqtype': 'json',
            'api_key': settings.NEXMO_KEY,
            'api_secret': settings.NEXMO_SECRET,
            'from': 'Touch-N-Go',
            'to': recipient,
            'text': message
        }
        sms = NexmoMessage(msg)
        sms.set_text_info(msg['text'])
        response = sms.send_request()
        return response
