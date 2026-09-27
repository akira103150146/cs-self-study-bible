# 第 1 章 Lab(C + Python)。
#   make build      編譯 src/sum.c、檢查 Python 語法
#   make pipeline   任務 2:把 sum.c 一層一層往下拆(規則寫在 src/pipeline.mk)
#   make test       執行全部測試
CC     ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -O0 -g

.PHONY: build test pipeline clean
build: build/sum
	python3 -m py_compile $(wildcard src/*.py)

build/sum: src/sum.c | build/.dir
	$(CC) $(CFLAGS) $< -o $@
build/.dir:
	@mkdir -p build && touch $@

include src/pipeline.mk

test: build
	PYTHONPATH=src python3 -m pytest -q -rA -p no:cacheprovider tests

clean:
	rm -rf build src/__pycache__
