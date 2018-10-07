# Basic TweetBot

A Twitter Bot that can perform the following actions automatically:
* tweet
* retweet
* favourite
* follow
* reply to mentions
* follow back

### Setting up the bot
First install the Python requirements
```
pip install -r requirements.txt
```

Set up a [Twitter App](https://apps.twitter.com/) (it might take a few days for your developer account to get approved). Once you have an account, add your key, token and secrets to a new file called `credentials.py` similar to the format of `credentials_example.py`.

To test the bot, simply run
```python tweetbot.py```

### Keeping the bot running
To keep the bot running even when the computer is switched of, use the `nohup` command. `nohup` ignores the hangup (HUP) signal and will print output to a file called `nohup.out` instead on the terminal.

In the Twitter Bot directory, run the following command
```nohup python tweetbot.py &```

You should receive output with a number in brackets
```Output:
   [?] 98695
```
This is the ID of the process. To stop the process, run
```kill 98695```
This will stop the Twitter Bot.

If you ever forget the ID of the process, you can retrieve the ID by running the `ps` command for process status, and the `-x` flag to include all processes not attached to terminals:
```ps -x```

To ensure that your bot is running correctly, you check the ```nohup.out``` file with a text editor such as nano
```nano nohup.out```
to check if the program returns the correct output. 
