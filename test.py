import os
import vtk
import pydicom
import numpy as np
from vtk.util import numpy_support

def load_dicom_series(folder_path):
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(folder_path)
    reader.Update()
    return reader.GetOutput()

def vtk_image_to_numpy(vtk_image):
    shape = vtk_image.GetDimensions()[::-1]
    vtk_array = vtk_image.GetPointData().GetScalars()
    numpy_array = numpy_support.vtk_to_numpy(vtk_array)
    numpy_array = numpy_array.reshape(shape)
    n_layer_repetitions = 5
    stretched_array = np.repeat(numpy_array,n_layer_repetitions,axis=0)
    
    return stretched_array

def create_surface_model(numpy_array):
    image_data = vtk.vtkImageData()
    image_data.SetDimensions(numpy_array.shape)
    image_data.AllocateScalars(vtk.VTK_DOUBLE, 1)
    
    for i in range(numpy_array.shape[0]):
        for j in range(numpy_array.shape[1]):
            for k in range(numpy_array.shape[2]):
                image_data.SetScalarComponentFromDouble(i,j,k, 0, numpy_array[i, j, k])
    # vtk_array = vtk.util.numpy_support.numpy_to_vtk(numpy_array.reval(order='F'),deep=True,array_type = vtk.VTK_UNSIGNED_CHAR)
    # image_data.GetPointData().SetScalars(vtk_array)

    iso_surface = vtk.vtkMarchingCubes()
    iso_surface.SetInputData(image_data)
    iso_surface.SetValue(0,120)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(iso_surface.GetOutputPort())
    actor =  vtk.vtkActor()
    actor.SetMapper(mapper)
    # contour_filter = vtk.vtkContourFilter()
    # contour_filter.SetInputData(image_data)
    # contour_filter.SetValue(0, 100)  # Adjust the threshold value as needed

    # mapper = vtk.vtkPolyDataMapper()
    # mapper.SetInputConnection(contour_filter.GetOutputPort())

    # actor = vtk.vtkActor()
    # actor.SetMapper(mapper)

    return actor

def main():
    folder_path = "./digest_article"
    reader = load_dicom_series(folder_path)
    numpy_array = vtk_image_to_numpy(reader)
    actor = create_surface_model(numpy_array)

    # Set up renderer and render window
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0, 0, 0)  # Set background color to white

    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(500, 500)

    # Set up render window interactor
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    # Initialize and start the rendering loop
    render_window.Render()
    render_window_interactor.Start()

if __name__ == "__main__":
    main()
#