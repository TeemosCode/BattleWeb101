with open("evaluation.txt", 'r') as name_file:
	with open('user_name_files', 'w') as target_file:
		for line in name_file:
			word = line.rstrip()
			if len(line) > 2:
				target_file.write(word)
				target_file.write(',')

