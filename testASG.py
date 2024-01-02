import vtk
from vtk.util import numpy_support
import os

def setup_renderer():
    reader = vtk.vtkDICOMImageReader()
    mapper = vtk.vtkSmartVolumeMapper()
    volume_property = vtk.vtkVolumeProperty()
    volume = vtk.vtkVolume()

    reader.SetDirectoryName(r"G:\Open GL\Tutorial 11\DICOM-Viewer\dicom_files\image-00000.dcm")
    mapper.SetInputConnection(reader.GetOutputPort())
    volume.SetMapper(mapper)
    volume.SetProperty(volume_property)

    renderer = vtk.vtkRenderer()
    renderer.AddVolume(volume)
    renderer.SetBackground(1.0, 1.0, 1.0) 

    render_window = vtk.vtkRenderWindow()
    render_window.SetWindowName("DICOM 3D Surface Rendering")
    render_window.SetSize(800, 800)

    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    style = vtk.vtkInteractorStyleTrackballCamera()
    render_window_interactor.SetInteractorStyle(style)

    render_window.Render()
    render_window_interactor.Start()

if __name__ == "__main__":
    setup_renderer()
