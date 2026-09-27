# 計概 Python Lab 共用 Makefile。
#   make build   檢查語法
#   make test    執行全部測試(pytest)
# 各 Lab 額外的規則寫在 lab.mk。
.PHONY: build test

build:
	python3 -m py_compile $(wildcard src/*.py)

-include lab.mk

test: build
	PYTHONPATH=src python3 -m pytest -q -rA -p no:cacheprovider tests
