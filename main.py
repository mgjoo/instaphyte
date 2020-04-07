from instaphyte import Instagram
import json
import datetime

api = Instagram()

save_dir = './outputs/'
hashtag = "apple"
num_posts = 10
num_posts_in_batch = 5

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