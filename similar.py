from sklearn.feature_extraction.text import TfidfVectorizer
import json
import numpy as np


def read_input(path):
    f = open(path)
    articles = json.load(f)
    texts = []
    for article in articles:
        result = []

        article_title = article['title']
        if article_title is not None:
            result.append(article_title)

        article_description = article['description']
        if article_description is not None:
            result.append(article_description)

        article_text = article['text']
        if article_text is not None:
            result.append(article_text)

        if len(result) > 0:
            texts.append('. '.join(result))

    f.close()
    return texts


def get_similar_index(row, limit):
    return np.argwhere(row >= limit).tolist()


def calculate_similarity(filename):
    input_path = './resources/{}.json'.format(filename)
    output_path = './resources/{}-bert.pkl'.format(filename)
    texts = read_input(input_path)
    tfidf = TfidfVectorizer().fit_transform(texts)
    pairwise_similarity = (tfidf * tfidf.T).toarray()
    np.fill_diagonal(pairwise_similarity, np.nan)

    # Get similar texts
    index = 4
    similar_indices = get_similar_index(pairwise_similarity[index], 0.5)

    similar = []

    for similar_index in similar_indices:
        similar.append(texts[similar_index[0]])

    return texts[index], similar


if __name__ == "__main__":
    file = '100-fi'
    evaluated_text, similar_texts = calculate_similarity(file)

    print("Evaluated text: ")
    print(evaluated_text)

    print("Similar texts: ")
    for text in similar_texts:
        print("\nSimilar: ")
        print(text)


