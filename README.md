# Image Registration Platform

Welcome to the Image Registration Platform, an advanced solution for pairwise and sequential image registration tasks. This platform is based on a robust algorithm, notably improved through sequential registration, and capable of applying transformations across various channels.

## Algorithm
The underlying algorithm of this platform has been published and is accessible through the following ACM link:
[Algorithm Publication](https://dl.acm.org/doi/abs/10.1145/3584371.3612965).

## Features

- **Pairwise Image Registration**: For pairwise registration, images are restricted to a maximum size of 300x300 pixels and should be in 8-bit format.
- **Sequential Registration**: When uploading a folder for sequential registration, ensure that files are sorted by name and end with "ch00", "ch01", "ch02", etc.
- **Image Normalization**: All images are converted to a normalized form during the registration process.

## Downloads
Executable versions for both Windows (EXE) and macOS (DMG) are available for download here:
[Download Executables](https://drive.google.com/drive/folders/1EQhWBDgfl3WsorAWo8MhXmH0gg4g8yNs?usp=sharing).

## Source Code
The complete source code for the algorithm can be found on GitHub:
[Biological & Biomedical Image Registration Repository](https://github.com/NabaviLab/Biological-Biomedical-Image-Registration).

## System Requirements

The performance of the algorithm, including time and computational complexity, is highly dependent on the specifics of the uploaded images and folders. 

Minimum system requirements for a mid-level system are as follows:

- **Windows**:
  - OS: Windows 10, 64-bit
  - Processor: Intel Core i5 or equivalent
  - RAM: 8 GB
  - Graphics: DirectX 11 compatible video card with at least 2 GB of VRAM
  - Storage: SSD with at least 20 GB of free space
  - .NET Framework 4.8 or higher

- **macOS**:
  - OS: macOS Catalina or later
  - Processor: Intel Core i5 or M1 chip
  - RAM: 8 GB
  - Graphics: Metal-capable graphics card
  - Storage: SSD with at least 20 GB of free space

*Note: These requirements are a baseline and actual performance will vary based on specific image processing tasks and data size.*

## License
This software is developed under the license of Dr. Nabavi's and Dr. Ostroff's labs. For more details on the software license, please visit the following university pages:
- [Dr. Nabavi's Lab](https://sheida-nabavi.uconn.edu/)
- [Dr. Ostroff's Lab](https://pnb.uconn.edu/person/linnaea/)

## Learn More
To learn more about the registration process and our platform, please visit our website:
[Ultraplex Tools](http://ultraplextools.cse.uconn.edu:5000/).

## Citation

If you use this platform in your research, please cite the following paper:

```bash
@inproceedings{hamzehei20233d,
title={3D Biological/Biomedical Image Registration with enhanced Feature Extraction and Outlier Detection},
author={Hamzehei, Sahand and Bai, Jun and Raimondi, Gianna and Tripp, Rebecca and Ostroff, Linnaea and Nabavi, Sheida},
booktitle={Proceedings of the 14th ACM International Conference on Bioinformatics, Computational Biology, and Health Informatics},
pages={1--10},
year={2023}
}
```
