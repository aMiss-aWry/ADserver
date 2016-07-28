DEST = test
CC = gcc
CFLAGS = -Wall -g

$(DEST) : test.c
	python -m compileall BTOClient
	$(CC) $(CFLAGS) test.c -o $(DEST)

.PHONY: clean
clean:
	/bin/rm -f $(DEST) *.gcov *.gcno *.gcda *.ad.c
