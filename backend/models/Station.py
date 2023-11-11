class Station:
    def __init__(
            self,
            st_id: int,
            latitude: float,
            longitude: float
    ):
        self.st_id = st_id
        self.latitude = latitude
        self.longitude = longitude

    def __eq__(self, other):
        return self.st_id == other
