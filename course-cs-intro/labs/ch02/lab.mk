# 第 2 章:src/base.c 不能偷用函式庫的轉換函式。
FORBIDDEN := \b(strto[a-z]*|sscanf|v?s?n?printf|fprintf|atoi|atol|atoll)[[:space:]]*\(

build: lint
.PHONY: lint
lint:
	@if grep -nE '$(FORBIDDEN)' src/base.c; then \
	    echo "src/base.c 不能使用 strtol / sscanf / printf / atoi 家族:請自己實作轉換"; exit 1; fi
