# -*- coding: utf-8 -*-
# --------------------------------------------------
# temp-mail.org wrapper test file
# Quentin 'MCXIV' Dufournet, 2023
# --------------------------------------------------
# Built-in
import sys
import os

# 3rd party
import temp8 as script

# --------------------------------------------------


def test_init():
    """ Scenario:
    * Init the class
    * Check if the mailbox.json file exists
    * Check the class attributes (i.e. file loaded properly)
    """

    mail = script.TempMail()
    assert os.path.exists('mailbox.json') == True
    assert mail.mailbox is not None
    assert mail.token is not None
    assert mail.timestamp is not None


def test_generate_mailbox():
    """ Scenario:
    * Init the class
    * Remove the mailbox.json file
    * Check if the file has been removed
    * Generate a new mailbox
    * Check if the file has been created
    * Check if the file is not empty
    """

    mail = script.TempMail()
    os.remove('mailbox.json')
    assert os.path.exists('mailbox.json') == False
    mail = mail.generate_mailbox()
    assert os.path.exists('mailbox.json') == True
    assert os.path.getsize('mailbox.json') > 0


def test_get_messages():
    """ Scenario:
    * Init the class
    * Get the messages
    * Check if the messages are not None (i.e. the request was successful, messages can be empty)
    """

    mail = script.TempMail()
    messages = mail.get_messages()
    assert messages is not None
