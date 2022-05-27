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
        num_participants = len(self.protocol_spec.participant_ids)
        for secret in self.value_dict.keys():
            secret_val = self.value_dict[secret]
            shares = share_secret(secret_val, num_participants)
            for index, id in enumerate(self.protocol_spec.participant_ids):
                if id == self.client_id:
                    self.my_shares[secret] = shares[index]
                else:
                    serialized_share = pickle.dumps(shares[index])
                    self.comm.send_private_message(
                        id, str(secret.id.__hash__()), serialized_share
                    )
        self.comm.publish_message(self.client_id + "_sent", "Done")

    def retrieve_share(self, secret: Secret) -> Share:
        if secret in self.my_shares:
            return self.my_shares[secret]
        else:
            share = pickle.loads(
                self.comm.retrieve_private_message(str(secret.id.__hash__()))
            )
            self.my_shares[secret] = share
            return share

    # Suggestion: To process expressions, make use of the *visitor pattern* like so:
    def process_expression(self, expr: Expression) -> Share:
        if isinstance(expr, Scalar):
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
                a, b, c = self.comm.retrieve_beaver_triplet_shares(expr.id)
                a = Share(a)
                b = Share(b)
                c = Share(c)
                x_a = x_share - a
                y_b = y_share - b
                z = c + (x * y_b) + (y * x_a) - (x_a * y_b)
                return z
        else:
            raise TypeError("Unrecognized type of operation")
        # elif isinstance(expr, SubOp):
        #     if has_scalar_operand == 0 or self.is_aggregating_client():
        #         return x - y
        #     else:
        #         if has_scalar_operand == 3:
        #             return Share(0)
        #         elif has_scalar_operand == 2:
        #             return x_share
        #         elif has_scalar_operand == 1:
        #             return y_share
        #         else:
        #             raise ValueError("Unkown value of the scalar_operand method")

        # elif isinstance(expr, MultOp):
        #     x, y = expr.get_operands()
        #     x = self.process_expression(x)
        #     y = self.process_expression(y)
        #     a, b, c = self.comm.retrieve_beaver_triplet_shares(expr.id)
        #     a = Share(a)
        #     b = Share(b)
        #     c = Share(c)

        #     if (
        #         isinstance(x, Share) and isinstance(y, Share)
        #     ) or self.is_aggregating_client():
        #         # x_a = self.process_expression(SubOp(x,a))
        #         # y_b = self.process_expression(SubOp(y,b))

        #         # z_expr = AddOp(c, AddOp(MulOp(x,y_b), SubOp(MulOp(y,x_a),MulOp(x_a,y_b))))

        #         # z = self.process_expression(z_expr)

        #         x_a = x - a
        #         y_b = y - b
        #         z = c + (x * y_b) + (y * x_a) - (x_a * y_b)

        #     else:
        #         return x * y

        #
        # Call specialized methods for each expression type, and have these specialized
        # methods in turn call `process_expression` on their sub-expressions to process
        # further.

    # Feel free to add as many methods as you want.
