https://www.dc.fi.udc.es/~cabalar/kr/2020/ex1.html

A script named benchmark.sh has been provided in the sat/ directory to solve and check the examples provided in the website with SAT.
A precondition of this script is that the folder that contains all the domxx.txt files is located in the root folder of the project.
To solve all of the provided examples, the script must be executed as follows:
$./benchmark_sat.sh

To solve the examples one by one, the program must be compiled and executed as follows:
$python3 hour_maze_sat.py <inputfile>

The python3 program outputs the formatted result to the command line and to the file result.txt

The ASP program can be used in the same way, since another script (benchmark_asp.sh) is provided to solve and check every example using ASP, and the individual examples can be solved following the same pattern as before:

$python3 hour_maze_asp.py <inputfile>
