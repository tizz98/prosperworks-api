from request import Request


class Api(object):
    def __init__(self, key, email):
        self.key = key
        self.email = email
        self.requests = Request(self.key, self.email)

    def get_company(self, id):
        from models import Company
        comp = Company(id)
        comp.populate(self)
        return comp

    def get_account(self):
        from models import Account
        acc = Account()
        acc.populate(self)
        return acc
