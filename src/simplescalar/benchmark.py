import subprocess
from os import path as ospath

def run_benchmark(args):
    info, env = args
    config, bench = info
    sim_cmd, input, output = env

    infile = None
    outfile = subprocess.PIPE

    if input is not None:
        infile = open(input, "r")
    if output is not None:
        outfile = open(output, "w")

    print("Running %-20s\t%s" % (config + "/" + bench, " ".join(sim_cmd)))
    proc = subprocess.Popen(
        sim_cmd,

        universal_newlines=True,

        # Allow redirection for sim programs
        stdin=infile,
        stdout=outfile,

        # sim-outorder outputs to STDERR
        stderr=subprocess.PIPE
    )

    if input is not None:
        infile.close()
    if output is not None:
        outfile.close()

    result = proc.communicate()
    output=result[1]

    return (info, str(output))

class Benchmark:
    def __init__(self, path, command, args=[], input=None, output=None):
        executable = ospath.join(path, command)

        if type(args) is not list:
            raise ValueError("Benchmark args must be a list")
        if not ospath.exists(executable):
            raise FileNotFoundError("Could not find benchmark executable at '%s'" % executable)
        if input is not None and not ospath.exists(input):
            raise FileNotFoundError("Could not find benchmark input file at '%s'" % input)

        self.executable = executable
        self.args = args
        self.input = input
        self.output = output

    def configure(self, simulator, config):
        command = [simulator]

        for name, value in config.options:
            command.append(name)
            command.append(value)

        command.append(self.executable)
        command.extend(self.args)

        return (command, self.input, self.output)
