from tweepy import Stream, OAuthHandler, StreamListener
import json
from datetime import *
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pprint import pprint

timestamp = datetime.strftime(datetime.now(),"%Y%m%d%H%M%S")
analyzer = SentimentIntensityAnalyzer()

class listener(StreamListener):
	global i, runningCompound
	i = 1
	runningCompound = 0.0

	def on_data(self, data):
		global i, runningCompound

		try:
			tweet = json.loads(data)
			#print len(tweet),tweet['user']['screen_name'],tweet['text']
			#print tweet['user']['location'],tweet['user']['geo_enabled'],tweet['coordinates'],tweet['geo'],tweet['place']

			if isNotReply("in_reply_to_screen_name", tweet):

				if len(tweets['no_reply'])<N*3:
					tweets['no_reply'].append(tweet)
					try:
						sentence = str(tweet['text'])
						print(sentence)
						score = sentimentScore(sentence)
						#print(score)
						score = score.get('compound')
						#print(score)
						runningCompound = (runningCompound*(i-1) + score)/i
						i = i + 1

					except Exception as inst:
						print("Unable to print", inst.args)

				else:
					timestamp=datetime.strftime(datetime.now(),"%Y%m%d%H%M%S")
					filename = path2+"dataset_noreply_%s.json"%timestamp
					f=open(filename,'w')
					json.dump(tweets['no_reply'],f, sort_keys=True, indent=4)
					f.close()
					tweets['no_reply'][:]=[]
					print (N, "tweets", timestamp)
					print("\n\n\n", "Running Compound Score: ", runningCompound, "\n\n\n")
				#print len(tweets['no_reply']),tweet['user']['screen_name'],tweet['text']

			else:

				if len(tweets['in_reply'])<N:
					tweets['in_reply'].append(tweet)

					try:
						sentence = str(tweet['text'])
						print(sentence)
						# score = sentimentScore(sentence)
						# #print(score)
						# score = score.get('compound')
						# #print(score)
						# runningCompound = (runningCompound*(i-1) + score)/i
						# i = i + 1

					except Exception as inst:
						print("Unable to print", inst.args)


					names['replyN'].append(tweet["in_reply_to_screen_name"])
					names['screenN'].append(tweet['user']['screen_name'])
				else:
					timestamp=datetime.strftime(datetime.now(),"%Y%m%d%H%M%S")

					f2=open(path1+"dataset_edges_%s.json"%timestamp,'w')

					for i in np.arange(len(names['replyN'])):
						f2.write(names['screenN'][i] + "," + names['replyN'][i] + '\n')

					f2.close()

					f=open(path1+"dataset_reply_%s.json"%timestamp,'w')
					json.dump(tweets['in_reply'],f)
					f.close()
					tweets['in_reply'][:]=[]
					print (N, "tweets", timestamp)
				#print 'Y', len(tweets['in_reply']),tweet['user']['screen_name'],tweet['text']
				#print len(tweet["in_reply_to_screen_name"]),tweet["in_reply_to_screen_name"]
				#sprint

		except Exception as inst:
			print ("something happened", inst.args)

	def on_error(self,status):
		if status == 420:
			# Returning False terminates the Stream to prevent incurring
			# more errors.
			return False;
		print ("Error",status)


def isNotReply(string, tweet):
	return (string not in tweet or tweet[string] == None or tweet[string] == 'null')

def sentimentScore(text):
	return analyzer.polarity_scores(text)

N=50
tweets={'in_reply':[],"no_reply":[]}
names={'replyN':[],"screenN":[]}
path1="Data1/"
path2="Data2/"
ConsumerKey="YpPSDUHum0regAT6vt390zRaR"
ConsumerSecret="0qpxgfv3SkD6GOZnIAxWVJA7TTewfFoVluPy8Dad5oKigQOxuZ"

AccessToken="2675842215-kXO7G1ZqaVo1hUcA2GUSmBz0Aupnfx5FLaZLvS7"
AccessTokenSecret="0HpMPy5z1APpsUyQgBBf9qm4eNmcFRFm1k65Nb8EU0CPB"

auth=OAuthHandler(ConsumerKey,ConsumerSecret)
auth.set_access_token(AccessToken, AccessTokenSecret)

twitterStream=Stream(auth, listener())

#track=["obama","trump"]
track=["war"]
[lon0,lat0,lon1,lat1]=[-74.1687,40.5722,-73.8062,40.9467]
twitterStream.filter(track=track,locations=[lon0,lat0,lon1,lat1])
