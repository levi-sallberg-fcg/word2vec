from sklearn.feature_extraction.text import TfidfVectorizer
import json
import numpy as np


class Article:
    def __init__(self, id, title, description, text):
        self.id = id
        self.title = title
        self.description = description
        self.text = text
        self.similar_articles = []

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


def find_result(similarities, score, count):
    result = []
    for similar_idx, similar in enumerate(similarities):
        if similar > score:
            result.append((similar_idx, similar))

    result.sort(key=lambda tup: tup[1], reverse=True)
    return result[0:count]


def calculate_similarity(filename, score, count):
    input_path = './resources/{}.json'.format(filename)

    articles = read_input(input_path)
    texts = []
    for article in articles:
        texts.append(article.get_content())

    # Compute and set similar articles
    tfidf = TfidfVectorizer().fit_transform(texts)
    pairwise_similarity = (tfidf * tfidf.T).toarray()
    np.fill_diagonal(pairwise_similarity, np.nan)

    for article_idx, article in enumerate(articles):
        similar_articles = []
        similarities = find_result(pairwise_similarity[article_idx], score, count)
        for similar in similarities:
            similar_article = articles[similar[0]]
            similar_score = similar[1]
            similar_articles.append((similar_article, similar_score))
        article.similar_articles = similar_articles

    return articles


if __name__ == "__main__":
    file = '10000'
    score_limit = 0.5
    count_limit = 10
    similarity_result = calculate_similarity(file, score_limit, count_limit)
    print(similarity_result)


