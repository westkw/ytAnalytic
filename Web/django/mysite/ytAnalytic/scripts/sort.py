import requests
from django.conf import settings
import ytAnalytic.scripts.search_api as api
import time

def sort_tag(requests, tag, vid_list):
    filtered = []
    for vid in vid_list:
        print(filtered)
        time.sleep(1)
        tag_list = api.tags(requests, vid['id'])
        if tag in tag_list:
            filtered.append(vid['id'])
    return filtered