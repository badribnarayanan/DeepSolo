FROM nvidia/cuda:11.1.1-cudnn8-devel-ubuntu18.04
# use an older system (18.04) to avoid opencv incompatibility (issue#3524)


ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y \
	python3-opencv ca-certificates python3-dev git wget sudo ninja-build
RUN ln -sv /usr/bin/python3 /usr/bin/python

# create a non-root user
ARG USER_ID=1000
RUN useradd -m --no-log-init --system  --uid ${USER_ID} appuser -g sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER appuser
WORKDIR /home/appuser

ENV PATH="/home/appuser/.local/bin:${PATH}"
RUN wget https://bootstrap.pypa.io/pip/3.6/get-pip.py && \
	python3 get-pip.py --user && \
	rm get-pip.py

# install dependencies
# See https://pytorch.org/ for other options if you use a different version of CUDA
RUN pip install --user tensorboard cmake onnx   # cmake from apt-get is too old
RUN pip install --user torch==1.9.0+cu111 torchvision==0.10.0+cu111 -f https://download.pytorch.org/whl/torch_stable.html

RUN pip install --user setuptools editdistance matplotlib numba numpy pillow polygon3 rapidfuzz scipy scikit-image scikit-learn shapely timm tqdm gdown


#copy deepsolo from local repo
RUN git clone https://github.com/badribnarayanan/DeepSolo deepsolo

# set FORCE_CUDA because during `docker build` cuda is not accessible
ENV FORCE_CUDA="1"
# This will by default build detectron2 for all common cuda architectures and take a lot more time,
# because inside `docker build`, there is no way to tell which architecture will be used.
ARG TORCH_CUDA_ARCH_LIST="Kepler;Kepler+Tesla;Maxwell;Maxwell+Tegra;Pascal;Volta;Turing"
ENV TORCH_CUDA_ARCH_LIST="${TORCH_CUDA_ARCH_LIST}"

RUN python -m pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu111/torch1.9/index.html

RUN pip install --user -e deepsolo
WORKDIR /home/appuser/deepsolo

#run docker
# docker run --gpus all -it \
# > --shm-size=8gb --env="DISPLAY" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
# > --name=deepsolo deepsolo:v0


# run deepsolo under user "appuser":
# wget http://images.cocodataset.org/val2017/000000439715.jpg -O input.jpg
# python3 demo/demo.py  \
	#--config-file configs/ViTAEv2_S/TotalText/finetune_150k_tt_mlt_13_15_textocr.yaml \
	#--input sf6_ocr_frame.png --output outputs/ \
	#--opts MODEL.WEIGHTS tt_vitaev2-s_finetune_synth-tt-mlt-13-15-textocr.pth

