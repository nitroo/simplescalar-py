import re

class Results:
    def __init__(self, configs=[], benchmarks=[]):
        self.ready = False
        self.stats = {}
        self.machines = {}
        self.filters = {}
        self.tags = {}
        self.benchmarks = [b[0] for b in benchmarks]
        self.configs = [c[0] for c in configs]

        for bench, tags in benchmarks:
            self.tags[bench] = tags

        # name/function computation pairs stored here
        self._handlers = {}

        for config, machine, fields in configs:
            self.stats[config] = {}
            self.machines[config] = machine
            self.filters[config] = fields

            for bench in self.benchmarks:
                self.stats[config][bench] = {}

    def update(self, config, bench, output):
        stats = self.process_output(output)
        self.add_stats(config, bench, stats)

    def compute(self):
        return self

    def each_pair(self):
        return [(c, b) for c in self.configs for b in self.benchmarks]

    # Retrieve data for a benchmark, limited by filters.
    def get_benchmark_stats(self, config, bench, filtered=True):
        if config not in self.stats:
            raise KeyError("Cannot find configuration '%s'" % config)

        values = []
        stats = self.stats[config]
        filters = self.get_filters(config)

        for field in filters:
            value = self.get_stat_value(config, bench, field)
            values.append(value)

        return values

    def get_config_stats(self, config):
        if config not in self.stats:
            raise KeyError("Cannot find configuration '%s'" % config)

        return self.stats[config]

    # Retrieve a list of values for all benchmarks under a particular configuration.
    def get_stat_column(self, config, field):
        if config not in self.stats:
            raise KeyError("Cannot find configuration '%s'" % config)
        values = []
        stats = self.stats[config]
        for bench in stats.keys():
            if field not in stats[bench]:
                raise KeyError("Cannot find '%s' for '%s/%s'" % (field, config, bench))

            values.append(stats[bench][field])

        return values

    # Retrieve data for a benchmark, limited by filters.
    def get_stat_value(self, config, bench, field):
        if config not in self.stats:
            raise KeyError("Cannot find configuration '%s'" % config)
        elif bench not in self.stats[config]:
            raise KeyError("Cannot find benchmark '%s' for configuration '%s'" % (bench, config))

        stats = self.stats[config]
        if field not in stats[bench]:
            raise KeyError("Cannot find '%s' for '%s/%s'" % (field, config, bench))

        return stats[bench][field]

    def get_filters(self, config):
        if config not in self.filters:
            raise KeyError("Cannot find configuration '%s'" % config)

        return self.filters[config]

    def get_machine_info(self, config, field):
        if config not in self.machines or field not in self.machines[config]:
            raise KeyError("Cannot get machine info '%s' for '%s'" % (field, config))

        return self.machines[config][field]

    def get_tagged_benchmarks(self, tag):
        found = []
        for bench in self.benchmarks:
            if tag in self.tags[bench]:
                found.append(bench)
        return found

    def process_output(self, output):
        STAT_BEGIN = r"sim: \*\* simulation statistics \*\*\n"
        STAT_FIELD = r"([\w\.]+)\s*([\w\.]+) #.*"

        match = re.search(STAT_BEGIN, output)
        if match is None:
            raise ValueError("Could not process simulation output")

        start = match.span()[1]
        stats = output[start:]

        fields = {}
        for m in re.finditer(STAT_FIELD, stats):
            name, value = m[1], m[2]
            fields[name] = value

        return fields

    def add_stats(self, config, bench, stats):
        try:
            self.stats[config][bench] = stats
        except KeyError:
            raise KeyError("Expecte %s/%s in results" % (config, bench))
