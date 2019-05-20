echo "setup environement"

conda --version

conda create -y -n ActiveImageLabeler
source activate ActiveImageLabeler
# conda install -y python
conda install -y python pylint pep8 flake8 yapf lxml
conda install -y opencv -c menpo 

pip install PyQt5

pip install pyinstaller
