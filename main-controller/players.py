import uuid
from datetime import datetime, timedelta


class Players(object):
    """Prevents and manages multiple users to one control point."""
    def __init__(self):
        super(Players, self).__init__()
        self._players = {}

    def add_player(self, joint, player):
        self._players[joint] = player

    def get_players(self):
        return (self._players)

    def garbage_collector(self):
        """ Removes inactive users. """
        cleaned_dict = {}
        for controller_ID in self._players:
            # Remove by time expiry
            if datetime.now() < self._players[controller_ID]._expiry:
                cleaned_dict[controller_ID] = self._players[controller_ID]
            else:
                pass
            # Remove by duplicate IP
            # Implement this to ensure no player is on two control points
        self._players = cleaned_dict
        print("Garbage collected.")


class Player(object):
    """Manages the data for a player."""
    def __init__(self, ip):
        super(Player, self).__init__()
        self._update_constant = 1
        self._ip = ip
        self._cookie = self.random_cookie()
        self._expiry = datetime.now() + timedelta(seconds=self._update_constant)

    def random_cookie(self):
        """Generates a random string to be used as a cookie."""
        return (uuid.uuid4())

    def update_expiry(self):
        """ Updates the expiry cookie to allow the user to
        control the joint for an additional time specified by
        Player._update_constant. in seconds."""
        self._expiry = datetime.now() + timedelta(seconds=self._update_constant)
