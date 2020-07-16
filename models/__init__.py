from collections.abc import MutableMapping
from datetime import datetime, date
# from time import sleep

# import pymysql
import config
from datetime import datetime
from copy import deepcopy
from database import pool

class Field:
    """
    A holder for the value inside a model instance. Allows some restriction
    options and defaults to the data contained within.

    typeof     : Make sure data coming in can be of this type
    default    : Set this default value if nothing is supplied
    fmt        : Date format, only used with datetime types
    hidden     : Hide this field from API enpoints, will be skipped when dict(model) is called
    modifiable : If False will raise and exception if this field is modified
    """
    def __init__(self,
                 typeof=str,
                 value=None,
                 default=None,
                 fmt="%Y-%m-%d",
                 hidden=False,
                 modifiable=True):
        self.modifiable = modifiable
        self.type = typeof
        self.hidden = hidden
        self.value = value or default
        self.fmt = fmt


    """
    Display field name and vlaue when printed.
    """
    def __repr__(self):
        return "<{0}:{1}>".format(self.type.__name__, self.value)

    """
    Return value that is safe for SQL insert.
    """
    def deserialize(self):

        # if self.type == datetime and self.value:
        #     return self.value.strftime(self.fmt)

        if self.type == list and self.value:
            return ",".join(self.value)

        return self.value

    """
    Serialise a database item into a python object
    """
    def serialize(self, value):
        if self.type == list and value:
            self.value = value.split(",")
        else:
            self.value = value

class Model(object):
    """
    Base Model class, all other Models will inherit from this
    """

    """PyMySQL database connection, config.py for settings"""
    db = None
    pool = pool

    """Every model should override this with the correct table name"""
    table_name = None

    """
    Create a new instance of Model class

    Can take a dictionary or keyword args to fill the internal fields

    eg:
        model = Model({"name" : "test"})
            or
        model = Model(name="test")

    Inheriting models should have class level attributes of class Field,
    this fills the self.fields attribute on an instance.

    All external calls to this class hang on the self.fields attr being
    populated.

    A call to self.get(username="test") can also fill the fields attr on
    an empty instance.
    """
    def __init__(self, _data={}, **kwargs):
        data = _data or kwargs
        self.fields = {}
        self.before_init(data)
        for k, v in self.__class__.__dict__.items():
            if isinstance(v, Field):
                self.fields[k] = deepcopy(v)
                if k in data.keys():
                    self.fields[k].serialize(data[k])


    """
    Override for __getattribute__ to allow dot accessor eg. model.username

    AttributeError will be thrown when a key is in the instance field attribute
    keys list. This will then call __getattr__(key) and allow the above mentioned
    dot operator
    """
    def __getattribute__(self, name):
        if name in ["__class__", "fields"]:
            return super(Model, self).__getattribute__(name)
        if name in self.fields:
            raise AttributeError
        return super(Model, self).__getattribute__(name)


    """
    Override for __getattr__ will be called if __getattribute throws an AttributeError
    """
    def __getattr__(self, key):
        if key in self.fields:
            return self.fields[key].value
        raise AttributeError("Field not present {}".format(key))


    """
    Override dictionary style getters 'model["username"]' to always
    lookup the value in self.fields
    """
    def __getitem__(self, key):
        if key in self.fields.keys():
            return self.fields[key].deserialize()
        else:
            return self.__dict__[key]


    """
    Override dictionary style setters 'model["username"] = "test"'

    Calls self.__setattr__ for convenience.
    """
    def __setitem__(self, key, val):
        self.__setattr__(key, val)


    """
    Override for dot notation setters 'model.username = "test"'

    This method will edit the Field objects value contained in self.fields

    @Exception raised if the Field is not modifiable
    @AttributeError raised if key is not found
    """
    def __setattr__(self, key, val):
        if key is "fields":
            super(Model, self).__setattr__(key, val)
        else:
            if key in self.fields:
                if self.fields[key].modifiable:
                    self.fields[key].value = val
                else:
                    raise Exception("Cannot modify field '{}'".format(key))
            else:
                raise AttributeError("Field {0} does not exist in Model {1}".format(key, self.__class__.__name__))

    def append_field(self, key, value):
        self.fields[key] = value 
        #print(self.fields)


    """
    TODO: Allow the deletion of Field.value using del()

    Not really needed for now
    """
    def __delitem__(self):
        pass

    """
    Display model name and id when printed
    """
    def __repr__(self):
        return "<Model:{0} '{1}'>".format(self.__class__.__name__, self.id)

    """
    Override length method will return the number of fields in this instance
    """
    def __len__(self):
        return len(self.fields)

    """
    Allow this object to be typed into a dictionary using 'dict(model)'

    This is used when JSON encoding a model: 'See helpers/json_encoder.py'
    """
    def __iter__(self):
        for k, v in self.fields.items():
            if not v.hidden:
                yield (k, v.value)

    """
    Hook to modify data before it is populated into 'self.fields'

    Useful to hash and set a password for a user.
    """
    def before_init(self, data=None):
        pass


    """
    Perform a check or function before a model is saved
    """
    def before_save(self, *args, **kwargs):
        pass


    """
    Save this model to the database, REPLACE INTO is used to avoid having multiple
    database calls. Will insert if the row does not exist or update if it does.
    """
    def save(self):
        try:
            self.before_save()
        except Exception as e:
            print("Pre-Save for model", self.table_name, "has failed", str(e))
            raise        

        connection = self.pool.get_conn()

        columns = []
        values = []

        for name, field in self.fields.items():
            if name == "id" and not field.value:
                continue
            columns.append(name)
            try:
                values.append(field.deserialize())
            except TypeError as e:
                raise TypeError("Field {0} is not of type {1}".format(name, field.type.__name__))

        query = """
            REPLACE INTO {0}
                ({1})
            VALUES
                ({2})
        """.format(self.table_name, ", ".join(columns), ", ".join(["%s"] * len(values)))

        # print(query)
        # print(values)

        with connection.cursor() as c:
            c.execute(query, tuple(values))
            connection.commit()

        self.pool.release(connection)


    """
    Update fields on instance, using dictionary style setters will go through __setattr__
    which will update the fields in self.fields

    A model.save() will need to be done after updating to save to the database
    """
    def update(self, _dict={}, **kwargs):
        data = _dict or kwargs

        if data:
            for k, v in data.items():
                #print(f"updating {k} to {v}")
                self[k] = v
        else:
            raise Exception("Nothing to update")

    """
    Delete the record from the database, will only run when an 'id' is present.

    @Exception raised when an id is not present.
    """
    def delete(self):
        connection = self.pool.get_conn()
        if self.id:
            with connection.cursor() as c:
                c.execute("""
                    DELETE FROM {0} WHERE id='{1}'
                """.format(self.table_name, self.id))
                connection.commit()
            self.pool.release(connection)
        else:
            self.pool.release(connection)
            raise Exception("User not in database")
        


    """
    Get a model from the database, using a single keyword argument as a filter.

    Class method allows you to use without instantiation eg.

        model = Model.get(username="test")

    Returns a populated user instance on success and False if the row count was 0

    """
    @classmethod
    def get(cls, **kwargs):
        temp = cls()
        connection = cls().pool.get_conn()

        if len(kwargs) > 1:
    
            keys = kwargs.keys()
            where = " and ".join(["{0} = %s".format(x) for x in keys])
            with connection.cursor() as c:
                query = """SELECT {0} FROM {1} WHERE {2}""".format(", ".join(temp.fields.keys()), cls.table_name, where)
                # with connection.cursor() as c:
                c.execute(query, [kwargs[x] for x in keys])
                data = c.fetchone()
        else:
            key = next(iter(kwargs))
            val = kwargs[key]


            with connection.cursor() as c:
                c.execute("""
                    SELECT
                        {fields}
                    FROM
                        {table}
                    WHERE   {cond}=%s""".format(
                            fields = ", ".join(temp.fields.keys()),
                            table = cls.table_name,
                            cond = key), (val,))

                data = c.fetchone()

        temp.pool.release(connection)
        return cls(data) if data else False

    @classmethod
    def get_many(cls, **kwargs):
        temp = cls()
        connection = temp.pool.get_conn()

        key = next(iter(kwargs))
        val = kwargs[key]

        results = []

        with connection.cursor() as c:

            c.execute("""
                SELECT
                    {fields}
                FROM
                    {table}
                WHERE   {cond}=%s""".format(
                        fields = ", ".join(temp.fields.keys()),
                        table = cls.table_name,
                        cond = key), (val,))

            data = c.fetchall()

            for item in data:
                results.append(cls(item))

        temp.pool.release(connection)
        return results

    def dump_fields(self):
        for key, value in self.fields.items():
            print(key, "=", value)
