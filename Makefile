export PYTHONUNBUFFERED := 1
PYTHON=python3.7

.DEFAULT_GOAL := dev.build

.PHONY: virtualenv
virtualenv:
	$PYTHON -m pip  install virtualenv

.PHONY: .venv
.venv:
	virtualenv .venv

.PHONY: activate
activate: .venv
	. .venv/bin/activate

install: .venv
	( \
       . .venv/bin/activate; \
       pip install -r snowplow-tsv-to-json-transformer/requirements.txt; \
    )

.PHONY: run
run:
	AWS_PROFILE=homepage-production sam local invoke SnowplowTsvToJsonFunction -e events/event.json

.PHONY: build.image
build.image:
	AWS_PROFILE=homepage-production sam build

.PHONY: package
package: build.image
	AWS_PROFILE=homepage-production sam package --s3-bucket petersiemen-lambda-artifacts \
 		--s3-prefix snowplow-tsv-to-json-transformer --output-template-file output-template.yaml
