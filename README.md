# cm6500-camera-python-processing
Exploratory Python scripts for Optech Titan / CM-6500 camera image preprocessing and raw Bayer decoding.
# Optech Titan Camera Python Processing

This repository contains exploratory Python scripts developed for processing imagery from an Optech Titan / CM-6500 camera workflow.

The scripts are shared as small examples of practical Python image-processing work in a remote-sensing production context. They are not presented as a complete operational software package.

## Context

The work relates to airborne remote sensing and image preparation workflows associated with Optech Titan data acquisition. The broader sensor context is connected to my MSc and later LiDAR/remote-sensing work.

My MSc thesis is:

**Okhrimenko, M. (2018). _Applications of Multi-spectral LiDAR: River Channel Bathymetry and Canopy Vegetation Indices_. MSc Thesis, University of Lethbridge.**

Available through the University of Lethbridge Library and ProQuest Dissertations & Theses.

ProQuest record:  
https://www.proquest.com/docview/2154850134

The MSc thesis focused on multispectral airborne LiDAR applications, including river bathymetry, LiDAR radiometry, spectral vegetation indices, and Optech Titan data processing.

## Repository contents

```text
batch_colour_balance_jpegs.py
decode_packed12_bayer_raw_to_tiff.py
```

## Script 1: Batch colour balancing of JPEG imagery

```text
batch_colour_balance_jpegs.py
```

This script batch-processes JPEG images from an input folder and writes colour-balanced JPEG outputs to a new folder.

The workflow includes:

- reading all `.jpg` files from a folder;
- applying gray-world white balance;
- reducing excessive saturation;
- applying gamma correction to lift shadows;
- saving high-quality JPEG outputs.

The script was used as a practical preprocessing test for imagery intended for photogrammetric / orthophoto workflows.

## Script 2: Exploratory decoding of CM-6500 packed 12-bit raw imagery

```text
exploratory_decode_cm6500_packed12_raw.py
```

This script is an exploratory attempt to decode a raw binary camera file from a CM-6500-style imaging workflow.

The workflow includes:

- reading raw binary image data;
- unpacking packed 12-bit sensor values;
- reconstructing a 6600 × 4400 Bayer image;
- testing Bayer demosaicing with OpenCV;
- applying simple auto white balance;
- applying gamma correction;
- saving the result as a compressed TIFF.

This script should be understood as exploratory code. It was written before full use of the camera calibration documentation in a more complete production workflow. It demonstrates the logic of raw binary image handling, packed 12-bit unpacking, Bayer demosaicing, and basic radiometric visualization.

## Notes on camera calibration

The CM-6500 camera calibration report used in the project provides instrument-specific information such as image dimensions, pixel size, focal length, principal point offsets, and distortion coefficients.

The calibration report itself is not included in this repository. The scripts are shared only as code examples and may require adaptation for other cameras, file formats, Bayer patterns, or production image-processing pipelines.

## Dependencies

The scripts use common Python scientific and image-processing libraries:

```text
numpy
opencv-python
tifffile
matplotlib
```

The batch JPEG colour-balancing script also uses:

```text
os
glob
```

## Code status

These scripts are preserved as exploratory research / production-support code.

They are not a polished Python package. Paths, filenames, camera constants, and Bayer pattern assumptions may need to be edited before running the scripts on another machine or dataset.

## Skills demonstrated

This repository illustrates experience with:

- Python scripting for remote-sensing workflows;
- OpenCV image processing;
- batch processing of image files;
- raw binary file handling;
- packed 12-bit image unpacking;
- Bayer image reconstruction and demosaicing;
- basic radiometric and colour balancing;
- practical integration of Python outputs with photogrammetric / orthophoto workflows.

## Author

**Maxim Okhrimenko**  
Remote sensing, LiDAR, geospatial modelling, and image-processing workflows
