# README

This is a script that generates a Youbot: remixing your old Tweets with a Markov chain generator to produce unique, ridiculous Tweets that you haven't thought of yet. 

Tweeting functionality is included but disabled by default. Feel free to host this somewhere with a cron job to actually make a Twitter bot. If you do, please [let me know](http://twitter.com/sashalaundy) :)

## To generate tweets: 

1. Download your Twitter archive from Twitter
2. Move the data/ folder from your archive into the repo
3. Run the script. Usage: `$ python script.py 10` where `10` is the number of fake tweets you want it to generate.
4. Optional: if you want to train the bot on a different corpus, just put the training text into one big file with newlines at the end of each line. Highly recommend on the order of 10^5 lines at minimum, otherwise you risk getting training lines back out verbatim. 

## To hook up to Twitter:

1. Grab your dev credentials from twitter.com and paste them into twitterclient.py
2. Turn on tweeting in markovgenerator.py
3. Set up hosting & cron
4. Profit
