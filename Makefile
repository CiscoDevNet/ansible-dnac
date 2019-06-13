.PHONY: all install uninstall build-role install-role remove-role help

all: install

install: ## Install this collection to the Ansble users path
	@ansible-playbook installer/install.yaml

uninstall: ## Uninstall this collection form the Ansible users path
	@ansible-playbook installer/uninstall.yaml

build-role: ## Build an Ansible role for the plugins
	@ansible-playbook installer/build.yaml

install-role: ## Install the Ansible role
	@cd build; ansible-galaxy install ciscodevnet.dnac

remove-role: ## Remove the Ansible role 
	@ansible-galaxy remove ciscodevnet.dnac
	
help: ## Display this help screen
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
