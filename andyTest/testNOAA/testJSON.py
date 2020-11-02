# this is first tests of JSON, also to plot matplotlib

import matplotlib.pyplot as plt
import numpy as np
import json


x = np.arange(0,9,1)
y = x*x
print(x)
print(y)

fig, ax = plt.subplots()  # Create a figure containing a single axes.
ax.plot(x,y)
#plt.show()
plt.close()


with open('output.json') as f:
    data = json.load(f)

print(type(data))
print(data['results'])

x = data['results']
print(type(x))
print(len(x))
print(x[0])
print(x[1])
print(x[2])
print(x[3])
print(x[4])
print(x[5])

print(x[5]['value'])

j = 0
t = []
p = []
d = []
b = []
for i in range(len(x)):
    if x[i]['datatype'] == 'TMAX':
        print(['j=' + str(j) + ' --TMAX= ' + str(x[i]['value'])])
        t.append(x[i]['value'])
        j = j + 1
        b.append(x[i]['date'][0:10])
        if x[i]['value'] > 266: d.append(x[i]['date'])   # TMAX > 266 = 26.6C = 80F
    if x[i]['datatype'] == 'TMIN': p.append(x[i]['value'])

print(t)
fig, ax = plt.subplots()  # Create a figure containing a single axes.
ax.plot(t)
ax.plot(p)
plt.show()
#plt.close()

fig, ax1 = plt.subplots()
ax1.plot(t, color='tab:red')

ax2 = ax1.twinx()
ax2.plot(p, color='tab:blue')
plt.show()
plt.close()


fig, ax1 = plt.subplots()
ax1.bar(range(len(p)),p, color=(112/255, 181/255, 131/255))
ax1.set_xlabel('Date', fontweight='bold')
ax1.set_ylabel('y lab 1',color=(112/255, 181/255, 131/255), fontweight='bold')
ax1.tick_params(axis='y', labelcolor=(112/255, 181/255, 131/255))
plt.xticks(ticks=range(len(b)), labels=b)
plt.xticks(rotation=45)

ax2 = ax1.twinx()
ax2.plot(range(len(p)),t, color='tab:red', linewidth=4, marker='o', markersize=12)
ax2.set_ylabel('y lab 2', color='tab:red', fontweight='bold')
ax2.tick_params(axis='y', labelcolor='tab:red')
plt.title('some title',  fontweight='bold', fontsize=32)
plt.tight_layout()
plt.savefig('test.eps')
plt.show()


print(b)
print(d)
#
