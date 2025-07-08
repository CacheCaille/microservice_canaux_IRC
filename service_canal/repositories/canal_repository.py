from app.models.canal import Canal

class canal_repository:
    @staticmethod
    def get_canals():
        """
        Retrieve all channels.
        """
        return Canal.query.all()


