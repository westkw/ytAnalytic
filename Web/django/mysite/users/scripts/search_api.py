from django.core.cache import caches, cache
import requests
from django.conf import settings

def channel_stats(requests, channel_id):
    if cache.get(channel_id) == None:
        search_url = 'https://www.googleapis.com/youtube/v3/channels'
        params = {
            'part' : 'statistics,snippet,contentDetails',
            'key' : settings.YOUTUBE_API_KEY,
            'type' : 'channel',
            'id' : channel_id
        }
        
        r = requests.get(search_url, params=params)
        results = r.json()['items'][0]
        # print(results)
        
        if results['statistics']['hiddenSubscriberCount']:
            sub_count = -1
        else:
            sub_count = results['statistics']['subscriberCount']

        stats = { 
            'id' : channel_id,
            'channelTitle' : results['snippet']['title'],
            'title' : results['snippet']['title'],
            'subCount' : sub_count,
            'viewCount' : results['statistics']['viewCount'],
            'videoCount' : results['statistics']['videoCount'],
            'thumbnail' : results['snippet']['thumbnails']['medium']['url'],
            'uploads' : results['contentDetails']['relatedPlaylists']['uploads']
        }
        cache.add(channel_id, stats)
    else:
        stats = cache.get(channel_id)
    return stats