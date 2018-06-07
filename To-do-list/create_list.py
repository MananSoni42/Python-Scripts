# To Do list in command line using Python

import sys

def Menu(AddedList, numList):

	print('''
	1. Add a new task
	2. Show number of tasks in the To-do list
	3. Search for a task
	4. Delete task by name
	5. Sort list by Due date
	6. Sort list by priority
	7. Reset list
	8. Show all tasks
	9. Exit
	''')

	finalList = AddedList
	count = numList

	userInput = int(input('Enter the action you want to perform [1-9]:\t'))

	# User Input Allocation

	if userInput == 1:
		x = addStuff(AddedList)
		Menu(x, len(x))

	if userInput == 2:
		print('\nThe number of tasks in your list is ' + str(count))
		Menu(finalList, count)

	if userInput == 3:
		print('\n --- Search a Task by Name ---- \n')

		inputSearch = input('\nEnter the Task you want to search: \t')

		numo = 0
		numoPositive = 0

		for text in finalList:

			if inputSearch in text:
				numoPositive = numoPositive + 1
				print('\n{No}. '.format(No = numo+1) + text)
			numo = numo + 1

		if numoPositive == 0:
			print('\nI couldn\'t find your search-keyword in any of the tasks in your list!\n')

		Menu(finalList, count)

	if userInput == 4:
		print('\n --- Delete a Task by Name ---- \n')

		inputDelete = input('\nEnter the \'name\' of the task you want to delete: \t')

		numDel = 0
		numNegative = 0

		for text in finalList:

			if inputDelete in text:
				numNegative = numNegative + 1
				print('\n{No}. '.format(No = numDel+1) + text)
				cage = numDel + 1
			numDel+= 1

		if numNegative > 1:
			numIndex = input('\nWhich of the above do you want to delete?: \t')
			finalList.pop(int(numIndex)-1)
			Menu(finalList,len(finalList))

		elif numNegative == 0:
			print('\nI couldn\'t find your search-keyword in any of the tasks in your list!\n')
			Menu(finalList,len(finalList))

		else:
			finalList.pop(cage-1)
			print('\nAbove task has been deleted\n')
			Menu(finalList,len(finalList))


	if userInput == 5:

		print('\n --- Sorted tasks with due date ---- \n')

		finalList.sort()
		from operator import itemgetter
		print(sorted(AddedList, key=itemgetter(1)))
		Menu(finalList, len(finalList))

	if userInput == 6:

		print('\n --- Sorted tasks in priority order---- \n')

		finalList.sort()
		from operator import itemgetter
		print(sorted(AddedList, key=itemgetter(2)))
		Menu(finalList, len(finalList))




	if userInput == 7:

		print('\n --- To-do List Reset ---- \n')

		emptyList = []
		Menu(emptyList, len(emptyList))

	if userInput == 8:

		print('\n --- Displaying all tasks ---- \n')

		if count == 0:
			print('\n There are no pending tasks to display!')

		else:
			for i in range(count):
				print(f'\n {i+1}. ' + str(finalList[i]) + '\n')
				#i = i+1

		Menu(finalList, count)

	if userInput == 9:
		print('\nExiting To-Do List\n')
		sys.exit()


# 1. Add a new Task

def addStuff(AddedList):

	print('\n --- Adding a new task to your list ---- \n')
	task = []
	taskInput = input('\nEnter the task name: \t')
	task.append(taskInput)
	taskDue   = input('\nEnter the due date: \t')
	task.append(taskDue)
	taskPriority = input('\nEnter "h" for high and "l" for low priority: \t')
	task.append(taskPriority)
	AddedList.append(task)

	return(AddedList)



# Main Function

print('------ Welcome to your to-do-list! ------\n')

AddedList = []
numList = len(AddedList)

Menu(AddedList,numList)
