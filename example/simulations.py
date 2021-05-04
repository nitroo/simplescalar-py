
from simplescalar import SimpleScalar

def main():
    ss = setup_environment()
    configure_simulations(ss)
    results = ss.run_benchmarks()

    print(results)

def configure_simulations(ss):
    ss.add_configuration("baseline",
        file="config/baseline.cfg",
        machine={"clock_rate":  1/(100 * 10**(-12)) },
        output_fields=["sim_IPC"]
    )

    ss.add_configuration("final",
        file="config/final.cfg",
        machine={"clock_rate": 1/(120 * 10**(-12))  },
        output_fields=["sim_IPC"]
    )


def setup_environment():
    import sys

    try:
        ss = SimpleScalar()

        ss.add_benchmark("mcf",
            path="/usr/share/simplescalar/ss-benchmark/mcf",
            command="mcf_base.i386-m32-gcc42-nn",
            args=["/usr/share/simplescalar/ss-benchmark/mcf/inp.in"],
            tags=["int"]
        )

        ss.add_benchmark("hmmer",
            path="/usr/share/simplescalar/ss-benchmark/hmmer",
            command="hmmer_base.i386-m32-gcc42-nn",
            args=["/usr/share/simplescalar/ss-benchmark/hmmer/bombesin.hmm"],
            tags=["int"]
        )

        ss.add_benchmark("milc",
            path="/usr/share/simplescalar/ss-benchmark/milc",
            command="milc_base.i386-m32-gcc42-nn",
            input="/usr/share/simplescalar/ss-benchmark/milc/su3imp.in",
            tags=["float"]
        )

        ss.add_benchmark("bzip2",
            path="/usr/share/simplescalar/ss-benchmark/bzip2",
            command="bzip2_base.i386-m32-gcc42-nn",
            args=["/usr/share/simplescalar/ss-benchmark/bzip2/dryer.jpg"],
            tags=["int"]
        )

        ss.add_benchmark("sjeng",
            path="/usr/share/simplescalar/ss-benchmark/sjeng",
            command="sjeng_base.i386-m32-gcc42-nn",
            args=["/usr/share/simplescalar/ss-benchmark/sjeng/text.txt"],
            tags=["int"]
        )

        ss.add_benchmark("equake",
            path="/usr/share/simplescalar/ss-benchmark/equake",
            command="equake_base.pisa_little",
            input="/usr/share/simplescalar/ss-benchmark/equake/inp.in",
            output="/usr/share/simplescalar/ss-benchmark/equake/inp.out",
            tags=["float"]
        )

        return ss
    except Exception as err:
        raise err
        print("Setup failed: %s" % str(err))
        sys.exit(1)

main()