# WOLF
INTRO:

The idea behind project is to execute various Machine Learning algorithms on user provided data and gather all the results in database which can further be queried to figure out the best performing algorithm and it's respective parameters on which the algorithm excelled.
WOLF follows best practices of executing a machine learning algorithm on a dataset, which are :
1) Splitting data – into training and testing files, in an efficient way
2) Running machine learning algorithms on the splitted data over a wide range of parameters w.r.t to the algorithm for better optimization
3) Performs metric calculation on the result set collected by executing various machine learning algorithms
4) Stores the results of each iteration in database, making it easy to trace the best performing parameter of an algorithm.
 
FUNCTIONING:

WOLF takes a configuration file as input, which gives user a leverage to decide on the parameters for all the different modules like Data-Spliting , Algorithms to be ran on data and even the Metric Calculation. Configuration file provided by user has to follow a particular format applied by WOLF.

Based on the user provided configuration file a shell script is created consisting of all the jobs to be executed on cluster. The shell script is then executed on cluster performing all the tasks in pipeline, from splitting data based on user provided input to saving data to database.
