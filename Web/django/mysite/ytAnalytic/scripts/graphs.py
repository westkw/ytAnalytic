import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt

colors = ['#ee4343', '#fcc5c5']

def example():
    df = px.data.iris() # iris is a pandas DataFrame
    plt_div = px.scatter(df, x="sepal_width", y="sepal_length")
    return plt_div

def like_dislike(likes, dislikes):
    labels = ['Likes','Dislikes']
    values = [likes, dislikes]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_traces(marker=dict(colors=colors))
    fig.update_layout(font_family="Segoe UI", title_text='Likes vs Dislikes', title_font_color="#282828")
    fig = fig.to_html()
    return fig

def view_comment(views, comments):
    labels = ['Views','Comments']
    values = [views, comments]
    fig = go.Figure([go.Bar(x=labels, y=values)])
    fig.update_layout(title_text='Views vs Comments', title_font_color="#282828")
    fig.update_traces(marker_color=colors)
    fig = fig.to_html()
    return fig

def tag_cloud(vid_list_stats):
    stopwords = set(STOPWORDS)
    tags = ''
    for vid in vid_list_stats:
        for tag in vid['tags']:
            tags += tag.lower()
    
    if tags == '':
        tags = 'empty'
    wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white',
                colormap = "Reds", 
                stopwords = stopwords, 
                min_font_size = 10).generate(tags)
    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud)
    plt.savefig('./ytAnalytic/static/ytAnalytic/wordcloud.png')

     
    