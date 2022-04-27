from pprint import pprint
import csv
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from elasticsearch import helpers


INDEX_NAME = "nccs"


def generate_data(filename):
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["_id"] = row["url"]
            row["_index"] = INDEX_NAME
            yield row


def load_data(client: Elasticsearch, filename: str):
    response = client.search(index=INDEX_NAME, size=0)
    doc_count = response["hits"]["total"]["value"]
    if doc_count > 0:
        print(f"Documents already indexed: {doc_count}")
        return
    success, failed = helpers.bulk(client, generate_data(filename), stats_only=True)
    print(f"Success: {success}, failed: {failed}")


def create_index(client: Elasticsearch, overwrite=False):
    indices = IndicesClient(client=client)
    if indices.exists(index=INDEX_NAME):
        if overwrite:
            indices.delete(INDEX_NAME)
        else:
            print(f"Index exists: {INDEX_NAME}")
            return
    index_settings = {
        "analysis": {
            "analyzer": {
                "metaphone_analyzer": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "metaphone_filter"
                    ]
                },
                "soundex_analyzer": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "soundex_filter"
                    ]
                }
            },
            "filter": {
                "metaphone_filter": {
                    "type": "phonetic",
                    "encoder": "metaphone",
                    "replace": True
                },
                "soundex_filter": {
                    "type": "phonetic",
                    "encoder": "refined_soundex",
                    "replace": True
                }
            }
        }
    }

    mappings = {
        "dynamic": "strict",
        "properties": {
            "url": {"type": "keyword"},
            "name": {"type": "keyword"},
            "address": {
                "type": "text",
                "fields": {
                    "kw": {
                        "type": "keyword"
                    },
                    "meta": {
                        "type": "text",
                        "analyzer": "metaphone_analyzer"
                    },
                    "sdex": {
                        "type": "text",
                        "analyzer": "soundex_analyzer"
                    }
                }
            },
        }
    }
    settings = {
        "number_of_replicas": 0,
        "number_of_shards": 1,
        "index": index_settings
    }
    response = indices.create(index=INDEX_NAME, mappings=mappings, settings=settings)
    pprint(response.body)


def main(*, overwrite=False):
    client = Elasticsearch(
        hosts="http://localhost:9200", basic_auth=("elastic", "changeme")
    )
    create_index(client, overwrite=overwrite)
    load_data(client, "nccs.csv")


if __name__ == "__main__":
    main(overwrite=True)
