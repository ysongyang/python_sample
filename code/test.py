num = 10
print('Guess what I think?')
bingo = False
while bingo == False:
    answer = int(input())
    if answer < num :
        print('too smaill')
    if answer>num :
        print('too big')
    if answer == num:
        print('BinGo?')
        bingo = True