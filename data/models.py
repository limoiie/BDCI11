from django.db import models

import json


class RawRecord01(models.Model):
    """ Model of raw record """
    newsId = models.CharField(max_length=40, primary_key=True)
    srcUrl = models.URLField()
    title = models.CharField(max_length=500)
    postTime = models.BigIntegerField()
    body = models.TextField()

    @staticmethod
    def load_from_json(json_str):
        """
        Load raw record from json str. The format of json should be
        like this:
        {
            "newsId": "111111111111111111111",
            "srcUrl": "http://www.baidu.com",
            "title": "This is title",
            "postTime": "1504171080000",
            "body": "This is body"
        }
        each raw record is corresponding to one json string
        :param json_str: json string with format like above
        :return: record
        """
        obj = json.loads(json_str)
        record = RawRecord01(newsId=obj['newsId'],
                             srcUrl=obj['srcUrl'],
                             title=obj['title'],
                             postTime=obj['postTime'],
                             body=obj['body'])
        return record


class Result01(models.Model):
    """
    Model of result under the analysis of raw result, each record
    will have several results, each result is about one entity in
    record.
    """
    raw_record = models.ForeignKey(RawRecord01, on_delete=models.CASCADE)
    eventLevel = models.CharField(max_length=20)
    keywords = models.CharField(max_length=400)
    name = models.CharField(max_length=200)
    digest = models.TextField()

    @staticmethod
    def load_from_json(json_str):
        """
        Load %class Result01 from json. The format of json should
        be like:
        {
            "newsId": "111111111111111111111",
            "entities": [
                 {
                     "eventLevel": "event-value",
                     "keywords": "keyword1|keyword2",
                     "name": "name-value",
                     "digest": "digest-value"
                 },
                 {
                     "eventLevel": "event-value",
                     "keywords": "keyword1|keyword2",
                     "name": "name-value",
                     "digest": "digest-value"
                 },
                 ...
            ]
        }
        each result is corresponding to one entity in json string
        show above with the same newsId.

        :param json_str: json string with format like above
        :return: yield one result each time.
        """
        obj = json.loads(json_str)
        record = RawRecord01.objects.get(pk=obj['newsId'])
        assert record is not None
        for entity in obj['entities']:
            result = record.result01_set.create(eventLevel=entity['eventLevel'],
                                                keywords=entity['keywords'],
                                                name=entity['name'],
                                                digest=entity['digest'])
            yield result
