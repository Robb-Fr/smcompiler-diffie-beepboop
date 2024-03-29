"""
Implementation of an SMC client.

MODIFY THIS FILE.
"""
# You might want to import more classes if needed.

import pickle
from typing import Dict, Set, Tuple, Union

from communication import Communication
from expression import AddOp, Expression, MultOp, Op, Scalar, Secret, SubOp
from protocol import ProtocolSpec
from secret_sharing import Share, reconstruct_secret, share_secret

# Feel free to add as many imports as you want.


class SMCParty:
    """
    A client that executes an SMC protocol to collectively compute a value of an expression together
    with other clients.

    Attributes:
        client_id: Identifier of this client
        server_host: hostname of the server
        server_port: port of the server
        protocol_spec (ProtocolSpec): Protocol specification
        value_dict (dict): Dictionary assigning values to secrets belonging to this client.
        my_shares (Dict[Secret, Share]): dictionnary associating this client's share for the given secrets
        b_triple (Dict[Expression, Tuple[int, int, int]]): the retrieved shares for the seen expressions
    """

    def __init__(
        self,
        client_id: str,
        server_host: str,
        server_port: int,
        protocol_spec: ProtocolSpec,
        value_dict: Dict[Secret, int],
    ):
        self.comm = Communication(server_host, server_port, client_id)

        self.client_id = client_id
        self.protocol_spec = protocol_spec
        self.value_dict = value_dict
        self.my_shares = {}
        self.b_triplet = {}

    def is_aggregating_client(self):
        """
        We specify the aggregating client as the first participant
        """
        return self.protocol_spec.participant_ids[0] == self.client_id

    def run(self) -> int:
        """
        The method the client use to do the SMC.
        """
        self.send_secret_shares()
        for id in self.protocol_spec.participant_ids:
            if id != self.client_id:
                # we wait for every party to have sent their share
                self.comm.retrieve_public_message(id, id + "_sent")
        my_final_share = self.process_expression(self.protocol_spec.expr)
        self.comm.publish_message(
            "final_share_" + self.client_id, pickle.dumps(my_final_share)
        )
        all_final_shares = [my_final_share]
        for id in self.protocol_spec.participant_ids:
            if id != self.client_id:
                all_final_shares.append(
                    pickle.loads(
                        self.comm.retrieve_public_message(id, "final_share_" + id)
                    )
                )
        return reconstruct_secret(all_final_shares)

    def send_secret_shares(self) -> None:
        """Method to create and send shares for each secret owned by this client to all of the other parties of the protocol"""
        num_participants = len(self.protocol_spec.participant_ids)
        for secret in self.value_dict.keys():
            secret_val = self.value_dict[secret]
            shares = share_secret(secret_val, num_participants)
            for index, id in enumerate(self.protocol_spec.participant_ids):
                if id == self.client_id:
                    # we store our local share
                    self.my_shares[secret] = shares[index]
                else:
                    serialized_share = pickle.dumps(shares[index])
                    self.comm.send_private_message(
                        id, str(secret.id.__hash__()), serialized_share
                    )
        # we inform others we finished sending our shares
        self.comm.publish_message(self.client_id + "_sent", "Done")

    def retrieve_share(self, secret: Secret) -> Share:
        """Manages the share retrieving associated to a secret. Maintains locally the already retrieved shares and queries the server otherwise."""
        if secret in self.my_shares:
            return self.my_shares[secret]
        else:
            share = pickle.loads(
                self.comm.retrieve_private_message(str(secret.id.__hash__()))
            )
            self.my_shares[secret] = share
            return share

    def retrieve_biever_triplet(self, expr: Expression) -> Tuple[int, int, int]:
        """Manages the beaver triplet retrieving associated to an expression. Maintains locally the already retrieved triplet and queries the server otherwise."""
        if expr in self.b_triplet:
            return self.b_triplet[expr]
        else:
            triplet = self.comm.retrieve_beaver_triplet_shares(expr.id)
            self.b_triplet[expr] = triplet
            return triplet

    # Suggestion: To process expressions, make use of the *visitor pattern* like so:
    def process_expression(self, expr: Expression) -> Share:
        if isinstance(expr, Scalar):
            # returns as share so it can be combined with overriden operations with other shares
            return Share(expr.value)

        if isinstance(expr, Secret):
            return self.retrieve_share(expr)

        assert isinstance(expr, Op)
        x, y = expr.get_operands()
        x_share = self.process_expression(x)
        y_share = self.process_expression(y)
        has_scalar_operand = expr.scalar_operand()
        if isinstance(expr, AddOp) or isinstance(expr, SubOp):
            if has_scalar_operand == 0 or self.is_aggregating_client():
                # we do not have constant to add/sub or we can because we're aggregators
                if isinstance(expr, AddOp):
                    return x_share + y_share
                if isinstance(expr, SubOp):
                    return x_share - y_share
            else:
                if has_scalar_operand == 3:
                    # both operands are scalar, nothing to add to secret sharing if not aggregating
                    return Share(0)
                elif has_scalar_operand == 2:
                    # right operand only is scalar, send my left share
                    return x_share
                elif has_scalar_operand == 1:
                    # left operand only is scalar, send my right share
                    return y_share
                else:
                    raise ValueError("Unkown value of the scalar_operand method")
        elif isinstance(expr, MultOp):
            if has_scalar_operand > 0:
                # one or more are scalar operands, we are in multiplication by constant
                return x_share * y_share
            else:
                a, b, c = self.retrieve_biever_triplet(expr)
                a = Share(a)
                b = Share(b)
                c = Share(c)
                x_a = x_share - a
                y_b = y_share - b
                self.comm.publish_message(
                    "beaver:x_a" + str(expr.id.__hash__()), pickle.dumps(x_a)
                )
                self.comm.publish_message(
                    "beaver:y_b" + str(expr.id.__hash__()), pickle.dumps(y_b)
                )
                for client in self.protocol_spec.participant_ids:
                    # performs beaver triplet product with notations similar to the one in the slides
                    if client != self.client_id:
                        x_a = x_a + pickle.loads(
                            self.comm.retrieve_public_message(
                                client, "beaver:x_a" + str(expr.id.__hash__())
                            )
                        )
                        y_b = y_b + pickle.loads(
                            self.comm.retrieve_public_message(
                                client, "beaver:y_b" + str(expr.id.__hash__())
                            )
                        )
                z = c + (x_share * y_b) + (y_share * x_a)
                if self.is_aggregating_client():
                    z = z - (x_a * y_b)
                return z
        else:
            raise TypeError("Unrecognized type of operation")

        # Call specialized methods for each expression type, and have these specialized
        # methods in turn call `process_expression` on their sub-expressions to process
        # further.
