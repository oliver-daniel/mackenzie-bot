# coding: utf-8
import os
import sys

from fbmq import Page
from flask import Flask, request

app = Flask(__name__)

page = Page(os.environ['PAGE_ACCESS_TOKEN'])


@app.route('/', methods=['GET'])
def verify():
    if request.args.get('hub.mode') == "subscribe" and \
            request.args.get('hub.challenge'):
        if request.args.get('hub.verify_token') == os.environ['VERIFY_TOKEN']:
            print("all good")
            return request.args['hub.challenge'], 200
        return "Verification token mismatch", 403

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_data(as_text=True)
    page.handle_webhook(data)

    return "ok", 200


@page.handle_message
def handle_message(event):
    sender_id = event.sender_id
    message = event.message

    log(message)

    page.send(sender_id, message.get('text').encode('utf-8'))


@page.after_send
def after_send(payload, response):
    log("message sent.")


def log(msg):
    if os.environ['DEBUG'] == "TRUE":
        print(str(msg))
        sys.stdout.flush()


if __name__ == '__main__':
    app.run()
