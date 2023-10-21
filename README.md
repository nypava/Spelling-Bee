# Spelling Bee
Spelling Bee is a multiplayer game in which players form words from a given set of 7 letters using a Telegram bot to submit their words.

## Installation
### Install python 
Install python3 from [offcial website.](https://www.python.org/downloads)
### Install pip 
You can install pip3 using [this](https://www.makeuseof.com/tag/install-pip-for-python/) article.
### Install dependecies

**Windows**
```
pip install -r requirements.txt
```
**Linux(debian)**
```
sudo apt-get update
sudo apt-get install python3-tk
python3 -m tkinter
pip install -r requirements.txt
```

# Usage
In [config.py](/config.py), replace bot_token with your bot token from @botfather. Add your Telegram ID to the admin_ids list to control the bot (it can be empty).

Then you can run the script

```
python main.py
```

To play a new game, clear the cache 
```
python clearcache.py
```
OR 
send /reset command to the bot.

## Customization
### Customization of text sent to players in bot
You can change bot text on [data/text.json](/data/text.json).

### Customization of names given to players
You can change names on [data/text.json](/data/name.json).

### Customization of letters (spellings)
You can change spellings on [data/text.json](/data/name.json), the first letter of the list is central letter.
## Game Rules

* All letters that you form must be in the list of letters.
* The word that you form must include the center letter.
* The length of the word must be at least 4.
* Letters can be used more than once.
* Points increase as the length of your word increases.


## Screenshots
**Starting a bot to let players to join the game**
![image](https://graph.org/file/795a0f59d095b1bea6d9f.jpg)

**Starting a game**
![image](https://telegra.ph/file/86232bd305e03b09f16c4.jpg)

**On game**
![image](https://graph.org/file/f60fe47154293d9576d29.jpg)

**Telegram bot accepting and valuating the user input**
![image](https://graph.org/file/c399cabbb6ec9a04571f6.jpg)