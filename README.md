# flameDainApp

instructions on how to install on flame machine

### Installation

#### Python3 environment:

Download Anaconda3 version 2018.12:

    $ wget https://repo.anaconda.com/archive/Anaconda3-2018.12-Linux-x86_64.sh

If you're not running bash already (tcsh is a standart for default flame user):
    
    $ /bin/bash
    
Install Anaconda3:

    $ bash Anaconda3-2018.12-Linux-x86_64.sh

Assuming that you've used default installation folder ~/anaconda3 run:

    $ echo ". ~/anaconda3/etc/profile.d/conda.sh" >> ~/.bashrc

press ctrl+d and run bash shell again

    $ /bin/bash
    
activate anaconda base environment:

    $ conda activate base
    
That will be our main environment to run DainApp, so we would need to launch bash shel and then to activate environment there before using it

#### Newer gcc in separate isolated environment:

DainApp requires gcc compiler newer then default one on CentOS 7.6 in order to be able to compile its cuda extensions. Luckily it is possible to install it in hassle-free way without interfearing with our main flame environment

    $ sudo yum install centos-release-scl-rh
    $ sudo yum install devtoolset-7-toolchain

#### Cuda and Cudnn

run:

    $ nvidia-smi
    
and check driver version and cuda version for this driver

in my case driver is 440.44 and cuda version is 10.2

Most of the installation later assume cuda version 10.2. If you have newer - try it and let me know if it works.

go to cuda download page:	https://developer.nvidia.com/cuda-toolkit-archive
click on the version and then Linux --> x86_64 --> CentOS --> 7 --> runfile(local)
do not use rpm unless you know what you're doing it is likely to kill your flame
there should be download url and install command, in my case:

    $ wget https://developer.download.nvidia.com/compute/cuda/10.2/Prod/local_installers/cuda_10.2.89_440.33.01_linux.run
    $ sudo sh cuda_10.2.89_440.33.01_linux.run

Do not install driver, uncheck it. (installing driver will likely break flame install)
Ignore cuda complainig about it.

To get to Cudnn download links nvidia will ask you to register as a developer.
cuDNN download page:	https://developer.nvidia.com/rdp/cudnn-archive,
and get the rpm files for Red Hat (x86_64 & Power architecture)
cuDNN Runtime Library for RedHat/Centos 7.3 (RPM)
cuDNN Developer Library for RedHat/Centos 7.3 (RPM)
cuDNN Code Samples and User Guide for RedHat/Centos 7.3 (RPM)

I'm using cuDNN v7.6.5 (November 18th, 2019), for CUDA 10.2
https://developer.nvidia.com/compute/machine-learning/cudnn/secure/7.6.5.32/Production/10.2_20191118/RHEL7_3-x64/libcudnn7-7.6.5.33-1.cuda10.2.x86_64.rpm
https://developer.nvidia.com/compute/machine-learning/cudnn/secure/7.6.5.32/Production/10.2_20191118/RHEL7_3-x64/libcudnn7-devel-7.6.5.33-1.cuda10.2.x86_64.rpm
https://developer.nvidia.com/compute/machine-learning/cudnn/secure/7.6.5.32/Production/10.2_20191118/RHEL7_3-x64/libcudnn7-doc-7.6.5.33-1.cuda10.2.x86_64.rpm
install all three rpms with 
    
    $ sudo yum localinstall libcudnn* 

#### Check build environment with Cuda and CuDNN

first we need system to pick up newly installed cuda libraries
    
    $ sudo ldconfig

make sure you're running bash with base anaconda environment activated. You should have (base) before your shell. if not run:
    
    $ /bin/bash
    $ conda activate

activate devtoolset for newer gcc:
    
    $ scl enable devtoolset-7 bash

you will loose (base) in front of the shell but it is ok.

check gcc version:
    
    $ gcc -v

it should be greater then 7, in my case gcc version 7.3.1 20180303 (Red Hat 7.3.1-5) (GCC)

    $ cd /usr/local/cuda

fix permissions to be able tu build as user

    $ sudo chmod -R a+rwX samples/
    $ cd samples
    
open makefile and change line 41
/usr/local/cuda/samples/Makefile
edit line 41:
FILTER_OUT := 0_Simple/cudaNvSci/Makefile

try to compile cuda samples

    $ make (or make -j [number of cpu's to use])

check the result of compilation

    $ cd /usr/local/cuda/samples/bin/x86_64/linux/release
    $ ./deviceQuery

you should see Result = PASS

check cudnn

    $ cd /usr/src/
    $ sudo chmod -R a+rwX cudnn_samples_v7/
    $ cd cudnn_samples_v7/mnistCUDNN/
    $ make
    $ ./mnistCUDNN
    
after running compiled command you should see "Test passed!" at the very end

#### Install Pytorch
I'm using 1.6.0 from here: https://pytorch.org/get-started/previous-versions/
    
    $ conda install pytorch==1.6.0 torchvision==0.7.0 cudatoolkit=10.2 -c pytorch
    
to test pytorch:
    
    $ python ~/anaconda3/lib/python3.7/site-packages/torch/utils/collect_env.py

among the answers there should be "Is CUDA available: Yes"

#### Install OpenCV

    $ pip install opencv-python
    $ pip install opencv-contrib-python

7) Get ffmpeg if you don't have it and put it somwhere in the bin path
(I use static build from https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
and place it in /usr/bin)

8) get Dain-App and original DAIN (for training)

9) Build cuda code (don't forget it has to be done from within anaconda environment we were using and  with devtoolset activated)

10)
