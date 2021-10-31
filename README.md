# Writing Forever...

This program will let you being displayed as writing on Instagram for ever!

## How?
The script is Selenium based and will mimic a user going to dm, and start writing..

## Why Selenium and not direct api call?
I would liked to, but the Instagram web app isn't using http call to trigger this writing event, and I do think that the android app is acting same

## How to use?

```
git clone https://github.com/ghrlt/writing-forever
cd writing-forever
python3 app.py
```
The program will next ask you your Instagram username & password; input them
> It is safe. Credentials are not stored in any way. Only Instagram cookies are saved and you can delete them if you want (WritingForever.\<username>.cookies)
 
Then, you will be asked if you want to use proxy, altough I do not recommend to.

Few seconds after, you will be prompted a list of your latest 16 chats (Groups excluded), input the id of the chat you want to appear as writing
and.. That's all !

## Notes
You can write random password as long as the cookie file is still there and valid

Proxy must be http/https

KeyboardInterrupt handling is broken.. Feel free to fork & fix

You can disable headless mode by running app like that
```
python3 app.py no-h
```
