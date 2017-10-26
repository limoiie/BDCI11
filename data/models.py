from django.db import models
from django.utils import timezone

import json


class Group01(models.Model):
    group_name = models.CharField(max_length=200)
    post_time = models.DateTimeField(default=timezone.now)
    pass


class RawRecord01(models.Model):
    """ Model of raw record """
    group = models.ForeignKey(Group01, on_delete=models.CASCADE)
    news_id = models.CharField(max_length=40)
    src_url = models.URLField()
    title = models.CharField(max_length=500)
    post_time = models.BigIntegerField()
    body = models.TextField()

    class Meta:
        unique_together = ("group", "news_id")

    @staticmethod
    def load_from_json(group, json_str):
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
        :param group: instance of %class Group01
        :param json_str: json string with format like above
        :return: record
        """
        assert isinstance(group, Group01)

        obj = json.loads(json_str)
        record = group.rawrecord01_set.create(news_id=obj['newsId'],
                                              src_url=obj['srcUrl'],
                                              title=obj['title'],
                                              post_time=obj['postTime'],
                                              body=obj['body'])
        return record


class Result01(models.Model):
    """
    Model of result under the analysis of raw result, each record
    will have several results, each result is about one entity in
    record.
    """
    raw_record = models.ForeignKey(RawRecord01, on_delete=models.CASCADE)
    event_level = models.CharField(max_length=20)
    keywords = models.CharField(max_length=400)
    name = models.CharField(max_length=200)
    digest = models.TextField()

    @staticmethod
    def load_from_json(group, json_str):
        """
        Load %class Result01 from json. The format of json should
        be like:
        {
            "newsId": "11111111111111111111",
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
                }
            ]
        }
        several results are corresponding to one raw record

        :param group: instance of %class Group01
        :param json_str: json string with format like above
        :return: result
        """
        assert isinstance(group, Group01)
        root = json.loads(json_str)
        raw_record = RawRecord01.objects.get(group=group, news_id=root['newsId'])

        results = list()
        for entity in root['entities']:
            result = raw_record.result01_set.create(event_level=entity['eventLevel'],
                                                    keywords=entity['keywords'],
                                                    name=entity['name'],
                                                    digest=entity['digest'])
            results.append(result)
        return results
