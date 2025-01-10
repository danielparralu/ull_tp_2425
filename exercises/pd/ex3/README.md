# 1. CREATE INITIAL CONDITIONS

First of all, you have to create a .txt file with the initial conditions of the problem. The file's content must be organised in 7 columns: the first one contains the value of the masses of the particles, the next three columns contain the particles' initial coordinates, and on the other hand, the last three columns contain the particles' initial velocities. You can write this kind of .txt file manually or you can use initialconditions.f90, a program that asks you to specify the number of particles (N) and their initial velocities' absolute value. Then, this program creates N particles distributed uniformly on the surface of a sphere of radius 1, having each of them an initial velocity pointing towards the center of the sphere. All the particles' velocities have the same absolute value and all the masses are equal (mass = 1/N). 

# 2. RUN THE MAIN PROGRAM

The Makefile file generates an executable called sim. Therefore, in order to execute the main program you have to write ./sim .

