ORG ?= openshift-lightspeed
IMAGE ?= quay.io/$(ORG)/intelliaide-skills
TAG ?= latest
CONTAINER_ENGINE ?= podman

.PHONY: build push vendor clean

build:
	$(CONTAINER_ENGINE) build -f Containerfile -t $(IMAGE):$(TAG) .

push: build
	$(CONTAINER_ENGINE) push $(IMAGE):$(TAG)

vendor:
	mkdir -p intelliaide/vendor/
	$(CONTAINER_ENGINE) run --rm \
	  -v $$(pwd)/intelliaide:/intelliaide:Z \
	  registry.redhat.io/rhel9/python-312:latest \
	  pip3.12 install --no-cache-dir --target /intelliaide/vendor/ \
	    -r /intelliaide/requirements.txt

clean:
	rm -rf intelliaide/__pycache__ intelliaide/**/__pycache__
