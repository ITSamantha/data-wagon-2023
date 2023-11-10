from datetime import datetime


class Destination:
    def __init__(
            self,
            wag_id: int,
            oper_date: datetime,
            disl_st_id: int,
            dest_st_id: int,
            train_id: int,
            id: int,
            form_st_id: int,
            target_st_id: int
    ):
        self.target_st_id = target_st_id
        self.form_st_id = form_st_id
        self.id = id
        self.train_id = train_id
        self.dest_st_id = dest_st_id
        self.disl_st_id = disl_st_id
        self.oper_date = oper_date
        self.wag_id = wag_id
