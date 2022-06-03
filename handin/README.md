# SMCompiler Tom & Manon

## Running tests
As described in the handout, tests are run by pytest:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest test_integration.py
```
We also implemented subtests in all test files.

## Running benchmarks
We made scripts `run_benchmark_` for running creating the benchmarks files with correct names for both our processor architectures.
```bash
# for 8cores arm64
./run_benchmark_tom.sh
```