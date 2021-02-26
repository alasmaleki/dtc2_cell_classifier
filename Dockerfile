FROM python:3.8-slim-buster
LABEL maintainer="Ali asghar Maleki | https://github.com/alasmaleki"
RUN apt-get update -y

# gcc compiler and opencv prerequisites
RUN apt-get -y install vim nano git build-essential libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev

# Detectron2 prerequisites
RUN pip install torch==1.7.1+cpu torchvision==0.8.2+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install cython
RUN pip install install pyyaml==5.1
RUN pip install -U 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'

# Detectron2 - CPU copy
RUN python -m pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.7/index.html
# Development packages
RUN pip install flask flask-cors requests opencv-python
COPY . /home
CMD  ["python", "/home/web_application/app.py" ]