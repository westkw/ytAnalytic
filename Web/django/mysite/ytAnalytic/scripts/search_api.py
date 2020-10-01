import requests
from django.conf import settings
import pprint


def search(requests, text):
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part' : 'snippet',
        'q' : text,
        'key' : settings.YOUTUBE_API_KEY,
        'maxResults' : 12,
        'type' : 'video'
    }

    video_ids = []
    r = requests.get(search_url, params=params)
    print(r)
    results = r.json()['items']

    for result in results:
        data = {
            'id' : result['id']['videoId'],
            'title': result['snippet']['title'],
            'thumbnail' : result['snippet']['thumbnails']['high']['url']
        }
        video_ids.append(data)

    return video_ids

def statistics(requests, video_id):
    search_url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part' : 'statistics,snippet',
        'key' : settings.YOUTUBE_API_KEY,
        'type' : 'video',
        'id' : video_id
    }
    
    r = requests.get(search_url, params=params)
    
    results = r.json()['items'][0]['statistics']
    stats = {
        'likeCount' : results['likeCount'], 
        'dislikeCount' : results['dislikeCount'],
        'viewCount' : results['viewCount'],
        'favoriteCount' : results['favoriteCount'],
        'commentCount' : results['commentCount']
    }
    return stats

def tags(requests, video_id):
    search_url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part' : 'snippet',
        'key' : settings.YOUTUBE_API_KEY,
        'type' : 'video',
        'id' : video_id
    }

    r = requests.get(search_url, params)
    results = r.json()['items'][0]
    #print(pprint.pprint(results['snippet']['tags']))
    return results['snippet']['tags']
