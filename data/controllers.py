from json import JSONDecodeError

from data.models import *


def extract_records_and_store(file_name, name):
    file = open(file_name, encoding='utf-8')
    if file and not file.closed:
        group = Group01.objects.create(group_name=name)

        num = 0
        for line in file:
            print('process line %d ...' % num)
            num += 1
            RawRecord01.load_from_json(group, line)
    else:
        raise Exception('Fall to open file %s.' % file_name)


def extract_results_and_store(file_name, group):
    file = open(file_name, encoding='utf-8')
    if file and not file.closed:
        num = 0
        for line in file:
            print('process line %d ...' % num)
            num += 1
            Result01.load_from_json(group, line)
    else:
        raise Exception('Fall to open file %s.' % file_name)
