# 任務 2:完成 pipeline 目標,把 src/sum.c 一層一層往下拆,每一步產生一個檔案:
#
#   build/sum.i        前處理(gcc -E)
#   build/sum.s        組合語言(gcc -S,從 sum.i 來)
#   build/sum.o        目的檔(gcc -c,從 sum.s 來)
#   build/sum.linked   連結後的執行檔(從 sum.o 來)
#   build/sum.dis      反組譯(objdump -d build/sum.o)
#   build/sum.pyc.txt  Python bytecode(python3 -m dis src/sum.py)
#
# 注意:recipe 那一行開頭必須是 Tab,不是空白。

pipeline:
	@echo "TODO: 完成 src/pipeline.mk 的 pipeline 目標" && exit 1
