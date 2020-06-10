all: myc

myc: src/*
	(cd src && make)
	cp src/myc .

clean:
	(cd src && make clean)
	rm myc
	rm test/*.c test/*.h