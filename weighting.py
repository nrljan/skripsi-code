# %%
import sys
import os
import json
from dateutil import parser
import networkx as nx
import pandas as pd

# %%
def add_or_inc_edge(G,f,t):
    """
    Adds an edge to the graph IF the edge does not exist already. 
    If it does exist, increment the edge weight.
    Used for quick-and-dirty calculation of projected graphs from 2-mode networks.
    """
    if G.has_edge(f,t):
        G[f][t]['weight']+=1
    else:
        G.add_edge(f,t,weight=1)

# %%
"""
Extract user and their relation based on reply and retweeted status/data.
The data is Indonesian.
After that, relation weighting with function add_or_inc_edge.
"""

tweet_dir='data/'
filez=os.listdir(tweet_dir)
G=nx.DiGraph()
for file in filez:
#file=filez[0]
    f_in=open(tweet_dir+file,'rb')
    
    print ("<<<<"+file+">>>>>")
    ### each line in the file corresponds to 1 tweet in a raw format
    ### we will build retweet networks from the at-tags in the file
    for line in f_in:
        try:
            tweet=json.loads(line)
        except:
            ##some JSON records are malformed. Skip them
            continue
        
        ## harvest attags from the JSON structure; skip tweet if there is an error
        try:
            author=tweet['user']['screen_name']
            attags=tweet['entities']['user_mentions']
            rep_to=tweet['in_reply_to_screen_name']
            #ret_from=tweet['retweeted_status']['user']['screen_name']
            #lang = tweet['lang']
        except:
            continue
        
       # if rep_to and lang == 'in':
        if rep_to:
            print (author, rep_to)
            add_or_inc_edge(G,author,rep_to)
        for attag in attags:
            #if lang == 'in':
            print (author, attag['screen_name'])
            add_or_inc_edge(G,author,attag['screen_name'])
        
    
        print ('.')
    print ("@@@@@")

# %%
