Import database liberary #for SQL_alchamy

class Store(db.model):
    create store table in DB

    id equals db.schema(intiger, primary key)
    name equals db.schema(string, must be uniqe)
    items equals db.schema(string, forign key equals items.id from items table)

    def __init__(self):
        self.self=self

    def render_jason(self):
        return (all item data in json format)

    Class method():
    def find_by_name(class, name):
        return json of all data

    
