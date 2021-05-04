from os import path as ospath

from simplescalar.client import Client
from simplescalar.benchmark import Benchmark, run_benchmark
from simplescalar.configuration import Configuration
from simplescalar.results import Results
from multiprocessing import Pool


class SimpleScalar:
    def __init__(self, sqlite_db=None):
        self.client = Client(
            # Not really in scope for the time being. A project of this scale
            # is probably fast enough
            # to get away with not caching results.
            sqlite_options={
                "enabled": sqlite_db is not None,
                "filename": sqlite_db
            }
        )

    def add_benchmark(self, name, path, command, args=[], input=None, output=None, tags=[]):
        if not ospath.exists(path):
            raise FileNotFoundError("Could not find benchmark path '%s'", path)

        benchmark = Benchmark(path, command, args, input, output)
        self.client.define_benchmark(name, benchmark, tags)

    def add_configuration(self, name, inherits_from=None, properties=None, file=None, machine=None, output_fields=[]):
        config = Configuration([("-config", file)])
        filter = output_fields
        self.client.define_configuration(name, machine, config, filter)


    def run_benchmarks(self):
        configs = self.client.list_configurations()
        benchmarks = self.client.list_benchmarks()
        results = Results(configs, benchmarks)

        sims = self.client.generate_simulations()
        pool = Pool(len(sims))

        print("Starting simulation processing")

        map_proc = pool.map_async(run_benchmark, sims)
        map_proc.wait()

        print("Finished simulation processing")

        for info, output in map_proc.get():
            results.update(*info, output)

        return results.compute()
