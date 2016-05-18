import time
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def hill_climb(f, step, xmin, xmax, ymin, ymax, plot=None):

	x = round(random.uniform(xmin, xmax), 2)
	y = round(random.uniform(ymin, ymax), 2)
	

	foundMin = False
	while(not foundMin):
		current = f(x,y)
		position = [current,x,y]

		#list of possible moves
		candidates = [(f(x+step,y),(x+step,y)), (f(x-step,y),(x-step,y)), (f(x,y+step),(x,y+step)), 
					  (f(x,y-step),(x,y-step)), (current,(x,y))]
		candidates.sort()
		if(candidates[0][0] == current):
			foundMin = True
			if plot != None:
				plot.scatter(x, y, f(x, y) + 0.01, c='y', marker='^', s=80)
		else:
			x, y = candidates[0][1]
			if plot != None:
				plot.scatter(x, y, current, c='r')
		
	return position


def hill_climb_random_restart(f, step, num_restarts, xmin, xmax, ymin, ymax, plot=None):

	position = hill_climb(f,step,xmin,xmax,ymin,ymax,plot)
	hmin = position[0]

	for i in range(1,num_restarts):
		new_position = hill_climb(f,step,xmin,xmax,ymin,ymax,plot)
		new_hmin = new_position[0]

		if new_hmin < hmin:
			hmin = new_hmin
			position = new_position

	return position


def simulated_annealing(f, step, max_temp, xmin, xmax, ymin, ymax, plot=None):

	prob = lambda old,new,curr_temp: round(math.exp((old-new)/curr_temp),10)
	path = []

	curr_temp = max_temp
	min_temp = 0.001
	alpha = 0.93

	x = round(random.uniform(xmin, xmax), 2)
	y = round(random.uniform(ymin, ymax), 2)

	solution = f(x,y)

	while curr_temp > min_temp:
		for i in range(20):
			new_x = round(random.uniform(x-step, x+step), 2)
			if new_x > xmax or new_x < xmin:
				new_x = x
			new_y = round(random.uniform(y-step, y+step), 2)
			if new_y > ymax or new_y < ymin:
				new_y = y
			new_solution = f(new_x,new_y)
			ap = prob(solution,new_solution,curr_temp)

			if ap > random.random():
				solution = new_solution
				x = new_x
				y = new_y
				if plot != None:
					if curr_temp > 1:
						plot.scatter(x, y, solution, c='r',linewidth=.001)
					else:
						plot.scatter(x, y, solution, c=(0,1,0),linewidth=.001)

		curr_temp = curr_temp*alpha

	return [solution, new_x, new_y]


def graph(f, step, xmin, xmax, ymin, ymax):


	X = np.arange(xmin, xmax, step)
	Y = np.arange(ymin, ymax, step)
	xc, yc = np.meshgrid(X, Y)

	Z = f(xc,yc)
	fig = plt.figure(1)
	ax = fig.add_subplot(111,projection="3d")
	ax.plot_wireframe(xc,yc,Z,rstride=1,cstride=1,color='b',linewidth=1)
   
	return ax
	
def main():

	step =  .01
	xmin = -2.5
	xmax =  2.5
	ymin = -2.5
	ymax =  2.5
	num_restarts = 12
	max_temp = 1000

	r = lambda x,y: np.sqrt(x**2 + y**2)
	z = lambda x,y: ((np.sin(x**2+3*y**2))/(0.1+r(x,y)**2) ) + (x**2 + 5*y**2) * ((np.exp(1-r(x,y)**2))/(2))
	
	runtime = []
	plot = graph(z,.1,xmin,xmax,ymin,ymax)

	hh = []
	hhrr = []
	sa = []
	hht = []
	hhrrt = []
	sat = []
	for i in range(1):
	#Hill Climbing
		start_time = time.time()
		result = hill_climb(z,step,xmin,xmax,ymin,ymax)
		hh.append(round(result[0],10))
		runtime = time.time() - start_time
		hht.append(round(runtime,10))
		print ("Hill Cimbing:        min = " + str(round(result[0],10)) + " runtime = " + str(round(runtime,10)) + " seconds")
		print ("                     X: " + str(round(result[1],3)) + 
			   "\n                     Y: " + str(round(result[2],3)) + "\n")

		#Hill Climbing w/ RR
		start_time = time.time()
		result = hill_climb_random_restart(z,step,num_restarts,xmin,xmax,ymin,ymax)
		hhrr.append(round(result[0],10))
		runtime = time.time() - start_time
		hhrrt.append(round(runtime,10))
		print ("Hill Cimbing w/ RR:  min = " + str(round(result[0],10))+ " runtime = " + str(round(runtime,10)) + " seconds")
		print ("                     X: " + str(round(result[1],3)) + 
			   "\n                     Y: " + str(round(result[2],3)) + "\n")

		#Simmulated Annealing
		start_time = time.time()
		result = simulated_annealing(z,.2,max_temp,xmin,xmax,ymin,ymax)
		sa.append(round(result[0],10))
		runtime = time.time() - start_time
		sat.append(round(runtime,10))
		print ("Simulated Annealing: min = " + str(round(result[0],10))+ " runtime = " + str(round(runtime,10)) + " seconds")
		print ("                     X: " + str(round(result[1],3)) + 
			   "\n                     Y: " + str(round(result[2],3)) + "\n")

	#print("mean hh: " + str(np.mean(hh)))
	#print("mean hhrr: " + str(np.mean(hhrr)))
	#print("mean sa: " + str(np.mean(sa)))
	#print("std hh: " + str(np.std(hh)))
	#print("std hh: " + str(np.std(hhrr)))
	#print("std hh: " + str(np.std(sa)))
	
	#print("mean hht: " + str(np.mean(hht)))
	#print("mean hhrrt: " + str(np.mean(hhrrt)))
	#print("mean sat: " + str(np.mean(sat)))
	#print("std hht: " + str(np.std(hht)))
	#print("std hhrrt: " + str(np.std(hhrrt)))
	#print("std sat: " + str(np.std(sat)))
	plt.show()  

main()