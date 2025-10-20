###############################################################################
## Makefile for apertium/apertium-dev
## Builds Apertium language pairs with vendor dependencies
###############################################################################

# Paths
DEV_ROOT := $(shell pwd)
VENDOR_DIR := $(DEV_ROOT)/vendor
BUILD_DIR := $(DEV_ROOT)/build
TEST_DIR := $(DEV_ROOT)/tests

# Vendor paths
APERTIUM_VENDOR := $(VENDOR_DIR)/apertium
LTTOOLBOX_VENDOR := $(VENDOR_DIR)/lttoolbox
APERTIUM_IDO := $(VENDOR_DIR)/apertium-ido
APERTIUM_EPO := $(VENDOR_DIR)/apertium-epo

# Install prefixes for vendor builds
VENDOR_INSTALL := $(VENDOR_DIR)/installed

# Update PATH to use vendor tools
export PATH := $(VENDOR_INSTALL)/bin:$(PATH)
export PKG_CONFIG_PATH := $(VENDOR_INSTALL)/lib/pkgconfig:$(PKG_CONFIG_PATH)
export LD_LIBRARY_PATH := $(VENDOR_INSTALL)/lib:$(LD_LIBRARY_PATH)

# Language pair
PAIR_DIR := $(DEV_ROOT)/apertium-ido-epo

.PHONY: all clean test vendor help

# Default target
all: pair

# Help
help:
	@echo "Apertium Development Makefile"
	@echo "============================="
	@echo ""
	@echo "Targets:"
	@echo "  make vendor    - Build vendor dependencies (lttoolbox, apertium)"
	@echo "  make pair      - Build Ido-Esperanto language pair"
	@echo "  make test      - Run all tests"
	@echo "  make clean     - Clean build artifacts"
	@echo "  make distclean - Clean everything including vendor builds"
	@echo ""

# Build vendor dependencies
.PHONY: vendor
vendor: $(VENDOR_INSTALL)/.stamp

$(VENDOR_INSTALL)/.stamp:
	@echo "==> Building vendor dependencies..."
	@mkdir -p $(VENDOR_INSTALL)
	
	@# Build lttoolbox first
	@if [ -d "$(LTTOOLBOX_VENDOR)" ]; then \
		echo "  -> Building lttoolbox..."; \
		cd $(LTTOOLBOX_VENDOR) && \
		./autogen.sh --prefix=$(VENDOR_INSTALL) && \
		make && \
		make install; \
	else \
		echo "ERROR: lttoolbox not found at $(LTTOOLBOX_VENDOR)"; \
		echo "Run 'git submodule update --init --recursive' first"; \
		exit 1; \
	fi
	
	@# Build apertium
	@if [ -d "$(APERTIUM_VENDOR)" ]; then \
		echo "  -> Building apertium..."; \
		cd $(APERTIUM_VENDOR) && \
		./autogen.sh --prefix=$(VENDOR_INSTALL) && \
		make && \
		make install; \
	else \
		echo "ERROR: apertium not found at $(APERTIUM_VENDOR)"; \
		exit 1; \
	fi
	
	@touch $(VENDOR_INSTALL)/.stamp
	@echo "==> Vendor dependencies built successfully"

# Build language pair
.PHONY: pair
pair: vendor
	@echo "==> Building Ido-Esperanto language pair..."
	@if [ -d "$(PAIR_DIR)" ]; then \
		mkdir -p $(BUILD_DIR); \
		$(MAKE) -C $(PAIR_DIR) BUILD_DIR=$(BUILD_DIR); \
		echo "==> Language pair built successfully"; \
	else \
		echo "ERROR: Language pair not found at $(PAIR_DIR)"; \
		exit 1; \
	fi

# Run tests
.PHONY: test
test: pair
	@echo "==> Running tests..."
	@if [ -d "$(TEST_DIR)" ]; then \
		$(MAKE) -C $(PAIR_DIR) test BUILD_DIR=$(BUILD_DIR); \
	else \
		echo "WARNING: Test directory not found at $(TEST_DIR)"; \
	fi

# Clean build artifacts
.PHONY: clean
clean:
	@echo "==> Cleaning build artifacts..."
	@rm -rf $(BUILD_DIR)
	@if [ -d "$(PAIR_DIR)" ]; then \
		$(MAKE) -C $(PAIR_DIR) clean 2>/dev/null || true; \
	fi
	@echo "==> Clean complete"

# Clean everything including vendor builds
.PHONY: distclean
distclean: clean
	@echo "==> Cleaning vendor builds..."
	@rm -rf $(VENDOR_INSTALL)
	@if [ -d "$(LTTOOLBOX_VENDOR)" ]; then \
		$(MAKE) -C $(LTTOOLBOX_VENDOR) distclean 2>/dev/null || true; \
	fi
	@if [ -d "$(APERTIUM_VENDOR)" ]; then \
		$(MAKE) -C $(APERTIUM_VENDOR) distclean 2>/dev/null || true; \
	fi
	@echo "==> Distclean complete"

# Verify vendor tools are available
.PHONY: check-tools
check-tools:
	@echo "==> Checking for required tools..."
	@which lt-comp > /dev/null || (echo "ERROR: lt-comp not found. Run 'make vendor' first" && exit 1)
	@which apertium-preprocess-transfer > /dev/null || (echo "ERROR: apertium-preprocess-transfer not found. Run 'make vendor' first" && exit 1)
	@echo "==> All required tools found"


