from os import path
import subprocess

class Client:
    def __init__(self, sqlite_options=None):
        self.benchmarks = {}
        self.configurations = {}
        self.tags = {}

    def list_configurations(self):
        configs = []
        for name, data in self.configurations.items():
            machine, file, filter = data
            configs.append((name, machine, filter))

        return configs

    def list_benchmarks(self):
        benchmarks = []
        for name, bench in self.benchmarks.items():
            benchmarks.append((name, self.tags[name]))
        return benchmarks

    def generate_simulations(self, simulator="sim-outorder"):
        sims = []
        for config_name, data in self.configurations.items():
            machine, config_file, fields = data
            for bench_name, bench in self.benchmarks.items():
                info = (config_name, bench_name)
                env = bench.configure(simulator, config_file)
                sims.append((info, env))

        return sims

    def define_benchmark(self, name, benchmark, tags):
        self.benchmarks[name] = benchmark
        self.tags[name] = tags

    def define_configuration(self, name, machine, config_file, filter):
        # All fields will be saved, but only fields in fields will be shown.
        self.configurations[name] = (machine, config_file, filter)
