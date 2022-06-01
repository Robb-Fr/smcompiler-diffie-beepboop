#!/bin/bash
pytest -k "parties" -v --benchmark-save="parties_1core_x86_64" --benchmark-histogram="parties_1core_x86_64" --benchmark-min-rounds=25
pytest -k "sec_add" -v --benchmark-save="sec_add_1core_x86_64" --benchmark-histogram="sec_add_1core_x86_64" --benchmark-min-rounds=25
pytest -k "scal_add" -v --benchmark-save="scal_add_1core_x86_64" --benchmark-histogram="scal_add_1core_x86_64" --benchmark-min-rounds=25
pytest -k "sec_mul" -v --benchmark-save="sec_mul_1core_x86_64" --benchmark-histogram="sec_mul_1core_x86_64" --benchmark-min-rounds=25
pytest -k "scal_mul" -v --benchmark-save="scal_mul_1core_x86_64" --benchmark-histogram="scal_mul_1core_x86_64" --benchmark-min-rounds=25
