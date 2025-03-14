# Copyright (c) 2021 - present / Neuralmagic, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from typing import Dict, List, Tuple

from setuptools import find_packages, setup


# default variables to be overwritten by the version.py file
is_release = None
version = "unknown"
version_major_minor = version

# load and overwrite version and release info from sparseml package
exec(open(os.path.join("src", "sparseml", "version.py")).read())
print(f"loaded version {version} from src/sparseml/version.py")
version_nm_deps = f"{version_major_minor}.0"

_PACKAGE_NAME = "sparseml" if is_release else "sparseml-nightly"

_deps = [
    "jupyter>=1.0.0",
    "ipywidgets>=7.0.0",
    "pyyaml>=5.0.0",
    "progressbar2>=3.0.0",
    "numpy>=1.0.0",
    "matplotlib>=3.0.0",
    "merge-args>=0.1.0",
    "onnx>=1.5.0,<=1.10.1",
    "pandas>=0.25.0",
    "packaging>=20.0",
    "psutil>=5.0.0",
    "pydantic>=1.5.0",
    "requests>=2.0.0",
    "scikit-image>=0.15.0",
    "scipy>=1.0.0",
    "tqdm>=4.0.0",
    "toposort>=1.0",
    "GPUtil>=1.4.0",
    "protobuf>=3.12.2,<4",
]
_nm_deps = [f"{'sparsezoo' if is_release else 'sparsezoo-nightly'}~={version_nm_deps}"]
_deepsparse_deps = [
    f"{'deepsparse' if is_release else 'deepsparse-nightly'}~={version_nm_deps}"
]

_onnxruntime_deps = ["onnxruntime>=1.0.0"]
_pytorch_deps = [
    "torch>=1.1.0,<=1.9.1",
    "tensorboard>=1.0",
    "tensorboardX>=1.0",
    "gputils",
]
_pytorch_vision_deps = _pytorch_deps + ["torchvision>=0.3.0,<=0.10.1"]
_tensorflow_v1_deps = ["tensorflow<2.0.0", "tensorboard<2.0.0", "tf2onnx>=1.0.0,<1.6"]
_tensorflow_v1_gpu_deps = [
    "tensorflow-gpu<2.0.0",
    "tensorboard<2.0.0",
    "tf2onnx>=1.0.0,<1.6",
]
_keras_deps = ["tensorflow~=2.2.0", "keras2onnx>=1.0.0"]

_dev_deps = [
    "beautifulsoup4==4.9.3",
    "black==21.5b2",
    "flake8==3.9.2",
    "isort==5.8.0",
    "m2r2~=0.2.7",
    "mistune==0.8.4",
    "myst-parser~=0.14.0",
    "rinohtype~=0.4.2",
    "sphinx~=3.5.0",
    "sphinx-copybutton~=0.3.0",
    "sphinx-markdown-tables~=0.0.15",
    "sphinx-multiversion~=0.2.4",
    "sphinx-pydantic~=0.1.0",
    "sphinx-rtd-theme~=0.5.0",
    "wheel>=0.36.2",
    "pytest~=6.2.0",
    "pytest-mock~=3.6.0",
    "flaky~=3.7.0",
    "sphinx-rtd-theme",
    "click<8.1",
]


def _setup_packages() -> List:
    return find_packages(
        "src", include=["sparseml", "sparseml.*"], exclude=["*.__pycache__.*"]
    )


def _setup_package_dir() -> Dict:
    return {"": "src"}


def _setup_install_requires() -> List:
    return _nm_deps + _deps


def _setup_extras() -> Dict:
    return {
        "dev": _dev_deps,
        "deepsparse": _deepsparse_deps,
        "onnxruntime": _onnxruntime_deps,
        "torch": _pytorch_deps,
        "torchvision": _pytorch_vision_deps,
        "tf_v1": _tensorflow_v1_deps,
        "tf_v1_gpu": _tensorflow_v1_gpu_deps,
        "tf_keras": _keras_deps,
    }


def _setup_entry_points() -> Dict:
    entry_points = {
        "console_scripts": [
            # sparsification
            "sparseml.benchmark=sparseml.benchmark.info:_main",
            "sparseml.framework=sparseml.framework.info:_main",
            "sparseml.sparsification=sparseml.sparsification.info:_main",
        ]
    }

    # transformers integration
    for task in [
        "masked_language_modeling",
        "question_answering",
        "text_classification",
        "token_classification",
    ]:
        entry_points["console_scripts"].extend(
            [
                f"sparseml.transformers.{task}=sparseml.transformers.{task}:main",
                f"sparseml.transformers.train.{task}=sparseml.transformers.{task}:main",
            ]
        )

    entry_points["console_scripts"].append(
        "sparseml.transformers.export_onnx=sparseml.transformers.export:main"
    )

    # image classification integration

    entry_points["console_scripts"].extend(
        [
            "sparseml.image_classification.export_onnx="
            "sparseml.pytorch.image_classification.export:main",
            "sparseml.image_classification.train="
            "sparseml.pytorch.image_classification.train:main",
            "sparseml.image_classification.lr_analysis="
            "sparseml.pytorch.image_classification.lr_analysis:main",
            "sparseml.image_classification.pr_sensitivity="
            "sparseml.pytorch.image_classification.pr_sensitivity:main",
        ]
    )

    # object detection integration

    entry_points["console_scripts"].extend(
        [
            "sparseml.yolov5.export_onnx=sparseml.yolov5.scripts:export",
            "sparseml.yolov5.train=sparseml.yolov5.scripts:train",
            "sparseml.yolov5.validation=sparseml.yolov5.scripts:val",
            "sparseml.yolov5.val_onnx=sparseml.yolov5.scripts:val_onnx",
        ]
    )

    return entry_points


def _setup_long_description() -> Tuple[str, str]:
    return open("README.md", "r", encoding="utf-8").read(), "text/markdown"


setup(
    name=_PACKAGE_NAME,
    version=version,
    author="Neuralmagic, Inc.",
    author_email="support@neuralmagic.com",
    description=(
        "Libraries for applying sparsification recipes to neural networks with a "
        "few lines of code, enabling faster and smaller models"
    ),
    long_description=_setup_long_description()[0],
    long_description_content_type=_setup_long_description()[1],
    keywords=(
        "inference, machine learning, neural network, computer vision, nlp, cv, "
        "deep learning, torch, pytorch, tensorflow, keras, sparsity, pruning, "
        "deep learning libraries, onnx, quantization, automl"
    ),
    license="Apache",
    url="https://github.com/neuralmagic/sparseml",
    package_dir=_setup_package_dir(),
    packages=_setup_packages(),
    install_requires=_setup_install_requires(),
    extras_require=_setup_extras(),
    entry_points=_setup_entry_points(),
    python_requires=">=3.6.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
