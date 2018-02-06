f = open('scores.txt',encoding='utf-8')
lines = f.readlines()
f.close()
results = []
for line in lines:
    data = line.split()
    sum = 0
    print(data)
    for score in data[1:]:
        sum += int(score)
    result = '%s \t:%d\n' % (data[0],sum)
    print(result)
    results.append(result)

out = open('result.txt','w',encoding='utf-8')
out.writelines(results)
out.close()