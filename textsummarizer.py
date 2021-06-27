import re
import streamlit as st

#NLTK Packages
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

#SPACY Packages
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

#Function for NLTK
def nltk_summarizer(docx):
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(docx)
    freqTable = dict()

    for word in words:
        word = word.lower()
        if word not in stopWords:
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1

    sentence_list= sent_tokenize(docx)
    #sentenceValue = dict()
    max_freq = max(freqTable.values())
    for word in freqTable.keys():
        freqTable[word] = (freqTable[word]/max_freq)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in freqTable.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = freqTable[word]
                    else:
                        sentence_scores[sent] += freqTable[word]#total number of length of words

    import heapq
    summary_sentences = heapq.nlargest(8, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary

#Function for SPACY
def spacy_summarizer(docx):
    #nlp=spacy.load('en_core_web_lg')
    #docx=nlp(docx)
    stopWords = list(STOP_WORDS)
    words = word_tokenize(docx)
    freqTable = dict()

    for word in words:
        word = word.lower()
        if word not in stopWords:
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1

    sentence_list= sent_tokenize(docx)
    #sentenceValue = dict()
    max_freq = max(freqTable.values())
    for word in freqTable.keys():
        freqTable[word] = (freqTable[word]/max_freq)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in freqTable.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = freqTable[word]
                    else:
                        sentence_scores[sent] += freqTable[word]#total number of length of words

    import heapq
    summary_sentences = heapq.nlargest(8, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary

def main():
    st.title("Text Summarizer App")
    activities = ["Summarize Via Text"]
    choice = st.sidebar.selectbox("Select Activity", activities)

    if choice == 'Summarize Via Text':
        st.subheader("Summary using NLP")
        article_text = st.text_area("Enter Text Here","Type here")
        #cleaning of input text
        article_text = re.sub(r'\\[[0-9]*\\]', ' ',article_text)
        article_text = re.sub('[^a-zA-Z.,]', ' ',article_text)
        article_text = re.sub(r"\b[a-zA-Z]\b",'',article_text)
        article_text = re.sub("[A-Z]\Z",'',article_text)
        article_text = re.sub(r'\s+', ' ', article_text)

        summary_choice = st.selectbox("Summary Choice" , ["NLTK","SPACY"])
        if st.button("Summarize Via Text"):
            if summary_choice == 'NLTK':
                summary_result = nltk_summarizer(article_text)
            elif summary_choice == 'SPACY':
                summary_result = spacy_summarizer(article_text)

            st.write(summary_result)

if __name__ == '__main__':
    main()