from django.shortcuts import render, redirect
from django.conf import settings
from .forms import BoolForm, UrlForm, TagForm
from .scripts import search_api, graphs, sort
from plotly import plot

'''
    View for the home page that contains a text field form to 
    input search queries. 
'''
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

'''
    View for the about page that contains a brief summary of
    the web app.
'''
def about(request):
   return render(request, 'ytAnalytic/about.html')

'''
    View for the searched page. This page gives a list of channels
    and videos that appear in the search query. These can be filtered
    by tag and duration. There is also a few data visualizations at
    the bottom.
'''
def searched(request):
    searched_url = request.session['searched_url']
    vid_list = search_api.search(searched_url)
    channel_list = search_api.channel_search(searched_url)
    tag = request.POST.get('tag')
    duration = request.POST.get('duration')
    submitbutton_tag = request.POST.get('Submit_tag')    
    selected_video = request.POST.get('select')
    submitbutton_vid = request.POST.get('Submit_vid')
    if selected_video != None:
        request.session['selected'] = selected_video.strip()
        return redirect('/video/')
    
    searched_url = request.session['searched_url']
    vid_list = search_api.search(searched_url)
    tag_list = sort.tag_list(vid_list)
    
    #filtering only videos containing that tag

    if tag != None and tag != '':
        if tag.strip() != 'None':
            filtered_id = sort.sort_tag(tag, vid_list)
            filtered_list = []
            for vid in vid_list:
                if vid['id'] in filtered_id:
                    filtered_list.append(vid)
            vid_list = filtered_list

    #Getting list of each video's statistics

    vid_list_stats = []
    for vid in vid_list:
        vid_list_stats.append(search_api.statistics(vid['id'], vid['thumbnail']))
    
    channel_list_stats = []
    for channel in channel_list:
        channel_list_stats.append(search_api.channel_stats(channel['id'], channel['channelTitle']))
    
    if duration != None and duration != '':
        vid_list_stats = sort.order_duration(duration, vid_list_stats)
    
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
    }
    tag = ''
    request.session['tag'] = ''
    return render(request, 'ytAnalytic/searched.html', context)

'''
    View for the video page. This page is for individual videos.
    It allows you to watch the video and see data visualizations of
    the video's statistics.
'''
def video(request, video_id='lMyD7kIGfHY'):
    stats = search_api.statistics(video_id, 'hello')
    title = stats['title']
    like = stats['likeCount']
    dislike = stats['dislikeCount']
    views = stats['viewCount']
    comments = stats['commentCount']
    tags = stats['tags']
    duration = stats['duration']
    like_dislike = graphs.like_dislike(like, dislike)
    view_comment = graphs.view_comment(views, comments)
    context = {
        'title': title,
        'id' : video_id,
        'like_dislike' : like_dislike,
        'view_comment' : view_comment,
        'tags' : tags
    }
    return render(request, 'ytAnalytic/video.html', context)

'''
    View for the channel page. This has a grid of uploaded videos
    from the channel. This page also has data visualizations at the 
    bottom to see trends of the video uploads.
'''
def channel(request, upload_id='UUuHZ1UYfHRqk3-5N5oc97Kw', channel_title=""):
    video_list = search_api.video_playlist(upload_id)
    vid_list_stats = []
    
    tag_list = sort.tag_list(vid_list_stats)
    tag = request.POST.get('tag')
    duration = request.POST.get('duration')
    submitbutton_tag = request.POST.get('Submit_tag')    
    
    if tag != None and tag != '':
        if tag.strip() != 'None':
            filtered_id = sort.sort_tag(tag, video_list)
            filtered_list = []
            for vid in video_list:
                if vid['id'] in filtered_id:
                    filtered_list.append(vid)
            video_list = filtered_list

    for vid in video_list:
        vid_list_stats.append(search_api.statistics(vid['id'], vid['thumbnail']))

    if duration != None and duration != '':
        vid_list_stats = sort.order_duration(duration, vid_list_stats)
    
    dur_chart = graphs.duration(vid_list_stats)
    view_chart = graphs.views(vid_list_stats)
    graphs.tag_cloud(vid_list_stats)
    
    context = {

        'channel_title' : channel_title,
        'vid_list' : vid_list_stats,
        'dur_chart' : dur_chart,
        'view_chart' : view_chart,
        'tag_list' : tag_list,
        'tag' : tag,
        'submitbutton_tag' : submitbutton_tag,
    }
    return render(request, 'ytAnalytic/channel.html', context)