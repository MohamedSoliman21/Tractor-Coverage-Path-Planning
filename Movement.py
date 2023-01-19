import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'r', animated=True)
f = np.linspace(-3, 3, 500)

def init():
	ax.set_xlim(-3, 3)
	ax.set_ylim(-0.25, 2)
	ln.set_data(xdata,ydata)
	return ln,

def update(frame):
	xdata.append(frame)
	ydata.append(np.exp(-frame**2))
	ln.set_data(xdata, ydata)
	return ln,

ani = FuncAnimation(fig, update, frames=f, init_func=init, blit=True, interval = 1, repeat=False)
plt.show()	


len=10; width=5;
pts=[];
for i in xrange(1,width+1):
    y_curr=i-1;
    if y_curr%2==0 :
        for j in xrange(0,len+1):
            pts.append([j,y_curr]);
    elif y_curr%2==1:
        for j in  xrange(1,len+2):
            pts.append([len+1-j,y_curr]);
pts=np.asarray(pts);
plt.plot(pts[:,0], pts[:,1])
plt.axis([-1, len+1, -1, width])
plt.show()