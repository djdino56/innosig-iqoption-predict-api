import os
import logging
import sys
import urllib.parse

# MONGO SETTINGS #######################
MONGO_HOST = os.environ.get('DB_HOST', '185.48.117.65')
MONGO_USERNAME = os.environ.get('DB_USERNAME', 'innosig_user')
MONGO_PASSWORD = os.environ.get('DB_PASSWORD', '9Aat3ZjF3wuvWkGCzzQNeXRG7GxqT6D2bnf2oc2rvuV4ZKxqz3')
# MONGO_HOST = os.environ.get('DB_HOST', 'hspaymentcs0.au4jt.mongodb.net')
# MONGO_USERNAME = os.environ.get('DB_USERNAME', 'hubble_solution_payment_user')
# MONGO_PASSWORD = os.environ.get('DB_PASSWORD', '68RF7jlGsKeNJidI')
MONGO_DBNAME = os.environ.get('DB_NAME', 'innosig-iqoption-predict')
MONGO_AUTH_SOURCE = "admin"

# MONGO_URI = "mongodb+srv://{username}:{password}@{host}/{dbname}?authSource=admin&retryWrites=true&w=majority".format(
#     username=urllib.parse.quote_plus(MONGO_USERNAME),
#     password=urllib.parse.quote_plus(MONGO_PASSWORD),
#     host=MONGO_HOST,
#     dbname=MONGO_DBNAME)

MONGO_URI = "mongodb://{username}:{password}@{host}/{dbname}?authSource=admin&retryWrites=true&w=majority".format(
    username=urllib.parse.quote_plus(MONGO_USERNAME),
    password=urllib.parse.quote_plus(MONGO_PASSWORD),
    host=MONGO_HOST,
    dbname=MONGO_DBNAME)

# IQOPTION SETTINGS #######################
IQ_OPTION_EMAIL = 'dino.spong@hubblesolutions.nl'
IQ_OPTION_PASSWORD = 'fgq3kxu6exq7ACD*muf'
IQ_OPTION_MODE = 'PRACTICE'
ALLOWED_INSTRUMENT_TYPES = {
    'EURUSD': 'forex',
    'SPY': 'cfd'
}

# APP SETTINGS #######################
DEFAULT_TIME_PERIOD = 120


# LOGGING SETTINGS #######################
root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

# EVE SETTINGS #######################
PAGINATION_LIMIT = 50000

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST']

MONGO_QUERY_BLACKLIST = ['$where']

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

RENDERERS = [
    'eve.render.JSONRenderer',
    # 'eve.render.XMLRenderer'
]

# We enable standard client cache directives for all resources exposed by the
# API. We can always override these global settings later.
CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

# Our API will expose the following resources (MongoDB collections).
# In order to allow for proper data validation, we define behaviour
# and structure.
accounts = {
    # the standard account entry point is defined as
    # '/accounts/<ObjectId>'. We define  an additional read-only entry
    # point accessible at '/accounts/<username>'.
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'username',
    },

    # We also disable endpoint caching as we don't want client apps to
    # cache account data.
    'cache_control': '',
    'cache_expires': 0,

    # Only allow superusers and admins.
    'allowed_roles': ['superuser', 'admin'],

    # Allow 'token' to be returned with POST responses
    'extra_response_fields': ['token'],

    'public_methods': ['POST'],
    'public_item_methods': ['POST'],

    # Finally, let's add the schema definition for this endpoint.
    'schema': {
        'email': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'username': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'password': {
            'type': 'string',
            'required': True,
        },
        'roles': {
            'type': 'list',
            'allowed': ['user', 'superuser', 'admin'],
            'required': False,
        },
        'token': {
            'type': 'string',
            'required': False,
        }
    },
}
candles = {
    # 'title' tag used in item links.
    'item_title': 'candles',
    'schema': {
        '_id': {
            'type': 'string',
            'required': True,
        },
        'market': {
            'type': 'string',
            'required': True,
        },
        'interval': {
            'type': 'string',
            'required': True,
        },
        'date': {
            'type': 'float',
            'required': True,
        },
        'trend': {
            'type': 'float',
            'required': True,
        },
        'yhat_lower': {
            'type': 'float',
            'required': True,
        },
        'yhat_upper': {
            'type': 'float',
            'required': True,
        },
        'trend_lower': {
            'type': 'float',
            'required': True,
        },
        'trend_upper': {
            'type': 'float',
            'required': True,
        },
        'multiplicative_terms': {
            'type': 'float',
            'required': True,
        },
        'multiplicative_terms_lower': {
            'type': 'float',
            'required': True,
        },
        'multiplicative_terms_upper': {
            'type': 'float',
            'required': True,
        },
        'additive_terms': {
            'type': 'float',
            'required': True,
        },
        'additive_terms_lower': {
            'type': 'float',
            'required': True,
        },
        'additive_terms_upper': {
            'type': 'float',
            'required': True,
        },
        'yhat': {
            'type': 'float',
            'required': True,
        }
    }
}

markets = {
    # 'title' tag used in item links.
    'item_title': 'markets',
    'schema': {
        '_id': {
            'type': 'string',
            'required': True,
        },
        'market': {
            'type': 'string',
            'required': True,
        },
        'interval': {
            'type': 'string',
            'required': True,
        }
    }
}

# The DOMAIN dict explains which resources will be available and how they will
# be accessible to the API consumer.
DOMAIN = {
    "accounts": accounts,
    "candles": candles,
    "markets": markets,
}
