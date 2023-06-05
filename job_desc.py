import json


"""
Class to load the job description file and extract information
"""

class job:
    def __init__(self, job_file):
        self.file = job_file
        self.title=""
        self.desc=""
        self.skills=[]

    def get_data(self):
        f= open(self.file)
        text = json.load(f)
        self.title = text[0]['title']
        self.desc = text[0]['description']

        for skill in text[0]['specific_skills']:
            self.skills.append(skill)

        for skill in text[0]['sector_skills']: #can be treated separately with different weight from specific skills
            self.skills.append(skill)
        return self.title, self.desc, self.skills



# job_obj = job("../summlinks-resums-matching-score/job_description_response.json")
# title, job_desc, skills = job_obj.get_data()
# print(f"title: {title} ")
# print(f"job description: {job_desc} ")
# print(f"skills: {skills} and total number of skills are {len(skills)}")
# print(skills[0]['title'] + "\n and the weight:  " + skills[0]['weigth'])









        


        



