class TagProcessor:

    def __init__(self, database):
        self.database = database

    def process(self, uid):

        symbol = self.database.get_symbol(uid)

        return symbol