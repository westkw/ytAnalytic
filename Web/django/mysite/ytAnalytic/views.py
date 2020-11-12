from django.shortcuts import render, redirect
from django.conf import settings
from .forms import BoolForm, UrlForm, TagForm
from .scripts import search_api, graphs, sort
from plotly import plot
import requests


def home(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            searched_url = form.cleaned_data.get('url_field')
            request.session['searched_url'] = searched_url
            return redirect('/searched/')
    else:
        form = UrlForm()

    context = {
        'form' : form
    }   

    return render(request, 'ytAnalytic/home.html', context)

def about(request):
   return render(request, 'ytAnalytic/about.html')

def searched(request):
    searched_url = request.session['searched_url']
    vid_list = search_api.search(requests, searched_url)
    channel_list = search_api.channel_search(requests, searched_url)

    #Getting tag from tag form
    # tag = ''
    # if request.method == 'POST':
    #     form = TagForm(request.POST)
    #     if form.is_valid():
    #         request.session['tag'] = form.cleaned_data.get('tag')
    #         return redirect('/searched/')
    # else:
    #     form = TagForm()
    # tag = request.session['tag']
    tag = request.POST.get('tag')
    duration = request.POST.get('duration')
    submitbutton_tag = request.POST.get('Submit_tag')
    print('the selected tags are:', tag)
    
    selected_video = request.POST.get('select')
    submitbutton_vid = request.POST.get('Submit_vid')
    print('the selected VIDEO is:', selected_video)
    if selected_video != None:
        request.session['selected'] = selected_video.strip()
        # print('Stripped id', selected_video.strip())
        return redirect('/video/')
    
    searched_url = request.session['searched_url']
    vid_list = search_api.search(requests, searched_url)
    tag_list = sort.tag_list(requests, vid_list)
    
    #filtering only videos containing that tag

    if tag != None and tag != '':
        if tag.strip() != 'None':
            filtered_id = sort.sort_tag(requests, tag, vid_list)
            filtered_list = []
            for vid in vid_list:
                if vid['id'] in filtered_id:
                    filtered_list.append(vid)
            vid_list = filtered_list

    #Getting list of each video's statistics

    vid_list_stats = []
    for vid in vid_list:
        vid_list_stats.append(search_api.statistics(requests, vid['id'], vid['thumbnail']))
    
    channel_list_stats = []
    for channel in channel_list:
        channel_list_stats.append(search_api.channel_stats(requests, channel['id'], channel['channelTitle']))
    
    # print('the stats are', vid_list_stats)

    if duration != None and duration != '':
        vid_list_stats = sort.order_duration(requests, duration, vid_list_stats)
    
    dur_chart = graphs.duration(vid_list_stats)
    view_chart = graphs.views(vid_list_stats)
    graphs.tag_cloud(vid_list_stats)
    
    context = {
        'tag_list' : tag_list,
        'vid_list' : vid_list_stats,
        'channel_list' : channel_list_stats,
        'searched_url' : searched_url,
        'tag' : tag,
        'submitbutton_tag' : submitbutton_tag,
        'submitbutton_vid' : submitbutton_vid,
        'dur_chart' : dur_chart,
        'view_chart' : view_chart
        # 'form' : form
    }
    tag = ''
    request.session['tag'] = ''
    return render(request, 'ytAnalytic/searched.html', context)

def video(request):
    # selected_video = request.session['selected']
    stats = search_api.statistics(requests, 'BjsfA6ZjMQ8', 'hello')
    like = stats['likeCount']
    dislike = stats['dislikeCount']
    views = stats['viewCount']
    comments = stats['commentCount']
    tags = stats['tags']
    duration = stats['duration']
    like_dislike = graphs.like_dislike(like, dislike)
    view_comment = graphs.view_comment(views, comments)
    context = {
        'like_dislike' : like_dislike,
        'view_comment' : view_comment,
        'tags' : tags
    }
    return render(request, 'ytAnalytic/video.html', context)

def channel(request):
    video_list = search_api.video_playlist(requests, 'UUuHZ1UYfHRqk3-5N5oc97Kw')
    vid_list_stats = []

    for vid in video_list:
        print('the first vid:', vid)
        vid_list_stats.append(search_api.statistics(requests, vid['id'], vid['thumbnail']))
    print(vid_list_stats)
    dur_chart = graphs.duration(vid_list_stats)
    view_chart = graphs.views(vid_list_stats)
    graphs.tag_cloud(vid_list_stats)
    
    context = {
        'vid_list' : vid_list_stats,
        'dur_chart' : dur_chart,
        'view_chart' : view_chart
    }
    return render(request, 'ytAnalytic/channel.html', context)