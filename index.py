from PyQt5.QtWidgets import *

import pyqtgraph as pg
import sys
import os
from pathlib import Path

from PyQt5.uic import loadUiType
import vtk
from PyQt5.QtWidgets import QApplication, QMainWindow
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.all import vtkConeSource, vtkPolyDataMapper, vtkActor, vtkRenderer

ui, _ = loadUiType('main.ui')


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        self.resize(1450, 900)

        self.folder_name = None
        self.iso_value = 90

        # Set a layout for vtk_frame
        self.vtk_frame.setLayout(QVBoxLayout())

        # Create a VTK rendering widget
        self.vtk_widget = QVTKRenderWindowInteractor(self.vtk_frame)

        # Add the vtk_widget to the vtk_frame's layout
        self.vtk_frame.layout().addWidget(self.vtk_widget)

        self.open_btn.clicked.connect(self.open_folder)

        self.iso_slider.valueChanged.connect(self.render_function)
        self.surface_rendering_radioButton.toggled.connect(self.render_function)

    def open_folder(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = QFileDialog.getExistingDirectory(self, 'Open Folder', current_dir)
        if folder_path:
            self.folder_name = os.path.basename(folder_path)
            print(self.folder_name)
            self.render_function()

    def render_function(self):

        if self.surface_rendering_radioButton.isChecked():
            actor, renderer = self.surface_rendering()
        else:
            actor, renderer = self.ray_casting_rendering()

        # Set up the VTK render window
        render_window = self.vtk_widget.GetRenderWindow()
        render_window.AddRenderer(renderer)

        # Set up the VTK interactor and start rendering
        interactor = render_window.GetInteractor()
        interactor.Initialize()

    def ray_casting_rendering(self):
        if self.folder_name is not None:
            # Load DICOM images
            reader = vtk.vtkDICOMImageReader()
            reader.SetDirectoryName(f"{self.folder_name}")
            reader.Update()

            # Create a volume property
            volumeProperty = vtk.vtkVolumeProperty()
            volumeProperty.ShadeOn()
            volumeProperty.SetInterpolationTypeToLinear()

            # Create a transfer function
            colorFunction = vtk.vtkColorTransferFunction()
            colorFunction.AddRGBPoint(0, 0.0, 0.0, 0.0)
            colorFunction.AddRGBPoint(255, 1.0, 1.0, 1.0)

            opacityFunction = vtk.vtkPiecewiseFunction()
            opacityFunction.AddPoint(0, 0.0)
            opacityFunction.AddPoint(255, 1.0)

            # Set the transfer functions in the volume property
            volumeProperty.SetColor(colorFunction)
            volumeProperty.SetScalarOpacity(opacityFunction)

            # Set scalar range for transfer functions
            scalarRange = reader.GetOutput().GetScalarRange()
            volumeProperty.SetScalarOpacityUnitDistance(scalarRange[1] - scalarRange[0])

            # Create a volume mapper and connect it to the DICOM reader
            volumeMapper = vtk.vtkGPUVolumeRayCastMapper()  # Use GPU-accelerated ray casting
            volumeMapper.SetInputConnection(reader.GetOutputPort())

            # Create a volume actor and set its mapper and property
            volumeActor = vtk.vtkVolume()
            volumeActor.SetMapper(volumeMapper)
            volumeActor.SetProperty(volumeProperty)

            # Create a renderer and add the volume actor
            renderer = vtk.vtkRenderer()
            renderer.SetBackground(0.0, 0.0, 0.0)  # Set background color to black
            renderer.AddVolume(volumeActor)

            return volumeActor, renderer

    def surface_rendering(self):
        if self.folder_name is not None:
            # Load DICOM images
            reader = vtk.vtkDICOMImageReader()
            reader.SetDirectoryName(f"{self.folder_name}")
            reader.Update()
            # Apply Marching Cubes to extract isosurface
            marchingCubes = vtk.vtkMarchingCubes()
            marchingCubes.SetInputConnection(reader.GetOutputPort())
            marchingCubes.SetValue(0, self.iso_value)  # Adjust isovalue as needed

            # Smooth the resulting surface
            smoother = vtk.vtkWindowedSincPolyDataFilter()
            smoother.SetInputConnection(marchingCubes.GetOutputPort())
            smoother.SetNumberOfIterations(100)  # Adjust number of iterations for desired smoothness
            smoother.BoundarySmoothingOn()
            smoother.SetFeatureAngle(120)
            smoother.SetEdgeAngle(90)
            smoother.SetPassBand(0.1)

            # Create a mapper and actor for the smoothed surface
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(smoother.GetOutputPort())

            actor = vtk.vtkActor()
            actor.SetMapper(mapper)

            # Create a renderer and render window
            renderer = vtk.vtkRenderer()
            renderer.AddActor(actor)

            return actor, renderer


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
