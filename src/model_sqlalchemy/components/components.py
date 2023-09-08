"""
C R U D   f u n c t i o n s
"""
from src.model_sqlalchemy.model import Fishing, Fish, Fisherman, Water


INITIAL_FISHING_LIST = ['Vis', 'Visser', 'Water']
INITIAL_SPECIES_LIST = ['Karper', 'Voorn', 'Snoek']
INITIAL_WATER_LIST = ['Beatrixkanaal', 'Philips visvijver', 'Klotputten']
INITIAL_FISHERMAN_LIST = [['Petri', 'Heil'], ['Pietje', 'Puk'], ['Evil', '<script>alert(1)</script>']]


class Components:
    def __init__(self, db):
        self._db = db

    def init_db(self):
        self._db.create_all()
        # Populate
        [self.chk_ins_fishing( name=pk ) for pk in INITIAL_FISHING_LIST]
        [self.chk_ins_fish( species=pk ) for pk in INITIAL_SPECIES_LIST]
        [self.chk_ins_fisherman( firstname=pk[0], lastname=pk[1] ) for pk in INITIAL_FISHERMAN_LIST]
        [self.chk_ins_water( name=pk ) for pk in INITIAL_WATER_LIST]
        self._db.session.commit()

    def get_first(self, obj, id):
        return self._db.session.query(obj).filter_by( id=id ).first()

    def chk_ins_fishing(self, **kwargs):
        exists = self._db.session.query(Fishing).filter_by( **kwargs ).first()
        if not exists:
            self._db.session.add( Fishing( **kwargs ) )

    def chk_ins_fish(self, **kwargs):
        exists = self._db.session.query(Fish).filter_by( **kwargs ).first()
        if not exists:
            self._db.session.add( Fish( **kwargs ) )

    def chk_ins_fisherman(self, **kwargs):
        exists = self._db.session.query(Fisherman).filter_by( **kwargs ).first()
        if not exists:
            self._db.session.add( Fisherman( **kwargs ) )

    def chk_ins_water(self, **kwargs):
        exists = self._db.session.query(Water).filter_by( **kwargs ).first()
        if not exists:
            self._db.session.add( Water( **kwargs ) )

    def updert_fish(self, fish):
        exists = self._db.session.query(Fish).filter_by( species=fish.species ).first()
        if not exists:
            self._db.session.add( fish )
        else:
            exists.species = fish.species
            exists.variety = fish.variety
            exists.length = fish.length
            exists.pounds = fish.pounds
            exists.note = fish.note
        self._db.session.commit()

    def updert_fisherman(self, fish):
        exists = self._db.session.query(Fisherman).filter_by( firstname=fish.firstname, lastname=fish.lastname ).first()
        if not exists:
            self._db.session.add( fish )
        else:
            exists.firstname = fish.firstname
            exists.lastname = fish.lastname
            exists.note = fish.note
        self._db.session.commit()

    def updert_water(self, water):
        exists = self._db.session.query(Water).filter_by( name=water.name ).first()
        if not exists:
            self._db.session.add( water )
        else:
            exists.name = water.name
            exists.note = water.note
        self._db.session.commit()

    def reset_database(self):
        self._db.drop_all()
        self.init_db()

    def _clear_table(self, table):
        for row in self._db.session.query( table ):
            self._db.session.delete( row )
        self._db.session.commit()
