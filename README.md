# temp8

```temp8``` is a wrapper for **[temp-mail.org](https://temp-mail.org/en/)**. It allows you to create temporary emails and check its inbox.

**temp-mail.org has now activated Cloudflare's anti-bot protection. This means that you can encounter some issues when using temp8.**

## Why temp8 ?

I could have paid for the API, but why would I do that when I can just use a few requests? It's not like they're going to sue me haha ^^^^. (pls don't)

## Output example
![temp8 output](img/demo_fixed.gif?raw=true "temp8 output example")

## Installation
```py
pip install -r requirements.txt
```

You will also need to install [nodejs](https://nodejs.org/en/download/) as [cloudscraper](https://www.github.com/VeNoMouS/cloudscraper) uses it to bypass Cloudflare's anti-bot protection.

## Quick start
```py
tempmail = TempMail() # This generates a random mailbox
print(tempmail.mailbox) # Prints the email address
print(tempmail.get_messages()) # Prints the inbox, and saves it locally as a json file
print(tempmail.get_mail_data(id)) # Prints the mail data and saves it locally (Attachements included)
```

## What does it do ?
It creates a random mail on **[temp-mail.org](https://temp-mail.org/en/)** and allows you to check its inbox.
Your new email address, its token, and the timestamp when it was created are stored in a file called ```mailbox.json```.
Every time you instantiate a ```TempMail``` object, it checks if the mailbox is still valid (Timestamp less than 1 hour). If it's not, it creates a new one.

## Contributing
Feel free to create a pull request if you want to add something to the project. I'll be happy to review it. :)