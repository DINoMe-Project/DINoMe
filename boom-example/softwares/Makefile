#=======================================================================
# Makefile for riscv-tests/isa
#-----------------------------------------------------------------------

isa_src_dir := .

default: all

#--------------------------------------------------------------------
# Build rules
#--------------------------------------------------------------------
ELF2HEX=/playpen/ziqiao/usr/local/bin/riscv64-unknown-elf-elf2hex
RISCV_PREFIX=/playpen/ziqiao/thesis/examples/lowrisc-chip-refresh-v0.6/riscv/bin/riscv64-unknown-elf-
RISCV_GCC = $(RISCV_PREFIX)gcc
ENTROPY = -DENTROPY=$(shell echo $$$$)
RISCV_GCC_OPTS = $(ENTROPY) -static -mcmodel=medany  -fvisibility=hidden -nostdlib -nostartfiles  -O0  
RISCV_OBJDUMP = $(RISCV_PREFIX)objdump --disassemble-all --disassemble-zeroes --section=.text --section=.text.startup --section=.text.init --section=.data --section=.data.secret --section=.data.offset --section=.data.size
RISCV_SIM = spike

vpath %.S $(isa_src_dir)

#------------------------------------------------------------
# Build assembly tests
%.riscv: %.S
#	$(RISCV_GCC)  -static -std=gnu99 -O2 -ffast-math -fno-common -fno-builtin-printf -DPREALLOCATE=1 -DHOST_DEBUG=0 \
		-c -I./../env \
		$< -o $@
#-Ttest.ld
	$(RISCV_GCC) $(RISCV_GCC_OPTS)  -Wl,-Ttest.ld  $< -o $@
%.hex: %.riscv 
	$(ELF2HEX) --bit-width 64 --input $< --output $@
%.S: %.c 
	$(RISCV_GCC) -O3  -S $< -o $@
%.dump: %.riscv 
	$(RISCV_OBJDUMP) $< > $@
%.dump0: %.riscv0 
	$(RISCV_OBJDUMP) $< > $@

%.out: 
	$(RISCV_SIM) %< 2> $@

%.out32: 
	$(RISCV_SIM) --isa=RV32 $< -o $@

%.riscv0: %.c 
	$(RISCV_GCC) $(RISCV_GCC_OPTS) $< -o $@

define compile_template

.PHONY: $(1)

tests += $$($(1)_tests)

endef

$(eval $(call compile_template,rv32ui,-m32))
$(eval $(call compile_template,rv32si,-m32))
$(eval $(call compile_template,rv32mi,-m32))
$(eval $(call compile_template,rv64ui))
$(eval $(call compile_template,rv64uf))
$(eval $(call compile_template,rv64si))
$(eval $(call compile_template,rv64mi))

tests_dump = $(addsuffix .dump, $(tests))
tests_hex = $(addsuffix .hex, $(tests))
tests_out = $(addsuffix .out, $(spike_tests))
tests32_out = $(addsuffix .out32, $(spike32_tests))

run: $(tests_out) $(tests32_out)
	echo; perl -ne 'print "  [$$1] $$ARGV \t$$2\n" if /\*{3}(.{8})\*{3}(.*)/' \
	       $(tests_out) $(tests32_out); echo;

junk += $(tests) $(tests_dump) $(tests_hex) $(tests_out) $(tests32_out)

#------------------------------------------------------------
# Default

all: $(tests_dump) $(tests_hex)

#------------------------------------------------------------
# Clean up

clean:
	rm -rf $(junk)
