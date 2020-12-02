import requests
from django.conf import settings
import pprint
from django.core.cache import caches, cache
import isodate

def search(requests, text):
    og_text = text
    text = text.replace(" ", "")
    if cache.get("vid" + text) == None:
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'part' : 'snippet',
            'q' : og_text,
            'key' : settings.YOUTUBE_API_KEY,
            'maxResults' : 12,
            'type' : 'video'
        }
        print('1')
        r = requests.get(search_url, params=params)
        print(r)
        print('2')
        video_data = []
        results = r.json()['items']
        for result in results:
            data = {
                'id' : result['id']['videoId'],
                'title': result['snippet']['title'],
                'thumbnail' : result['snippet']['thumbnails']['high']['url']
            }
            video_data.append(data)
        cache.add('vid' + text, video_data)
    else:
        video_data = cache.get('vid' + text)

    return video_data

def channel_search(requests, text):
    og_text = text
    channel_data = []
    text = text.replace(" ", "")
    if cache.get('ch' + text) == None:
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'part' : 'snippet',
            'q' : og_text,
            'key' : settings.YOUTUBE_API_KEY,
            'maxResults' : 4,
            'type' : 'channel'
        }

        print('3')
        r = requests.get(search_url, params=params)
        print(r)
        print('4')
        results = r.json()['items']
        # print(results)
        for result in results:
            data = {
                'id' : result['id']['channelId'],
                'channelTitle' : result['snippet']['channelTitle']
            }
            channel_data.append(data)
        cache.add('ch' + text, channel_data)
    else:
        channel_data = cache.get('ch' + text)
    return channel_data 


def statistics(requests, video_id, thumbnail):
    if cache.get(video_id) == None:
        search_url = 'https://www.googleapis.com/youtube/v3/videos'
        params = {
            'part' : 'statistics,snippet,contentDetails',
            'key' : settings.YOUTUBE_API_KEY,
            'type' : 'video',
            'id' : video_id
        }
        
        print('5')
        r = requests.get(search_url, params=params)
        print(r)
        print('6')
        results = r.json()['items'][0]
        
        try:
            tag = results['snippet']['tags']
        except KeyError:
            tag = ['']
        
        try:
            comment_count = results['snippet']['commentCount']
        except KeyError:
            comment_count = 0

        duration = results['contentDetails']['duration']
        duration = isodate.parse_duration(duration)
        durationMin = dur_min(duration)
        print('video_id', video_id)
        stats = { 
            'id' : video_id,
            'thumbnail' : thumbnail,
            'title' : results['snippet']['title'],
            'likeCount' : results['statistics']['likeCount'], 
            'dislikeCount' : results['statistics']['dislikeCount'],
            'viewCount' : results['statistics']['viewCount'],
            'favoriteCount' : results['statistics']['favoriteCount'],
            'commentCount' : comment_count,
            'tags' : tag,
            'duration' : duration,
            'durationMin' : durationMin
        }
        cache.add(video_id, stats)
    else:
        stats = cache.get(video_id)
    return stats


def channel_stats(requests, channel_id, channelTitle):
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
            'channelTitle' : channelTitle,
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

def video_playlist(requests, playlist_id):
    if cache.get(playlist_id) == None:
        search_url = 'https://www.googleapis.com/youtube/v3/playlistItems'
        params = {
            'part' : 'snippet',
            'key' : settings.YOUTUBE_API_KEY,
            'playlistId' : playlist_id,
            'maxResults' : 12
        }
        
        r = requests.get(search_url, params=params)
        results = r.json()['items']
        uploads = []
        for result in results:        
            stats = { 
                'id' : result['snippet']['resourceId']['videoId'],
                'thumbnail' : result['snippet']['thumbnails']['high']['url']
            }
            print('the stats are:', stats)
            uploads.append(stats)
        cache.add(playlist_id, uploads)
    else:
        uploads = cache.get(playlist_id)
    return uploads


def dur_min(dur):
    dur = str(dur).split(':')
   
    hour = int(dur[0])
    min = int(dur[1])
    sec = int(dur[2])

    return (hour * 60) + (min) + (sec / 60)
