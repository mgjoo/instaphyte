from instaphyte import Instagram
import json
import datetime
import time
import os

depth = 3

hashtags = [
    "교대역맛집", 
    "서초역맛집", 
    "샤로수길맛집", 
    "낙성대역맛집", 
]

save_dir = './outputs/related_hashtags/'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

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
            #print(related_tag)
            if 'node' in related_tag:
                new_hashtags.append(related_tag['node']['name'])
    hashtags = new_hashtags
