from json import JSONDecodeError

from data.models import *


def extract_records_and_store(file, name):
    group = Group01.objects.create(group_name=name)
    try:
        for line in file:
            RawRecord01.load_from_json(group, line)
    except JSONDecodeError:
        group.delete()
        return False
    return True


def extract_results_and_store(file, group_id):
    group = Group01.objects.get(pk=group_id)
    if group:
        try:
            for line in file:
                Result01.load_from_json(group, line)
        except JSONDecodeError:
            return False
    else:
        return False
    return True
