import spacy
import re
import string
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import numpy as np
from langdetect import detect
from google_trans_new import google_translator  
from transformers import pipeline

nlp = spacy.load("en_core_web_sm")

def get_education_level(text):
    if 'PhD' in text or 'PHD' in text or 'phd' in text:
        return 3
    elif 'masters degree' in text or 'Masters Degree' in text or 'Masters' in text:
        return 2 
    elif 'bachelor' in text or 'bachelors' in text :
        return 1
    else:
        return 0


def extract_experience_years(text):
    """
    returns the number of years that the applicant was active in the relevant activities(education and work)
    draw back is, if a person take poses inbetween jobs total number of years he/she works will be incorrect
    this works with the assumption that the applicant works all the time after first univercity graduation.
    """
    pattern = r"\b\d{4}\b"  # a match of four-digit numbers
    year_matches = re.findall(pattern, text)
    active_years = 0
    try:
        active_years = max(year_matches) - min(year_matches)
    except:
        print("no year format found in the given text")
        active_years=0

    return active_years

def detect_and_translate(text):   
    """ 
    this function is responsible to detect language and translate to english if it is not already in english
    """ 
    result_lang = detect(text)    
    if result_lang == 'en':
        return text 
    
    else:
        translator = google_translator()
        translate_text = translator.translate(text,lang_src=result_lang,lang_tgt='en')
        return translate_text 
        

def summarize_text(text):     
    """summarizing given text"""
    summarizer = pipeline("summarization")
    summarized = summarizer(text)  
    return summarized   



def preprocess_jobdesc(text):
    """ 
    Preprocess given text: change letters to lower case, remove punctuation marks, toknize words, remove stop words and steam words.
    """
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)

    stop_words = set(stopwords.words('english'))    
    tokens = [token for token in tokens if token not in stop_words]

    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return tokens




text_to_remove = ['contact', 'english', 'german', 'dutch', 'nederlands', 'french', 'top', 'skills', 'languages', 'language',
                   'years', 'working', 'certificates', 'page', 'education',  "january", "february", "march", "april", "may", "june", 
                   "july", "august", "september", "october", "november", "december"]

def preprocess_resume(text):     
    """ 
    Preprocess given text: remove non-unicode chars, translate if it is not english, summarize text,
    change letters to lower case, toknize words, remove stop words and steam words.
    """  
    text = text.lower()
    text = re.sub(r'[^\x00-\x7F]+', '', text) # remove non unicode chars
    text = detect_and_translate(text)
    text = summarize_text(text)

    
    
    if isinstance(text, str):
        text = re.sub(r'\d+', '', text)  # remove numbers

    # # filtered_text = [word for word in text if word not in text_to_remove]#remove some words and month names that are not necessary for comparison

    nlp_txt = nlp(text)
    clean_text = ' '.join([token.text for token in nlp_txt if token.ent_type_ not in ['PERSON', 'EMAIL', 'URL']])
    tokens = word_tokenize(clean_text)
    stop_words = set(stopwords.words('english'))    
    tokens = [token for token in tokens if token not in stop_words]
    tokens = [token for token in tokens if token not in text_to_remove]

    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return tokens


def word2vec_similarity(job_desc, resume, model):
    """ 
    calculates the cosine similarity between the given job_desc and resume and returns the score
    """
    job_desc_tokens = preprocess_jobdesc(job_desc)
    resume_tokens = preprocess_resume(resume)

    # remove vocabularies not in the model
    job_desc_tokens = [token for token in job_desc_tokens if token in model]
    resume_tokens = [token for token in resume_tokens if token in model]

    job_desc_embedding = np.mean(model[job_desc_tokens], axis = 0)
    resume_embedding = np.mean(model[resume_tokens], axis = 0)

    # cosine similarity score
    similarity_score = np.dot(job_desc_embedding, resume_embedding) / (np.linalg.norm(job_desc_embedding) * np.linalg.norm(resume_embedding))
    return similarity_score







    

