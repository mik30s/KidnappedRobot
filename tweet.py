import twitter
import argparse
import os, redis
from typing import Dict, List
import threading, time
from google.cloud import datastore

ReplyDict = Dict[str, Dict[str, str]]

class KidnappedTweet:
    def __init__(self):
        self.api = twitter.Api(
            consumer_key='HjmuHu5jECTofRmd1pHs8NeHg',
            consumer_secret='ZaEKo2smSV58e9nopzD8GCgVmayeOjF343gRXnJv9nwh0gmPDx',
            access_token_key='1051534889307258880-TOpjUkMZY1MxQinKP0Qz2xIZRtwaBT',
            access_token_secret='L6DKU3aRKAvdZ33ionzDE4TWwvfo4v3YVo07KLiAyUWLW'
        )
        self.redis_db = redis.Redis(
            host='locahost',
            port='3666'
        )
        self.tweetThread = None
        self.watchThread = None
        self.tweetIds = []

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

    def __store_replies(self, reply:ReplyDict):
        self.redis_db.set(reply['record_id'], {
            'user_id':reply['user_id'],
            'user_screen_name': reply['user_screen_name'],
            'text': reply['text']
        })

    def tweetCallback(self):
        # make a tweet and get id
        img_fp = os.path.abspath('./img/scibldg.jpg')
        #print(type(img_fp))
        i = 0
        while True:
            ret = self.make_tweet('Where am I? ({0})'.format(i), img_fp)
            print("{0} tweeted: {1}, {2}".format(ret.user.name, ret.text, ret.id))
            self.tweetIds.append(ret.id)
            time.sleep(60)
            i = i+1
    
    def readCommentsCallback(self):    
        while True:
            for tweetId in self.tweetIds:
                comments = self.get_comments(tweetId)
                print('Tweet: {0}\ngot:\n\t {1}'.format(tweetId, comments))
                time.sleep(5)
                if len(comments) > 0:
                    for comment in comments:
                        self.__store_replies(comment)
            time.sleep(80)
            

    def start(self):  
        print('start commenting...')           
        self.tweetThread = threading.Thread(target=self.tweetCallback)
        self.tweetThread.start()
        
        self.commentsThread = threading.Thread(target=self.readCommentsCallback)
        self.commentsThread.start()
             
    def end(self):
        self.tweetThread.join()
        self.commentsThread.join()
        print('end commenting...')           
   
        
if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument('--msg')
    parser.add_argument('--rep_id')
    parser.add_argument('--img')
    parser.add_argument('--watch', type=bool)
    args = parser.parse_args()
    
    tweet = KidnappedTweet()
    
    if args.watch != None:
        tweet.start()
        
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













