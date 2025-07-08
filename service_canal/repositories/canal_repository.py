from models.canal import Canal

def get_canals():
    """
    Retrieve all channels.
    """
    return Canal.query.all()


