# 任務 2 參考解:把 src/sum.c 一層一層往下拆。

pipeline: build/sum.i build/sum.s build/sum.o build/sum.linked build/sum.dis build/sum.pyc.txt

build/sum.i: src/sum.c | build/.dir
	$(CC) -E $< -o $@
build/sum.s: build/sum.i
	$(CC) -S -O0 $< -o $@
build/sum.o: build/sum.s
	$(CC) -c $< -o $@
build/sum.linked: build/sum.o
	$(CC) $< -o $@
build/sum.dis: build/sum.o
	objdump -d $< > $@
build/sum.pyc.txt: src/sum.py | build/.dir
	python3 -m dis $< > $@
