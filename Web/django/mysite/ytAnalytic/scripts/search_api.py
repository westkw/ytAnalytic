import requests
from django.conf import settings
import pprint
from django.core.cache import caches, cache


def search(requests, text):
    if cache.get(text) == None:
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'part' : 'snippet',
            'q' : text,
            'key' : settings.YOUTUBE_API_KEY,
            'maxResults' : 12,
            'type' : 'video'
        }


        r = requests.get(search_url, params=params)
        video_data = []
        #print(r)
        results = r.json()['items']

        for result in results:
            data = {
                'id' : result['id']['videoId'],
                'title': result['snippet']['title'],
                'thumbnail' : result['snippet']['thumbnails']['high']['url']
            }
            video_data.append(data)
        cache.add(text, video_data)
    else:
        video_data = cache.get(text)

    return video_data

def statistics(requests, video_id):
    if cache.get(video_id) == None:
        search_url = 'https://www.googleapis.com/youtube/v3/videos'
        params = {
            'part' : 'statistics,snippet,contentDetails',
            'key' : settings.YOUTUBE_API_KEY,
            'type' : 'video',
            'id' : video_id
        }
        
        r = requests.get(search_url, params=params)
        results = r.json()['items'][0]
        
        try:
            tag = results['snippet']['tags']
        except KeyError:
            tag = ['']
        
        stats = {
            'likeCount' : results['statistics']['likeCount'], 
            'dislikeCount' : results['statistics']['dislikeCount'],
            'viewCount' : results['statistics']['viewCount'],
            'favoriteCount' : results['statistics']['favoriteCount'],
            'commentCount' : results['statistics']['commentCount'],
            'tags' : tag,
            'duration' : results['contentDetails']['duration']
        }
        cache.add(video_id, stats)
    else:
        stats = cache.get(video_id)
    return stats
