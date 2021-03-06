import requests
from django.conf import settings
import ytAnalytic.scripts.search_api as api
import time

def sort_tag(tag, vid_list):
    tag = tag.strip()
    print('sort tag:', tag)
    filtered = []
    for vid in vid_list:
        # print(filtered)
        time.sleep(1)
        tag_list = api.statistics(requests, vid['id'], vid['thumbnail'])['tags']
        tag_list = [tag.lower() for tag in tag_list]
        if tag in tag_list:
            # print(tag)
            filtered.append(vid['id'])
    return filtered

def tag_list(vid_list):
    tags = []
    for vid in vid_list:
        vid_tags = api.statistics(vid['id'], vid['thumbnail'])['tags']
        for tag in vid_tags:
            tag = tag.lower()
            if tag not in tags:
                tags.append(tag)
    return tags

def order_duration(selection, vid_list):
    if selection.strip() == 'shortest':
        vid_list = sorted(vid_list, key= lambda i: i['durationMin'])
        return vid_list
    elif selection.strip() == 'longest':
        vid_list = sorted(vid_list, key= lambda i: i['durationMin'], reverse=True)
        return vid_list
    return vid_list

def durFunc(e):
    return e['durationMin']