##
# Lint and type-check
##

.PHONY: python-lint
python-lint:
	# Check syntax and style
	ruff check
	ruff format --check --diff

.PHONY: python-lintfix
python-lintfix:
	# Automatically fix syntax and style
	ruff check --fix-only
	ruff format

.PHONY: lint
lint:
	docker-compose exec node npm run lint

.PHONY: lintfix
lintfix:
	docker-compose exec node npm run lintfix

.PHONY: type-check
type-check:
	docker-compose exec node npm run type-check

##
# Migration and Django tests
##

.PHONY: migrationtest
migrationtest:
	# Check if there are any model changes without migrations
	./manage.py makemigrations --dry-run --no-input --check --settings tests.test_settings

.PHONY: unittests
unittests:
	# Run unit tests with coverage
	coverage run runtests.py

.PHONY: coveragetest
coveragetest: unittests
	# Generate coverage report and require minimum coverage
	coverage report

.PHONY: coverage
coverage: unittests
	# Generate test coverage html report
	coverage html
	@echo "Coverage report is located at ./var/htmlcov/index.html"

.PHONY: django-checks
django-checks:
	python manage.py check --fail-level WARNING

##
# These targets are to be used by GitHub actions
##

.PHONY: install-pipeline
install-pipeline:
	pip install -U pip
	pip install -r requirements.txt
	@echo "===== PACKAGE DEPENDENCIES ====="
	@pip freeze | grep -ve "^-e" | sed 's/^/  /'
	@echo "================================"
	pip freeze > installed_requirements.txt
	pip install -r requirements_local.txt
	ln -s local.example.ini content/local.ini
	echo "*:*:*:postgres:postgres" > "$${HOME}/.pgpass"
	chmod 600 "$${HOME}/.pgpass"
	./manage.py collectstatic --link --settings=tests.test_settings

.PHONY: release
release: export TAG = release-${GITHUB_RUN_NUMBER}
release:
	# Commit the frontend build
	git commit -m 'Make release' --allow-empty
	# Create and push release tag
	git tag $$TAG
	git push origin $$TAG

	# Clone leukeleu-ansible repo and create a new commits and pull requests in leukeleu-ansible
	git clone --depth 1 https://deployer:$$DEPLOYER_ACCESS_TOKEN@github.com/leukeleu/leukeleu-ansible.git
	$(MAKE) -C leukeleu-ansible release host=s_mysite
	$(MAKE) -C leukeleu-ansible release host=l_mysite
