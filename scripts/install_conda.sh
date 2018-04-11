wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"

source $HOME/miniconda/bin/activate

conda config --add channels defaults
conda config --add channels conda-forge
conda config --add channels bioconda
conda clean --index-cache
