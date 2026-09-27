# 計概 C Lab 共用 Makefile。
#   make build   只編譯(測試程式與 src/app_*.c 的指令列工具)
#   make test    編譯並執行全部測試
# 目錄慣例:include/(ctest.h)、src/(你的程式)、tests/(test_*.c)。
# 各 Lab 額外的規則寫在 lab.mk。
CC      ?= gcc
CTEST_TIMEOUT ?= 5
CFLAGS  ?= -std=c17 -Wall -Wextra -g -O0 -fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer
CPPFLAGS += -Iinclude -Isrc -DCTEST_TIMEOUT=$(CTEST_TIMEOUT) -D_DEFAULT_SOURCE
LDLIBS  += -lm

LIB_SRC := $(filter-out src/app_%.c,$(wildcard src/*.c))
APPS    := $(patsubst src/app_%.c,build/%,$(wildcard src/app_*.c))
TESTS   := $(patsubst tests/%.c,build/%,$(wildcard tests/test_*.c))
HDRS    := $(wildcard src/*.h include/*.h)

.PHONY: build test clean
build: $(TESTS) $(APPS)

-include lab.mk

build/test_%: tests/test_%.c $(LIB_SRC) $(HDRS) | build/.dir
	$(CC) $(CFLAGS) $(CPPFLAGS) $< $(LIB_SRC) -o $@ $(LDLIBS)
build/%: src/app_%.c $(LIB_SRC) $(HDRS) | build/.dir
	$(CC) $(CFLAGS) $(CPPFLAGS) $< $(LIB_SRC) -o $@ $(LDLIBS)
build/.dir:
	@mkdir -p build && touch $@

test: build
	@fail=0; for t in $(TESTS); do ASAN_OPTIONS=detect_leaks=1 ./$$t || fail=1; done; exit $$fail

clean:
	rm -rf build
