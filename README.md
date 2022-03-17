# Project

aZaMon is an e-commerce aggregator, where sellers can list products and users can buy them.
(Buy being a figurative word, we don't have an actual payment system)

## Members

Group 9

- Deep Majumder (19CS30015)
- Aaditya Agrawal (19CS10003)
- Pritkumar Godhani (19CS10048)

## Setup

We have tested this to work on **Ubuntu 20.04** (with _Python 3.8_) and **Arch Linux** (with _Python 3.10_).
You need to have the ability to create virtual-environments (usually installed on Ubuntu with `apt install python3-venv`)
and also `pip` to install packages (usually installed on Ubuntu with `apt install python3-pip`).
It is also recommended to have `sqlite3` installed (`apt install sqlite3`).

## Running

```shell
python3 -m venv venv
source ./venv/bin/activate # For bash and zsh
source ./venv/bin/activate.fish # For fish
pip install -r requirements.txt
FLASK_APP=flaskr FLASK_ENV=development flask init-db # Setup db
FLASK_APP=flaskr FLASK_ENV=development flask run # Run the app
```

Then, open `http://localhost:5000/` in Google Chrome/Chromium (the only browsers we have tested the app to run on).

# Video links

[Project Demo](https://youtu.be/cH0tRPOxrec)

[Code Explanation](https://youtu.be/Cw-MFi72u-A) (_Optional_)
