from modelmorph.db.domain import DBRepository, QueryAnswere


class AzureDBRepository(DBRepository):
    def __init__(self):
        pass

    def _connect_db(self) -> None:
        pass

    def execute_query(self, query: str) -> QueryAnswere:
        pass