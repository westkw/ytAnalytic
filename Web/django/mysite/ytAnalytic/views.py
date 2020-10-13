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
    
    #Getting tag from tag form
    
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            request.session['tag'] = form.cleaned_data.get('tag_field')
            return redirect('/searched/')
    else:
        form = TagForm()
    tag = request.session['tag']
    searched_url = request.session['searched_url']
    vid_list = search_api.search(requests, searched_url)
    
    #filtering only videos containing that tag

    if tag != '':
        filtered_id = sort.sort_tag(requests, tag, vid_list)
        filtered_list = []
        for vid in vid_list:
            if vid['id'] in filtered_id:
                filtered_list.append(vid)
        vid_list = filtered_list

    #Getting list of each video's statistics

    vid_list_stats = []
    for vid in vid_list:
        vid_list_stats.append(search_api.statistics(requests, vid['id']))
    graphs.tag_cloud(vid_list_stats)
    context = {
        'list' : vid_list,
        'searched_url' : searched_url,
        'form' : form
    }
    tag = ''
    request.session['tag'] = ''
    return render(request, 'ytAnalytic/searched.html', context)

def video(request):
    stats = search_api.statistics(requests, 'ikRJSIYm2RM')
    like = stats['likeCount']
    dislike = stats['dislikeCount']
    views = stats['viewCount']
    comments = stats['commentCount']
    tags = stats['tags']
    fig = graphs.example()
    graph = fig.to_html(full_html=False, default_height=500, default_width=700)
    like_dislike = graphs.like_dislike(like, dislike)
    view_comment = graphs.view_comment(views, comments)
    context = {
        'graph' : graph,
        'like_dislike' : like_dislike,
        'view_comment' : view_comment,
        'tags' : tags
    }
    return render(request, 'ytAnalytic/video.html', context)