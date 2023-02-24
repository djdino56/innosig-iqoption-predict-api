import hashlib
from database.models.account import Account


def create_account(account: dict):
    _bot = Account(**account)
    _bot.save()


def main():
    account = {
        "name": "WP Access System",
        "token": hashlib.md5("WP Access System".encode('utf-8')).hexdigest(),
        "roles": ["user"]
    }
    create_account(account)


if __name__ == '__main__':
    main()
