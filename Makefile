.PHONY: all install uninstall help

all: install

install: ## Install this collection to the Ansble users path
	@ansible-playbook installer/install.yaml

uninstall: ## Uninstall this collection form the Ansible users path
	@ansible-playbook installer/uninstall.yaml

help: ## Display this help screen
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

