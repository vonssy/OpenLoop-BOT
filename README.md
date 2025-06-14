# OpenLoop.SO Sentry Node BOT
OpenLoop.SO Sentry Node BOT

- Register Here : [OpenLoop.SO Sentry Node Dashboard](https://openloop.so/auth/register?ref=ol92f69d11)
- Download [OpenLoop.SO Sentry Node Extension](https://chromewebstore.google.com/detail/openloopso-sentry-node-ex/effapmdildnpkiaeghlkicpfflpiambm)
- Use Code `ol92f69d11`

## Features

  - Auto Get Account Information
  - Auto Run With [Free Proxyscrape](https://proxyscrape.com/free-proxy-list) Proxy - `Choose 1`
  - Auto Run With Private Proxy - `Choose 2`
  - Auto Run Without Proxy - `Choose 3`
  - Auto Rotate Invalid Proxies - `y` or `n`
  - Auto Complete Available Tasks
  - Auto Send Ping Every 15 Minutes
  - Multi Accounts With Threads

## Requiremnets

- Make sure you have Python3.9 or higher installed and pip.
- 2captcha key (optional)

## Instalation

1. **Clone The Repositories:**
   ```bash
   git clone https://github.com/vonssy/OpenLoop-BOT.git
   ```
   ```bash
   cd OpenLoop-BOT
   ```

2. **Install Requirements:**
   ```bash
   pip install -r requirements.txt #or pip3 install -r requirements.txt
   ```

## Configuration

- **2captcha_key.txt:** You will find the file `2captcha_key.txt` inside the project directory. Make sure `2captcha_key.txt` contains data that matches the format expected by the script. Here are examples of file formats:
  ```bash
    your_2captcha_key
  ```

- **accounts.json:** You will find the file `accounts.json` inside the project directory. Make sure `accounts.json` contains data that matches the format expected by the script. Here are examples of file formats:
  ```json
    [
        {
            "Email": "your_email_address_1",
            "Password": "your_password_1"
        },
        {
            "Email": "your_email_address_2",
            "Password": "your_password_2"
        }
    ]
  ```

### Note

- If you don't have a 2cpatcha key, you can fetch the data manually and put it in tokens.json according to the format.

<div style="text-align: center;">
  <img src="image.png" alt="Image" width="500"/>
</div>
  
- **tokens.json:** You will find the file `tokens.json` inside the project directory. Make sure `tokens.json` contains data that matches the format expected by the script. Here are examples of file formats:
  ```json
    [
        {
            "Email": "your_email_address_1",
            "accessToken": "your_access_token_1"
        },
        {
            "Email": "your_email_address_2",
            "accessToken": "your_access_token_2"
        }
    ]
  ```

- **proxy.txt:** You will find the file `proxy.txt` inside the project directory. Make sure `proxy.txt` contains data that matches the format expected by the script. Here are examples of file formats:
  ```bash
    ip:port # Default Protcol HTTP.
    protocol://ip:port
    protocol://user:pass@ip:port
  ```

## Setup

```bash
python setup.py #or python3 setup.py
```

## Run

```bash
python bot.py #or python3 bot.py
```

## Buy Me a Coffee

- **EVM:** 0xe3c9ef9a39e9eb0582e5b147026cae524338521a
- **TON:** UQBEFv58DC4FUrGqinBB5PAQS7TzXSm5c1Fn6nkiet8kmehB
- **SOL:** E1xkaJYmAFEj28NPHKhjbf7GcvfdjKdvXju8d8AeSunf
- **SUI:** 0xa03726ecbbe00b31df6a61d7a59d02a7eedc39fe269532ceab97852a04cf3347

Thank you for visiting this repository, don't forget to contribute in the form of follows and stars.
If you have questions, find an issue, or have suggestions for improvement, feel free to contact me or open an *issue* in this GitHub repository.

**vonssy**