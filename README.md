# TSP-GA
Travelling Salesman Problem Genetic Algorithm for my Nuffield Future Researcher Project

I have uploaded the Travelling Salesman Problem code I wrote over the weekend. Sorry for the late submission, I can't seem to get the code to work. I roughly followed the method found here, https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35. I replaced some parts which were too complex for me, but I have run into more errors. Can you see where I've went wrong?

Update: With the updated version of the code, I can see that the errors, that I can see, are being caused by a confusion between the list datatype and the Route object, I've looked on stackoverflow but can't find any similar posts.

Update 2: The program has been completed, the TSP GA Complete program will randomly generate a list of cities and an x and y co-ordinate for each, it will then go through a number of generations, and output the initial distance, then the final distance. The program can be modified easily to instead be given a list of cities and their properties. The error I had before was because I failed to declare the routes created at the end of the program as Route objects before assigning them to the population list.
