PYTHON=python3
PIP=pip3
GUNZIP=gunzip
DOCKER=docker

COMMAND=$(PYTHON) src/experiments.py
IMAGE=sspy/simplescalar
OPTIONS=\
	-v $(PWD)/src:/opt/app/src\
	-v $(PWD)/config:/opt/app/config/\
	-v $(PWD)/dist:/opt/app/dist/\
	--rm -ti\

run: configure
	@$(DOCKER) run $(OPTIONS) $(IMAGE) $(COMMAND)

run-docker: configure
	@$(DOCKER) run $(OPTIONS) $(IMAGE) ${ARGS}

configure: simplescalar
	@echo "environment configured successfully.\n"

simplescalar:
	@$(DOCKER) images | grep $(IMAGE) \
		&& echo "Image '$(IMAGE)' has already been built." \
		|| $(DOCKER) build -t $(IMAGE) -f resources/Dockerfile.simplescalar resources

# Add more tasks that may be particular to a local dev environment.
-include resources/Makefile
