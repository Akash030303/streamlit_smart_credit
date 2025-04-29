import pandas as pd

class KnowledgeRetrievalAgent:
    def __init__(self):
        self.data = pd.read_csv('data/credit_card_applicants_100.csv')

    def fetch(self, user_id):
        record = self.data[self.data['user_id'] == user_id]
        if not record.empty:
            return record.iloc[0].to_dict()
        else:
            return None
