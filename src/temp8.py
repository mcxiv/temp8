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
import cloudscraper

# --------------------------------------------------


class TempMail:
    def __init__(self):
        """
        If a mailbox config exists, load the data from the file, and if the data is more than an hour old,
        generate a new mailbox
        """

        self.scraper = cloudscraper.create_scraper()

        if os.path.exists('mailbox.json') and os.path.getsize('mailbox.json') > 0:
            with open('mailbox.json', 'r') as f:
                data = json.load(f)
                self.timestamp = data['timestamp']
            if time.time() - self.timestamp > 3600:
                self.generate_mailbox()

        else:
            mailbox = self.generate_mailbox()
            if mailbox == -1:
                sys.exit('Error: Could not generate a mailbox. Please, try again.')

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
            'User-Agent': UserAgent().random,
        }

        timeout = time.time()
        while 1:
            response = self.scraper.post('https://web2.temp-mail.org/mailbox', headers=headers)
            if response.status_code == 200:
                break
            if time.time() - timeout >= 5:
                return -1
            self.scraper = cloudscraper.create_scraper()

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
            'User-Agent': UserAgent().random,
            'Authorization': f'Bearer {self.token}',
        }

        timeout = time.time()
        while 1:
            response = self.scraper.get('https://web2.temp-mail.org/messages', headers=headers)
            if response.status_code == 200:
                break
            if time.time() - timeout >= 5:
                return -1
            self.scraper = cloudscraper.create_scraper()

        return response.json()['messages']


if __name__ == '__main__':
    tempmail = TempMail()
    rprint('[bold green]Your mailbox: ', tempmail.mailbox)
    while 1:
        rprint('[bold magenta]Last mail received:')
        try:
            messages = tempmail.get_messages()
            if messages == -1:
                rprint('[bold red]Error while getting messages, retrying in 10 seconds')
            else:
                print_json(json.dumps(messages[-1], indent=4))
        except IndexError:
            rprint('[bold red]No mail received yet')
        time.sleep(10)
