from django.test import TestCase

import json

from data.models import RawRecord01, Result01, Group01

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

        # one group for one file of raw records
        group = Group01.objects.create(group_name='group')

        records = list()
        # extract from tested method
        for j in test_records:
            record = RawRecord01.load_from_json(group, j)
            records.append(record)

        for a, b in zip(dicts, records):
            assert a['newsId'] == b.news_id
            assert a['srcUrl'] == b.src_url
            assert a['title'] == b.title
            assert a['postTime'] == b.post_time
            assert a['body'] == b.body

        print('\n=> RawRecord01ModelTests.test_load_from_json pass!')


class Result01ModelTests(TestCase):
    @staticmethod
    def extract_results_from_json():
        uniform_results = dict()
        for j in test_results:
            result = json.loads(j)
            uniform_results[result['newsId']] = result['entities']
        return uniform_results

    @staticmethod
    def extract_results_by_method(group):
        """ Extract results by %code Result01.load_from_json """

        results = list()
        # extract results from tested method
        for j in test_results:
            results_per_record = Result01.load_from_json(group, j)
            results.extend(results_per_record)

        results_uniform = dict()
        # construct uniform records for compare conveniently
        for result in results:
            d = dict()
            d['eventLevel'] = result.event_level
            d['keywords'] = result.keywords
            d['name'] = result.name
            d['digest'] = result.digest

            news_id = result.raw_record.news_id
            if news_id not in results_uniform.keys():
                results_uniform[news_id] = list()
            results_uniform[news_id].append(d)
        return results_uniform

    @staticmethod
    def test_load_from_json():
        # one group for one file of raw records
        group = Group01.objects.create(group_name='group')

        # extract records
        records = [RawRecord01.load_from_json(group, j) for j in test_records]
        # save record into database from which %code Result01.load_from_json will read
        for record in records:
            record.save()

        # extract results by two different method
        results_from_json = Result01ModelTests.extract_results_from_json()
        results_by_method = Result01ModelTests.extract_results_by_method(group)

        assert results_from_json == results_by_method

        print('\n=> Result01ModelTests.test_load_from_json pass!')
