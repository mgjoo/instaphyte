from instaphyte import Instagram

api = Instagram()

# Get 1 posts from #apple
for post in api.hashtag("apple", 1):
    print(post)