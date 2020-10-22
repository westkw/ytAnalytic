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
    submitbutton_tag = request.POST.get('Submit_tag')
    print('the selected tags are:', tag)
    
    selected_video = request.POST.get('select')
    submitbutton_vid = request.POST.get('Submit_vid')
    print('the selected VIDEO is:', selected_video)
    if selected_video != None:
        request.session['selected'] = selected_video.strip()
        print('Stripped id', selected_video.strip())
        return redirect('/video/')
    
    searched_url = request.session['searched_url']
    vid_list = search_api.search(requests, searched_url)
    tag_list = sort.tag_list(requests, vid_list)
    
    #filtering only videos containing that tag

    if tag != None:
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
        'tag_list' : tag_list,
        'vid_list' : vid_list,
        'searched_url' : searched_url,
        'tag' : tag,
        'submitbutton_tag' : submitbutton_tag,
        'submitbutton_vid' : submitbutton_vid 
        # 'form' : form
    }
    tag = ''
    request.session['tag'] = ''
    return render(request, 'ytAnalytic/searched.html', context)

def video(request):
    selected_video = request.session['selected']
    stats = search_api.statistics(requests, '3K4VwKZ-4Os')
    like = stats['likeCount']
    dislike = stats['dislikeCount']
    views = stats['viewCount']
    comments = stats['commentCount']
    tags = stats['tags']
    duration = stats['duration']
    print(duration)
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