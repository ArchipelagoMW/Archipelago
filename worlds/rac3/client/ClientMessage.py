from typing import Optional

from NetUtils import ClientStatus


class ClientMessage:
    cmd: str = None
    key: str = None
    default: str = None
    want_reply: bool = None
    operations: list[dict[str, str]] = None
    status: ClientStatus[int] = None
    locations: list[int] = None

    def __init__(self,
                 cmd,
                 key: Optional[str] = None,
                 default: Optional[str] = None,
                 want_reply: Optional[bool] = False,
                 operations: Optional[list[dict[str, str]]] = None,
                 status: Optional[ClientStatus[int]] = None,
                 locations: Optional[list[int]] = None):
        self.cmd = cmd
        self.key = key
        self.default = default
        self.want_reply = want_reply
        self.operations = operations
        self.status = status
        self.locations = locations

    def output(self) -> dict:
        output = {}
        for attr in dir(self):
            output.update({attr: getattr(self, attr)})
        return output

    @staticmethod
    def set(slot: int, team: int, planet: str) -> dict:
        cmd = 'Set'
        key = f'rac3_current_planet_{slot}_{team}'
        default = f'Galaxy'
        want_reply = False
        operations = [{
            "operation": 'replace',
            "value": planet,
        }]
        return ClientMessage(cmd, key=key, default=default, want_reply=want_reply, operations=operations).output()

    @staticmethod
    def location_checks(locations: list[int]) -> dict:
        cmd = 'LocationChecks'
        return ClientMessage(cmd, locations=locations).output()

    @staticmethod
    def status_update(status: ClientStatus[int]) -> dict:
        cmd = 'StatusUpdate'
        return ClientMessage(cmd, status=status).output()

    @staticmethod
    def location_scouts(locations: list[int]) -> dict:
        cmd = 'LocationScouts'
        return ClientMessage(cmd, locations=locations).output()
