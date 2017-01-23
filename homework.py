import sys
import time

def togglePlayer(player):
	if player == "X":
		player = "O"
	elif player == "O":
		player = "X"
	return player

def isValidRaid(row, col, player, stateDict):
	opponent = togglePlayer(player)

	
	#CHECK_LEFT
	if (int(col)-1) >= 0:
		key = str(row)+"_"+str(int(col)-1)
		if stateDict.get(key) == opponent:
			return True
	#CHECK_RIGHT
	if (int(col)+1) < n:
		key = str(row)+"_"+str(int(col)+1)
		if stateDict.get(key) == opponent:
			return True
	
	#CHECK_DOWN
	if (int(row)+1) < n:
		key = str(int(row)+1)+"_"+str(col)
		if stateDict.get(key) == opponent:
			return True

	#CHECK_UP
	if (int(row)-1) >= 0:
		key = str(int(row)-1)+"_"+str(col)
		if stateDict.get(key) == opponent:
			return True
	
	return False

def fetchActions(n, player, stateDict):
	actions = []
	keys = stateDict.keys()
	append = actions.append
	r = range(0,int(n))
	for row in r:
		for col in r:
			key = str(row)+"_"+str(col)
			if key not in keys:
				key = key + "_S"
				append(key)


	for key in sorted(keys):
		if stateDict[key] == player:
			indexVal = key.split("_")
			row = indexVal[0]
			col = indexVal[1]
			

			#RAID_LEFT
			if (int(col)-1) >= 0:
				keyVal = str(row)+"_"+str(int(col)-1)
				if keyVal not in keys and isValidRaid(row, int(col)-1 , player, stateDict):
					keyVal = keyVal + "_R"
					if keyVal not in actions:
						append(keyVal)
			#RAID_RIGHT
			if (int(col)+1) < n:
				keyVal = str(row)+"_"+str(int(col)+1)
				if keyVal not in keys and isValidRaid(row, int(col)+1, player, stateDict):
					keyVal = keyVal + "_R"
					if keyVal not in actions:
						append(keyVal)
			#RAID_DOWN
			if (int(row)+1) < n:
				keyVal = str(int(row)+1)+"_"+str(col)
				if keyVal not in keys and isValidRaid(int(row)+1, col, player, stateDict):
					keyVal = keyVal + "_R"
					if keyVal not in actions:
						append(keyVal)
			#RAID_UP
			if (int(row)-1) >= 0:
				keyVal = str(int(row)-1)+"_"+str(col)
				if keyVal not in keys and isValidRaid(int(row)-1, col, player, stateDict):
					keyVal = keyVal + "_R"
					if keyVal not in actions:
						append(keyVal)
			
	return actions

def terminalTest(n, stateDict):
	size = int(n)*int(n)
	if len(stateDict) == size:
		return True
	return False

def result(stateDict, a, player):
	newStateDict = stateDict.copy()
	opponent = togglePlayer(player)
	indexVal = a.split("_")
	row = indexVal[0]
	col = indexVal[1]
	moveType = indexVal[2]

	if moveType == "S":
		key = str(row)+"_"+str(col)
		newStateDict[key] = player

	elif moveType == "R":
		key = str(row)+"_"+str(col)
		newStateDict[key] = player

		#CHECK_LEFT
		if (int(col)-1) >= 0:
			key = str(row)+"_"+str(int(col)-1)
			if stateDict.get(key) == opponent:
				newStateDict[key] = player
		#CHECK_RIGHT
		if (int(col)+1) < n:
			key = str(row)+"_"+str(int(col)+1)
			if stateDict.get(key) == opponent:
				newStateDict[key] = player
		
		#CHECK_DOWN
		if (int(row)+1) < n:
			key = str(int(row)+1)+"_"+str(col)
			if stateDict.get(key) == opponent:
				newStateDict[key] = player

		#CHECK_UP
		if (int(row)-1) >= 0:
			key = str(int(row)-1)+"_"+str(col)
			if stateDict.get(key) == opponent:
				newStateDict[key] = player
			
	return newStateDict


def utility(youPlay, cellValues, stateDict):
	opponent = togglePlayer(youPlay)
	playerSum = 0.0
	opponentSum = 0.0
	keys = stateDict.keys()
	for key in keys:
		indexVal = key.split("_")
		row = indexVal[0]
		col = indexVal[1]
		if stateDict[key] == youPlay:
			playerSum = playerSum + float(cellValues[int(row)][int(col)])
		elif stateDict[key] == opponent:
			opponentSum = opponentSum + float(cellValues[int(row)][int(col)])
	return float(playerSum) - float(opponentSum)


def maxValue(n, youPlay, player, depth, stateDict, cellValues, alpha, beta, mode):
	if terminalTest(n, stateDict) or depth == 0:
		return (utility(youPlay, cellValues, stateDict), None)
	val = float("-inf")
	player = togglePlayer(player)
	actions = fetchActions(n, player, stateDict)
	resultAction = None
	for a in actions:
		value = minValue(n, youPlay, player, int(depth)-1, result(stateDict, a, player), cellValues, alpha, beta, mode)[0]
		if value > val:
			val = value
			resultAction = a
			print resultAction
		if mode == "ALPHABETA":
			if val >= beta:
				return (val,resultAction)
			alpha = max(alpha, val)
	return (val,resultAction)

def minValue(n, youPlay, player, depth, stateDict, cellValues, alpha, beta, mode):
	if terminalTest(n, stateDict) or depth == 0:
		return (utility(youPlay, cellValues, stateDict), None)
	val = float("inf")
	player = togglePlayer(player)
	actions = fetchActions(n, player, stateDict)
	resultAction = None
	for a in actions:
		value = maxValue(n, youPlay, player, int(depth)-1, result(stateDict, a, player), cellValues, alpha, beta, mode)[0]
		if value < val:
			val = value
			resultAction = a
			print resultAction
		if mode == "ALPHABETA":
			if val <= alpha:
				return (val, resultAction)
			beta = min(beta, val)
	return (val, resultAction)


def minimaxDecision(n, youPlay, depth, cellValues, boardStateDict, mode):
	player = youPlay
	actions = fetchActions(n, player, boardStateDict)

	alpha = 0
	beta = 0

	maxVal = float("-inf")
	for a in actions: 
		val = minValue(n, youPlay, player, int(depth)-1, result(boardStateDict, a, player), cellValues, alpha, beta, mode)[0]
		if val > maxVal:
			maxVal = val
			resultAction = a
	return resultAction

def alphaBetaSearch(n, youPlay, depth, cellValues, boardStateDict, mode):
	player = youPlay
	player = togglePlayer(player)
	
	alpha = float("-inf")
	beta = float("inf")
	value, resultAction = maxValue(n, youPlay, player, int(depth), boardStateDict, cellValues, alpha, beta, mode)
	return resultAction
	
if __name__ == "__main__":

	start = time.time()

	inputFile = open("input.txt","r")

	n = 0
	mode = ""
	youPlay = ""
	depth = 0
	cellValues = []
	boardState = []
	
	for lineNo,line in enumerate(inputFile):
		if lineNo == 0:
			n = line.strip()
		elif lineNo == 1:
			mode = line.strip()
		elif lineNo == 2:
			youPlay = line.strip()
		elif lineNo == 3:
			depth = line.strip()
		elif lineNo < (4 + int(n)):
			val = line.split()
			cellValues.append(val)
		elif lineNo < (4 + int(n) + int(n)):
			val = list(line.strip())
			boardState.append(val)

	boardStateDict = {}
	r = range(0,int(n))
	for row in r:
		for col in r:
			if boardState[row][col] != ".":
				key = str(row)+"_"+str(col)
				boardStateDict[key] = boardState[row][col]

	outputFile = open("output.txt","w")
	if mode == "MINIMAX":
		action = minimaxDecision(n, youPlay, depth, cellValues, boardStateDict, mode)
		val = action.split("_")
		row = val[0]
		col = val[1]
		moveType = val[2]
		if moveType == "S":
			moveType = "Stake"
		elif moveType == "R":
			moveType = "Raid"
		outputFile.write(chr(int(col)+65) + str(int(row)+1) +" "+moveType+"\n")
		resultDict = result(boardStateDict, action, youPlay)
		result = [[0]*int(n) for i in r]
		for row in r:
			for col in r:
				key = str(row)+"_"+str(col)
				if key in resultDict.keys():
					result[row][col] = resultDict[key]
				else:
					result[row][col] = "."
			outputFile.write("".join(result[row])+"\n")
	elif mode == "ALPHABETA":
		action = alphaBetaSearch(n, youPlay, depth, cellValues, boardStateDict, mode)
		val = action.split("_")
		row = val[0]
		col = val[1]
		moveType = val[2]
		if moveType == "S":
			moveType = "Stake"
		elif moveType == "R":
			moveType = "Raid"
		outputFile.write(chr(int(col)+65) + str(int(row)+1) +" "+moveType+"\n")
		resultDict = result(boardStateDict, action, youPlay)
		result = [[0]*int(n) for i in r]
		for row in r:
			for col in r:
				key = str(row)+"_"+str(col)
				if key in resultDict.keys():
					result[row][col] = resultDict[key]
				else:
					result[row][col] = "."
			outputFile.write("".join(result[row])+"\n")
	outputFile.close()
	end = time.time()
	#print end-start