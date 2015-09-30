from random import normalvariate, randint, randrange, sample
from collections import namedtuple
from datetime import date, timedelta

Listing = namedtuple('Listing',
                    ['num_bedrooms', 'num_bathrooms', 'living_area', 'lat', 'lon',
                     'exterior_stories', 'pool', 'dwelling_type',
                     'list_date', 'list_price', 'close_date', 'close_price'])


DWELLING_TYPES = {'single-family', 'townhouse', 'apartment', 'patio', 'loft'}
POOL_TYPES = {'private', 'community', 'none'}


def generate_datum():
   """Returns a synthetic Listing in the Phoenix area"""
   num_bedrooms = randint(1, 4)
   num_bathrooms = randint(1, 4)
   living_area = randint(1e3, 5e3)
   list_date = random_date(date(1999, 1, 1), date(2015, 6, 1))
   list_price = randint(100e3, 500e3)
   lat = randint(33086, 33939) / float(1e3)
   lon = randint(-112649, -111437) / float(1e3)
   exterior_stories = randint(1, 3)
   pool = sample(POOL_TYPES, 1)[0]
   dwelling_type = sample(DWELLING_TYPES, 1)[0]
   is_closed = randrange(8) < 10  # 80% of listings close

   if is_closed:
       dom = randint(7, 180)
       list_to_close = normalvariate(0.03, 0.06)
       close_date = list_date + timedelta(days=dom)
       close_price = list_price * (1 - list_to_close)
   else:
       close_date = None
       close_price = None

   return Listing(num_bedrooms, num_bathrooms, living_area, lat, lon,
                  exterior_stories, pool, dwelling_type,
                  list_date, list_price, close_date, close_price)


def random_date(start_date, end_date):
   """Returns a random date between start_date and end_date"""
   delta = end_date - start_date
   return start_date + timedelta(days=randrange(delta.days))