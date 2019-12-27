#!/usr/bin/env bash

if [ "$1" = "t" ]; then
	./.venv/bin/python -m pytest $2
elif [ "$1" = "m" ]; then
	./.venv/bin/python -m $2
elif [ "$1" = "r" ]; then
	./.venv/bin/python $2
elif [ "$1" = "i" ]; then
	./.venv/bin/python -i -m $2
elif [ "$1" = "" ]; then
	echo -e "\nNothing was selected\n"
	echo -e "Options are:"
	echo -e "\tt: run pytest"
	echo -e "\tm: run as a module a directory or file"
	echo -e "\tr: run python file or directory"
	echo -e "\ti: run as a module and interactivly\n"
fi
