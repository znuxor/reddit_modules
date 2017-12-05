#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import pickle
import praw

secrets = pickle.load(open(os.path.expanduser('~/secrets.p'), 'rb'))
reddit = praw.Reddit(**secrets)
day = time.strftime("%a", time.gmtime())
hour = time.gmtime().tm_hour
if day in ['Sat', 'Sun']:
    reddit.subreddit('socialskills').mod.update(link_type='all')
    print("all posts")
else:
    reddit.subreddit('socialskills').mod.update(link_type='self')
    print("self posts")
