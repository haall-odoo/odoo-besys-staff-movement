

VENV_NAME=".venv"

DB_NAME=TestModule
MODULE_NAME=staff_movements

ODOO_PATH="${HOME}/Desktop/labodoo-img/worktree/src/19.0/odoo"
ENTERPRISE_PATH="${HOME}/Desktop/labodoo-img/worktree/src/19.0/enterprise"
MODULE_PATH="${HOME}/Desktop/odoo-besys-staff-movement"
INTERNAL_PATH=""

PATHS=${ODOO_PATH} ${ENTERPRISE_PATH} ${MODULE_PATH}

all: reset_db run

setup_venv:
	@python3 -m venv "./$${VENV_NAME}"
	@. ./.venv/bin/activate
	@for RPATH in $(PATHS); do \
		if [ -f "$${RPATH}/requirements.txt" ]; then \
			echo "Installing requirement for $${RPATH##*/}"; \
			pip install -r "$${RPATH}/requirements.txt"; \
		fi \
	done

reset_db:
	@${ODOO_PATH}/odoo-bin db drop ${DB_NAME}

run:
	@${ODOO_PATH}/odoo-bin server --addons-path="${ODOO_PATH}/addons,${ENTERPRISE_PATH},${MODULE_PATH}" -d ${DB_NAME} -i ${MODULE_NAME} -u ${MODULE_NAME} --dev xml,reload --with-demo

clean:
	@rm -rf ${MODULE_PATH}/${MODULE_NAME}/*__pycache__