import tweepy

# authorization tokens
consumer_key = "Nb5xwy1q93AgUAJnEHN7q2ssI"
consumer_secret = "7EajnwNOVF93ngykqtkQQIKdbkurSnyd5vKOYe8ICwY4QdDmqD"
access_key = "1232312367087665152-IeWXIq0bN5q87UWUE0VmNsnnJOqNeL"
access_secret = "C1KMiKkOqAjUaUmlT2GhuGklIzebtCGFUA35BQbDstrZJ"


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.id_str)
        # if "retweeted_status" attribute exists, flag this tweet as a retweet.
        is_retweet = hasattr(status, "retweeted_status")

        # check if text has been truncated
        if hasattr(status,"extended_tweet"):
            text = status.extended_tweet["full_text"]
        else:
            text = status.text

        # check if this is a quote tweet.
        is_quote = hasattr(status, "quoted_status")
        quoted_text = ""
        if is_quote:
            # check if quoted tweet's text has been truncated before recording it
            if hasattr(status.quoted_status,"extended_tweet"):
                quoted_text = status.quoted_status.extended_tweet["full_text"]
            else:
                quoted_text = status.quoted_status.text

        # remove characters that might cause problems with csv encoding
        remove_characters = [",","\n"]
        for x in remove_characters:
            text.replace(x," ")
            quoted_text.replace(x, " ")


        with open("happy.csv", "a", encoding='utf-8') as f:
            f.write("%s,%s,%s,%s,%s,%s\n" % (status.created_at,status.user.screen_name,is_retweet,is_quote,text,quoted_text))

if __name__ == "__main__":
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    auth.set_access_token(access_key, access_secret)

    api = tweepy.API(auth)


    streamListener = StreamListener()

    stream = tweepy.Stream(auth=api.auth, listener=streamListener,tweet_mode='extended')

    tags = ["#happy"]

    stream.filter(track=tags)

