class FoodTruck(object):
    def __init__(self, applicant=None, objectid=None, latitude=None,
                 longitude=None, fooditems=None, dayshours=None,
                 website=None, twitter=None, yelp=None, rank=None,
                 location=None, schedule_dict=None, location_desc=None,
                 past_week_twitter_favs=None, is_sponsor=None):
        self._applicant = applicant
        self._objectid = objectid
        self._latitude = latitude
        self._longitude = longitude
        self._fooditems = fooditems
        self._dayshours = dayshours
        self._website = website
        self._twitter = twitter
        self._yelp = yelp
        self._rank = rank
        self._schedule_dict = schedule_dict
        self._location_desc = location_desc
        self._location = location
        self._past_week_twitter_favs = past_week_twitter_favs
        self._is_sponsor = is_sponsor

    def __repr__(self):
        return "applicant:{applicant}, objectid:{objectid}, " \
               "latitude:{latitude}, longitude:{longitude}, " \
               "fooditems:{fooditems}, dayshours:{dayshours}, " \
               "website:{website}, twitter:{twitter}, yelp:{yelp}, " \
               "rank:{rank}, schedule_dict:{schedule_dict}, " \
               "location_desc:{location_desc}, location:{location}, " \
               "past_week_twitter_favs:{past_week_twitter_favs}, " \
               "is_sponsor:{is_sponsor}".format(
                    applicant=str(self._applicant),
                    objectid=str(self._objectid),
                    latitude=str(self._latitude),
                    longitude=str(self._longitude),
                    fooditems=str(self._fooditems),
                    dayshours=str(self._dayshours),
                    website=str(self._website),
                    twitter=str(self._twitter),
                    yelp=str(self._yelp),
                    rank=str(self._rank),
                    schedule_dict=str(self._schedule_dict),
                    location_desc=str(self._location_desc),
                    location=str(self._location),
                    past_week_twitter_favs=str(self._past_week_twitter_favs),
                    is_sponsor=str(self._is_sponsor)
                )

    def __str__(self):
        return self.__repr__()

    @property
    def applicant(self):
        return self._applicant

    @applicant.setter
    def applicant(self, value):
        # if not isinstance(value, str):
        #     raise ValueError('applicant must be an string!')
        self._applicant = value

    @property
    def objectid(self):
        return self._objectid

    @objectid.setter
    def objectid(self, value):
        # if not isinstance(value, str):
        #     raise ValueError('objectid must be an string!')
        self._objectid = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        # if not isinstance(value, float):
        #     raise ValueError('latitude must be an float!')
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        # if not isinstance(value, float):
        #     raise ValueError('longitude must be an float!')
        self._longitude = value

    @property
    def fooditems(self):
        return self._fooditems

    @fooditems.setter
    def fooditems(self, value):
        self._fooditems = value

    @property
    def dayshours(self):
        return self._dayshours

    @dayshours.setter
    def dayshours(self, value):
        self._dayshours = value

    @property
    def website(self):
        return self._website

    @website.setter
    def website(self, value):
        self._website = value

    @property
    def twitter(self):
        return self._twitter

    @twitter.setter
    def twitter(self, value):
        self._twitter = value

    @property
    def yelp(self):
        return self._yelp

    @yelp.setter
    def yelp(self, value):
        self._yelp = value

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value):
        self._rank = value

    @property
    def schedule_dict(self):
        return self._schedule_dict

    @schedule_dict.setter
    def schedule_dict(self, value):
        self._schedule_dict = value

    @property
    def location_desc(self):
        return self._location_desc

    @location_desc.setter
    def location_desc(self, value):
        self._location_desc = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def past_week_twitter_favs(self):
        return self._past_week_twitter_favs

    @past_week_twitter_favs.setter
    def past_week_twitter_favs(self, value):
        self._past_week_twitter_favs = value

    @property
    def is_sponsor(self):
        return self._is_sponsor

    @is_sponsor.setter
    def is_sponsor(self, value):
        self._is_sponsor = value
