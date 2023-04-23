
from dataclasses import dataclass


@dataclass
class SocketIdentity:

    identifier: str
    index: int
    name: str

    def get_from_sockets(self, socket_collection, ignore_identifier=False, ignore_index=False, ignore_name=False):
        socket = None

        if not ignore_identifier and self.identifier:
            socket = socket_collection[self.identifier]

        if not ignore_name and not socket and self.name:
            for s in socket_collection:
                if s.name == self.name:
                    socket = s
                    break

        if not ignore_index and not socket and 0 <= self.index < len(socket_collection):
            socket = socket_collection[self.index]

        return socket
