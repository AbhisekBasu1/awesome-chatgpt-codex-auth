.PHONY: generate validate links check

generate:
	python3 scripts/generate_outputs.py

validate:
	python3 -m compileall scripts
	python3 scripts/validate_data.py
	python3 scripts/generate_outputs.py --check

links:
	python3 scripts/check_links.py --verify-evidence

check: validate
