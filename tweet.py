import twitter
import argparse
from typing import List

StringVector = List[str]

class KidnappedTweet:
    def __init__(self):
        self.api = twitter.Api(
            consumer_key='HjmuHu5jECTofRmd1pHs8NeHg',
            consumer_secret='ZaEKo2smSV58e9nopzD8GCgVmayeOjF343gRXnJv9nwh0gmPDx',
            access_token_key='1051534889307258880-TOpjUkMZY1MxQinKP0Qz2xIZRtwaBT',
            access_token_secret='L6DKU3aRKAvdZ33ionzDE4TWwvfo4v3YVo07KLiAyUWLW'
        )

    def make_tweet(self, message: str) -> int :
        status:twitter.Status = None
        try:
            status = self.api.PostUpdate(message)
        except UnicodeDecodeError:
            print('Message could not be encoded as unicode!')
            return status
        return status

    def get_comments(self) -> StringVector :
        pass

if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument('msg')
    args = parser.parse_args()

    tweet = KidnappedTweet()
    ret = tweet.make_tweet(args.msg)

    if ret != None:
        print("{0} tweeted: {1}".format(ret.user.name, ret.text))

