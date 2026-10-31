# Copyright cocotb contributors
# Copyright (c) 2013 Potential Ventures Ltd
# Copyright (c) 2013 SolarFlare Communications Inc
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause

SIM ?= icarus

TOPLEVEL_LANG ?= verilog

PWD=$(shell pwd)

export PYTHONPATH := $(PWD)/../model:$(PYTHONPATH)

VERILOG_SOURCES = $(PWD)/../hdl/adder.sv

COCOTB_TOPLEVEL     := adder
COCOTB_TEST_MODULES := test_adder

include $(shell cocotb-config --makefiles)/Makefile.sim
