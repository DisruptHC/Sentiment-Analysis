from tweepy import Stream, OAuthHandler, StreamListener
import json
from datetime import *
import numpy as np

timestamp=datetime.strftime(datetime.now(),"%Y%m%d%H%M%S")
				
class listener(StreamListener):
	def on_data(self,data):
		try:
			tweet= json.loads(data)
			#print len(tweet),tweet['user']['screen_name'],tweet['text']
			#print tweet['user']['location'],tweet['user']['geo_enabled'],tweet['coordinates'],tweet['geo'],tweet['place']
			
			if "in_reply_to_screen_name"  not in tweet or tweet["in_reply_to_screen_name"] == None or tweet["in_reply_to_screen_name"] == 'null':
				
				if len(tweets['no_reply'])<N*3:
					tweets['no_reply'].append(tweet)
				else:
					timestamp=datetime.strftime(datetime.now(),"%Y%m%d%H%M%S")
					f=open(path2+"dataset_noreply_%s.json"%timestamp,'w')
					json.dump(tweets['no_reply'],f)
					f.close()
					tweets['no_reply'][:]=[]
					print N, "tweets", timestamp
				#print len(tweets['no_reply']),tweet['user']['screen_name'],tweet['text']
				
			else:
				
				if len(tweets['in_reply'])<N:
					tweets['in_reply'].append(tweet)
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
					print N, "tweets", timestamp
				#print 'Y', len(tweets['in_reply']),tweet['user']['screen_name'],tweet['text']
				#print len(tweet["in_reply_to_screen_name"]),tweet["in_reply_to_screen_name"]
				#sprint
			
		except Exception as inst:
			print "something happened", inst.args

	def on_error(self,status):
		print "Error",status

N=50
tweets={'in_reply':[],"no_reply":[]}
names={'replyN':[],"screenN":[]}
path1="Data1/"
path2="Data2/"
ConsumerKey="Y542qT6sJfKauDPh0Zbs0uI2I"
ConsumerSecret="HuUh1n1QH7q6i8KkLpC7FcvIwSi4mZ4ZFDR2ZeVpVm0yRKLJHr"

AccessToken="1858877738-6HAvRxjjehxv9yeh5xu8sVAgaKEji2dV9PTE3Nt"
AccessTokenSecret="YZAFp87kluASSOUXMDLZLSA3HD5DYDhaTn6HUf0zR4rPs"

auth=OAuthHandler(ConsumerKey,ConsumerSecret)
auth.set_access_token(AccessToken, AccessTokenSecret)

twitterStream=Stream(auth, listener())

#track=["obama","trump"]
track=["obama"]
[lon0,lat0,lon1,lat1]=[-74.1687,40.5722,-73.8062,40.9467]
twitterStream.filter(track=track,locations=[lon0,lat0,lon1,lat1])





