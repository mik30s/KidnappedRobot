import twitter
import argparse
import os
from typing import Dict, List

ReplyDict = Dict[str, Dict[str, str]]

class KidnappedTweet:
    def __init__(self):
        self.api = twitter.Api(
            consumer_key='HjmuHu5jECTofRmd1pHs8NeHg',
            consumer_secret='ZaEKo2smSV58e9nopzD8GCgVmayeOjF343gRXnJv9nwh0gmPDx',
            access_token_key='1051534889307258880-TOpjUkMZY1MxQinKP0Qz2xIZRtwaBT',
            access_token_secret='L6DKU3aRKAvdZ33ionzDE4TWwvfo4v3YVo07KLiAyUWLW'
        )

    def make_tweet(self, message: str, photo=None) -> int :
        status:twitter.Status = None
        try:
            status = self.api.PostUpdate(message, media=photo)
        except UnicodeDecodeError:
            print('Message could not be encoded as unicode!')
            return status
        return status

    def get_comments(self, tweet_id) -> ReplyDict:
        comments = []
        replies = self.api.GetReplies(since_id=tweet_id)
        for reply in replies:
            #print(repl)
            comments.append({
                "record_id": reply.id_str,
                "user_id": str(tweet_id),
                "user_screen_name": reply.in_reply_to_screen_name, 
                "text": reply.text
            })
        return comments

    def start_watching(self):
        pass
        
if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument('--msg')
    parser.add_argument('--rep_id')
    parser.add_argument('--img')
    args = parser.parse_args()
    
    tweet = KidnappedTweet()
    
    if args.msg != None:
        img_fp = None
        if args.img != None:
            print('loading image')
            img_fp = os.path.abspath(args.img)
            #print(type(img_fp))
        ret = tweet.make_tweet(args.msg, img_fp)
        if ret != None:
            print("{0} tweeted: {1}, {2}".format(ret.user.name, ret.text, ret.id))
    if args.rep_id != None:
        replies = tweet.get_comments(args.rep_id)
        print('Replies {}'.format(replies))

