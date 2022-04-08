import json
import gensim
import nltk
import os
from gensim.models import Word2Vec
from nltk.tokenize import sent_tokenize, word_tokenize
nltk.download('punkt')


def read_input(path):
    f = open(path)
    articles = json.load(f)
    texts = []
    for article in articles:
        article_text = article['text']
        if article_text is not None:
            texts.append(article_text)

        article_title = article['title']
        if article_title is not None:
            texts.append(article_title)

        article_description = article['description']
        if article_description is not None:
            texts.append(article_description)

    f.close()
    merged_text = ' '.join(texts).replace('\n', '')
    return merged_text


def train_model(filename):
    input_path = './resources/{}.json'.format(filename)
    output_path = './resources/{}.model'.format(filename)

    if os.path.exists(output_path):
        trained_model = Word2Vec.load(output_path)
    else:
        text = read_input(input_path)
        sentences = []

        for i in sent_tokenize(text):
            words = []

            for j in word_tokenize(i):
                words.append(j.lower())

            sentences.append(words)

        trained_model = gensim.models.Word2Vec(sentences)
        trained_model.save(output_path)

    return trained_model


if __name__ == "__main__":

    model = train_model('large')

    test_word = 'act'
    most_similar = model.wv.most_similar(test_word, topn=5)
    print("Mot similar to '{}': ".format(test_word))
    for item in most_similar:
        print("'{}' with score {}".format(item[0], item[1]))

