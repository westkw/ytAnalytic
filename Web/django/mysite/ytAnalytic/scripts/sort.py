import requests
from django.conf import settings
import ytAnalytic.scripts.search_api as api
import time

def sort_tag(requests, tag, vid_list):
    tag = tag.strip()
    filtered = []
    for vid in vid_list:
        print(filtered)
        time.sleep(1)
        tag_list = api.statistics(requests, vid['id'])['tags']
        tag_list = [tag.lower() for tag in tag_list]
        if tag in tag_list:
            print(tag)
            filtered.append(vid['id'])
    return filtered

def tag_list(requests, vid_list):
    tags = []
    for vid in vid_list:
        vid_tags = api.statistics(requests, vid['id'])['tags']
        for tag in vid_tags:
            tag = tag.lower()
            if tag not in tags:
                tags.append(tag)
    return tags