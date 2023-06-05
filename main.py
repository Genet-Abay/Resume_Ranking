import pandas as pd
import preprocessing as pp
import job_desc as jd
from gensim.models import keyedvectors
import csv


def start_task(job_des_path, resume_path):
    """
    this function starts the process by reading the files from given file paths. It iterates over the rows of resume file and compute 
    the similarity between each resume with job description and finally retuns the list of scores for each corresponding applicant
    """

    #Reading job title, description and required skills
    job_obj = jd.job(job_des_path)
    title, job_desc, skills = job_obj.get_data()

    #read resumes from given csv file
    df = pd.read_csv(resume_path)
    score_list = []
    model_path = "../GoogleNews-vectors-negative300.bin.gz"
    model = keyedvectors.load_word2vec_format(model_path, binary=True)

    #iterate over rows of the csv file to get each resume, calculate the score and get list of scores for all ids
    for _, row in df.iterrows():
        individual_score = {}
        resume = row[1]

        education_level = pp.get_education_level(resume)
        applicant_active_years = pp.extract_experience_years(resume)    
        similarity_with_description = pp.word2vec_similarity(job_desc, resume, model)
        skill_score=0

        for i in range(0, len(skills)):
            weight = 2
            if skills[i]['weigth'] == 'Must have':
                weight=5
            
            skill_score += pp.word2vec_similarity(skills[i]['title'], resume, model) * weight

        final_score = education_level+applicant_active_years+similarity_with_description+skill_score  


        individual_score['id'] = row['id']
        individual_score['rank'] = final_score
        score_list.append(individual_score)

        return score_list
    


def main():
    job_path = "../summlinks-resums-matching-score/job_description_response.json"
    resumes_path = "../summlinks-resums-matching-score/resumes.csv"
    scores = start_task(job_path, resumes_path)
    header = scores[0].keys()

    with open("../summlinks-resums-matching-score/result.csv", 'w', newline='') as op_file:
        writer=csv.DictWriter(op_file, header)
        writer.writeheader()
        writer.writerows(scores)



if __name__ == "__main__":
    main()









