import json
import os

class DataManager:
    def __init__(self, file_path='data.json'):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def get_grades(self):
        return list(self.data.keys())

    def get_subjects(self, grade):
        return list(self.data.get(grade, {}).keys())

    def get_books(self, grade, subject):
        return list(self.data.get(grade, {}).get(subject, {}).keys())

    def get_topics(self, grade, subject, book):
        return list(self.data.get(grade, {}).get(subject, {}).get(book, {}).keys())

    def get_exercises(self, grade, subject, book, topic):
        return list(self.data.get(grade, {}).get(subject, {}).get(book, {}).get(topic, {}).keys())

    def get_details(self, grade, subject, book, topic, ex):
        return self.data[grade][subject][book][topic][ex]