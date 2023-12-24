import streamlit as st
import preprocessor, helper #local file func
import matplotlib.pyplot as plt
from io import StringIO
import pandas as pd

st.sidebar.title("WhatsApp Chat Analyzer")

#create a file uploaded to upload txt file
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    bytes_data = stringio.read()
    data = bytes_data
    #bytes_data = uploaded_file.getvalue()
    #convert byte to string
    data = data.splitlines()
    #call the preprocess func to give df
    df = preprocessor.preprocess(data)

    #provide an option to analyze data on group level or specific user
    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, 'Overall')
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)
    
    #button to analyze chat
    if(st.sidebar.button("Show Analysis")):
        #Display basic stats in 4 cols
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header(":blue[Total Messages]")
            st.title(num_messages)
        with col2:
            st.header(":blue[Total Words]")
            st.title(words)
        with col3:
            st.header(":blue[Media Shared]")
            st.title(num_media_messages)
        with col4:
            st.header(":blue[Links Shared]")
            st.title(num_links)
            
            
        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title(':blue[Most Busy Users]')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud (Top Frequent words)
        st.title(":blue[Wordcloud]")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title(':blue[Most commmon words]')
        most_common_df = helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        #FAQ
        st.title(':blue[FAQ]')
        qns_df = helper.fnq(selected_user,df)   
        if qns_df.shape[0] > 0:
            st.dataframe(qns_df)

        # emoji analysis
        st.title(":blue[Emoji Analysis]")
        emoji_df = helper.emoji_helper(selected_user,df)
        if emoji_df.shape[0] > 0:
            col1,col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig,ax = plt.subplots()
                ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
                st.pyplot(fig)
        else:
            st.write(":red[No Emojis Send by this user]")
        
