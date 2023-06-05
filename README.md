# Ranking resumes
The project aims to rank the given resumes as a csv files, each row for each individual applicant, id field represents name and resume_text toknized resume text.


## Notes
- I have considered education level, years of experience and skills to calculate the total score.
- For skills weight "Must have" has given a wighted value of 5 and "Nice to have" to 2.

## Stpes that I have followed described as follows

1- Job title, job description and list of skills(both specific and sector) are extracted from the json file provided.

2- Job description preprocessed and summarized so that it will be ready to compare with resume.

3- Skills are preprocessed but not summarized.

4- For each resume in each row "resume_text" 
   If language is Dutch it is translated to English
   Summarize the text
   Preprocess the text (cleaning, toknizing, lemmatizing...)

5- I have used word2vec with cosine similarity score to calculate the rank between each resume and job(description and skills)

6- All the scores from the education level, job description and skills summed up to get final rank and put into a list of dictionary containing id and rank.

7- Finally the result is written to a csv file.

	
## Prerequisites
 
python 3.10, NLTK, Spacy, gensim, langdetect, google_trans_new, transformers, pandas

 	
 
## Output  
Output is csv file containing ID(name of applicant) and rank(score of the resume)
		
		
		
## License

Free license

## Contact

Genet Abay Shiferaw: genetabay.s@gmail.com
