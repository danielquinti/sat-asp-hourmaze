#Group members: Daniel Quintillán Quintillán, Sergio García Cascón.
#Emails: daniel.quintillan@udc.es, sergio.gcascon@udc.es
import subprocess
import sys
import os

def get_ASP_result(columns,rows):
	subprocess.call("clingo 0 general.lp instance.lp > raw_result.txt", shell=True);
	
	raw_output_file=open('raw_result.txt','r')
	raw_output=raw_output_file.read()
	raw_output_file.close()

	#obtain a list of strings following the pattern cell_value(X,Y,H)
	#X is the row
	#Y is the column
	#H is the hour
	atoms = raw_output.split('\n')[4].split(' ')

	#Initialize a list of empty strings with the dimensions of the maze
	solution_array=[]
	for index in range(rows*columns):
		solution_array.append("")

	#Fill the list using the coordinates of the maze as indexes
	for atom in range(len(atoms)):
		triplet=atoms[atom].replace('cell_value(',"").replace(")","").split(',')
		cell_row=int(triplet[0])-1
		cell_column=int(triplet[1])-1
		cell_value=triplet[2]
		solution_array[cell_row*columns+cell_column]=hexadecimal(cell_value)

	#Convert the list into a string with the desired format
	st=""
	for current_row in range(rows):
		for current_column in range(columns):
			st+=solution_array[current_row*columns+current_column]
		st+="\n"

	result_file = open("result.txt", "w")
	result_file.write(st)
	result_file.close()
	print(st)

def hexadecimal(number):
	if number == "10":
		result = 'A'
	elif number == "11":
		result = 'B'
	elif number == "12":
		result = 'C'
	else:
		result = number
	return result

def base_10(number):
	if number == "A":
		result = '10'
	elif number == "B":
		result = '11'
	elif number == "C":
		result = '12'
	else:
		result = number
	return result


def process_input_file(filename):
	#extract a list of lines from the input file
	input_file = open(filename,'r')
	lines = input_file.read().split("\n")
	input_file.close()

	#the first two lines represent the dimensions of the problem
	columns = int(lines[0])
	rows    = int(lines[1])
	description  =""
	description += "columns("+lines[0]+").\n"
	description += "rows("+lines[1]+").\n"

	current_row    = 0
	current_column = 0
	for current_line in range(2,len(lines)):
		#the even rows can contain horizontal walls and cell values
		if current_line % 2 ==0:
			line=lines[current_line]
			for current_char in range(0,len(line)):
				if current_char % 2 ==0:
					if line[current_char]!="x":
						description+="cell_value("+str(current_row+1)+","+str(current_column+1)+","+base_10(line[current_char])+").\n"
				else:
					if line[current_char]!=" ":
						description+="right_wall("+str(current_row+1)+","+str(current_column+1)+").\n"
					current_column+=1
			current_column=0

		#the odd rows contain only vertical walls
		else:
			if current_line<len(lines):
				line=lines[current_line]
				for current_char in range(0,len(line),2):
					if line[current_char]!=" ":
						description+="down_wall("+str(current_row+1)+","+str(current_column+1)+").\n"
					current_column+=1
				current_column=0
				current_row+=1

	#open a file to store the description of this particular instance of the problem
	description_file=open("instance.lp", "w")
	description_file.write(description)
	description_file.close()
	return (columns,rows)


if __name__ == '__main__':
	(columns,rows)=process_input_file(sys.argv[1])
	get_ASP_result(columns,rows)