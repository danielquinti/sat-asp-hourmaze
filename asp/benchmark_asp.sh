#!/bin/bash
python3 hour_maze_asp.py ../examples/dom01.txt && diff -q ../examples/sol01.txt result.txt
python3 hour_maze_asp.py ../examples/dom02.txt && diff -q ../examples/sol02.txt result.txt
python3 hour_maze_asp.py ../examples/dom03.txt && diff -q ../examples/sol03.txt result.txt
python3 hour_maze_asp.py ../examples/dom04.txt && diff -q ../examples/sol04.txt result.txt
python3 hour_maze_asp.py ../examples/dom08.txt && diff -q ../examples/sol08.txt result.txt
python3 hour_maze_asp.py ../examples/dom09.txt && diff -q ../examples/sol09.txt result.txt
python3 hour_maze_asp.py ../examples/dom46.txt && diff -q ../examples/sol46.txt result.txt
python3 hour_maze_asp.py ../examples/dom47.txt && diff -q ../examples/sol47.txt result.txt