from typing import Optional, List


class GGbanObject:
    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: {self.__dict__}>"

    def __repr__(self) -> str:
        return self.__str__()


class CommentField(GGbanObject):
    number: int
    date: str
    status: str
    message: str

    def __init__(self, number: int, date: str, status: str, message: str):
        self.number = number
        self.date = date
        self.status = status
        self.message = message


class BanQuery(GGbanObject):
    ban: bool
    ban_reason: str

    def __init__(self, ban: bool, ban_reason: Optional[str] = None):
        self.ban = ban
        if self.ban:
            self.ban_reason = ban_reason
        else:
            self.ban_reason = None


class ReportQuery(GGbanObject):
    origin_id: Optional[int]
    "Author user ID"
    reported_id: int
    "Reported user ID"
    date: str
    "Datetime"
    status: str
    "Ban status"
    comment: List[CommentField]
    "List of comments"

    def __init__(
        self,
        reported_id: int,
        date: str,
        status: str,
        comment: List[CommentField],
        origin_id: Optional[int] = None,
    ):
        self.origin_id = origin_id
        self.reported_id = reported_id
        self.date = date
        self.status = status
        self.comment = [CommentField(**comment) for comment in comment]
