# DICOM VIEWER

This application utilizes VTK (Visualization Toolkit) along with PyQt5 for visualizing DICOM images. It provides two rendering modes: surface rendering using Marching Cubes and ray casting for volume rendering.

## Features

- **Surface Rendering**: Utilizes Marching Cubes algorithm to extract and visualize iso-surfaces from DICOM images.
- **Volume Rendering**: Uses GPU-accelerated ray casting to render DICOM volumes with adjustable opacity and color mapping.
- **Interactive UI**: PyQt5 is used for the graphical user interface, allowing users to interactively select DICOM folders, adjust rendering parameters, and switch between surface and volume rendering.

## Requirements

Ensure you have the following dependencies installed:

- Python 3.x
- PyQt5
- VTK (install using `pip install vtk`)
- numpy (dependency of VTK)
- matplotlib (dependency of VTK)

## Installation and Usage

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/omarshaban02/DICOM-Viewer.git
   cd DICOM-Viewer
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   python main.py
   ```

4. **Using the Application:**
   - Click on the "Open Folder" button to select a folder containing DICOM images.
   - Use the slider to adjust the iso-value for surface rendering or volume rendering parameters.
   - Select the rendering mode (surface or volume) using radio buttons.
   - The application will visualize the DICOM data accordingly.


## Contributors <a name = "contributors"></a>
<table>
  <tr>
    <td align="center">
    <a href="https://github.com/AbdulrahmanGhitani" target="_black">
    <img src="https://avatars.githubusercontent.com/u/114954706?v=4" width="150px;" alt="Abdulrahman Shawky"/>
    <br />
    <sub><b>Abdulrahman Shawky</b></sub></a>
    </td>
<td align="center">
    <a href="https://github.com/omarnasser0" target="_black">
    <img src="https://avatars.githubusercontent.com/u/100535160?v=4" width="150px;" alt="omarnasser0"/>
    <br />
    <sub><b>Omar Abdulnasser</b></sub></a>
    </td>
         <td align="center">
    <a href="https://github.com/AhmedKamalMohammedElSayed" target="_black">
    <img src="https://avatars.githubusercontent.com/u/96977876?v=4" width="150px;" alt="Ahmed Kamal"/>
    <br />
    <sub><b>Ahmed Kamal</b></sub></a>
    </td>
         <td align="center">
    <a href="https://github.com/AbdullahOmran" target="_black">
    <img src="https://avatars.githubusercontent.com/u/30219936?v=4" width="150px;" alt="Abdullah Omran"/>
    <br />
    <sub><b>Abdullah Omran</b></sub></a>
    </td>
 <td align="center">
    <a href="https://github.com/MO-Nigo" target="_black">
    <img src="https://avatars.githubusercontent.com/u/103186952?v=4" width="150px;" alt="Mohammed Ali"/>
    <br />
    <sub><b>Mohammed Ali</b></sub></a>
    </td>
    <td align="center">
    <a href="https://github.com/MohammedAziz" target="_black">
    <img src="https://avatars.githubusercontent.com/u/103120952?v=4" width="150px;" alt="Mohammed Aziz"/>
    <br />
    <sub><b>Mohammed Aziz</b></sub></a>
    </td>
      </tr>
 </table>
