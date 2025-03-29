from dataclasses import dataclass


@dataclass
class OperationStatus:
    status: str
    message: str

    def as_dict(self):
        return {"status": self.status, "message": self.message}
