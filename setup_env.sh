echo "setup environement"

conda --version

conda create -y -n ActiveImageLabeler

conda activate ActiveImageLabeler
# conda install -y python
conda install -y  pylint pep8 flake8 yapf lxml pandas

conda install -y opencv -c menpo 

conda install -y ipython

pip install ninja yacs cython matplotlib tqdm opencv-python --user

# conda install -c pytorch pytorch-nightly torchvision cudatoolkit=9.0
# This worked for me
conda install -c pytorch pytorch-nightly torchvision=0.2.2 cudatoolkit=10.0
pip install PyQt5

pip install pyinstaller

export INSTALL_DIR=$PWD
# install pycocotools
cd $INSTALL_DIR

git clone https://github.com/cocodataset/cocoapi.git

cd cocoapi/PythonAPI

python setup.py build_ext install

# install apex
cd $INSTALL_DIR

git clone https://github.com/NVIDIA/apex.git

cd apex

python setup.py install --cuda_ext --cpp_ext

cd $INSTALL_DIR

git clone https://github.com/meryusha/seeds_faster.git

cd seeds_faster

python setup.py build develop

cd $INSTALL_DIR

unset INSTALL_DIR
