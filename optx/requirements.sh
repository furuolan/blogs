apt-get -y update
apt-get -y upgrade
conda update -y pip
apt-get install libglpk-dev
CVXOPT_BUILD_GLPK=1 pip install cvxopt
