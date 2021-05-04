# simplescalar-py

A simple, Work-in-progress library for working with [SimpleScalar](http://www.simplescalar.com/) in Python. This tool was developed with the sole intention of making my use cases more convenient. I have no affiliation with the project.

## NOTICE!!!

This code is not fit for human consumption. The environment is still hard-coded for my use cases in many ways, so until work has been done to make this library more user-friendly, it'll be a pain to use. I plan to improve upon it when I find the time, and it may be maintained in the future.

## TODO

Everything.

My early priorities include cleaning up the docker setup/dev environment, defining the scope and basic featureset of the library going forward, and working toward making this a project people can actually use if anyone wants to use it.


## Setup

Until the dev environment has been cleaned up, you'll need to source your own `resources/simplescalar.tar.gz` and `resources/ss-benchmark.tar.gz`. SimpleScalar isn't fun to install, so this is a high priority.

Once you have those, the makefile should build the docker image and use it to run simulations. The image is huge, by the way.

## Usage

In lieu of documentation, I've provided some example usage code in `example/simulations.py`. See `src/simplescalar/results.py` for information on how to extract statistics after running a simulation.
