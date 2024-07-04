from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import sys
import os
from pathlib import Path
from PyQt5.uic import loadUiType
import pyqtgraph as pg
from PyQt5.uic import loadUiType
import sys
import os

import vtk
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.all import vtkConeSource, vtkPolyDataMapper, vtkActor, vtkRenderer

ui, _ = loadUiType('main.ui')


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        self.resize(1450, 900)

        self.folder_name = None
        self.iso_value = self.iso_slider.value()
        self.render_timer = QTimer(self)

        # We Set up a timer to delay rendering after slider changes
        self.render_timer.setSingleShot(True)
        self.render_timer.timeout.connect(self.render_function)

        # Setting a layout for our vtk_frame
        self.vtk_frame.setLayout(QVBoxLayout())

        # Create a VTK rendering widget
        self.vtk_widget = QVTKRenderWindowInteractor(self.vtk_frame)
        self.vtk_frame.layout().addWidget(self.vtk_widget)
        
        # connecting with functions
        self.open_btn.clicked.connect(self.open_folder)
        self.iso_slider.valueChanged.connect(self.start_render_timer)
        self.surface_rendering_radioButton.toggled.connect(self.render_function)

    def start_render_timer(self):
        if self.surface_rendering_radioButton.isChecked():
            self.render_timer.start(150)

    def open_folder(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = QFileDialog.getExistingDirectory(self, 'Open Folder', current_dir)
        if folder_path:
            self.folder_name = os.path.basename(folder_path)
            self.render_function()

    def render_function(self):
        if self.surface_rendering_radioButton.isChecked():
            actor, renderer = self.surface_rendering()
        else:
            actor, renderer = self.ray_casting_rendering()

        # Set up the VTK render window
        render_window = self.vtk_widget.GetRenderWindow()
        renderer.SetBackground(0.0, 0.0, 0.0)
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
            volume_property = vtk.vtkVolumeProperty()
            volume_property.ShadeOn()
            volume_property.SetInterpolationTypeToLinear()

            # Create a transfer function
            color_function = vtk.vtkColorTransferFunction()
            color_function.AddRGBPoint(0, 0.0, 0.0, 0.0)
            color_function.AddRGBPoint(255, 1.0, 1.0, 1.0)

            opacity_function = vtk.vtkPiecewiseFunction()
            opacity_function.AddPoint(0, 0.0)
            opacity_function.AddPoint(255, 1.0)

            # Set the transfer functions in the volume property
            volume_property.SetColor(color_function)
            volume_property.SetScalarOpacity(opacity_function)

            # Set scalar range for transfer functions
            scalar_range = reader.GetOutput().GetScalarRange()
            volume_property.SetScalarOpacityUnitDistance(scalar_range[1] - scalar_range[0])

            # Create a volume mapper and connect it to the DICOM reader
            volume_mapper = vtk.vtkGPUVolumeRayCastMapper()  # Use GPU-accelerated ray casting
            volume_mapper.SetInputConnection(reader.GetOutputPort())

            # Create a volume actor and set its mapper and property
            volume_actor = vtk.vtkVolume()
            volume_actor.SetMapper(volume_mapper)
            volume_actor.SetProperty(volume_property)

            # Create a renderer and add the volume actor
            renderer = vtk.vtkRenderer()
            renderer.SetBackground(0.0, 0.0, 0.0)
            renderer.AddVolume(volume_actor)

            return volume_actor, renderer

    def surface_rendering(self):
        if self.folder_name is not None:
            # Load DICOM images
            reader = vtk.vtkDICOMImageReader()
            reader.SetDirectoryName(f"{self.folder_name}")
            reader.Update()

            self.iso_value = self.iso_slider.value()

            # Apply Marching Cubes to extract iso_surface
            marching_cubes = vtk.vtkMarchingCubes()
            marching_cubes.SetInputConnection(reader.GetOutputPort())
            marching_cubes.SetValue(0, self.iso_value)  # Adjust isovalue as needed

            # Smooth the resulting surface
            smoother = vtk.vtkWindowedSincPolyDataFilter()
            smoother.SetInputConnection(marching_cubes.GetOutputPort())
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
