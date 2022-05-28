"""
Test for our Custom Application of the SMCompiler - Balélec
"""

import time
from multiprocessing import Process, Queue

import pytest

from expression import Scalar, Secret
from protocol import ProtocolSpec
from server import run

from smc_party import SMCParty

"""
Use same utility functions from test_integration.py
"""

def smc_client(client_id, prot, value_dict, queue):
    cli = SMCParty(
        client_id,
        "localhost",
        5000,
        protocol_spec=prot,
        value_dict=value_dict
    )
    res = cli.run()
    queue.put(res)
    print(f"{client_id} has finished!")


def smc_server(args):
    run("localhost", 5000, args)


def run_processes(server_args, *client_args):
    queue = Queue()

    server = Process(target=smc_server, args=(server_args,))
    clients = [Process(target=smc_client, args=(*args, queue)) for args in client_args]

    server.start()
    time.sleep(3)
    for client in clients:
        client.start()

    results = list()
    for client in clients:
        client.join()

    for client in clients:
        results.append(queue.get())

    server.terminate()
    server.join()

    # To "ensure" the workers are dead.
    time.sleep(2)

    print("Server stopped.")

    return results

def suite(parties, expr, expected):
    participants = list(parties.keys())

    prot = ProtocolSpec(expr=expr, participant_ids=participants)
    clients = [(name, prot, value_dict) for name, value_dict in parties.items()]

    results = run_processes(participants, *clients)

    for result in results:
        assert result == expected


"""
Custom Application: Balélec Negotiations 

Three parties, the CLIC Bar, the Balélec committee and a drink wholesaler, are trying to estimate the conditions under which they could be profitable during this edition of Balélec. 
The CLIC Bar estimates n_drinks, the number of drinks they believe they will sell during the festival. 
The Balélec committee estimates festival_price, the price at which they would like drinks to be sold during the festival. 
The drink wholesaler estimates base_price, the price at which it would like to sell its drinks to the festival for resale. 
They would like to each obtain an estimation of how much profit they will make, given the value they have estimated. Since this is a negotiation, they do not which to reveal their estimations to the other parties but wish to determine if their aggregated estimations work well together. 

A few precisions: 
- The CLIC Bar agreeed to give two free drinks to Martin Vetterli 
- They want to compute this overall profit over the next 10 years 

The final value is therefore : P = ((n_drinks - 2) * (festival_price - base_price)) * 10

"""

def test_balelec():
    n_drinks = Secret()
    festival_price = Secret()
    base_price = Secret()

    n_free_drinks = 2
    n_years = 10 

    parties = {
        "CLIC": {n_drinks: 3000},
        "Balelec": {festival_price: 8},
        "Wholesaler": {base_price: 4},
    }

    expr = ( ( n_drinks - Scalar(n_free_drinks)) * (festival_price - base_price) ) * Scalar(n_years)
    expected = ((3000-2) * (8-4)) * 10 
    suite(parties, expr, expected)