from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

from src.Const import EMPTY

base = declarative_base()


class Base(base):

    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class Fishing( base ):
    __tablename__ = 'fishing'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column( String( 50 ) )

    def __init__(self, name):
        self.name = name

    def toDict(self, id=0):
        return {
            'id': id,
            'name': self.name
        }


class Fish( base ):
    __tablename__ = 'fish'
    id = Column(Integer, primary_key=True, autoincrement=True)
    species = Column( String( 50 ) )
    variety = Column( String( 50 ) )
    length = Column( Float( precision=3 ) )
    pounds = Column( Float( precision=3 ) )
    note = Column( String( 256 ) )

    # Alphabetical order
    def __init__(self, species=EMPTY, variety=EMPTY, length=0.0, pounds=0.0, note=EMPTY):
        self.species = species
        self.variety = variety
        self.lenght = length
        self.pounds = pounds
        self.note = note

    def toDict(self, id=0):
        return {
            'id': id,
            'species': self.species,
            'variety': self.variety,
            'length': self.length,
            'pounds': self.pounds,
            'note': self.note,
        }


class Fisherman( base ):
    __tablename__ = 'fisherman'
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column( String( 50 ) )
    lastname = Column( String( 50 ) )
    note = Column( String( 256 ) )

    # Alphabetical order
    def __init__(self, firstname=EMPTY, lastname=EMPTY, note=EMPTY):
        self.firstname = firstname
        self.lastname = lastname
        self.note = note

    def toDict(self, id=0):
        return {
            'id': id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'note': self.note,
        }


class Water( base ):
    __tablename__ = 'water'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column( String( 50 ) )
    type = Column( String( 20 ) )
    note = Column( String( 256 ) )

    # Alphabetical order
    def __init__(self, name=EMPTY, type=EMPTY, note=EMPTY):
        self.name = name or EMPTY
        self.type = type or EMPTY
        self.note = note or EMPTY

    def toDict(self, id=0):
        return {
            'id': id,
            'name': self.name,
            'type': self.type,
            'note': self.note,
        }

