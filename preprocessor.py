import pandas as pd
import re

def preprocess(data):
    
    print(data[:5])
    datetime = []
    msg = []

    for line in data:
        if line.find('[') == -1 and line.find(']') == -1:
            datetime.append('')
            msg.append(line)
        else:       
            out = str(line).split(']')
            out[0] = out[0].replace('[', '')
            datetime.append(str(out[0]))
            msg.append(str(out[1]))
            
            
    df = pd.DataFrame({'user_message': msg, 'message_date': datetime})
     # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'],format='mixed', errors = 'ignore')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    df1 = df.replace('',float('NaN'))
    df = df1.dropna()

    #separate Users and Message
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

   
    return df