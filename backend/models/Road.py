class Road:
    def __init__(
            self,
            start_id: int,
            end_id: int,
            len: int,
            id: int
    ):
        self.start_id = start_id
        self.end_id = end_id
        self.len = len
        self.id = id

    def __str__(self):
        return 'Road: {0}, {1}, {2}, {3}'.format(self.start_id, self.end_id, self.len, self.id)
