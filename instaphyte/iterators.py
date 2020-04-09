from socialreaper.apis import ApiError
from socialreaper.iterators import Source, Iter, IterError

from instaphyte.api import InstagramAPI


class Instagram(Source):
    def __init__(self):
        super().__init__()

        self.api = InstagramAPI()

    class InstagramIter(Iter):
        def __init__(self, node, function, count, response_key, edge_key):
            super().__init__()

            self.node = node
            self.function = function
            self.max = count
            self.response_key = response_key
            self.edge_key = edge_key
            self.max_id = None

        def get_data(self):
            self.page_count += 1

            try:
                self.response = self.function(self.node, self.max_id)

                page = self.response['graphql'][self.response_key][
                    "edge_" + self.response_key + "_to_" + self.edge_key]
                self.data = page["edges"]
                self.max_id = None if "page_info" not in page else page["page_info"]["end_cursor"]
                
                if not self.max_id and self.edge_key == "media":
                    raise StopIteration

                if self.edge_key == "related_tags":
                    count = dict()
                    count['count'] = self.response['graphql']['hashtag']['edge_hashtag_to_media']['count']
                    self.data.append(count)
                    self.max = len(self.data) 
                
            except ApiError as e:
                raise IterError(e, vars(self))

    def hashtag(self, tag, count=0):
        return self.InstagramIter(tag, self.api.hashtag, count, "hashtag", "media")

    def hashtag_related_tags(self, tag, count=0):
        return self.InstagramIter(tag, self.api.hashtag_related_tags, count, "hashtag", "related_tags")

    def hashtag_top_posts(self, tag, count=9):
        return self.InstagramIter(tag, self.api.hashtag_top_posts, count, "hashtag", "top_posts")