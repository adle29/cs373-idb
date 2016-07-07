ifeq ($(CI), true)
    COVERAGE := coverage
    PYLINT   := pylint
else
    COVERAGE := coverage-3.5
	PYLINT   := pylint3
endif


IDB1.log:
	git log > IDB1.log

check:

clean:

config:
	git config -l

format:
	
status:
	make clean
	@echo
	git branch
	git remote -v
	git status


models.html: apps/models.py
	pydoc3 -w models

test: 
