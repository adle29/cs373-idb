ifeq ($(CI), true)
    COVERAGE := coverage
    PYLINT   := pylint
else
    COVERAGE := coverage-3.5
	PYLINT   := pylint3
endif


Site.log:
	git log > site.log

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

test: 