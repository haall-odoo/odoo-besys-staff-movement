

VENV_NAME=".venv"

DB_NAME=TestModule
MODULE_NAME=staff_movements

ODOO_PATH="${HOME}/Desktop/labodoo-img/worktree/src/19.0/odoo"
ENTERPRISE_PATH="${HOME}/Desktop/labodoo-img/worktree/src/19.0/enterprise"
MODULE_PATH="${HOME}/Desktop/odoo-besys-staff-movement"
INTERNAL_PATH=""

PATHS=${ODOO_PATH} ${ENTERPRISE_PATH} ${MODULE_PATH}

all: prerun run

setup_venv:
	@python3 -m venv "./$${VENV_NAME}"
	@. ./.venv/bin/activate
	@for RPATH in $(PATHS); do \
		if [ -f "$${RPATH}/requirements.txt" ]; then \
			echo "Installing requirement for $${RPATH##*/}"; \
			pip install -r "$${RPATH}/requirements.txt"; \
		fi \
	done

prerun:
	@dropdb ${DB_NAME}

run:
	@${ODOO_PATH}/odoo-bin --addons-path="${ENTERPRISE_PATH}, ${ODOO_PATH}/addons, ${MODULE_PATH}" -d ${DB_NAME} -i hr,hr_maintenance -u ${MODULE_NAME}

clean:
	@rm -rf ${MODULE_PATH}/${MODULE_NAME}/*/__pycache__