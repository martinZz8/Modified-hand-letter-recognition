1. Nvidia CUDA version for RTX 3060: release 11.5, V11.5.50
Build cuda_11.5.r11.5/compiler.30411180_0
To check currently installed CUDA version on machine, in cmd use: nvcc --version
Note: Here is used CUDA v11.5.0

__Previous versions of CUDA:__
https://developer.nvidia.com/cuda-toolkit-archive

__Torch verions installed:__
torch			1.12.1+cu113
torchaudio		0.12.1+cu113
torchvision		0.13.1+cu113
torchmetrics	1.2.1

__Installation of specific versions of torch:__
python -m pip install torch==1.12.1 torchaudio==0.12.1 torchvision==0.13.1 --index-url https://download.pytorch.org/whl/cu113
python -m pip install torchmetrics==1.2.1

Note: It probably could also be cu115 (--index-url https://download.pytorch.org/whl/cu115)

__Previous versions of PyTorch:__
https://pytorch.org/get-started/previous-versions/