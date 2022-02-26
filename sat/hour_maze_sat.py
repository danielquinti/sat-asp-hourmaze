#Group members: Daniel Quintillán Quintillán, Sergio García Cascón.
#Emails: daniel.quintillan@udc.es, sergio.gcascon@udc.es
import sys
import subprocess
from itertools import combinations

hours = 12
num_of_clauses = 0

def maze_dimensions(lines):
	columns=int(lines[0])
	rows=int(lines[1])
	return (rows, columns)

def maze_string(lines):
	maze = ""
	position=0
	for line in lines:
		if (position > 1):
			# Replace the newline with a wall to avoid adjacency between the
			#last position of a row and the first position of the next one
			maze += line[:-1] + "|"
		position+=1
	return maze

def base_10(char):
	if (char == 'A'):
		char = '10'
	elif (char == 'B'):
		char = '11'
	elif (char == 'C'):
		char = '12'		
	return char

def variable_number(current_cell, value):
	return current_cell*12+value

def consecutive_hours(number):
	clockw = (number+1)%12
	counterclockw = (number-1)%12
	if clockw == 0:
		clockw = 12
	if counterclockw == 0:
		counterclockw = 12
	return (clockw,counterclockw)

def cell_combinations(hour, cells):
	global num_of_clauses
	# Number of times an hour value can be repeated in the final result. It depends on the maze's dimensions.	
	reps = cells // 12
	# This rule establishes the number of cells in which a specific hour value must be present at least once.
	# We obtain all the possible cell combinations.	
	# This will be applied in combinatorics.
	m=range(cells)
	n = cells - reps + 1
	combs = combinations(m,n)			
	combination_clauses = ""
	for item in combs:
		index = 0
		for cell in item:
			cell_value = variable_number(cell,1+hour)
			if (index == n-1):
				combination_clauses += str(cell_value) + " 0\n"				
			else:
				combination_clauses += str(cell_value) + " "			
			index += 1		
		num_of_clauses += 1		
	return combination_clauses

def process_restrictions(input_file):
	global num_of_clauses

	file=open(input_file, "r")
	lines=file.readlines()
	file.close()

	(rows,columns)=maze_dimensions(lines)
	maze = maze_string(lines)
	variables=hours*rows*columns
	number_of_cells= rows*columns	
	
	# The modified string grants an easier traversal than the original

	# Partial substrings optimize execution time
	fact_clauses = ""
	same_cell_clauses=""
	not_null_clauses = ""
	neighbour_classes = ""
	comb_clauses = ""

	current_cell = -1	
	# Traverse all the chars in the string
	for char in range(len(maze)):
		# Walls and the space between cells are ignored for this counter
		if (maze[char] != '|' and 
			maze[char] != ' ' and maze[char] != '-'):
			current_cell += 1

			
			# If a number is detected, it is written as a fact.
			if (maze[char] != 'x'):
				fact = variable_number(current_cell,int(base_10(maze[char])))
				fact_clauses += str(fact) + " 0\n"
				num_of_clauses += 1

			# Any hour for a specific cell discards the rest of the hours from appearing in that cell
			for current_hour in range(hours-1):		
				current_cell_value = variable_number(current_cell,1+current_hour)	
				for impossible_hour in range(current_hour,hours):	
					if (current_hour != impossible_hour):	
						impossible_cell_value = variable_number(current_cell,1+impossible_hour)								
						same_cell_clauses +=  (str(-current_cell_value) + " " + str(-impossible_cell_value) + " 0\n")							
						num_of_clauses +=1

			for hour in range(hours):
				number =variable_number(current_cell,1+hour)			

				
				(clockw,counterclockw) = consecutive_hours(hour+1)
				not_last_column = (current_cell+1) % columns
				
				#For every column except the last one, a cell value restricts its right neighbour if there is no wall between them
				if not_last_column and (maze[char+1] != '|'):					
					right_neighbour =current_cell+1
					adjacent_values_right = (variable_number(right_neighbour, clockw),variable_number(right_neighbour, counterclockw))
					neighbour_classes += (str(-number) + " " + str(adjacent_values_right[0]) + " " + str(adjacent_values_right[1]) + " 0\n")					
					num_of_clauses += 1

				# For every row except the last one, a cell value influences its bottom neighbour if there is no wall between them
				if ((current_cell < number_of_cells-columns) and (maze[char+columns*2] != '-')):
					bottom_neighbour = (current_cell+columns)
					adjacent_values_bottom = (variable_number(bottom_neighbour, clockw),variable_number(bottom_neighbour, counterclockw))
					neighbour_classes += (str(-number) + " " + str(adjacent_values_bottom[0]) + " " + str(adjacent_values_bottom[1]) + " 0\n")					
					num_of_clauses += 1
			
		
				# At least one value for each cell
				current_cell_value = variable_number(current_cell,1+hour)
				if (hour == 11):
					not_null_clauses += (str(current_cell_value) + " 0\n")
				else:
					not_null_clauses += (str(current_cell_value) + " ")							
			
			num_of_clauses += 1	

	# Every hour must be repeated N*M/12 times
	for hour in range(hours):
		comb_clauses += cell_combinations(hour,number_of_cells)

	clauses = ""
	clauses = fact_clauses + same_cell_clauses + not_null_clauses + neighbour_classes + comb_clauses
	sat_file = open("satfile.txt", "w")
	sat_file.write("p cnf " + str(variables) + " " + str(num_of_clauses) + "\n")						
	sat_file.write(clauses)
	sat_file.close()

	return (rows,columns)

def process_result(number):	
		real = int(number)%12
		if real == 10:
			result = 'A'
		elif real == 11:
			result = 'B'
		elif real == 0:
			result = 'C'
		else:
			result = str(real)
		return result

def get_sat_result(rows,columns,input_file):
	subprocess.call("clasp --verbose=0 satfile.txt > raw_result.txt", shell=True);
	raw_result_file = open("raw_result.txt", "r")
	
	#Filter the output to get only the positive atoms
	result=raw_result_file.read().split(' 0')[0].replace('v','').replace('\n','').split(" ")
	solution_array=[]
	for atom in result[1:]:
		if not atom.startswith('-'):
			solution_array.append(process_result(atom))
	
	#Print with the desired format 
	solution_string=""
	for row in range(rows):
		for column in range(columns):
			solution_string+=solution_array[row*columns+column]
		solution_string+="\n"
	print(solution_string)
	result_file=open('result.txt','w')
	result_file.write(solution_string)
	result_file.close()
if __name__ == '__main__':
	(rows,columns) = process_restrictions(sys.argv[1])
	get_sat_result(rows,columns,sys.argv[1])