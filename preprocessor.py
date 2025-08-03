import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{4},\s+\d{1,2}:\d{2}(?:\s|\u202f|\u00A0)?[ap]m\s+-'
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df=pd.DataFrame({'user_message':message,'message_date':dates})
    df['message_date_cleaned'] = df['message_date'].str.replace('\u202f', ' ', regex=True).str.strip(' -')

    # Step 2: Parse the cleaned date string
    df['message_date'] = pd.to_datetime(df['message_date_cleaned'], format="%d/%m/%Y, %I:%M %p")

    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'(^.*?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['date'].dt.year
    df['full_date']=df['date'].dt.date
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute
    df.drop(columns='date',inplace=True)
    return df