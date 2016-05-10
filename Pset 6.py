#!/usr/bin/python

#import numpy as np
import random

##################################################################
###################### Testing Tools #############################
##################################################################

'''
Generates inputs for gradient descent.
Inputs:
    voters: the number of voters, or n from the pdf
    demographic: number of demographic info.
    error: How well our model will fit the data. Below 10 and its pretty good. Above 50 it's pretty bad.
Output:
    Theta:      n by m matrix from pdf
    Y:          length n vector of preferences
    true_x:     x from which we generated Y. If error is low, this will be quite close to optimal.
                When testing, you should check if the final x you get has a low mean_square_diff with this
    initial_x:  perturbed version of true_x. Useful starting point
'''
def generate_parameters(voters,demographic,error):

    #Randomly generate true params Theta, true_x, and Y
    Theta = 100*np.random.rand(voters,demographic)
    true_x = 10*np.random.rand(1,demographic) - 5
    Y = Theta.dot(true_x.transpose())
    Y = Y.transpose()
    Y = Y + np.random.normal(scale=error,size=voters)

    #Perturb the true x to get something close
    scaling = 0.5*np.ones((1,demographic))+np.random.rand(1,demographic)
    initial_x = np.multiply(true_x,scaling)

    #Somewhat hacky way to convert away from np arrays to lists
    Theta = Theta.tolist()
    Y = [Y[0][i] for i in xrange(voters)]
    true_x = [true_x[0][i] for i in xrange(demographic)]
    initial_x = [initial_x[0][i] for i in xrange(demographic)]

    return Theta,Y,true_x,initial_x


'''
This function is used by the tests and may be useful to use when calculating whether you should stop
This function takes two vectors as input and computes the mean of their squared error
Inputs:
  v1, a length k vector
  v2, a length k vector
Output:
  mse, a float for their mean-squared error
'''
def mean_square_diff(v1,v2):
    diff_vector = [v1[i]-v2[i] for i in xrange(len(v1))]
    mse = 1.0/len(v1)*sum(difference**2 for difference in diff_vector)
    return mse


##################################################################
#################### Part B: Gradient Descent ####################
##################################################################

# GRADIENT DESCENT SPECIFICS
# The stopping condition is given below, namely, when the mean squared diff of the x's
# between iterations is less than some constant. Note, this is not the mean squared diff
# of f(x) but of the vector x itself! For instance
#    x_at_iteration_k = [1,2,4,5]
#    x_at_iteration_k+1 = [1,4,2,6]
#    mean_square_change = mean_square_diff(x_at_iteration_k,x_at_iteration_k+1)

'''
Compute a 'sufficiently close to optimal' x using gradient descent
Inputs:
  Theta - The voting Data as a n by m array
  Y - The favorabilty scores of the voters
  initial_x - An initial guess for the optimal parameters provided to you
  eta - The learning rate which will be given to you.
Output:
  nearly optimal x.
'''
def gradient_descent(Theta, Y, initial_x, eta):
    #We've initialized some variables for you
	n,m = len(Theta),len(Theta[0])
	current_x = initial_x
	mean_square_change = 1

	def gradient(x):
		sums = [0]*n
		for i in range (n):
			for j in range (m):
				sums[i] += x[j]*Theta[i][j]

		grad = [0]*m
		for i in range (0,n):
			for j in range (0,m):
				grad[j] += (1./float(n))*((Y[i]-sums[i])*Theta[i][j])
		return grad

	while mean_square_change > 0.0000001:
		old_x = current_x
		grad = gradient(old_x)
		change = [eta*g for g in grad]
		update = [0]*m
		for i in range(m):
			update[i]=old_x[i]+change[i]
		current_x = update
		mean_square_change=mean_square_diff(current_x,old_x)
	return current_x


##################################################################
############### Part C: Minibatch Gradient Descent################
##################################################################

################################## ALGORITHM OVERVIEW ###########################################
# Very similar to above but now we are going to take a subset of 10                             #
# voters on which to perform our gradient update. We could pick a random set of 10 each time    #
# but we're going to do this semi-randomly as follows:                                          #
#   -Generate a random permutation of [0,1...,n] (say, [5,11,2,8 . . .])                        #
#    This permutation allows us to choose a subset of 10 voters to focus on.                    #
#   -Have a sliding window of 10 that chooses the first 10 elements in the permutation          #
#    then the next 10 and so on, cycling once we reach the end of this permutation              #
#   -For each group of ten, we perform a subgradient update on x.                               #
#    You can derive this from the J(x)^mini                                                     #
#   -Lastly, we only update our stopping condition, mean_square_change                          #
#    when we iterate through all n voters. Counter keeps track of this.                         #
#################################################################################################

'''
Minibatch Gradient Descent
Compute a 'sufficiently close to optimal' x using gradient descent with small batches
Inputs:
  Theta - The voting Data as a n by m array
  Y - The favorabilty scores of the voters
  initial_x - An initial guess for the optimal parameters provided to you
  eta - The learning rate which will be given to you.
Output:
  nearly optimal x.
'''
def minibatch_gradient_descent(Theta, Y, initial_x, eta):
    # We've gotten you started. Voter_ordering is a random permutation.
    # Window position can be used to keep track of the sliding window's position
	n,m = len(Theta),len(Theta[0])
	current_x = initial_x
	voter_ordering = range(n)
	random.shuffle(voter_ordering)
	mean_square_change = 1
	window_position = 0
	counter = 0

	def gradient(x,start):
		grad = [0]*m
		for i in range (start,start+10):
			sums = 0
			v = voter_ordering[i]
			for j in range (m):
				sums += x[j]*Theta[v][j]
			for j in range (0,m):
				grad[j] += .1*((Y[v]-sums)*Theta[v][j])
		return grad

	old_x = current_x
	while mean_square_change > 0.003:
		grad = gradient(current_x,counter*10)
		change = [eta*g for g in grad]

		update = [0]*m
		for i in range(m):
			update[i]=current_x[i]+change[i]
		current_x=update
		counter+=1
		if counter == n/10:
			mean_square_change = mean_square_diff(current_x,old_x)
			old_x = current_x
			counter = 0
	return current_x

##################################################################
############## Part D: Line search Gradient Descent###############
##################################################################

def add(x,y):
	n = len(x)
	sums = [0]*n
	for i in range (n):
		sums[i] = x[i]+y[i]
	return sums

def dot(x,y):
	n = len(x)
	product = 0
	for i in range(n):
		product+=x[i]*y[i]
	return product

def mult(c,x):
	return [c*g for g in x]
	

'''
Compute the mean-squared error between the prediction for Y given Theta and the current parameters x
and the actual voter desires, Y.
Input:
  Theta - The voting Data as a n by m array
  Y - The favorabilty scores of the voters. Length n.
  x - The current guess for the optimal parameters. Length m.
Output:
  A float for the prediction error.
'''
def prediction_error(Theta,Y,x):
	prediction_error = 0
	n = len(Theta)
	for i in range(n):
		prediction_error+=((Y[i]-dot(Theta[i],x))**2)*(1/float(n))
	return prediction_error

'''
This function should return the next current_x after doubling the learning rate
until we hit the max or the prediction error increases
Inputs:
    current_x   Current guess for x. Length m.
    gradient    Gradient of current_x. Length m.
    min_rate    Fixed given rate.
    max_rate    Fixed max rate.
Output:
    updated_x   Check pseudocode.
'''
def line_search(Theta,Y,current_x,gradient,min_rate=0.0000001,max_rate=0.1):
    eta = min_rate
    current_x = add(current_x,mult(eta,compute_gradient(Theta,Y,current_x)))
    while eta < max_rate:
    	temp_x = add(current_x,mult(eta,compute_gradient(Theta,Y,current_x)))
    	if prediction_error(Theta,Y,temp_x) < prediction_error(Theta,Y,current_x):
    		current_x = temp_x
    		eta = 2*eta
    	else:
    		return current_x
    return current_x


'''
Inputs:
  Theta  The voting Data as a n by m array
  Y      The favorabilty scores of the voters. Length n.
  x      The current guess for the optimal parameters. Length m.
Output:
  gradient Length m vector of the gradient.
'''
def compute_gradient(Theta,Y,current_x):
	n,m = len(Theta),len(Theta[0])
	mean_square_change = 1

	sums = [0]*n
	for i in range (n):
		for j in range (m):
			sums[i] += current_x[j]*Theta[i][j]

	grad = [0]*m
	for i in range (0,n):
		for j in range (0,m):
			grad[j] += (1./float(n))*((Y[i]-sums[i])*Theta[i][j])
	return grad

def gradient_descent_complete(Theta,Y,initial_x):
    n,m = len(Theta),len(Theta[0])
    delta = 1
    current_x = initial_x
    last_error = prediction_error(Theta,Y,current_x)
    while delta > 0.1:
        gradient = compute_gradient(Theta,Y,current_x)
        current_x = line_search(Theta,Y,current_x,gradient,0.000001,0.1)
        current_error = prediction_error(Theta,Y,current_x)
        delta = last_error - current_error
        last_error = current_error

    return current_x