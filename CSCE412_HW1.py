import string
import random

userstr1 = input("Enter the first string: ")
userstr2 = input("Enter the second string: ")
k = len(userstr1)
ref = userstr1

if len(userstr2) < len(userstr1):
	k = len(userstr2)
	ref = userstr2
	
# This effectively performs a coin flip at each index to determine whether the bit will be set
# to 1 or 0
def gen_string(str):
	new_str = ""
	for s in str:
		if random.randint(1, 2) == 1:
			new_str = new_str + "0"
		else:
			new_str = new_str + "1"
	return new_str

# This iterates through the candidate string and tests if the two strings the user entered
# match at any index where a bit is set to 1.
def eval(cand, str1, str2):
	score = 0
	for i in range(len(cand)):
		if cand[i] == "1":
			if str1[i] == str2[i]:
				score += 1
				# print("hit")
			else:
				score -= 1
				# print("miss")
	return score


if __name__ == "__main__":
	test_str = gen_string(ref)
	print(test_str)
	print(eval(test_str, userstr1, userstr2))