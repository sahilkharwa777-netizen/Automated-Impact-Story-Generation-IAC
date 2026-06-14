import pandas as pd


def load_feedback(file_path):

    data = pd.read_csv(file_path)

    return data