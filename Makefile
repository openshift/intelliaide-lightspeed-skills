ORG ?= openshift-lightspeed
IMAGE ?= quay.io/$(ORG)/intelliaide-skills
TAG ?= latest

.PHONY: build push vendor clean

build:
	podman build -f Containerfile -t $(IMAGE):$(TAG) .

push: build
	podman push $(IMAGE):$(TAG)

vendor:
	mkdir -p intelliaide/vendor/
	podman run --rm --user root \
	  -v $$(pwd)/intelliaide:/intelliaide:Z \
	  registry.redhat.io/rhel9/python-312:latest \
	  pip3.12 install --no-cache-dir --target /intelliaide/vendor/ \
	    -r /intelliaide/requirements.txt

clean:
	rm -rf intelliaide/__pycache__ intelliaide/**/__pycache__
