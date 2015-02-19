#from nexmomessage import NexmoMessage
from nexmo.libpynexmo.nexmomessage import NexmoMessage


class NexmoClient:
    api_key = '835ff543'
    secret = '68d3f00d'

    def send(recipient, path):
        msg = {
            'reqtype': 'json',
            'api_key': NexmoClient.api_key,
            'api_secret': NexmoClient.secret,
            'from': 'Yishai',
            'to': recipient,
            'text': "Hello, please follow this link: "+path
        }
        sms = NexmoMessage(msg)
        sms.set_text_info(msg['text'])
        response = sms.send_request()
        return response
