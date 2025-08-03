import pandas as pd
from collections import Counter
import emoji
import datetime as dt


def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['users']==selected_user]
    #1
    num_messages = df.shape[0]
    #2
    words = []
    for message in df['messages']:
        words.extend(message.split())
    #3
    num_media  =  df[df['messages'] == '<Media omitted>\n'].shape[0]

    #4
    del_msg = df[df['messages']=='This message was deleted\n'].shape[0]



    return num_messages, len(words),num_media,del_msg


def most_busy_user(df):
    x=df['users'].value_counts().head()
    new_df=round((df['users'].value_counts()/df['users'].shape[0])*100,2).reset_index().rename(columns={'count':'Percent'})
    return x,new_df


def most_common_words(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stop_word=f.read()
    if selected_user != 'Overall':
        df=df[df['users']==selected_user]



    words = []
    for message in df['messages']:
        for word in message.lower().split():
            if word not in stop_word:
                words.append(word)

    common_df=pd.DataFrame(Counter(words).most_common(20))

    return common_df


def emoji_s(selected_user,df):

    if selected_user != 'Overall':
        df=df[df['users']==selected_user]


    emojis=[]
    for message in df['messages']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df



def timeline(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['users']==selected_user]

    df['month_num'] = df['month'].apply(lambda x: dt.datetime.strptime(x, '%B').month)
    timel=df.groupby(['year', 'month_num']).count()['messages'].reset_index()
    return timel

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['users']==selected_user]

    daily=df.groupby('full_date').count()['messages'].reset_index()
    return daily