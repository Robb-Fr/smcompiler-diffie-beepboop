"""
Trusted parameters generator.

MODIFY THIS FILE.
"""

import random as rd
import math

import collections
from typing import (
    Dict,
    Set,
    Tuple,
)

from communication import Communication
from secret_sharing import(
    share_secret,
    Share,
)

# Feel free to add as many imports as you want.


class TrustedParamGenerator:
    """
    A trusted third party that generates random values for the Beaver triplet multiplication scheme.
    """

    def __init__(self):
        self.participant_ids: Set[str] = set()
        self.num_participants = len(self.participant_ids)

        self.operation_triplets = {}

        self.client_id_dict = {}

        for id, i in zip(self.participant_ids, range(0, self.num_participants)):
            self.client_id_dict[id] = i 


    def add_participant(self, participant_id: str) -> None:
        """
        Add a participant.
        """
        self.participant_ids.add(participant_id)
        self.num_participants += 1
        self.client_id_dict[participant_id] = self.num_participants

    def retrieve_share(self, client_id: str, op_id: str) -> Tuple[Share, Share, Share]:
        """
        Retrieve a triplet of shares for a given client_id.
        """
        int_id = self.client_id_dict[client_id]

        if op_id not in self.operation_triplets:
            self.operation_triplets[op_id] = BeaverTriplet(self.num_participants)

        beaver_triplet = self.operation_triplets[op_id]
        return beaver_triplet.get_shares(int_id)

    # Feel free to add as many methods as you want.

class BeaverTriplet:
    def __init__(self, num_participants):
        self.a, self.b = rd.sample(range(0, int(math.floor(math.sqrt(Share.FIELD_Q)))), 2)
        self.c = self.a * self.b

        self.a_shares = share_secret(self.a, num_participants)
        self.b_shares = share_secret(self.b, num_participants)
        self.c_shares = share_secret(self.c, num_participants)

    def get_shares(self, client_id: int) -> Tuple[Share, Share, Share]:
        return self.a_shares[client_id-1], self.b_shares[client_id-1], self.a_shares[client_id-1]