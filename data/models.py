from django.db import models

import json


class RawRecord01(models.Model):
    newsId = models.CharField(max_length=40, primary_key=True)
    srcUrl = models.URLField()
    title = models.CharField(max_length=500)
    postTime = models.BigIntegerField()
    body = models.TextField()

    @staticmethod
    def load_from_json(json_str):
        obj = json.loads(json_str)
        record = RawRecord01(newsId=obj['newsId'],
                             srcUrl=obj['srcUrl'],
                             title=obj['title'],
                             postTime=obj['postTime'],
                             body=obj['body'])
        return record


class Result01(models.Model):
    raw_record = models.ForeignKey(RawRecord01, on_delete=models.CASCADE)
    eventLevel = models.CharField(max_length=20)
    keywords = models.CharField(max_length=400)
    name = models.CharField(max_length=200)
    digest = models.TextField()

    @staticmethod
    def load_from_json(json_str):
        obj = json.loads(json_str)
        record = RawRecord01.objects.get(pk=obj['newsId'])
        assert record is not None
        for entity in obj['entities']:
            result = record.result01_set.create(eventLevel=entity['eventLevel'],
                                                keywords=entity['keywords'],
                                                name=entity['name'],
                                                digest=entity['digest'])
            yield result
