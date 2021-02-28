# Built in modules
import argparse
import pickle

"""
Inverted Index
This project is to build inverted index for articles in wikipedia.
The purpose of information retrieval is finding material of an unstructured nature that satisfies an information need
from within large collections. An example of an information retrieval task is the search for relevant Wikipedia articles
by a given query. In the simplest case, we want to find articles that contain all words from the query. To do this,
we can iterate through all documents one by one and check that all words from the query are present in the document.
However, Wikipedia currently has over 51 million articles, so direct search is too expensive.

Modern search engines use special data structures for fast search, such as inverted index.
An inverted index is a data structure that for each word indicates a set of articles containing that word.
To find a set of suitable articles for a query, we need to intersect sets of articles for all words in the query.
"""

"""
- Class InvertedIndex with methods init and query. 
- InvertedIndex constructor takes the build_inverted_index's output from previous step. 
- But in this step the function build_inverted_index should return InvertedIndex object. 
- Method query takes iterable as an argument, choose common articles for all words in the query
"""


class InvertedIndex :
    def __init__(self, word_to_docs_mapping) :
        self.word_to_docs_mapping = word_to_docs_mapping

    def query(self, words) :
        common_article_id = ()
        words = list(words)
        for word in words :
            if self.word_to_docs_mapping.get(word) is not None:
                common_article_id = common_article_id \
                    .intersection(self.word_to_docs_mapping.get(word)) if common_article_id \
                    else self.word_to_docs_mapping.get(word)
            else:
                common_article_id = ()
        return sorted(common_article_id)  # set of common article_id for all words

    def dump(self, filepath) :
        with open(filepath, 'wb') as write_data_file :
            pickle.dump(self.word_to_docs_mapping, write_data_file)

    @classmethod
    def load(cls, filepath) :
        with open(filepath, 'rb') as read_data_file :
            return cls(pickle.load(read_data_file)).word_to_docs_mapping


"""
    - This function takes as an argument the path to the Wikipedia dump file. This function should return a
      dictionary where the key is article_id and the value is the article name and its content.
    - Cast article_id to int.
    - For article_name + article_content, trim the space characters on the right and left.
    - When reading a file, use the encoding='utf8'.
"""


def load_document(filepath) :
    global articles
    articles = {}
    with open(filepath, 'r', encoding='UTF-8') as source_data_file :
        source_data_file_lst = list(source_data_file.read().split("\n"))
        for line in source_data_file_lst :
            if len(line) != 0 :
                article_id, article = line.split(maxsplit=1)
                article = article.strip()
                articles[int(article_id)] = article

    return articles


"""
- This function takes the load_document's output as a parameter and returns a dictionary {word: set of article_id}. 
- Split words in articles by whitespace characters.
"""


def build_inverted_index(articles) :
    global word_to_docs_mapping
    word_to_docs_mapping = {}
    for article_id, article in articles.items() :
        for word in article.split() :
            if word_to_docs_mapping.get(word) is not None :
                articled_ids = word_to_docs_mapping.get(word)
                articled_ids.add(article_id)
                word_to_docs_mapping.setdefault(word, {word : {article_id}}).update(articled_ids)
            else :
                word_to_docs_mapping[word] = {article_id}
    return InvertedIndex(word_to_docs_mapping)


# Command line interface

parser = argparse.ArgumentParser(description='Building and query inverted indexes.')
sub_parser = parser.add_subparsers(dest='command')

build = sub_parser.add_parser('build')
query = sub_parser.add_parser('query')

build.add_argument('--dataset', type=str, required=True)
build.add_argument('--index', type=str, required=True)

query.add_argument('--index', type=str, required=True)
query.add_argument('--query_file', type=str, required=True)

args = parser.parse_args()

if args.command == 'build' :
    inverted_index = InvertedIndex(build_inverted_index(load_document(args.dataset)))
    inverted_index.dump(args.index)

elif args.command == 'query' :
    inverted_index = InvertedIndex.load(args.index)
    with open(args.query_file, 'r') as read_query_file :
        list_of_queries = read_query_file.read().split("/n")
    for query in list_of_queries :
        print(inverted_index.query(query))
