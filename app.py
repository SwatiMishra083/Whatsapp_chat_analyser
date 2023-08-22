import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

# level 1
st.sidebar.title("Whatsapp Chat Analyser")

# this is utaya from file_uploader in streamlit document it gives a uploading file and edited sidebar in it
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

# this is done by me code
#     convering into string and displaying in streamlit
    data = bytes_data.decode("utf-8")
    # st.text(data)
# ab preprocess use karke data ko ache se show karna h
    df = preprocessor.preprocess(data)
    # st.dataframe(df) #this was to print dataframe

# fetch unique users in dropdown sidebar
    user_list = df['user'].unique().tolist()

    # if we change the chat then edit will be required here as well
    if ' BECMPN1-2023-24' in user_list:
        user_list.remove(' BECMPN1-2023-24')
        # for friends chat
    if ' F.R.I.E.N.D.S.' in user_list:
       user_list.remove(' F.R.I.E.N.D.S.')

    user_list.sort()
    user_list.insert(0,"overall")

    selected_user = st.sidebar.selectbox("show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):
# level2
        num_messages, words,num_links = helper.fetch_stats(selected_user,df)

        st.title("Top statistics")

        # , num_media_messages
        #4 columns for total msges, words , media shared, links
        col1, col2, col3, col4 = st.columns(4) #Note: The st.beta_columns function and other elements of Streamlit are subject to updates and changes as the library evolves.
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Media shared")
        #     st.title(num_media_messages)
        with col4:
            st.header("links shared")
            st.title(num_links)

# level 7
# monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'], color = 'green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

# level 8
# daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'], color = 'black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

# level 9
# activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = 'orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


# level 10
# activity heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)




# level 3
# finding the busiest users in the group(Group level)
        if selected_user == 'overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)


# level 4
# WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


# level 5
# most common words

        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)
        # st.dataframe(most_common_df)

# level 6
# emoji analysis

        emoji_df = helper.emoji_helper(selected_user, df)
        st.title('Emoji Analysis')
        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)





