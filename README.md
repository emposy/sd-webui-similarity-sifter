## SimilaritySifter for Stable Diffusion WebUI
This is a WebUI extension for AUTOMATIC1111's Stable Diffusion web UI that allows you to filter generated images by facial similarity using the face_recognition library.

### Features
- Filter generated images by facial similarity to a given reference image
- Supports both txt2img and img2img generation
- Provides a simple and intuitive user interface within the WebUI
- Utilizes the powerful face_recognition library for accurate facial comparisons

## Prerequisites

### Installing on Windows

Before installing SimilaritySifter on Windows, you need to install the following:

- Build Tools for Visual Studio 2022 or Visual Studio 2022
  - If you plan to use features other than Build Tools in Visual Studio, or if you are unsure, refer to the separate page "Installing Visual Studio Community 2022 on Windows". Note that Visual Studio includes Build Tools.
  - If you only plan to use the Build Tools feature of Visual Studio, refer to the separate page "Installing Build Tools for Visual Studio 2022 on Windows".
- CMake
  - CMake is a build tool. You can download it from the official CMake download page: https://cmake.org/download/

### Installing on Mac or Linux

First, make sure you have dlib already installed with Python bindings:

- [How to install dlib from source on macOS or Ubuntu](https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf)

Then, make sure you have CMake installed:

- On macOS, you can install it using Homebrew:
  ```
  brew install cmake
  ```
- On Linux, you can install it using your distribution's package manager. For example, on Ubuntu:
  ```
  sudo apt-get install cmake
  ```

## Installation

1. Open the "Extensions" tab in your Stable Diffusion WebUI.
2. Go to the "Install from URL" subtab.
3. Paste the following URL into the "URL for extension's git repository" field: `https://github.com/emposy/sd-webui-similarity-sifter.git`
4. Click the "Install" button.
5. Wait for the installation to complete. You will see a message saying "Installed into stable-diffusion-webui\extensions\sd-webui-similarity-sifter. Use Installed tab to restart".
6. Go to the "Installed" subtab, click "Check for updates", and then click "Apply and restart UI" to activate the extension.

### Prerequisites
SimilaritySifter requires the following dependencies:

- Python 3.10.6+
- dlib with Python bindings (see installation instructions)
- cmake (install with brew install cmake on macOS)
These dependencies will be automatically installed during the extension installation process.

### Usage
1. In the WebUI, navigate to the "SimilaritySifter" tab.
2. Check the "Enable SimilaritySifter" checkbox.
3. Click the "Upload Image" button and select an image containing the face you want to use as a reference.
4. (Optional) Check the "Remove Low Similarity Images" checkbox and adjust the "Similarity Threshold" slider to remove images below the specified similarity.
5. Generate images using txt2img or img2img as usual.
6. The generated images will be sorted based on facial similarity to the reference image, with the most similar images appearing first.

### Limitations
- The face_recognition library is trained on adults and may not work well with children's faces.
- Accuracy may vary between ethnic groups. See the face_recognition wiki for more details.
- Performance may be slower compared to generating images without the facial similarity filter.

### Acknowledgements
SimilaritySifter is built upon the following libraries and projects:

- Stable Diffusion web UI by AUTOMATIC1111
- [face_recognition](https://github.com/ageitgey/face_recognition) by Adam Geitgey
Special thanks to the developers and contributors of these amazing projects!

### License
SimilaritySifter is released under the MIT License.