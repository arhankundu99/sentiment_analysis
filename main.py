import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


def get_tweet_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'

    return 'negative'


class TwitterClient(object):

    def __init__(self):

        api_key = 'gOrvz1WPr5VcgWFOI4oYGOeWR'
        api_key_secret = 'cqEwHTAA7ZQnJqfcEae0K4XbzkLRGGlvaRNML8EEloDko5dnQv'
        access_token = '1306221655941812226-J2uKBdJPmCIHQRvhJWHzAD34IRDlEd'
        access_token_secret = 'vDnVQ589FQQSnjkbVwVOIwcqyThlhfPft9ecopzgFnUHT'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(api_key, api_key_secret)

            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)

            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)

        except:
            print("Error: Authentication Failed")

    def get_tweets(self, query, count=10):
        tweets = []

        try:
            # calling twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                parsed_tweet = {'text': tweet.text, 'sentiment': get_tweet_sentiment(tweet.text)}
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))


def get_sentiments():
    api = TwitterClient()

    tweets = api.get_tweets(query=metro_name, count=100)

    # positive tweets
    positive_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(positive_tweets) / len(tweets)))

    # negative tweets
    negative_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100 * len(negative_tweets) / len(tweets)))

    # neutral tweets
    neutral_tweets_count = len(tweets) - (len(negative_tweets) + len(positive_tweets))
    print("Neutral tweets percentage: {} % \ ".format(100 * neutral_tweets_count / len(tweets)))

    print("\n\nPositive tweets:")
    for tweet in positive_tweets[:50]:
        print(tweet['text'])

    print("\n\nNegative tweets:")
    for tweet in negative_tweets[:50]:
        print(tweet['text'])


if __name__ == "__main__":
    metro_name = input("Enter Metro Name: ")
    get_sentiments()
