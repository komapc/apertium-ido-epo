###############################################################################
## Top-level Makefile for apertium-dev repository
## Orchestrates builds across all subprojects
###############################################################################

# Project root paths
ROOT_DIR := $(shell pwd)
APERTIUM_DEV := $(ROOT_DIR)/apertium
TOOLS_DIR := $(ROOT_DIR)/tools
EXTRACTOR_DIR := $(TOOLS_DIR)/extractor/ido-esperanto-extractor
WEB_DIR := $(TOOLS_DIR)/web/ido-epo-translator-web

# Default target
.PHONY: all
all: core

# Help target
.PHONY: help
help:
	@echo "Apertium Development Repository"
	@echo "================================"
	@echo ""
	@echo "Available targets:"
	@echo "  make core        - Build Apertium language pairs"
	@echo "  make extractor   - Run dictionary extractor pipeline"
	@echo "  make web         - Build web translator UI"
	@echo "  make test        - Run all tests"
	@echo "  make clean       - Clean all build artifacts"
	@echo "  make install     - Install Apertium tools (requires sudo)"
	@echo "  make status      - Show status of all subprojects"
	@echo ""
	@echo "Development targets:"
	@echo "  make vendor      - Build vendor dependencies"
	@echo "  make submodules  - Initialize and update submodules"
	@echo ""

# Initialize submodules
.PHONY: submodules
submodules:
	@echo "==> Initializing and updating submodules..."
	git submodule update --init --recursive
	@echo "==> Submodules ready"

# Build vendor dependencies (lttoolbox, apertium)
.PHONY: vendor
vendor: submodules
	@echo "==> Building vendor dependencies..."
	@if [ -d "$(APERTIUM_DEV)/vendor" ]; then \
		$(MAKE) -C $(APERTIUM_DEV) vendor; \
	else \
		echo "WARNING: Vendor directory not found. Run 'make submodules' first."; \
		exit 1; \
	fi
	@echo "==> Vendor dependencies built"

# Build core Apertium language pairs
.PHONY: core
core:
	@echo "==> Building Apertium language pairs..."
	@if [ -d "$(APERTIUM_DEV)" ]; then \
		$(MAKE) -C $(APERTIUM_DEV); \
	else \
		echo "ERROR: $(APERTIUM_DEV) not found"; \
		echo "Run migration first or check STRUCTURE.md"; \
		exit 1; \
	fi
	@echo "==> Core build complete"

# Run extractor pipeline
.PHONY: extractor
extractor:
	@echo "==> Running dictionary extractor..."
	@if [ -d "$(EXTRACTOR_DIR)" ]; then \
		$(MAKE) -C $(EXTRACTOR_DIR); \
	else \
		echo "ERROR: $(EXTRACTOR_DIR) not found"; \
		exit 1; \
	fi
	@echo "==> Extractor complete"

# Build web translator UI
.PHONY: web
web:
	@echo "==> Building web translator UI..."
	@if [ -d "$(WEB_DIR)" ]; then \
		cd $(WEB_DIR) && npm install && npm run build; \
	else \
		echo "ERROR: $(WEB_DIR) not found"; \
		exit 1; \
	fi
	@echo "==> Web build complete"

# Run tests
.PHONY: test
test:
	@echo "==> Running tests..."
	@if [ -d "$(APERTIUM_DEV)" ]; then \
		$(MAKE) -C $(APERTIUM_DEV) test; \
	else \
		echo "ERROR: Tests directory not found"; \
		exit 1; \
	fi
	@echo "==> All tests passed"

# Clean all build artifacts
.PHONY: clean
clean:
	@echo "==> Cleaning all build artifacts..."
	@if [ -d "$(APERTIUM_DEV)" ]; then \
		$(MAKE) -C $(APERTIUM_DEV) clean; \
	fi
	@if [ -d "$(EXTRACTOR_DIR)" ]; then \
		$(MAKE) -C $(EXTRACTOR_DIR) clean 2>/dev/null || true; \
	fi
	@if [ -d "$(WEB_DIR)" ]; then \
		cd $(WEB_DIR) && npm run clean 2>/dev/null || true; \
	fi
	@echo "==> Clean complete"

# Install Apertium tools system-wide
.PHONY: install
install: vendor
	@echo "==> Installing Apertium tools..."
	@echo "This requires sudo privileges"
	@cd $(APERTIUM_DEV)/vendor/lttoolbox && sudo make install
	@cd $(APERTIUM_DEV)/vendor/apertium && sudo make install
	@echo "==> Installation complete"

# Show status of all subprojects
.PHONY: status
status:
	@echo "==> Repository Status"
	@echo ""
	@echo "Apertium Language Pairs:"
	@if [ -d "$(APERTIUM_DEV)/apertium-ido-epo" ]; then \
		echo "  ✓ Ido-Esperanto pair found"; \
	else \
		echo "  ✗ Ido-Esperanto pair NOT found"; \
	fi
	@echo ""
	@echo "Tools:"
	@if [ -d "$(EXTRACTOR_DIR)" ]; then \
		echo "  ✓ Dictionary extractor found"; \
	else \
		echo "  ✗ Dictionary extractor NOT found"; \
	fi
	@if [ -d "$(WEB_DIR)" ]; then \
		echo "  ✓ Web translator found"; \
	else \
		echo "  ✗ Web translator NOT found"; \
	fi
	@echo ""
	@echo "Vendor Dependencies:"
	@if [ -d "$(APERTIUM_DEV)/vendor/apertium" ]; then \
		echo "  ✓ apertium submodule present"; \
	else \
		echo "  ✗ apertium submodule NOT present (run 'make submodules')"; \
	fi
	@if [ -d "$(APERTIUM_DEV)/vendor/lttoolbox" ]; then \
		echo "  ✓ lttoolbox submodule present"; \
	else \
		echo "  ✗ lttoolbox submodule NOT present (run 'make submodules')"; \
	fi
	@echo ""

# Development convenience targets
.PHONY: dev-setup
dev-setup: submodules vendor
	@echo "==> Setting up development environment..."
	@if [ -d "$(WEB_DIR)" ]; then \
		cd $(WEB_DIR) && npm install; \
	fi
	@if [ ! -d "venv" ]; then \
		python3 -m venv venv; \
		./venv/bin/pip install -r requirements-wiki.txt 2>/dev/null || true; \
	fi
	@echo "==> Development environment ready"
	@echo ""
	@echo "To activate Python environment: source venv/bin/activate"

.PHONY: quick-test
quick-test:
	@echo "==> Quick test: Ido → Esperanto"
	@cd $(APERTIUM_DEV)/apertium-ido-epo && \
		echo "me havas granda kato" | apertium -d . ido-epo

###############################################################################
## Backward compatibility (temporary during migration)
###############################################################################

# These targets work with old paths and show migration warnings
.PHONY: old-path-warning
old-path-warning:
	@echo "WARNING: You are using old paths"
	@echo "Please update your scripts to use new structure"
	@echo "See STRUCTURE.md and MIGRATION_PLAN.md"


