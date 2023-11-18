import streamlit as st
def create_sublists(paragraph, sublist_size, sub_size=5):
    sentences = paragraph.split('. ')  # Split at period followed by a space
    sentences = [s.strip() for s in sentences]  # Remove leading/trailing spaces

    # Split further at exclamation marks and question marks
    split_sentences = []
    for sentence in sentences:
        split_sentences.extend(sentence.split('! '))
        split_sentences.extend(sentence.split('? '))

    split_sentences = [s.strip() for s in split_sentences]  # Remove leading/trailing spaces
    
    original_list = split_sentences
    sublists = []
    sublist = []

    s=''
    c=0
    for element in original_list:
        s=s+element
        c+=1
        if c==sub_size:
            sublist.append(s)
            s=''
            c=0
        if len(sublist) == sublist_size:
            sublists.append(sublist)
            sublist = []
    
    # Add the remaining elements if the original list length is not divisible by sublist_size
    if s!='':
        sublist.append(s)
        sublists.append(sublist)

    return sublists


def analyze_sentiment(file_path) -> None:

    # [START analyze_sentiment]
    import os
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient
    from dotenv import dotenv_values

    env_vars = dotenv_values('D:\BriefWise\Text-Summerizer\Text_Summarizer\.env')
    endpoint = st.secrets["endpoint"]
    key = st.secrets["key"]

    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # Read the file
    with open(file_path, 'r') as file:
        text = file.read()
    
    # Split the text into smaller chunks
    chunks = create_sublists(text, 10)
    c=0
    for chunk in chunks:
        result = text_analytics_client.analyze_sentiment(chunk, show_opinion_mining=True)
        docs = [doc for doc in result if not doc.is_error]

        for idx, doc in enumerate(docs):
            if doc.sentiment == "positive":
                c+=1
            elif doc.sentiment == "negative":
                c-=1
    if c>0:
        return ("Positive")
    elif c<0:
        return ("Negative")
    else:
        return ("Neutral")
    # [END analyze_sentiment]
