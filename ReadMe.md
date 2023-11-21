# Cryptography Competition Frontend

This repository contains the frontend application for our Cryptography Competition. It is developed using PyQt6 and third-party theme PyQtFluent.

## Table of Contents

1. Features
2. Prerequisites
3. Installation
4. Usage

## Preview

![image](https://github.com/Jay-Waves/foo/assets/88886108/5dbd041d-9b73-415f-8129-406d046da0ef)

## Prerequisites

- Python 3.8 or later
- Ubuntu 22.04, or Arch Linux
- x86, or amd64

## Installation

Follow the steps below to set up the frontend application on your Ubuntu system:

### 1\. Install Qt6:

Before installing PyQt6, you need to have Qt6 installed on your system. 

```bash
# in ubuntu:
sudo apt install qt6-default

# in arch:
sudo apt install qt6-base
```

### 2\. Create a Python Virtual Environment:

It's a good practice to use a virtual environment of Python projects to avoid any dependency conflicts. 

```bash
cd /path/to/your/workspace

# Create virtual environment
python -m venv ./foo && cd foo

# Activate the virtual environment
source ./bin/activate
```

### 3\. Install PyQt6 and Fluent Theme in the Virtual Environment:

**Only the basic package for pyqt6 needed**

```bash
pip install pyqt6

pip install PyQt6-Fluent-Widgets -i https://pypi.org/simple/
```

### 4\. Clone this repository and Begin:

```bash
git clone https://github.com/luminous-whispers/foo
```

## Usage

After installation, you can run the frontend application using the following command (make sure your virtual environment is activated):

```bash
python foo/my_app.py
```

## Contributing

refresh the resource:
```bash
/usr/lib/qt6/rcc -g python -o resource.py resource.qrc
```


## License
