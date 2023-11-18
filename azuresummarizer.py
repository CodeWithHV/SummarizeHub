import os
from dotenv import load_dotenv
import streamlit as st
# Enter your Azure Text Analytics subscription key and endpoint into a .env file in the same directory as this script

# Get value from .env file
load_dotenv()
endpoint = st.secret["endpoint"]
key = st.secret["key"]

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

def generate_summary(file_path):
    # [START extract_summary]
    import os
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    # Read the file
    with open(file_path, 'r') as file:
        text = file.read()

    chunks = create_sublists(text, 9)
    summaries = []
    for chunk in chunks:
        poller = text_analytics_client.begin_extract_summary(chunk)
        extract_summary_results = poller.result()
        for result in extract_summary_results:
            if result.kind == "ExtractiveSummarization":
                return(" ".join([sentence.text for sentence in result.sentences]))
    
    return ' '.join(summaries)
            
    # [END extract_summary]

