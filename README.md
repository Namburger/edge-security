# EdgeSecurity
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![made-with-coral](https://img.shields.io/badge/Made%20with-Coral-orange)](https://coral.ai/)
[![made-with-bash](https://img.shields.io/badge/Made%20with-Bash-1f425f.svg)](https://www.gnu.org/software/bash/)
[![made-with-opencv](https://img.shields.io/badge/Made%20with-OpenCV-blue)](https://opencv.org/)
[![made-with-tflite](https://img.shields.io/badge/Made%20with-Tensorflow--Lite-orange)](https://www.tensorflow.org/lite/)
[![made-with-opencv](https://img.shields.io/badge/Made%20with-Python-blue)](https://www.python.org/)
[![ai-with-ai](https://img.shields.io/badge/AI%20with-AI-brightgreen)](https://en.wikipedia.org/wiki/Artificial_intelligence)

![Demo](templates/demo.gif?style=centerme)

## Install requirements
```
$ ./scripts/install_requirements.sh
```
**Note:** Should works on most platforms but the intended target are arm machines.

## Example run:
* With CPU (supper slow):
```
$ python3 main.py config/without_edgetpu.cfg
```
* With TPU:
```
$ python3 main.py config/with_edgetpu.cfg
```

**Note:** Please modify the config.
