##########################################################################
## This repository holds the codes for the paper:                       ##
##                                                                      ##
## Paper Title:                                                         ##
##   Understanding user perceptions of DeepSeek: Insights from          ##
##   sentiment, topic and network analysis using a Reddit-based study   ##
##                                                                      ##
## Author:                                                              ##
##   Naisarg Patel                                                      ##
##                                                                      ##
## Journal: Frontiers in Artificial Intelligence                        ##
## Year: 2026                                                           ##
## DOI: https://doi.org/10.3389/frai.2025.1703949                       ##
##                                                                      ##
## License: GNU General Public License v3.0 (GPL-3.0)                   ##
## Contact: naisargbpatel14<at>gmail<dot>com                            ##
##########################################################################

from tqdm import tqdm
import pandas as pd
from collections import Counter

from process_paragraph import process_paragraph
from nltk.sentiment.vader import SentimentIntensityAnalyzer
tqdm.pandas()


def sentiment():
    df = pd.read_csv("r_deepseek_comments_with_topics.csv")
    sia = SentimentIntensityAnalyzer()
    df["Sentiment"] = df["Body"].progress_apply(lambda x: sia.polarity_scores(process_paragraph(x))["compound"])
    df["Sentiment"] = df["Sentiment"].apply(lambda x: 1 if x > 0.05 else (-1 if x < -0.05 else 0))
    df.to_csv("r_deepseek_comments_with_topics_sentiment.csv", index=False, encoding='utf-8')
    print(df.head())

def add_parent_author():
    df = pd.read_csv("r_deepseek_comments_with_topics_sentiment.csv")
    pdf = pd.read_csv("r_deepseek_posts.csv")
    df["Parent_ID"] = df["Parent_ID"].progress_apply(lambda x: x.split("_")[1])
    df["Parent_Author_Post"] = df["Parent_ID"].map(pdf.set_index("ID")["Author"])
    df["Parent_Author_Self"] = df["Parent_ID"].progress_apply(lambda x: df[df["ID"] == x]["Author"].values[0] if (type(x) == str and x in df["ID"].values) else None)
    df.drop(columns=["Parent_ID", "Title", "Probability"], inplace=True)
    df["Parent_Author"] = df["Parent_Author_Post"].combine_first(df["Parent_Author_Self"])
    df.drop(columns=["Parent_Author_Post", "Parent_Author_Self"], inplace=True)
    print("Total number of rows:", len(df))
    print("Number of rows with NaN in Parent_Author:", df["Parent_Author"].isna().sum())
    df.to_csv("r_deepseek_comments_with_topics_sentiment_pa.csv", index=False, encoding='utf-8')
    print(df.head())


def network():
    df = pd.read_csv("r_deepseek_comments_with_topics_sentiment_pa.csv")
    df.drop(columns=["ID", "Body"], inplace=True)
    print("Total number of rows:", len(df))
    print("Number of rows with NaN in Parent_Author:", df["Parent_Author"].isna().sum())
    i = 0
    df = df[df["Topic"] == i]
    df.reset_index(drop=True, inplace=True)
    df.drop(columns=["Topic"])
    df.to_csv(f"r_deepseek_network_data_{i}.csv", index=False, encoding='utf-8')


def parent_topic_senti():
    pdf = pd.read_csv("r_deepseek_posts.csv")
    def calculate_parent_sentiment(pid):
        if pid in pdf["Author"]:
            return pdf[pdf["ID"] == pid]["Sentiment"].value_counts().idxmax()
    df = pd.read_csv("r_deepseek_comments_with_topics_sentiment.csv")
    parents = df["Parent_ID"].unique()
    for parent in parents:
        tdf = df[df["Parent_ID"] == parent]
        df = pd.concat([df, pd.DataFrame([{
            "ID": None,
            "Title": None,
            "Body": None,
            "Author": parent,
            "Topic": tdf["Topic"].value_counts().idxmax(),
            "Parent_ID": None,
            "Probability": None,
            "Sentiment": calculate_parent_sentiment(parent),
        }])], ignore_index=True)
    df.to_csv("r_deepseek_comments_with_topics_sentiment_pa.csv", index=False, encoding='utf-8')

sentiment()
parent_topic_senti()