from databases import Database


class BaseRepository:
    """ any other repository must inherit this class to have access to db """

    def __init__(self, db: Database) -> None:
        self._db = db

    @property
    def db(self) -> Database:
        return self._db
