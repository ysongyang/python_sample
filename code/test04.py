"""
l = ['meat','egg','fish','milk']
#for i in l:
    #print(i)

print(l[-1])
l.append('stc')
#del l[0]
print(l)
print(l[1:-1])
"""
from random import choice

score = [0,0]
direction = ['left', 'center', 'right']

def kick():
    print('=== You Kick！ ===')
    print('Choose one side to shoot:')
    print('left,center,right')

    you = input()
    print('You kicked ' + str(you))
    com = choice(direction)  # 随机挑选一个
    print('Computer saved ' + com)
    if you != com:
        print('Goal!')
        score[0] +=1
    else:
        print('Oops...')
    print('Score：%d(you) - %d(com)\n'% (score[0],score[1]))

    print('=== You Save！===')
    print('Choose one side to save:')
    print('left,center,right')
    you = input()
    print('You kicked ' + str(you))
    com = choice(direction)  # 随机挑选一个
    print('Computer kicked '+com)
    if you == com:
        print('Saved!')
    else:
        print('Oops...')
        score[1] +=1
    print('Score: %d(you) - %d(com)\n' %(score[0],score[1]))

for i in range(5):
    print('=== Round %d ===' % (i+1))
    kick()
    while(score[0]== score[1]):
        i +=1
        print('=== Round %d ===' % (i+1))
        kick()
        if score[0] > score[1]:
            print('You win!')
        else:
            print('you Lose.')
