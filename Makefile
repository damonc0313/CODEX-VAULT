.PHONY: test check-gil check-gil-free-threaded

TEST?=pytest -q

# Run the coverage-aware pytest suite. The default command can be overridden
# by exporting TEST for ad-hoc debugging (e.g., TEST="pytest -k smoke").
test:
	$(TEST)

# Print the interpreter's GIL status.
check-gil:
	python -m codex_framework.utils.gil_status

# Fail when the interpreter is not free-threaded.
check-gil-free-threaded:
	python -m codex_framework.utils.gil_status --require-free-threading
