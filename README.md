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


#WOLF USER MANUAL:

This Manual contains three parts:

I   WOLF Environment Setup

II  WOLF Installation 

III Run WOLF

IV  Results



Part I: WOLF Environment Setup

1. Add the following command to your ~/.profile
   module load pyyaml/3.11-py27
   module load scikit-learn/0.17.0_gnu
2. login login1.ittc.ku.edu
3. mkdir <your local directory>


Part II: WOLF Installation 

1. Acquire the privilege for access https://gitlab.ittc.ku.edu/jhuan/WOLF.git. You need to log into https://gitlab.ittc.ku.edu at least onece using your ITTC account before the privilege can be assigned to you. You may need to install and use KU Anywhere VPN to access  https://gitlab.ittc.ku.edu if you are not using KU's network. For the details of KU Anywhere, please see https://technology.ku.edu/kuanywhere. 
2. cd <your local directory>
3. get the latest version of WOLF: git clone https://gitlab.ittc.ku.edu/jhuan/WOLF.git


Part III: Run WOLF

1. cd WOLF
2. python Wolf.py -i <config file>. 
   An example config file, wolf_test.yaml, has been provided for testing. You may edit the following line:
   email: xxx@xx.xx.xx 
   in culster_config section of wolf_test.yaml to change xxx@xx.xx.xx to your email so that you can get notifications of running status when you run WOLF with wolf_test.yaml using:
   python Wolf.py -i wolf_test.yaml.    


Part IV: Results

The final results generated from WOLF is stored in a file called Results.xlsx. An example file is provided in the WOLF/docs directory.
1. Get Results.xlsx
    Connect to kuanywhere.ku.edu through KU Anawhere VPN.
   1) Mac and Linux
      a. Open a terminal
      b. sftp login1.ittc.ku.edu
      c. cd <your local directory>/WOLF
      d. get Results.xlsx
   2) Windows
      You may use different kinds SFTP clients to access login1.ittc.ku.edu. WinSCP is free SFTP client for windows, the details of WinSCP can be found in https://winscp.net/eng/index.php.      
2. Results.xlsx
   The content of Results.xlsx consists of metrics of different algorightms you specify in the WOLF configuration file.
