from django.test import TestCase

import json

from data.models import RawRecord01, Result01

test_records = [
    '{"newsId":"aa8ca5ff0a1b882dff018b1e3353f16e409b33b8",'
    '"srcUrl":"http://news.foodmate.net/2017/08/441965.html",'
    '"title":"This is title 01",'
    '"postTime":1504171080000,'
    '"body":"This is body 01"}',
    '{"newsId":"aa8ca5ff0a1b882dff018b1e3353f16e409b33b9",'
    '"srcUrl":"http://news.foodmate.net/2017/08/441966.html",'
    '"title":"This is title 02",'
    '"postTime":1504171080000,'
    '"body":"This is body 02"}'
]

test_results = [
    '{"newsId":"aa8ca5ff0a1b882dff018b1e3353f16e409b33b8",'
    '"entities":['
    '{"eventLevel":"中性","keywords":"none|none","name":"name1","digest":"This is digest 1"},'
    '{"eventLevel":"正向","keywords":"none|none","name":"name2","digest":"This is digest 2"}'
    ']}',
    '{"newsId":"aa8ca5ff0a1b882dff018b1e3353f16e409b33b9",'
    '"entities":['
    '{"eventLevel":"正向","keywords":"none|none","name":"name3","digest":"This is digest 3"},'
    '{"eventLevel":"负向","keywords":"none|none","name":"name4","digest":"This is digest 4"}'
    ']}'
]


class RawRecord01ModelTests(TestCase):
    @staticmethod
    def test_load_from_json():
        # extract from json
        dicts = [json.loads(j) for j in test_records]
        # extract from tested method
        records = [RawRecord01.load_from_json(j) for j in test_records]

        for a, b in zip(dicts, records):
            assert a['newsId'] == b.newsId
            assert a['srcUrl'] == b.srcUrl
            assert a['title'] == b.title
            assert a['postTime'] == b.postTime
            assert a['body'] == b.body

        print('\n=> RawRecord01ModelTests.test_load_from_json pass!')


class Result01ModelTests(TestCase):
    @staticmethod
    def test_load_from_json():
        # extract records
        records = [RawRecord01.load_from_json(j) for j in test_records]
        # save record into database from which %code Result01.load_from_json will read
        for record in records:
            record.save()

        # extract results from json
        results_uniform_from_json = dict()
        for j in test_results:
            result = json.loads(j)
            results_uniform_from_json[result['newsId']] = result['entities']

        results_uniform = dict()
        # extract results from tested method
        results = [Result01.load_from_json(j) for j in test_results]
        # construct uniform records for compare conveniently
        for results_per_record in results:
            news_id = None
            ls = list()
            for result in results_per_record:
                news_id = result.raw_record_id if news_id is None else news_id
                d = dict()
                d['eventLevel'] = result.eventLevel
                d['keywords'] = result.keywords
                d['name'] = result.name
                d['digest'] = result.digest
                ls.append(d)
            results_uniform[news_id] = ls

        assert results_uniform_from_json == results_uniform

        print('\n=> Result01ModelTests.test_load_from_json pass!')
