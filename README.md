# Understanding User Perceptions of DeepSeek: Insights from Sentiment, Topic and Network Analysis Using a Reddit-Based Study

**Paper Title:** Understanding user perceptions of DeepSeek: insights from sentiment, topic and network analysis using a Reddit-based study

**DOI:** [https://doi.org/10.3389/frai.2025.1703949](https://doi.org/10.3389/frai.2025.1703949)

**Journal:** Frontiers in Artificial Intelligence, Volume 8 - 2025

**Authors:** Naisarg Patel, Rajesh Sharma, Prakash Lingasamy, Vino Sundararajan, Sajitha Lulu Sudhakaran, Vijayachitra Modhukur

This repository contains the Python scripts used for data processing and analysis in the research paper "Understanding User Perceptions of DeepSeek: Insights from Sentiment, Topic and Network Analysis Using a Reddit-Based Study".

## Overview

This study analyzes Reddit discussions about DeepSeek using multiple computational methods including sentiment analysis, topic modeling, emotion detection, and network analysis. The scripts process Reddit posts and comments data to extract insights about user perceptions and interactions.

## File Descriptions

### Data Processing Scripts

**`posts.py`**
- Converts Reddit posts from JSONL format to CSV format
- Extracts key fields: ID, Title, Body, Date, Time, Subreddit, URL, Upvotes, Score, Awards, Comments, Crosspost
- Filters out removed and deleted posts
- Usage: `python posts.py <jsonl_file> <output_csv_file>`

**`comments.py`**
- Converts Reddit comments from JSONL format to CSV format
- Extracts fields: ID, Body, Date, Time, Subreddit, URL, Parent_ID, Upvotes, Awards
- Filters out removed/deleted comments and comments with removed parent posts
- Usage: `python comments.py <comments_jsonl> <posts_jsonl> <output_csv>`

### Text Processing and Analysis

**`process_paragraph.py`**
- Core text preprocessing module used by other scripts
- Functions include:
  - Emoji conversion to text descriptions
  - HTML entity decoding
  - Abbreviation expansion
  - Emoticon replacement
  - Stop word removal (preserving negation words)
  - Spell checking and correction
  - Lemmatization
  - Text cleaning and normalization

**`helpers.py`**
- Utility functions supporting the analysis pipeline
- Features:
  - File backup functionality with timestamp
  - Abbreviation dictionary for text expansion
  - Common helper functions used across multiple scripts

### Sentiment and Emotion Analysis

**`analyse_sentiment.py`**
- Performs sentiment analysis using VADER (Valence Aware Dictionary and sEntiment Reasoner)
- Processes text content and assigns sentiment scores and categories
- Outputs: Compound Score, Overall Sentiment (Positive/Negative/Neutral), Numerical Sentiment
- Creates backup of existing files before processing
- Usage: Run as module or import `file_sentiment()` function

**`emotion.py`**
- Emotion detection using the `j-hartmann/emotion-english-distilroberta-base` transformer model
- Classifies text into emotion categories (joy, sadness, anger, fear, etc.)
- Uses HuggingFace transformers library for state-of-the-art emotion recognition
- Processes multiple files provided as command line arguments
- Usage: `python emotion.py <file1.csv> <file2.csv> ...`

### Content Analysis

**`extract_links.py`**
- Extracts and analyzes URLs from Reddit posts and comments
- Features:
  - URL cleaning and normalization
  - Short URL expansion (follows redirects)
  - Link frequency analysis
  - Outputs both individual links and aggregated link counts
- Generates two output files: `*_links.csv` and `*_link_counts.csv`
- Usage: `python extract_links.py <input_csv_file>`

**`generate_wordcloud.py`**
- Creates word cloud visualizations from processed text data
- Features:
  - Advanced text preprocessing
  - Custom stopword filtering
  - Lemmatization and spell checking
  - Configurable word cloud generation
- Supports multiple input files
- Usage: `python generate_wordcloud.py <file1.csv> <file2.csv> ...`

### Topic and Network Analysis

**`topic.py`**
- Topic modeling and sentiment integration functions
- Features:
  - Sentiment analysis integration with topic data
  - Parent-author relationship mapping for network analysis
  - Data preparation for network visualization
- Functions:
  - `sentiment()`: Adds sentiment scores to topic-modeled data
  - `add_parent_author()`: Maps parent-child relationships for network analysis

## Dependencies

The scripts require the following Python packages:

```
pandas
numpy
nltk
transformers
torch
tqdm
requests
wordcloud
matplotlib
spellchecker
emoji
```

### NLTK Data Requirements
```python
import nltk
nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
```

## Data Flow

1. **Data Extraction**: `posts.py` and `comments.py` convert raw Reddit JSONL data to structured CSV format
2. **Text Processing**: `process_paragraph.py` standardizes and cleans text content
3. **Sentiment Analysis**: `analyse_sentiment.py` adds sentiment scores and classifications
4. **Emotion Detection**: `emotion.py` adds emotion categories to the dataset
5. **Content Analysis**: `extract_links.py` and `generate_wordcloud.py` extract additional insights
6. **Topic Integration**: `topic.py` combines sentiment with topic modeling results for network analysis

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this code in your research, please cite the original paper:

```bibtex
@ARTICLE{10.3389/frai.2025.1703949,
    
AUTHOR={Patel, Naisarg  and Sharma, Rajesh  and Lingasamy, Prakash  and Sundararajan, Vino  and Lulu Sudhakaran, Sajitha  and Modhukur, Vijayachitra },
           
TITLE={Understanding user perceptions of DeepSeek: insights from sentiment, topic and network analysis using a Reddit-based study},
          
JOURNAL={Frontiers in Artificial Intelligence},
          
VOLUME={Volume 8 - 2025},
  
YEAR={2026},
  
URL={https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1703949},
  
DOI={10.3389/frai.2025.1703949},
  
ISSN={2624-8212},
  
ABSTRACT={IntroductionThe launch of DeepSeek, a Chinese open-source generative AI model, generated substantial discussion regarding its capabilities and implications. The r/deepseek subreddit emerged as a key forum for real-time public evaluation. Analyzing this discourse is essential for understanding the sociotechnical perceptions shaping the integration of emerging AI systems.MethodsWe analyzed 46,649 posts and comments from r/deepseek (January–May 2025) using a computational framework combining VADER sentiment analysis, Hartmann emotion classification, BERTopic for thematic modeling, hyperlink extraction, and directed network analysis. Data preprocessing included cleaning, normalization, and lemmatization. We also examined correlations between sentiment/emotion scores and dominant topics.ResultsSentiment was predominantly positive (posts: 47.23%; comments: 44.26%), with neutral sentiment comprising ~30% of content. The most frequent emotion was neutrality, followed by surprise and fear, indicating ambivalent user reactions. Prominent topics included open-source AI models, DeepSeek usage, device compatibility, comparisons with ChatGPT, and censorship concerns. Hyperlink analysis indicated strong engagement with GitHub, Hugging Face, and DeepSeek's own services. Network analysis revealed a fragmented but active community, depicting Open-Source AI Models as the most cohesive cluster.DiscussionCommunity discourse framed DeepSeek as both a technical tool and a geopolitical issue. Enthusiasm centered on its performance, accessibility, and open-source nature, while concerns were voiced about censorship, data privacy, and potential ideological influence. The integrated analysis shows that collective perception emerged through decentralized, dialogic engagement, reflecting broader sociotechnical tensions related to openness, trust, and legitimacy in global AI development.}}
```
