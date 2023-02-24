# -*- coding: utf-8 -*-

import os
from eve import Eve
from eve.auth import TokenAuth

from database.models.account import Account
from routes.home import HomeRoute

if 'PORT' in os.environ:
    port = int(os.environ.get('PORT'))
    host = '0.0.0.0'
else:
    port = 5000
    host = '0.0.0.0'


class RolesAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        # use Eve's own db driver; no additional connections/resources are used
        accounts = Account.get_collection()
        lookup = {'token': token}
        if allowed_roles:
            # only retrieve a user if his roles match ``allowed_roles``
            lookup['roles'] = {'$in': allowed_roles}
        account = accounts.find_one(lookup)
        # set 'AUTH_FIELD' value to the account's ObjectId
        # (instead of _Id, you might want to use ID_FIELD)
        if account and '_id' in account:
            self.set_request_auth_value(account['_id'])
            return account
        else:
            return None


app = Eve(auth=RolesAuth)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,if-match')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,PATCH')
    return response


home_requests = HomeRoute(app)

if __name__ == '__main__':
    app.run(host=host, port=port)
