from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import os, sys
from tqdm import tqdm
import re, emoji
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker

stop_words = set(stopwords.words('english'))

stop_words = stop_words.union(["nan", "make", "need", "ape", "still", "using", "much","thing", "day", "month", "year","time", "think", "even","anyone", "said", "may", "removed", "like", "got", "deleted", "feel", "get", "know", 'us', 'go', 'also', 'rheumatoid', 'arthritis', 'hi', 'thank', "one"])


tqdm.pandas()


files_list = sys.argv[1:]
folder = 'sentiment'
#os.makedirs(f'wordclouds/{folder}', exist_ok=True)
def main():
    for f in (files_list):
        print(f"Generating wordcloud for {f}")
        df = pd.read_csv(f"{f}", encoding='utf-8')
        df['body_pro'] = df['Body'].progress_apply(process_paragraph)
        text = " ".join(df['body_pro'].astype(str))

        wordcloud = WordCloud(width=1600, height=800, background_color='white', margin=1).generate(text)

        plt.figure(figsize=(20, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')

        output_file = f'{f.removesuffix(".csv")}.png'
        plt.savefig(output_file, format='png', bbox_inches='tight', pad_inches=0.5)
        plt.close()


abbreviations = {
    "dr": "doctor",
    "dr.": "doctor",
    "doc": "doctor",
    "ive": "i have",
    "id": "i had",
    "dont": "do not",
    "cant": "cannot",
    "ill": "i will",
    "wont": "will not",
    "im": "I am",
    "ive": "I have",
    "isnt": "is not",
    "arent": "are not",
    "wasnt": "was not",
    "werent": "were not",
    "hasnt": "has not",
    "havent": "have not",
    "hadnt": "had not",
    "doesnt": "does not",
    "didnt": "did not",
    "wouldnt": "would not",
    "shouldnt": "should not",
    "couldnt": "could not",
    "mustnt": "must not",
    "mightnt": "might not",
    "neednt": "need not",
    "yall": "you all",
    "youre": "you are",
    "hes": "he is",
    "shes": "she is",
    "theyre": "they are",
    "whos": "who is",
    "whats": "what is",
    "wheres": "where is",
    "heres": "here is",
    "theres": "there is",
    "lets": "let us",
    "thats": "that is",
    "aint": "is not",
    "gonna": "going to",
    "wanna": "want to",
    "gotta": "got to",
    "kinda": "kind of",
    "sorta": "sort of",
    "lotta": "lot of",
    "lemme": "let me",
    "gimme": "give me",
    "dunno": "do not know",
    "cmon": "come on",
    "nothin": "nothing",
    "somethin": "something",
    "everythin": "everything",
    "tellin": "telling",
    "showin": "showing",
    "goin": "going",
    "doin": "doing",
    "makin": "making",
    "thinkin": "thinking",
    "theyd": "they would",
    "wanna": "want to",
    "gonna": "going to",
    "gotta": "got to",
    "kinda": "kind of",
    "sorta": "sort of",
    "ain't": "is not",
    "y'all": "you all",
    "cuz": "because",
    "outta": "out of",
    "coulda": "could have",
    "shoulda": "should have",
    "woulda": "would have",
    "hafta": "have to",
    "tryna": "trying to",
    "betcha": "bet you",
    "whatcha": "what are you",
    "bro": "brother",
    "sis": "sister",
    "brb": "be right back",
    "btw": "by the way",
    "lol": "laugh out loud",
    "idk": "I do not know",
    "omg": "oh my god",
    "thx": "thanks",
    "pls": "please",
    "b4": "before",
    "u": "you",
    "r": "are",
    "ur": "your",
    "gr8": "great",
    "l8r": "later",
    "b/c": "because",
    "bday": "birthday",
    "msg": "message",
    "np": "no problem",
    "fyi": "for your information",
    "tbh": "to be honest",
    "rn": "right now",
    "tho": "though",
    "bff": "best friend forever",
    "omw": "on my way",
    "bc": "because",
    "tks": "thanks",
    "thnks": "thanks",
    "w/": "with",
    "w/o": "without",
    "b4n": "bye for now",
    "cya": "see you",
    "gr8": "great",
    "lmk": "let me know",
    "smh": "shaking my head",
    "tbh": "to be honest",
    "ikr": "I know right",
    "rofl": "rolling on the floor laughing",
    "np": "no problem",
    "imo": "in my opinion",
    "fomo": "fear of missing out",
    "irl": "in real life",
    "afk": "away from keyboard",
    "gg": "good game",
    "yw": "you're welcome",
    "atm": "at the moment",
    "bbl": "be back later",
    "bfn": "bye for now",
    "cu": "see you",
    "ez": "easy",
    "hbu": "how about you",
    "hbd": "happy birthday",
    "hmu": "hit me up",
    "jk": "just kidding",
    "nvm": "never mind",
    "oic": "oh I see",
    "omg": "oh my god",
    "sup": "what's up",
    "ttyl": "talk to you later",
    "txt": "text",
    "wtf": "what the heck",
    "yolo": "you only live once",
    "ttys": "talk to you soon",
    "y": "why",
    "yrs": "years",
    "yr": "year",
    "u": "you",
    "youll": "you will",
    'lmao': "laughing",
    'lmfao': "laughing",
    'meds': "medications",
}

emoticon_dict = {
    ":)": "happy",
    ":(": "sad",
    ":D": "very happy",
    ";)": "wink",
    ":O": "surprised",
    ":|": "neutral",
    ":'(": "crying",
    "XD": "laughing",
    ":/": "skeptical",
    ":3": "cute",
    ">:(": "angry",
    "O:)": "angelic",
    ">:O": "shocked",
    "<3": "love",
    "(:": "happy",
}

lemmatizer = WordNetLemmatizer()

spell = SpellChecker(distance=1)
spell.word_frequency.add("covid")

def correct(word):
    if spell.correction(word) is not None:
        return spell.correction(word)
    else:
        return word

def process_paragraph(paragraph):
    #de-emojinize
    paragraph = str(paragraph)
    paragraph = emoji.demojize(paragraph.strip().lower())
    pattern = r':([a-zA-Z_]+):'
    paragraph = re.sub(pattern, lambda m: m.group(1).replace('_', ' '), paragraph.replace("::", ": :"))

    for emoticon, translation in emoticon_dict.items(): paragraph = paragraph.replace(emoticon, translation)
    #remove links
    paragraph = re.sub(r'http\S+|www\S+|https\S+', '', paragraph, flags=re.MULTILINE)
    #remove emails
    paragraph = re.sub(r'(?:mailto:\s*)?[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '', paragraph)
    #remove username
    paragraph = re.sub(r'@\w+', '', paragraph.lower())
    #remove hashtag
    paragraph = re.sub(r'#\w+', '', paragraph.lower())
    #break sentences
    paragraph = paragraph.replace(".", " ")
    #keep only text
    paragraph = re.sub(r'[^A-Za-z ]+', '', paragraph)
    #correct stretched words
    paragraph = re.sub(r'(.)\1{2,}', r'\1\1', paragraph).lower()

    tokens = word_tokenize(paragraph)
    for i in range(len(tokens)):
        if tokens[i] in abbreviations:
            tokens[i] = abbreviations[tokens[i]].lower()
    paragraph = " ".join(tokens)


    tokens = [word.lower() for word in word_tokenize(paragraph) if word not in stop_words]
    corrected_tokens = [lemmatizer.lemmatize(correct(word)) for word in tokens]

    corrected_tokens = [word for word in corrected_tokens if word.strip() and word not in stop_words]

    
    correct_paragraph = " ".join(corrected_tokens)

    return correct_paragraph.strip().lower()


if __name__ == '__main__':
    main()