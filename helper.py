from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import string
import re
import emoji
extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

#func will only work in group chat analysis
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df

def remove_stop_words(message):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    y = []
    for word in message.lower().split():
        if word not in stop_words:
            y.append(word)
    return " ".join(y)

def remove_punctuation(message):
  x = re.sub('[%s]'% re.escape(string.punctuation), '', message)
  return x

def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']    
    temp['message'] = temp['message'].apply(remove_punctuation)
    temp['message'] = temp['message'].apply(remove_stop_words)
    #temp['message'] = temp['message'].apply(lambda x: [item for item in x if item not in stop])

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc

def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']    
    temp['message'] = temp['message'].apply(remove_stop_words)
    temp['message'] = temp['message'].apply(remove_punctuation)
    #temp['message'] = temp['message'].apply(lambda x: [item for item in x if item not in stop])
    words = []

    for message in temp['message']:
        words.extend(message.split())
        
    words = [ele for ele in words if len(ele) > 6]

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def fnq(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    qns = []
    for message in df['message']:
        if message.find('?') != -1:
            qns.append(message)
    qns_df = pd.DataFrame({'Questions':qns})
    return qns_df
