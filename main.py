from instaphyte import Instagram
import json
import datetime
import time
import os

# 인기 게시물
save_dir = './outputs/top_posts/'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

input_folder_path = "./outputs/related_hashtags/"
input_list = os.listdir(input_folder_path)

hashtags = []
for inp in input_list:
    json_data = ''
    with open(input_folder_path + inp, encoding='UTF8') as json_file:
        json_data = json.load(json_file)

    for related_tag in json_data:
        if 'node' in related_tag:
            hashtags.append(related_tag['node']['name'])

api = Instagram()
num_top_posts = 9
num_top_posts_in_batch = 9
for i, hashtag in enumerate(hashtags, 1):
    print ('hashtag ({}/{}): {}'.format(i, len(hashtags), hashtag))

    start = time.time()
    posts_list = []
    for i, post in enumerate(api.hashtag_top_posts(hashtag, num_top_posts)): 
        posts_list.append(post)

        if (i > 0 and (i + 1) % num_top_posts_in_batch == 0) or i == (num_top_posts - 1):
            dt = datetime.datetime.now()
            out_path = save_dir + hashtag + '_top_posts_' + dt.strftime("%Y%m%d_%H%M%S_%f") + '.json'

            with open(out_path, 'w') as f:
                f.write(json.dumps(posts_list, indent=4))

            print('{}/{}, {}'.format(i + 1, num_top_posts, out_path))

            posts_list.clear()
    end = time.time()
    print("elapsed time (s): ", end - start)

"""
# 최신게시물
save_dir = '../instaphyte-analyzer/input/' + hashtag + '/'

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

num_posts = 1000
num_posts_in_batch = 100

start = time.time()
posts_list = []
for i, post in enumerate(api.hashtag(hashtag, num_posts)): 
    posts_list.append(post)

    if (i > 0 and (i + 1) % num_posts_in_batch == 0) or i == (num_posts - 1):
        dt = datetime.datetime.now()
        out_path = save_dir + hashtag + '_' + dt.strftime("%Y%m%d_%H%M%S_%f") + '.json'

        with open(out_path, 'w') as f:
            f.write(json.dumps(posts_list, indent=4))

        print('{}/{}, {}'.format(i + 1, num_posts, out_path))

        posts_list.clear()
end = time.time()
print("elapsed time (s): ", end - start)
"""