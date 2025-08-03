import streamlit as st
import preprocessor,helper
st.sidebar.title('WHATSAPP CHAT ANALYZER')
import matplotlib.pyplot as plt

uploaded_file=st.sidebar.file_uploader("Pick a folder")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")

    df=preprocessor.preprocess(data)
    st.dataframe(df)
    user_list=df['users'].unique().tolist()
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user=st.sidebar.selectbox('Analysis wrt',user_list)

    num_messages,words,media,del_msg=helper.fetch_stats(selected_user,df)


    if st.sidebar.button('Show Analysis'):
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Message")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media")
            st.title(media)

        with col4:
            st.header('Total no of Deleted msg')
            st.title(del_msg)



        if selected_user=='Overall':
            st.title('most Busy User')
            x,new_df=helper.most_busy_user(df)
            fig, ax = plt.subplots()
            col1,col2=st.columns(2)


            with col1:
                ax.bar(x.index,x.values,color='r')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)


    # WordCloud
    # most common words

        st.title('Most common words')
        common_word = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        col1,col2 = st.columns(2)
        with col1:
            ax.bar(common_word[0], common_word[1])
            st.pyplot(fig)
            plt.xticks(rotation='vertical')

        with col2:
            st.dataframe(common_word)


        emoji_df = helper.emoji_s(selected_user,df)
        st.title('Emoji Analysis')
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()

            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(),autopct='%0.2f')
            st.pyplot(fig)

        with col2:
            st.dataframe(emoji_df)


        time2=helper.timeline(selected_user,df)
        st.title('Time Analysis')
        fig,ax=plt.subplots()
        ax.plot(time2['year'],time2['messages'],color='green')
        col1,col2=st.columns(2)
        with col1:

            st.pyplot(fig)

        with col2:
            st.dataframe(time2)

        daily=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        col1,col2=st.columns(2)
        with col1:
            ax.plot(daily['full_date'],daily['messages'],color='green')
            st.pyplot(fig)
            plt.xticks(rotation='vertical')
        with col2:
            st.dataframe(daily)
