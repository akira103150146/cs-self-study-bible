#!/bin/sh
# 任務 5 參考解:檢查開發工具鏈。
status=0
for tool in gcc make python3 git gdb; do
    if command -v "$tool" >/dev/null 2>&1; then
        echo "$tool: $("$tool" --version 2>&1 | head -n 1)"
    else
        echo "$tool: MISSING"
        status=1
    fi
done
exit $status
