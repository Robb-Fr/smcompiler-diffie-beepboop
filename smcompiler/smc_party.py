"""
Implementation of an SMC client.

MODIFY THIS FILE.
"""
# You might want to import more classes if needed.

import collections
import json
import pickle
from typing import (
    Dict,
    Set,
    Tuple,
    Union
)

from communication import Communication
from expression import (
    Expression,
    Scalar,
    Secret,
    AddOp,
    MultOp,
    SubOp
)
from protocol import ProtocolSpec
from secret_sharing import(
    reconstruct_secret,
    share_secret,
    Share,
)

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
    """

    def __init__(
            self,
            client_id: str,
            server_host: str,
            server_port: int,
            protocol_spec: ProtocolSpec,
            value_dict: Dict[Secret, int]
        ):
        self.comm = Communication(server_host, server_port, client_id)

        self.client_id = client_id
        self.protocol_spec = protocol_spec
        self.value_dict = value_dict
        self.my_shares = {}

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
        
        self.process_expression(self.protocol_spec.expr)
        raise NotImplementedError("You need to implement this method.")

    def send_secret_shares(self):
        num_participants = len(self.protocol_spec.participant_ids)
        for key in self.value_dict.keys():
            secret_val = self.value_dict[key]
            shares = share_secret(secret_val, num_participants)
            for id in self.protocol_spec.participant_ids:
                if id == self.client_id:
                    self.my_shares[key.id] = shares[id]
                else:
                    serialized_share = pickle.dumps(shares[id])
                    self.comm.send_private_message(id, str(key.id.__hash__()), serialized_share)


    # Suggestion: To process expressions, make use of the *visitor pattern* like so:
    def process_expression(
            self,
            expr: Expression
        ) -> Share:
        if isinstance(expr, AddOp):
            x,y = expr.get_operands()
            x = self.process_expression(x)
            y = self.process_expression(y)
            if (isinstance(x, Share) and isinstance(y, Share)) or self.is_aggregating_client():
                return x + y
            else:
                if isinstance(x,Share):
                    return x
                else:
                    return y

        elif isinstance(expr, SubOp):
            x,y = expr.get_operands()
            x = self.process_expression(x)
            y = self.process_expression(y)
            if (isinstance(x, Share) and isinstance(y, Share)) or self.is_aggregating_client():
                return x - y
            else:
                if isinstance(x,Share):
                    return x
                else:
                    return y

        elif isinstance(expr, MulOp):
            x,y = expr.get_operands()
            x = self.process_expression(x)
            y = self.process_expression(y)
            a,b,c = self.comm.retrieve_beaver_triplet_shares(expr.id)
            a = Share(a)
            b = Share(b)
            c = Share(c)

            if (isinstance(x, Share) and isinstance(y, Share)) or self.is_aggregating_client():
                # x_a = self.process_expression(SubOp(x,a))
                # y_b = self.process_expression(SubOp(y,b))

                # z_expr = AddOp(c, AddOp(MulOp(x,y_b), SubOp(MulOp(y,x_a),MulOp(x_a,y_b))))

                # z = self.process_expression(z_expr)

                x_a = x - a
                y_b = y - b 
                z = c + (x * y_b) + (y * x_a) - (x_a * y_b)

            else:
                return x * y

        elif isinstance(expr, Secret):
            if self.value_dict(expr) is not None: 
                return Share(self.value_dict(expr))
            else:
                raise RuntimeError("Expr is/contains an empty secret")

            # figure out what to do with secret: split into shares? 

        elif isinstance(expr, Scalar):
            return Share(expr.value)

        else:
            raise RuntimeError("Expr of unknown type (expected AddOp, SubOp, MulOp, Secret or Scalar")
        #
        # Call specialized methods for each expression type, and have these specialized
        # methods in turn call `process_expression` on their sub-expressions to process
        # further.
        pass

    # Feel free to add as many methods as you want.