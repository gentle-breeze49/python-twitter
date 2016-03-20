import json
from calendar import timegm

try:
    from rfc822 import parsedate
except ImportError:
    from email.utils import parsedate

import time


class TwitterModel(object):

    """ Base class from which all twitter models will inherit. """

    def __init__(self, **kwargs):
        self.param_defaults = {}

    def __str__(self):
        return self.AsJsonString()

    def __eq__(self, other):
        return other and self.AsDict() == other.AsDict()

    def __ne__(self, other):
        return not self.__eq__(other)

    def AsJsonString(self):
        return json.dumps(self.AsDict(), sort_keys=True)

    def AsDict(self):
        data = {}
        for (key, value) in self.param_defaults.items():
            if getattr(getattr(self, key, None), 'AsDict', None):
                data[key] = getattr(self, key).AsDict()
            elif getattr(self, key, None):
                data[key] = getattr(self, key, None)
        return data

    @classmethod
    def NewFromJsonDict(cls, data, **kwargs):
        """ Create a new instance based on a JSON dict.

        Args:
            data: A JSON dict, as converted from the JSON in the twitter API

        Returns:
            A twitter.Media instance
        """

        if kwargs:
            for key, val in kwargs.items():
                data[key] = val

        return cls(**data)


class Media(TwitterModel):

    """A class representing the Media component of a tweet. """

    def __init__(self, **kwargs):
        self.param_defaults = {
            'id': None,
            'expanded_url': None,
            'display_url': None,
            'url': None,
            'media_url_https': None,
            'media_url': None,
            'type': None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "Media(ID={media_id}, Type={type}, DisplayURL='{url}')".format(
            media_id=self.id,
            type=self.type,
            url=self.display_url)


class List(TwitterModel):

    """A class representing the List structure used by the twitter API. """

    def __init__(self, **kwargs):
        self.param_defaults = {
            'id': None,
            'name': None,
            'slug': None,
            'description': None,
            'full_name': None,
            'mode': None,
            'uri': None,
            'member_count': None,
            'subscriber_count': None,
            'following': None,
            'user': None}

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

        if 'user' in kwargs:
            self.user = User.NewFromJsonDict(kwargs.get('user'))

    def __repr__(self):
        return "List(ID={list_id}, FullName={full_name}, Slug={slug}, User={user})".format(
            list_id=self.id,
            full_name=self.full_name,
            slug=self.slug,
            user=self.user.screen_name)


class Category(TwitterModel):

    """A class representing the suggested user category structure. """

    def __init__(self, **kwargs):
        self.param_defaults = {
            'name': None,
            'slug': None,
            'size': None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "Category(Name={name}, Slug={slug}, Size={size})".format(
            name=self.name,
            slug=self.slug,
            size=self.size)


class DirectMessage(TwitterModel):

    """A class representing a Direct Message. """

    def __init__(self, **kwargs):
        self.param_defaults = {
            'id': None,
            'created_at': None,
            'sender_id': None,
            'sender_screen_name': None,
            'recipient_id': None,
            'recipient_screen_name': None,
            'text': None}

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        if self.text and len(self.text) > 140:
            text = self.text[:140] + "[...]"
        else:
            text = self.text
        return "DirectMessage(ID={dm_id}, Sender={sender}, Time={time}, Text={text})".format(
            dm_id=self.id,
            sender=self.sender_screen_name,
            time=self.created_at,
            text=text)


class Trend(TwitterModel):

    """ A class representing a trending topic. """

    def __init__(self, **kwargs):
        self.param_defaults = {
            'events': None,
            'name': None,
            'promoted_content': None,
            'query': None,
            'timestamp': None,
            'url': None,
            'volume': None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "Trend(Name={name}, Time={ts}, URL={url})".format(
            name=self.name,
            ts=self.timestamp,
            url=self.url)


class Hashtag(TwitterModel):

    """ A class representing a twitter hashtag. """

    def __init__(self, **kwargs):
        self.param_defaults = {
            'text': None
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "Hashtag(Text={text})".format(
            text=self.text)


class Url(TwitterModel):

    """ A class representing an URL contained in a tweet. """

    def __init__(self, **kwargs):
        self.param_defaults = {
            'expanded_url': None,
            'url': None}

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "URL(URL={url}, ExpandedURL={eurl})".format(
            url=self.url,
            eurl=self.expanded_url)


class UserStatus(TwitterModel):

    """ A class representing the UserStatus structure. This is an abbreviated
    form of the twitter.User object. """

    connections = {'following': False,
                   'followed_by': False,
                   'following_received': False,
                   'following_requested': False,
                   'blocking': False,
                   'muting': False,
                   }

    def __init__(self, **kwargs):
        self.param_defaults = {
            'blocking': False,
            'followed_by': False,
            'following': False,
            'following_received': False,
            'following_requested': False,
            'id': None,
            'id_str': None,
            'muting': False,
            'name': None,
            'screen_name': None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

        if 'connections' in kwargs:
            for param in self.connections:
                if param in kwargs['connections']:
                    setattr(self, param, True)

    def __repr__(self):
        conns = [param for param in self.connections if getattr(self, param)]
        return "UserStatus(ID={uid}, Name={sn}, Connections=[{conn}])".format(
            uid=self.id,
            sn=self.screen_name,
            conn=", ".join(conns))


class User(TwitterModel):

    """A class representing the User structure. """

    def __init__(self, **kwargs):
        self.param_defaults = {
            'contributors_enabled': None,
            'created_at': None,
            'default_profile': None,
            'default_profile_image': None,
            'description': None,
            'favourites_count': None,
            'followers_count': None,
            'friends_count': None,
            'geo_enabled': None,
            'id': None,
            'lang': None,
            'listed_count': None,
            'location': None,
            'name': None,
            'notifications': None,
            'profile_background_color': None,
            'profile_background_image_url': None,
            'profile_background_tile': None,
            'profile_banner_url': None,
            'profile_image_url': None,
            'profile_link_color': None,
            'profile_sidebar_fill_color': None,
            'profile_text_color': None,
            'protected': None,
            'screen_name': None,
            'status': None,
            'statuses_count': None,
            'time_zone': None,
            'url': None,
            'utc_offset': None,
            'verified': None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "User(ID={uid}, Screenname={sn})".format(
            uid=self.id,
            sn=self.screen_name)


class Status(TwitterModel):
    """A class representing the Status structure used by the twitter API.
    """

    def __init__(self, **kwargs):
        self.param_defaults = {
            'contributors': None,
            'coordinates': None,
            'created_at': None,
            'current_user_retweet': None,
            'favorite_count': None,
            'favorited': None,
            'geo': None,
            'hashtags': None,
            'id': None,
            'id_str': None,
            'in_reply_to_screen_name': None,
            'in_reply_to_status_id': None,
            'in_reply_to_user_id': None,
            'lang': None,
            'location': None,
            'media': None,
            'now': None,
            'place': None,
            'possibly_sensitive': None,
            'retweet_count': None,
            'retweeted': None,
            'retweeted_status': None,
            'scopes': None,
            'source': None,
            'text': None,
            'truncated': None,
            'urls': None,
            'user': None,
            'user_mentions': None,
            'withheld_copyright': None,
            'withheld_in_countries': None,
            'withheld_scope': None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    @property
    def created_at_in_seconds(self):
        """Get the time this status message was posted, in seconds since the epoch.

        Returns:
          The time this status message was posted, in seconds since the epoch.
        """
        return timegm(parsedate(self.created_at))

    @property
    def relative_created_at(self):
        """Get a human readable string representing the posting time

        Returns:
          A human readable string representing the posting time
        """
        fudge = 1.25
        delta = int(self.now) - int(self.created_at_in_seconds)

        if delta < (1 * fudge):
            return 'about a second ago'
        elif delta < (60 * (1 / fudge)):
            return 'about %d seconds ago' % (delta)
        elif delta < (60 * fudge):
            return 'about a minute ago'
        elif delta < (60 * 60 * (1 / fudge)):
            return 'about %d minutes ago' % (delta / 60)
        elif delta < (60 * 60 * fudge) or delta / (60 * 60) == 1:
            return 'about an hour ago'
        elif delta < (60 * 60 * 24 * (1 / fudge)):
            return 'about %d hours ago' % (delta / (60 * 60))
        elif delta < (60 * 60 * 24 * fudge) or delta / (60 * 60 * 24) == 1:
            return 'about a day ago'
        else:
            return 'about %d days ago' % (delta / (60 * 60 * 24))

    @property
    def Now(self):
        """Get the wallclock time for this status message.

        Used to calculate relative_created_at.  Defaults to the time
        the object was instantiated.

        Returns:
          Whatever the status instance believes the current time to be,
          in seconds since the epoch.
        """
        if self._now is None:
            self._now = time.time()
        return self._now

    @Now.setter
    def Now(self, now):
        self._now = now

    def __repr__(self):
        """A string representation of this twitter.Status instance.
      The return value is the ID of status, username and datetime.
      Returns:
        A string representation of this twitter.Status instance with
        the ID of status, username and datetime.
      """
        if self.user:
            representation = "Status(ID=%s, screen_name='%s', created_at='%s')" % \
                             (self.id, self.user.screen_name, self.created_at)
        else:
            representation = "Status(ID=%s,  created_at='%s')" % (self.id, self.created_at)
        return representation

    @staticmethod
    def NewFromJsonDict(data):
        """Create a new instance based on a JSON dict.

        Args:
          data: A JSON dict, as converted from the JSON in the twitter API
        Returns:
          A twitter.Status instance
        """
        if 'user' in data:
            from twitter import User
            user = User.NewFromJsonDict(data['user'])
        else:
            user = None

        if 'retweeted_status' in data:
            retweeted_status = Status.NewFromJsonDict(data['retweeted_status'])
        else:
            retweeted_status = None

        if 'current_user_retweet' in data:
            current_user_retweet = data['current_user_retweet']['id']
        else:
            current_user_retweet = None

        urls = None
        user_mentions = None
        hashtags = None
        media = list()

        if 'entities' in data:
            if 'urls' in data['entities']:
                print(data['entities']['urls'])
                urls = [Url.NewFromJsonDict(u) for u in data['entities']['urls']]
            if 'user_mentions' in data['entities']:
                from twitter import User

                user_mentions = [User.NewFromJsonDict(u) for u in data['entities']['user_mentions']]
            if 'hashtags' in data['entities']:
                hashtags = [Hashtag.NewFromJsonDict(h) for h in data['entities']['hashtags']]
            if 'media' in data['entities']:
                media = [Media.NewFromJsonDict(m) for m in data['entities']['media']]

        # the new extended entities
        if 'extended_entities' in data:
            if 'media' in data['extended_entities']:
                media = [Media.NewFromJsonDict(m) for m in data['extended_entities']['media']]

        return super(Status, Status).NewFromJsonDict(data,
                                                     user=user,
                                                     urls=urls,
                                                     user_mentions=user_mentions,
                                                     hashtags=hashtags,
                                                     media=media)
