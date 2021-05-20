import fasttext
import html
from nltk.corpus import stopwords
import nltk
import re
import streamlit as st
import numpy as np

nltk.download('stopwords')
words = stopwords.words("german")
model = fasttext.load_model('ML4B/Desktop/Git/FT.bin')

def cleaner(text):
    tweet = html.unescape(text)
    without_stop_words = [word for word in tweet.split() if word.lower() not in words]
    tweet = " ".join(without_stop_words)
    tweet = text.lower()
    tweet = re.sub(r"ä", "ae", tweet)
    tweet = re.sub(r"ö", "oe", tweet)
    tweet = re.sub(r"ü", "ue", tweet)
    tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet)
    tweet = re.sub('[!“#$%&‘()*+,./:;<=>?@[\]^_`{|}~€"-]', '', tweet)

    return tweet


def predict(tweet):
    prediction = model.predict(cleaner(tweet))
    prediction = prediction[0]
    prediction = "".join(prediction)
    prediction = re.sub("__label__", "", prediction)
    return prediction

def main():
    st.title("Party Classification")
    html_temp = """
    <div style="background-color:#025246 ;padding:10px">
    <h2 style="color:white;text-align:center;">Predict a party based on a tweet</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    tweet = st.text_input("Tweet","Type Here")
    safe_html="""  
      <div style="background-color:#F4D03F;padding:10px >
       <h2 style="color:white;text-align:center;"> Your forest is safe</h2>
       </div>
    """
    danger_html="""  
      <div style="background-color:#F08080;padding:10px >
       <h2 style="color:black ;text-align:center;"> Your forest is in danger</h2>
       </div>
    """

    if st.button("Predict"):
        output=predict(tweet)
        st.success('The predicted party is {}'.format(output))

if __name__=='__main__':
    main()