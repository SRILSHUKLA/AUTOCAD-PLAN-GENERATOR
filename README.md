# DraftEase 🏗️
![image](https://github.com/user-attachments/assets/44b2aa51-38da-48ad-8b8a-8aeb9a9d45d4)


## Overview

**DraftEase** is a web-based tool that converts architectural floor plan images into editable CAD files (DXF format). Instead of relying on AI, DraftEase uses a custom algorithmic approach to trace architectural elements such as walls and rooms from clear floor plan images, making the output reliable and lightweight.

## Features

- **Image-to-CAD Conversion**: Upload floor plan images and convert them to DXF format
- **Algorithmic Tracing Engine**: Detects structure outlines using traditional computer vision techniques
- **Fast and Lightweight**: No heavy AI models, runs efficiently even on basic setups
- **Editable CAD Output**: Generated DXF files are compatible with all major CAD software
- **Intuitive UI**: Drag-and-drop upload and instant download of output files

## Dataset Attribution

This project utilizes floor plan samples collected by Cubicasa5K dataset for development and testing.
Cubicasa5K is a high-quality floorplan dataset provided for research purposes.
The CubiCasa5K dataset was introduced in the following paper:

"CubiCasa5k: A Dataset and an Improved Multi-Task Model for Floorplan Image Analysis"
P. Renevey, O. Loosli, M. R. Oswald, and R. G. Cavallaro
International Conference on Pattern Recognition (ICPR), 2020.

You can download the cubicasa5k dataset from kaggle using this link:
https://www.kaggle.com/datasets/qmarva/cubicasa5k

License for the dataset:
https://creativecommons.org/licenses/by-nc/4.0/

## Technologies Used

- Python (Flask)
- HTML5, CSS3, JavaScript
- OpenCV and PIL for image processing
- DXF writing using `ezdxf` or custom tracing logic

## 🔧 How It Works  
### - Uploading & Converting Floor Plan Images  
1. **Upload** → Select a clean floor plan image (PNG, JPG).  
2. **Trace** → The backend processes the image and extracts architectural outlines.  
3. **Convert** → The traced shapes are converted into DXF file elements.  
4. **Download** → Instantly download the DXF for editing in AutoCAD or similar CAD software.  

### - Generating Custom Floor Plans  
1. **Specify** → Enter room types, dimensions, and layout preferences.  
2. **Generate** → Our model creates a floor plan matching your requirements.  
3. **Download** → Export the auto-generated DXF file to refine in AutoCAD.

## Installation

To run DraftEase locally:

```bash
git clone https://github.com/SRILSHUKLA/AUTOCAD-PLAN-GENERATOR.git
cd AUTOCAD-PLAN-GENERATOR
python app.py

=======
# House-GAN: Floorplan Generation Engine

A powerful machine learning engine for generating realistic house floorplans using Generative Adversarial Networks (GANs).

## Overview

House-GAN is a deep learning system that generates realistic house floorplans based on bubble diagrams (graphical representations of room layouts). It uses a relational GAN architecture that takes into account the relationships between rooms and their constraints.

## Features

- Generate realistic floorplans from bubble diagrams
- Maintain room relationships and constraints
- Support for different room configurations
- Vector-based floorplan outputs
- Multi-GPU training support
- Comprehensive visualization tools

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/housegan.git
cd housegan
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
housegan/
├── src/                    # Source code
│   ├── models/            # Model architectures
│   ├── data/              # Data processing
│   └── utils/             # Utility functions
├── models/                # Pretrained models
├── data/                  # Dataset storage
├── scripts/               # Training and evaluation scripts
├── tests/                 # Unit tests
├── docs/                  # Documentation
└── notebooks/             # Jupyter notebooks
```

## Usage

### Training

To train the model from scratch:

```bash
python scripts/train.py --target_set D --exp_folder exp_example
```

### Generation

To generate floorplans using a pretrained model:

```bash
python scripts/generate.py --model_path models/pretrained.pth
```

### Evaluation

To evaluate model performance:

```bash
python scripts/evaluate.py --model_path models/pretrained.pth
```

## Model Architecture

The system consists of:
- Generator: Creates floorplan layouts from latent vectors and room information
- Discriminator: Evaluates the realism of generated floorplans
- CMP (Conditional Message Passing): Handles relational aspects between rooms

## Dataset

The model is trained on the LIFULL HOME's database containing 117,587 real floorplans. The data is processed into vector graphics format and converted into room bounding boxes and bubble diagrams.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this code in your research, please cite:

```bibtex
@inproceedings{nauata2020house,
  title={House-gan: Relational generative adversarial networks for graph-constrained house layout generation},
  author={Nauata, Nelson and Chang, Kai-Hung and Cheng, Chin-Yi and Mori, Greg and Furukawa, Yasutaka},
  booktitle={European Conference on Computer Vision},
  pages={162--177},
  year={2020},
  organization={Springer}
}
```

## Contact

For questions and feedback, please open an issue in the repository.
