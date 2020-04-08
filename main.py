from instaphyte import Instagram
import json
import datetime
import time

api = Instagram()

save_dir = './outputs/'
hashtag = "맛집"
num_posts = 10000
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

related_tags_list = []
for related_tag in api.hashtag_related_tags(hashtag): 
    related_tags_list.append(related_tag)

dt = datetime.datetime.now()
out_path = save_dir + hashtag + '_related_tags_' + dt.strftime("%Y%m%d_%H%M%S_%f") + '.json'

with open(out_path, 'w') as f:
    f.write(json.dumps(related_tags_list, indent=4))

print('{}/{}, {}'.format(len(related_tags_list), len(related_tags_list), out_path))