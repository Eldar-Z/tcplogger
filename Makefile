TARGET = main.py

.PHONY: all test clean

all:
	python3 $(TARGET)

test:
	python3 test.py 2 5

clean:
	rm -rf *.pyc __pycache__
