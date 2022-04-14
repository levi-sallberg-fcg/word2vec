from sklearn.feature_extraction.text import TfidfVectorizer
import json
import numpy as np


class Article:
    def __init__(self, id, title, description, text):
        self.id = id
        self.title = title
        self.description = description
        self.text = text
        self.similar_ids = []

    def get_content(self):
        result = []
        if self.title is not None:
            result.append(self.title)
        if self.description is not None:
            result.append(self.description)
        if self.text is not None:
            result.append(self.text)
        if len(result) > 0:
            return '. '.join(result)
        else:
            return ''


def read_input(path):
    f = open(path)
    articles = json.load(f)
    f.close()

    result = []
    for article in articles:
        result.append(
            Article(id=article['id'], title=article['title'], description=article['description'], text=article['text'])
        )

    return result


def get_similar_index(row, limit):
    return np.argwhere(row >= limit).tolist()


def calculate_similarity(filename):
    input_path = './resources/{}.json'.format(filename)
    score_limit = 0.5

    articles = read_input(input_path)
    texts = []
    for article in articles:
        texts.append(article.get_content())

    # Compute and set similar articles
    tfidf = TfidfVectorizer().fit_transform(texts)
    pairwise_similarity = (tfidf * tfidf.T).toarray()
    np.fill_diagonal(pairwise_similarity, np.nan)

    for article_idx, article in enumerate(articles):
        similarities = pairwise_similarity[article_idx]
        similar_indices = np.argwhere(similarities >= score_limit).tolist()
        similar_articles = []
        for similar_index in similar_indices:
            similar_articles.append(articles[similar_index[0]])
        article.similar_ids = similar_articles

    return articles


if __name__ == "__main__":
    file = '1000'
    articles = calculate_similarity(file)
    print(articles)


