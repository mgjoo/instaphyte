from instaphyte import Instagram
import json
import datetime
import time
import os

depth = 2

hashtags = [
    "맛집", 
]

save_dir = './outputs/related_hashtags/맛집/'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

_dict = dict()

api = Instagram()
for d in range(0, depth):
    print('depth ({}/{}):'.format(d + 1, depth))

    new_hashtags = []
    for hashtag in hashtags:
        related_tags_list = []

        start = time.time()
        for related_tag in api.hashtag_related_tags(hashtag): 
            related_tags_list.append(related_tag)

        dt = datetime.datetime.now()
        out_path = save_dir + hashtag + '_related_tags_' + dt.strftime("%Y%m%d_%H%M%S_%f") + '.json'

        with open(out_path, 'w') as f:
            f.write(json.dumps(related_tags_list, indent=4))

        print('depth ({}/{}) - {}/{}, {}'.format(d + 1, depth, len(related_tags_list), len(related_tags_list), out_path))

        end = time.time()
        print("elapsed time (s): ", end - start)

        for related_tag in related_tags_list:
            if 'node' in related_tag:
                tag = related_tag['node']['name']
                new_hashtags.append(tag)
                
                if tag not in _dict:
                    _dict[tag] = 1
                else:
                    _dict[tag] = _dict[tag] + 1

    hashtags = new_hashtags

print(_dict)

res = sorted(_dict.items(), key=(lambda x: x[1]), reverse = True)

with open('./outputs/result.json', 'w', encoding='utf-8') as make_file:
    json.dump(res, make_file, indent="\t", ensure_ascii=False)