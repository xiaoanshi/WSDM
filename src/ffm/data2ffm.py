# _*_ coding: utf-8 _*_

import collections
from csv import DictReader
from datetime import datetime
import pandas as pd
train_path = '../../data/train.csv'
test_path = '../../data/test.csv'
train_ffm = '../../output/ffm/train.ffm'
test_ffm = '../../output/ffm/test.ffm'
vali_path = '../../output/ffm/validation.csv'
feature_index = '../../output/ffm/feat_index.txt'

df = pd.read_csv(train_path, nrows=1)

field = [x for x in df.columns if x not in ['msno', 'total_secs', 'avg_total_secs', 'msno_hash']]

table = collections.defaultdict(lambda: 0)


# 为特征名建立编号, filed
def field_index(x):
    index = field.index(x)
    return index


def getIndices(key):
    indices = table.get(key)
    if indices is None:
        indices = len(table)
        table[key] = indices
    return indices


with open(train_ffm, 'w') as outfile:
    for e, row in enumerate(DictReader(open(train_path)), start=1):
        features = []
        for k, v in row.items():
            if k in field:
                if len(v) > 0:
                    idx = field_index(k)
                    kv = k + '_' + v
                    features.append('{0}:{1}:1'.format(idx, getIndices(kv)))

        if e % 100000 == 0:
            print(datetime.now(), 'creating train.ffm...', e)
        outfile.write('{0} {1}\n'.format(row['is_churn'], ' '.join('{0}'.format(val) for val in features)))

with open(test_ffm, 'w') as f1, open(vali_path, 'w') as f2:
    f2.write('msno,is_churn'+'\n')
    for t, row in enumerate(DictReader(open(test_path)), start=1):
        features = []
        for k, v in row.items():
            if k in field:
                if len(v) > 0:
                    idx = field_index(k)
                    kv = k + '_' + v
                    features.append('{0}:{1}:1'.format(idx, getIndices(kv)))
        if t % 100000 == 0:
            print(datetime.now(), 'creating validation data and test.ffm...', t)
        f1.write('{0} {1}\n'.format(row['is_churn'], ' '.join('{0}'.format(val) for val in features)))
        f2.write(str(t) + ',' + row['is_churn'] + '\n')

f1.close()
f2.close()

fo = open(feature_index, 'w')
fo.write(str(len(table)))
fo.close()
print(len(table))