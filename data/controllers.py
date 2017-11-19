from json import JSONDecodeError

from data.models import *

import jieba
from jieba import posseg as pseg


def read_negative_words(filename='C:\\Users\\LiGengWang\\Downloads\\BDCI2017-fahai\\DATA\\NEGATIVE.txt', pt=False):
    negatives = dict()
    file = open(filename, encoding='utf-8')
    for line in file:
        words = line.split('\t')
        if '正' in words[1]:
            negatives[words[0]] = '正向'
        elif '负' in words[1]:
            negatives[words[0]] = '负向'
        else:
            negatives[words[0]] = '中性'

    if pt:
        for w, t in negatives.items():
            print('%s:\t%s' % (w, t))
    return negatives


negative_pairs = read_negative_words()

group_suffix = ['店', '局', '院', '社',
                # '部',
                '楼',
                '队',
                '厂',
                '摊', '坊',
                # '业',
                '园',
                '馆', '堂', '铺', '室', '厅',
                # '处',
                '档', '所', '场',
                # '点',
                '站',
                '库', '房', '会', '屋',
                # '面',
                '汤',
                '粥', '串',
                # '锅',
                '饼', '府', '办',
                '厦', '团', '委', '庄', '苑',
                # '家', # 专家
                '吧', '酒家', '渔行',
                '地产', '房产', '车行', '商行', '银行',
                '分行', '支行', '品行', '茶行', '珠宝行',
                '批发', '园区', '摊床', '小区', '社区',
                '摊位', '中心', '学校', '基地', '门市',
                '科技', '餐饮', '百货', '政府', '超市',
                '公司', '餐厅',
                '小学', '中学', '大学', '党校',
                '频道',
                '商城', '火锅城', '美食城', '服装城', '娱乐城',
                '加工点', '兑换点', '加油点', '零售点',
                '管理处', '经销处', '直销处', '办事处',
                '批发部', '经营部', '销售部', '门市部',
                '经销部', '服务部', '餐饮部', '加工部',
                '俱乐部', '贸易部', '分部']


def clean_ps(name):
    """ clean out () and （） and the content between them """
    clean_name = ''

    name = name.replace('(', '（')
    name = name.replace(')', '）')

    s_index = 0
    while True:
        l_index = name.find('（', s_index)
        if l_index >= 0:
            clean_name += name[s_index:l_index]
            r_index = name.find('）', s_index)
            if r_index >= 0:
                s_index = r_index + 1
            else:
                break
        else:
            clean_name += name[s_index:len(name)]
            break
    return clean_name


def filter_results_with_suffix():
    """ print un-entities from results """
    count = 0
    for result in Result01.objects.all():
        name = clean_ps(result.name)
        for suffix in group_suffix:
            if name.endswith(suffix):
                break
        else:
            print('%s\t: %s' % (count, result.name))
            count += 1


def filter_results_by_suffix(suffix):
    count = 0
    for result in Result01.objects.all():
        name = clean_ps(result.name)
        if name.endswith(suffix):
            print('%d:\t%s' % (count, result.name))
            count += 1


def filter_results_by_event(event):
    count = 0
    for res in Result01.objects.all():
        if res.event_level == event:
            print('%d:\t%s' % (count, res.name))
            count += 1


def print_seg(string):
    custom_jieba()
    for w, f in pseg.cut(string):
        print('%s: \t%s' % (w, f))


def custom_jieba():
    jieba.add_word('食', tag='n')
    jieba.add_word('刺', tag='n')
    jieba.add_word('超市', tag='n')
    jieba.add_word('娇娇', tag='na')
    jieba.add_word('出厂', tag='v')
    jieba.add_word('生产', tag='v')
    jieba.add_word('标称', tag='v')
    jieba.add_word('量贩', tag='an')
    jieba.add_word('百度', tag='nt')
    jieba.add_word('开发公司', tag='nz')
    jieba.add_word('海王生物', tag='nt')
    jieba.add_word('美团', tag='nt')
    jieba.add_word('百度外卖', tag='nt')
    jieba.add_word('美团外卖', tag='nt')
    jieba.add_word('超市发', tag='nt')
    jieba.add_word('农业部', tag='nz')
    jieba.add_word('本报讯', tag='n')


def unique_entities(entities):
    unique_entities_list = list()
    # only print out unique entity
    for i in entities:
        for j in entities:
            if i != j and i in j:
                break
        else:
            unique_entities_list.append(i)
    return unique_entities_list


def print_items(items):
    count = 0
    for i in items:
        print('%d:\t%s' % (count, i))
        count += 1


def extract_entity_rough(string, default_event_level='中性'):
    custom_jieba()

    string = string.replace('（', '(')
    string = string.replace('）', ')')
    string += '。'  # it is caused that some buff should flush by a 'x'
    words = [(w, f) for w, f in pseg.cut(string)]

    name = ''
    name_suffix = ''
    flag = False
    matched_left_p = False
    matched_left_q = False
    entities = set()

    sentence = ''
    sentences = list()
    for w, f in words:
        sentence += w
        if w == '。' or w == '；' or w == ';' or w == ' ':
            if len(sentence) > 8:  # the length of a sentence should longer than 8
                sentences.append(sentence)
            sentence = ''

        # ignore content between '《' and '》'
        if w == '《':
            matched_left_q = True
        elif matched_left_q:
            if w == '》':
                matched_left_q = False
            continue

        # content between '(' and ')' should be looked as a part of name
        if matched_left_p or w == '(':
            matched_left_p = True
            if name_suffix == '':
                if name != '':  # () should not be in the front of a sentence
                    name += w
            else:
                name_suffix += w
            if w == ')':
                matched_left_p = False
            continue

        # compose words which could be a compound word
        # if 'nt' == f:
        #     name_suffix += w
        #     name += name_suffix
        #     entities.add(name)
        #     flag = True
        #     name = ''
        #     name_suffix = ''
        # if 'n' in f or 'z' in f or 'a' in f or 'c' == f or 'f' == f or 'q' == f or 'g' in f or 't' in f \
        if 'v' != f and 'x' not in f and 'w' not in f and 'un' != f \
                and 'p' != f and 'u' not in f and 'd' != f \
                and ('m' != f or (name_suffix != '' or name != '')):
            name_suffix += w
            for i in group_suffix:
                if w.endswith(i) and ('n' in f or 'j' == f):  # end word should be n.
                    name += name_suffix
                    name_suffix = ''
                    flag = True
                    break
        else:
            if flag and (len(name) > 4 or (len(name) > 3 and name.endswith('学'))):
                entities.add(name)
            flag = False
            name = ''
            name_suffix = ''

    entity_pairs = list()
    entities = unique_entities(entities)
    for e in entities:
        name = e
        event_level = default_event_level
        digest = ''

        for s in sentences:
            if e in s:
                digest = s
                for w, t in negative_pairs.items():
                    if w in digest:
                        event_level = t
                        break
                break

        if e.endswith('局') or e.endswith('院'):
            event_level = '中性'

        # print('%s:\t\t%s,\t\t%s' % (e, event_level, digest))
        entity_pairs.append({'eventLevel': event_level, 'keywords': '', 'name': name, 'digest': digest})

    res = dict()
    res['newsId'] = ''
    res['entities'] = entity_pairs
    return res


def judge_event_level_from_record_title():
    count = 0
    negatives = negative_pairs
    for rec in RawRecord01.objects.all():
        for w, t in negatives.items():
            if w in rec.title:
                print('%d\t%s\t%s' % (count, w, rec.title))
                count += 1
                break
    print('ratio: ', count / RawRecord01.objects.count())


def extract_entity_rough_by_news_id(news_id):
    record = RawRecord01.objects.get(news_id=news_id)
    result = extract_entity_rough_naive(record.news_id, record.title, record.body)
    return result


def extract_entity_rough_naive(news_id, title, body):
    negatives = negative_pairs
    default_event_level = '中性'
    for w, t in negatives.items():
        if w in title:
            default_event_level = negatives[w]
            break
    result = extract_entity_rough(body, default_event_level)
    result['newsId'] = news_id
    return result


def extract_entity_rough_by_json(json_str):
    record = json.loads(json_str)
    return extract_entity_rough_naive(record['newsId'], record['title'], record['title'] + '。' + record['body'])


def test():
    count = 0
    in_filename = r'C:\Users\LiGengWang\Downloads\BDCI2017-fahai\DATA\DATA_TEST.txt'
    in_file = open(in_filename, encoding='utf-8')
    filename = r'C:\Users\LiGengWang\Downloads\BDCI2017-fahai\DATA\RESULT_TEST_T.txt'
    out_file = open(filename, 'w', encoding='utf-8')
    for line in in_file:
        print(count)
        count += 1
        out_file.write(json.dumps(extract_entity_rough_by_json(line), ensure_ascii=False))
        out_file.write('\n')

    in_file.close()
    out_file.close()


def show_names_len():
    counts = dict()
    for result in Result01.objects.all():
        n = len(result.name)
        if n < 5:
            print(result.name)
        c = counts.get(n, 0)
        counts[n] = c + 1

    for k, v in counts.items():
        print('len %d has %d' % (k, v))


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
