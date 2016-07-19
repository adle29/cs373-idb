FILES := apiary.apib IDB2.log models.html apps/models.py apps/test.py  UML.pdf


ifeq ($(CI), true)
    COVERAGE := coverage
    PYLINT   := pylint
else
    COVERAGE := coverage-3.5
	PYLINT   := pylint3
endif


IDB1.log:
	git log > IDB1.log

IDB2.log:
	git log > IDB2.log

sha:
	git rev-parse HEAD

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

config:
	git config -l

format:
	autopep8 -i apps/models.py
	autopep8 -i apps/test.py

status:
	make clean
	@echo
	git branch
	git remote -v
	git status


models.html: apps/models.py
	pydoc3 -w models

test: 
	python3 apps/test.py

apitest:
	python3 apps/apitest.py 
