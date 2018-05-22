import random

predictions = []
base = []
features = []

with open('../mallet/res.txt', 'r', encoding='utf8') as f:
    for l in f:
        l = l[:-1]
        fields = l.split()
        predictions.append(
            (int(fields[0]), ((fields[1], fields[2]), (fields[3], fields[4])))
        )

with open('../mallet/data_set.mallet', 'r', encoding='utf8') as f:
    for l in f:
        l = l[:-1]
        fields = l.split()
        features.append(
            (int(fields[0]), l)
        )

with open('data_set_2.mallet', 'r', encoding='utf8') as f:
    lines = [l[:-1] for l in f.readlines()]
    base = [(int(l.split()[0]), l) for l in lines]

predictions = dict(predictions)
features = dict(features)
base = dict(base)

final = {}
for i in predictions.keys():
    the_max = max(predictions[i], key=lambda x: x[1])
    index = 0 if predictions[i][0][1] == the_max else 1
    pred = predictions[i][index][0]
    final[i] = {
        'base': base[i],
        'features': features[i],
        'label': features[i].split()[1],
        'pred': pred
    }

errors = [v for k, v in final.items() if v['label'] != v['pred']]

while True:
    e = random.choice(errors)
    print('base\t', e['base'])
    print('f\t', e['features'])
    print('l\t', e['label'])
    print('p\t', e['pred'])
    print()
    input()
