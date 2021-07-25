# Medusa 🐍

Medusa is a python package helpful in dataset creation or modification.

## Table Of Contests

- [Installation](#installation)
- [Usage](#usage)
- [General](#general)
    - [Commands](#commands)

## Installation

Pre-requirements:

```shell
sudo apt-get install build-essential cmake
sudo apt-get install libgtk-3-dev
sudo apt-get install libboost-all-dev
```

`pip install git+https://github.com/sqoshi/medusa.git`

## Usage

`medusa command --arguments`

Example:
`medusa convert /dataset --img-ext jpg`

## General

## Commands

### `convert`

Convert images to other image extension.

| argument | default | description|
|----------|---------|------------|
| --input-dir | None | Path to input directory with images. |
| --output-dir | converted_images | Output directory path (does not have to exist) |
| --img-ext | png | Target image extension [ `jpg`,`jpeg`,`webp`,`png`] |
| first_positional | None | Allow to pass single image.|

### `detect-faces`

Find and crop faces in image.

| argument | default | description|
|----------|---------|------------|
| --input-dir | None | Path to input directory with images. |
| --output-dir | detected_faces | Output directory path (does not have to exist) |
| --img-ext | png | Target image extension [ `jpg`,`jpeg`,`webp`,`png`] |
| --target-width | 160 | Width of output image.|
| --target-height | 160 | Height of output image.|
| first_positional | None | Allow to pass single image.|

----------------------
During _*nvidia graphics card*_ setup you may encounter a lot of bugs (TENSORFLOW).

Possible fixes:

1. `sudo ln -s /usr/local/cuda-11.0/targets/x86_64-linux/lib/libcusolver.so.11 ~/Documents/medusa/venv/lib/python3.8/site-packages/tensorflow/python/libcusolver.so.11`
2. `@reboot root for a in /sys/bus/pci/devices/*; do echo 0 | tee -a $a/numa_node; done > /dev/null`  append
   to  `/etc/crontab`
