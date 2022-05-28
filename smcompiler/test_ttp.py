"""
Unit tests for the trusted parameter generator.
Testing ttp is not obligatory.

MODIFY THIS FILE.
"""

from ttp import TrustedParamGenerator, BeaverTriplet
from secret_sharing import Share


def test_nump():
    ttp = TrustedParamGenerator()
    assert ttp.num_participants == 0

    ttp.add_participant('0')
    assert ttp.num_participants == 1 

    ttp.add_participant('1')
    assert ttp.num_participants == 2

    ttp.add_participant('2')
    assert ttp.num_participants == 3


def test_participants():
    ttp = TrustedParamGenerator()

    ttp.add_participant('0')
    ttp.add_participant('1')
    ttp.add_participant('2')
    ttp.add_participant('2')
    ttp.add_participant('3')

    assert ttp.participant_ids == {'0','1','2','3'}

def test_beaver():
    triplet = BeaverTriplet(3)

    assert triplet.a * triplet.b == triplet.c 
    assert Share(triplet.a) * Share(triplet.b) == Share(triplet.c)

    a_1, b_1, c_1 = triplet.get_shares(0)
    a_2, b_2, c_2 = triplet.get_shares(1)
    a_3, b_3, c_3 = triplet.get_shares(2)

    assert a_1 + a_2 + a_3 == Share(triplet.a)
    assert b_1 + b_2 + b_3 == Share(triplet.b)
    assert c_1 + c_2 + c_3 == Share(triplet.c)


def test_retrieveshare():
    ttp = TrustedParamGenerator()

    ttp.add_participant('0')
    ttp.add_participant('1')
    ttp.add_participant('2')

    assert ttp.client_id_dict == {'0':0, '1':1, '2':2}

    s0_0 = ttp.retrieve_share('0', 'add0')
    s0_0_again = ttp.retrieve_share('0', 'add0')

    assert s0_0 == s0_0_again 

    s0_1 = ttp.retrieve_share('1', 'add0')
    s0_2 = ttp.retrieve_share('2', 'add0')

    assert (s0_0[0] + s0_1[0] + s0_2[0]) * (s0_0[1] + s0_1[1] + s0_2[1]) == (s0_0[2] + s0_1[2] + s0_2[2])

    s1_0 = ttp.retrieve_share('0', 'mul1')

    assert s0_0 != s1_0 




