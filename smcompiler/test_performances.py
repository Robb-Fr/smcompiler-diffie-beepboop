"""
Test for measuring performance with pytest-benchmark
"""
import random as rd
import time
from multiprocessing import Process, Queue

import pytest

from expression import Expression, Scalar, Secret
from protocol import ProtocolSpec
from server import run
from smc_party import SMCParty

"""
Use same utility functions from test_integration.py
"""


def parametrized_parties_expr(
    nb_parties: int = 3,
    nb_secret_additions: int = 0,
    nb_scalar_additions: int = 0,
    nb_secret_multiplications: int = 0,
    nb_scalar_multiplications: int = 0,
) -> tuple[dict[str, dict[Secret, int]], Expression]:

    assert nb_parties > 1
    secrets = [Secret() for _ in range(nb_parties)]
    # we make sure our secret values will not make the computation overcome the Share.FIELD_Q value
    parties = {
        "Party_{}".format(i + 1): {sec: 1 if rd.random() < 0.8 else 2}
        for i, sec in enumerate(secrets)
    }
    # print("Created parties: {}".format(parties))

    expr = None

    if nb_secret_additions > 0:
        expr = secrets[0]
        for i in range(nb_secret_additions):
            expr += secrets[(i + 1) % nb_parties]
    elif nb_scalar_additions > 0:
        expr = Scalar(0)
        for i in range(nb_scalar_additions):
            expr += Scalar(i + 1)
    elif nb_secret_multiplications > 0:
        expr = secrets[0]
        for i in range(nb_secret_multiplications):
            expr *= secrets[(i + 1) % nb_parties]
    elif nb_scalar_multiplications > 0:
        expr = Scalar(1)
        for i in range(nb_scalar_multiplications):
            # we make sure our secret values will not make the computation overcome the Share.FIELD_Q value
            # the recursive stack will disallow more than 1000 recursions, in esperance we'll be way below
            expr *= Scalar(1 if rd.random() < 0.99 else 2)

    if expr is None:
        raise ValueError(
            "There must be one value of the nb of operations greater than 0"
        )
    else:
        # print("Computing expression: {}".format(expr))
        return parties, expr


def smc_client(client_id, prot, value_dict, queue):
    cli = SMCParty(
        client_id, "localhost", 5000, protocol_spec=prot, value_dict=value_dict
    )
    res = cli.run()
    queue.put(res)
    print(f"{client_id} has finished!")


def smc_server(args):
    run("localhost", 5000, args)


def create_environement(
    parties: dict[str, dict[Secret, int]], expr: Expression
) -> tuple[Process, list[Process], Queue]:
    participants = list(parties.keys())

    prot = ProtocolSpec(expr=expr, participant_ids=participants)
    clients = [(name, prot, value_dict) for name, value_dict in parties.items()]

    queue = Queue()

    server_proc = Process(target=smc_server, args=(participants,))

    return server_proc, clients, queue


def run_processes(
    clients: list[tuple[str, ProtocolSpec, dict[Secret, int]]], queue: Queue
) -> None:
    """Function to benchmark: runs all the client processes until they all join. WARNING, assumes a running server and does not deal with its termination."""
    clients_proc = [Process(target=smc_client, args=(*args, queue)) for args in clients]

    for client in clients_proc:
        client.start()

    for client in clients_proc:
        client.join()


def start_server_proc(server_proc: Process) -> None:
    server_proc.start()
    time.sleep(3)


def check_results_stop_serv_proc(
    server_proc: Process, queue: Queue, nb_clients: int
) -> None:
    results = [queue.get() for _ in range(nb_clients)]

    server_proc.terminate()
    server_proc.join()

    time.sleep(2)
    print("Server stopped.")

    res_0 = results[0]
    # print("Result: {}".format(res_0))
    assert all([res == res_0 for res in results])


def test_nb_parties_2(benchmark):
    parties, expr = parametrized_parties_expr(nb_parties=2, nb_secret_additions=1)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_parties_4(benchmark):
    parties, expr = parametrized_parties_expr(nb_parties=4, nb_secret_additions=1)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_parties_8(benchmark):
    parties, expr = parametrized_parties_expr(nb_parties=8, nb_secret_additions=1)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_parties_16(benchmark):
    parties, expr = parametrized_parties_expr(nb_parties=16, nb_secret_additions=1)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_parties_32(benchmark):
    parties, expr = parametrized_parties_expr(nb_parties=32, nb_secret_additions=1)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_sec_add_1(benchmark):
    parties, expr = parametrized_parties_expr(nb_secret_additions=1)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_sec_add_4(benchmark):
    parties, expr = parametrized_parties_expr(nb_secret_additions=4)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_sec_add_32(benchmark):
    parties, expr = parametrized_parties_expr(nb_secret_additions=32)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_sec_add_256(benchmark):
    parties, expr = parametrized_parties_expr(nb_secret_additions=256)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_sec_add_512(benchmark):
    parties, expr = parametrized_parties_expr(nb_secret_additions=512)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_scal_add_1(benchmark):
    parties, expr = parametrized_parties_expr(nb_scalar_additions=1)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_scal_add_4(benchmark):
    parties, expr = parametrized_parties_expr(nb_scalar_additions=4)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_scal_add_32(benchmark):
    parties, expr = parametrized_parties_expr(nb_scalar_additions=32)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_scal_add_256(benchmark):
    parties, expr = parametrized_parties_expr(nb_scalar_additions=256)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_scal_add_512(benchmark):
    parties, expr = parametrized_parties_expr(nb_scalar_additions=512)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_sec_mul_1(benchmark):
    parties, expr = parametrized_parties_expr(nb_secret_multiplications=1)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_sec_mul_4(benchmark):
    parties, expr = parametrized_parties_expr(nb_secret_multiplications=4)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_sec_mul_32(benchmark):
    parties, expr = parametrized_parties_expr(nb_secret_multiplications=32)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_sec_mul_256(benchmark):
    parties, expr = parametrized_parties_expr(nb_secret_multiplications=256)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_sec_mul_400(benchmark):
    parties, expr = parametrized_parties_expr(nb_secret_multiplications=400)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_scal_mul_1(benchmark):
    parties, expr = parametrized_parties_expr(nb_scalar_multiplications=1)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_scal_mul_4(benchmark):
    parties, expr = parametrized_parties_expr(nb_scalar_multiplications=4)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_scal_mul_32(benchmark):
    parties, expr = parametrized_parties_expr(nb_scalar_multiplications=32)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_scal_mul_256(benchmark):
    parties, expr = parametrized_parties_expr(nb_scalar_multiplications=256)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))


def test_nb_scal_mul_400(benchmark):
    parties, expr = parametrized_parties_expr(nb_scalar_multiplications=400)
    server_proc, clients, queue = create_environement(parties, expr)
    start_server_proc(server_proc)
    benchmark(run_processes, clients, queue)
    check_results_stop_serv_proc(server_proc, queue, len(clients))
