import os
import json
from expertai.nlapi.cloud.client import ExpertAiClient
from flask import Flask, request
from github import Github
from expertai.nlapi.cloud.client import ExpertAiClient
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
# from dotenv import load_dotenv
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('punkt')
nltk.download('stopwords')
# load_dotenv()

server = Flask(__name__)
client = ExpertAiClient()
g = Github(os.environ["GITHUB_TOKEN"])



def _create_dictionary_table(text_string):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text_string)
    stem = PorterStemmer()
    frequency_table = dict()
    for wd in words:
        wd = stem.stem(wd)
        if wd in stop_words:
            continue
        if wd in frequency_table:
            frequency_table[wd] += 1
        else:
            frequency_table[wd] = 1

    return frequency_table

def _calculate_sentence_scores(sentences, frequency_table):
    sentence_weight = dict()

    for sentence in sentences:
        sentence_wordcount = (len(word_tokenize(sentence)))
        sentence_wordcount_without_stop_words = 0
        for word_weight in frequency_table:
            if word_weight in sentence.lower():
                sentence_wordcount_without_stop_words += 1
                if sentence[:7] in sentence_weight:
                    sentence_weight[sentence[:7]] += frequency_table[word_weight]
                else:
                    sentence_weight[sentence[:7]] = frequency_table[word_weight]
        try:
            sentence_weight[sentence[:7]] = sentence_weight[sentence[:7]] / sentence_wordcount_without_stop_words
        except:
            pass

    return sentence_weight

def _calculate_average_score(sentence_weight) -> int:
   
    #calculating the average score for the sentences
    sum_values = 0
    for entry in sentence_weight:
        sum_values += sentence_weight[entry]

    #getting sentence average value from source text
    average_score = (sum_values / len(sentence_weight))

    return average_score

def _get_article_summary(sentences, sentence_weight, threshold):
    sentence_counter = 0
    article_summary = ''

    for sentence in sentences:
        if sentence[:7] in sentence_weight and sentence_weight[sentence[:7]] >= (threshold):
            article_summary += " " + sentence
            sentence_counter += 1

    return article_summary

language = 'en'
    # output = client.full_analysis(body={"document": {"text": text}}, params={'language': language})
# response = client.specific_resource_analysis(body={"document": {"text": text}}, params={'language': language, 'resource':'disambiguation'})

# # print(response.knowledge, response.tokens, response.sentences)

# print(f'{"TOKEN":{20}} {"LEMMA":{8}}')

# for token in response.tokens:
#     print(f'{text[token.start:token.end]:{20}} {token.lemma:{8}}')



def _run_article_summary(article):

    frequency_table = _create_dictionary_table(article)
    response = client.specific_resource_analysis(body={"document": {"text": article}}, params={'language': language, 'resource':'disambiguation'})
    sentences = [article[sentence.start: sentence.end] for sentence in response.sentences]
    # senctences = ""

    sentence_scores = _calculate_sentence_scores(sentences, frequency_table)

    threshold = _calculate_average_score(sentence_scores)

    repo_summary = _get_article_summary(sentences, sentence_scores, 1.5 * threshold)

    return repo_summary

def _nltk_article_summary(article):
    frequency_table = _create_dictionary_table(article)
    # response = client.specific_resource_analysis(body={"document": {"text": article}}, params={'language': language, 'resource':'disambiguation'})
    # sentences = [article[sentence.start: sentence.end] for sentence in response.sentences]
    sentences = sent_tokenize(article)

    sentence_scores = _calculate_sentence_scores(sentences, frequency_table)

    threshold = _calculate_average_score(sentence_scores)

    repo_summary = _get_article_summary(sentences, sentence_scores, 1.5 * threshold)

    return repo_summary

def analyze_text(text):
    language = 'en'
    # output = client.full_analysis(body={"document": {"text": text}}, params={'language': language})
    response = client.full_analysis(body={"document": {"text": text}}, params={'language': language})
    # print("Output arrays size:")
    # for topics in output.tokens:
    #     print(topics.lemma, topics.atoms, topics.syncon)
    # print("JSON representation:")
    print(response)


    # Tokens' lemma and part-of-speech

    print("\nTab separated list of tokens' lemma and part-of-speech:")
    # document = response.json["data"]

    shortened_text = ''
    for main_sentence in response.main_sentences:
        shortened_text += main_sentence.value
    return shortened_text

@server.route("/nltk", methods=['POST'])
def nltkanalyze():
    repo_url = request.json["repoUrl"]
    repo_name = repo_url.replace("https://github.com/", "")
    repo = g.get_repo(repo_name)
    readme = repo.get_readme()
    text = readme.decoded_content
    decoded_text = text.decode("utf-8")
    shortened_text = _nltk_article_summary(decoded_text)
    return {
        "readme": decoded_text,
        "shortened": shortened_text
    }

@server.route("/nltkrepo", methods=['POST'])
def nltkrepo():
    repo_url = request.json["repoUrl"]
    repo_name = repo_url.replace("https://github.com/", "")
    repo = g.get_repo(repo_name)
    readme = repo.get_readme()
    text = readme.decoded_content
    decoded_text = text.decode("utf-8")
    shortened_text = _run_article_summary(decoded_text)
    return {
        "readme": decoded_text,
        "shortened": shortened_text
    }

@server.route("/repo", methods=['POST'])
def index():
    print(request.json)
    repo_url = request.json["repoUrl"]
    repo_name = repo_url.replace("https://github.com/", "")
    print(repo_name)
    repo = g.get_repo(repo_name)
    readme = repo.get_readme()
    text = readme.decoded_content
    decoded_text = text.decode("utf-8")
    shortened_text = analyze_text(decoded_text)
    # text = "Michael Jordan was one of the best basketball players of all time. Scoring was Jordan's stand-out skill, but he still holds a defensive NBA record, with eight steals in a half."
    
    # print("knowledge: ", len(output.knowledge))
    # print("paragraphs: ", len(output.paragraphs))
    # print("sentences: ", len(output.sentences))
    # print("phrases: ", len(output.phrases))
    # print("tokens: ", len(output.tokens))
    # print("mainSentences: ", output.main_sentences)
    # print("mainPhrases: ", output.main_phrases)
    # print("mainLemmas: ", len(output.main_lemmas))
    # print("mainSyncons: ", len(output.main_syncons))
    # print("topics: ", len(output.topics))
    # print("entities: ", len(output.entities))
    # print("entities: ", len(output.relations))
    # print("sentiment.items: ", len(output.sentiment.items))
    return {
        "readme": decoded_text,
        "shortened": shortened_text
    }

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))