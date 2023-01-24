# -*- coding: utf-8 -*-
# --------------------------------------------------
# temp-mail.org wrapper
# Quentin 'MCXIV' Dufournet, 2023
# --------------------------------------------------
# Built-in
import sys
import time
import json
import os

# 3rd party
import requests
from fake_useragent import UserAgent
from rich import print_json, print as rprint

# --------------------------------------------------


class TempMail:
    def __init__(self):
        """
        If a mailbox config exists, load the data from the file, and if the data is more than an hour old,
        generate a new mailbox
        """

        self.userAgent = UserAgent().random
        if os.path.exists('mailbox.json') and os.path.getsize('mailbox.json') > 0:
            with open('mailbox.json', 'r') as f:
                data = json.load(f)
                self.timestamp = data['timestamp']
            if time.time() - self.timestamp > 3600:
                self.generate_mailbox()

        else:
            self.generate_mailbox()

        with open('mailbox.json', 'r') as f:
            data = json.load(f)
            self.token = data['token']
            self.mailbox = data['mailbox']
            self.timestamp = data['timestamp']

    def generate_mailbox(self):
        """
        It generates a new email address and saves it to a file
        """

        headers = {
            'User-Agent': self.userAgent,
        }

        response = requests.post('https://web2.temp-mail.org/mailbox', headers=headers)
        if response.status_code != 200:
            sys.exit('Error: Could not generate a new mail')

        response = response.json()
        response['timestamp'] = time.time()

        with open('mailbox.json', 'w+') as f:
            json.dump(response, f, indent=4, sort_keys=True)

    def get_messages(self):
        """
        It gets the messages from the temp-mail.
        :return: A list of dictionaries.
        """

        headers = {
            'User-Agent': self.userAgent,
            'Authorization': f'Bearer {self.token}',
        }

        response = requests.get('https://web2.temp-mail.org/messages', headers=headers)
        if response.status_code != 200:
            sys.exit('Error: Could not get messages')

        return response.json()['messages']


if __name__ == '__main__':
    tempmail = TempMail()
    rprint('[bold green]Your mailbox: ', tempmail.mailbox)
    while 1:
        rprint('[bold magenta]Last mail received:')
        try:
            print_json(json.dumps(tempmail.get_messages()[-1], indent=4))
        except IndexError:
            rprint('[bold red]No mail received yet')
        time.sleep(10)
