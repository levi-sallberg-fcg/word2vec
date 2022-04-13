import pandas as pd
from keybert import KeyBERT
import os


def bert_keywords(text, min_score):
    topics = []
    if text is None:
        return topics
    else:
        kw_model = KeyBERT()
        keywords = kw_model.extract_keywords(text)
        for keyword in keywords:
            if keyword[1] >= min_score:
                topics.append(keyword[0])
        return topics


def bert_get_topics(filename):
    input_path = './resources/{}.json'.format(filename)
    output_path = './resources/{}-bert.pkl'.format(filename)

    if os.path.exists(output_path):
        print("load bert result")
        df = pd.read_pickle(output_path)
    else:
        print("generate bert topics")
        df = pd.read_json(input_path)
        df['topics'] = df.apply(lambda row: bert_keywords(row['text'], 0.5), axis=1)
        df.to_pickle(output_path)

    return df


if __name__ == "__main__":
    file = '500'
    result = bert_get_topics(file)
    print(result)

