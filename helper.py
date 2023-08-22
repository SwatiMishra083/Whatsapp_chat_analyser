from urlextract import URLExtract
from wordcloud import WordCloud
extract = URLExtract()
import pandas as pd
from collections import Counter
import emoji

# level 1, 2
def fetch_stats(selected_user,df):
    #  # from here  shortcut is applied
    if selected_user!='overall':
        df = df[df['user'] == selected_user]
    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
# fetch number of media
#     error coming in this line
#       num_media_messages = df[df['message'] =='\u200e image omitted\n'].shape[0]

    # fetch number of links
    links=[]
    for message in  df['message']:
        links.extend(extract.find_urls(message))


    return num_messages, len(words),len(links)
        # , num_media_messages

# level 3
def most_busy_users(df):
    x = df['user'].value_counts().head()
    # value_counts(): This method is applied to the extracted column (df['user']) and calculates the frequency count of unique values in that column. In other words, it counts how many times each unique user appears in the DataFrame.
    #.head() = top few are shownmostly top 5.

    df= round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'user': 'name', 'count': 'percentage'})
    return x, df

# level 4
# function for wordcloud
def create_wordcloud(selected_user, df):


    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != ' F.R.I.E.N.D.S.']
    temp = temp[temp['message'] != 'sticker omitted\n']
    temp = temp[temp['message'] != ' ']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


# level 5
# most common words
def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()


    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != ' F.R.I.E.N.D.S.']
    temp = temp[temp['message'] != 'sticker omitted\n']
    temp = temp[temp['message'] != ' ']


    words = []
    for message in temp['message']:
        for word in message.lower().split():
            # if word not in stop_words:
           if word.strip() and word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20) )
    return most_common_df

# level 6
# emoji analysis


def emoji_helper(selected_user, df):

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    emojis =[]
    for message in df['message']:
        # emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
        emojis.extend([c for c in message if c in emoji.demojize(message)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

# monthly timeline
def monthly_timeline(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

# daily timeline
def daily_timeline(selected_user, df):
        if selected_user != 'overall':
            df = df[df['user'] == selected_user]

        daily_timeline = df.groupby('only_date').count()['message'].reset_index()

        return daily_timeline

# activity map
# col 1
def week_activity_map(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()
# col2
def month_activity_map(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()


# activity heatmap
def activity_heatmap(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap


