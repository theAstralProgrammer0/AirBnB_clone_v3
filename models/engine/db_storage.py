#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

str2class = {
            "Amenity": Amenity, 
            "City": City,
            "Place": Place,
            "Review": Review,
            "State": State,
            "User": User
         }


class DBStorage:
    """interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """retrieve all objs on current database session"""
        new_dict = {}

        # iterate over str2class
        for clss in str2class:
            # validate cls arg as part of classes
            if cls is None or cls is str2class[clss] or cls is clss:
                objs = self.__session.query(str2class[clss]).all()
                # iterate over objs returned to populate new_dict
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the obj to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create a database session"""
        Base.metadata.create_all(self.__engine) # create tables based on models

        # create a configured "session factory" that will generate 
        # new Session objects when called
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)

        # provide thread-safe session management, 
        # creating a registry of session objects for different threads.
        Session = scoped_session(sess_factory)

        # hands over a Session object to DBStorage __session
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """retrieve an object based on its class and id"""
        if cls is None or id is None:
            return None
        elif type(cls) is str and cls in str2class and isinstance(id, str):
            obj = self.__session.query(str2class[cls]).filter_by(id=id).first()
        elif cls in str2class.values() and isinstance(id, str):
            obj = self.__session.query(cls).filter_by(id=id).first()
        return obj

    def count(self, cls=None):
        """count objects based on class or all objects"""
        count = 0
        if cls is None:
            for clss in str2class: 
                count += self.__session.query(str2class[clss]).count()
        elif type(cls) is str and cls in str2class:
            count += self.__session.query(str2class[cls]).count()
        elif cls in str2class.values():
            count += self.__session.query(cls).count()

        return count
