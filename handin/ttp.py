"""
Trusted parameters generator.

MODIFY THIS FILE.
"""

import random as rd
import math

from typing import (
    Dict,
    Set,
    Tuple,
)

from communication import Communication
from secret_sharing import (
    share_secret,
    Share,
)


class BeaverTriplet:
    """Class holding the 3 values and their associated shares for a BeaverTriplet in FIELD_Q"""

    def __init__(self, num_participants):
        self.a, self.b = rd.sample(
            range(0, int(math.floor(math.sqrt(Share.FIELD_Q)))), 2
        )
        self.c = self.a * self.b

        self.a_shares = share_secret(self.a, num_participants)
        self.b_shares = share_secret(self.b, num_participants)
        self.c_shares = share_secret(self.c, num_participants)

    def get_shares(self, client_id: int) -> Tuple[Share, Share, Share]:
        return (
            self.a_shares[client_id],
            self.b_shares[client_id],
            self.c_shares[client_id],
        )


class TrustedParamGenerator:
    """
    A trusted third party that generates random values for the Beaver triplet multiplication scheme.
    """

    def __init__(self):
        self.participant_ids: Set[str] = set()
        self.num_participants = len(self.participant_ids)
        # stores the triplets associated to each operation
        self.operation_triplets = {}
        # map a string client to an int client id
        self.client_id_dict = {}

    def add_participant(self, participant_id: str) -> None:
        """
        Add a participant.
        """
        self.participant_ids.add(participant_id)
        self.num_participants += 1
        self.client_id_dict[participant_id] = self.num_participants - 1

    def retrieve_share(self, client_id: str, op_id: str) -> Tuple[Share, Share, Share]:
        """
        Retrieve a triplet of shares for a given client_id.
        """
        int_id = self.client_id_dict[client_id]

        if op_id not in self.operation_triplets:
            # we need a new beaver triplet for this operation
            self.operation_triplets[op_id] = BeaverTriplet(self.num_participants)

        beaver_triplet = self.operation_triplets[op_id]
        return beaver_triplet.get_shares(int_id)
