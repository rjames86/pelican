import json


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'as_json'):
            return obj.as_json()
        else:
            return json.JSONEncoder.default(self, obj)


class Base(object):
    def as_json(self):
        return self.__dict__


class Author(Base):
    def __init__(self, name, url=None, avatar=None):
        self.name = name
        self.url = url
        self.avatar = avatar

    @classmethod
    def from_pelican_author(cls, json_feed_generator, author):
        author_url = json_feed_generator.settings.get('AUTHOR_URL').format(slug=author.slug)
        return cls(
            author.name,
            json_feed_generator.build_url(author_url),
            None
        )


class Item(Base):
    def __init__(self,
                 item_id,
                 content_html,
                 url=None,
                 external_url=None,
                 title=None,
                 content_text=None,
                 summary=None,
                 image=None,
                 banner_image=None,
                 date_published=None,
                 date_modified=None,
                 author=None,
                 tags=None):
        self.id = item_id
        self.url = url
        self.external_url = external_url
        self.title = title
        self.content_html = content_html
        self.content_text = content_text
        self.summary = summary
        self.image = image
        self.banner_image = banner_image
        self.date_published = date_published
        self.date_modified = date_modified
        self.author = author
        self.tags = tags

    def __repr__(self):
        return '<Item id=%s>' % (self.id)


class JsonFeedGenerator(object):
    def __init__(self,
                 author,
                 description,
                 favicon,
                 feed_url,
                 home_page_url,
                 title,
                 user_comment,
                 version,
                 items=[]):
        self.author = author
        self.description = description
        self.favicon = favicon
        self.feed_url = feed_url
        self.home_page_url = home_page_url
        self.items = items
        self.title = title
        self.user_comment = user_comment
        self.version = version

    def write(self, output_filepath, encoding):
        json.dump(self, output_filepath, cls=JSONEncoder)

    def add_item(self,
                 title,
                 link,
                 unique_id,
                 description,
                 content,
                 categories,
                 author_name,
                 pubdate,
                 updateddate):

        self.items.append(
            Item(id=unique_id,
                 content_html=content,
                 url=link,
                 external_url=link,
                 title=title,
                 content_text=content,
                 summary=description,
                 image=None,
                 banner_image=None,
                 date_published=pubdate,
                 date_modified=updateddate,
                 author=Author(author_name),
                 tags=categories)
        )
