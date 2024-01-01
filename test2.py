import pydicom
import vtk
import pyvista as pv
import numpy as np
import glob

# Load DICOM files into a list
dcm_files = [pydicom.dcmread(f) for f in sorted(glob.glob(r"D:\projects\project\DICOM Viewer\DICOM-Viewer\dicom_files\0012.DCM"))]
# Get pixel arrays and spacing information
print(dcm_files[0].PixelSpacing)
pixel_arrays = [dcm.pixel_array for dcm in dcm_files]
for dcm in dcm_files:
    spacing = np.array([dcm.PixelSpacing[0], dcm.PixelSpacing[1], float(dcm.SliceThickness)])
    # Combine arrays into a 3D volume
    volume = np.stack(pixel_arrays, axis=2)
    # Create VTK image data from the volume
    vtk_image = vtk.vtkImageData()
    vtk_image.SetDimensions(volume.shape)
    vtk_image.SetSpacing(spacing)
    vtk_image.AllocateScalars(vtk.VTK_UNSIGNED_SHORT, 1)

    # Copy pixel data to VTK image
    vtk_array = vtk.util.numpy_support.numpy_to_vtk(volume.ravel(order='F'), deep=True, array_type=vtk.VTK_UNSIGNED_SHORT)
    vtk_image.GetPointData().SetScalars(vtk_array)
    # Apply Marching Cubes algorithm to create a surface mesh
    contour = vtk.vtkMarchingCubes()
    contour.SetInputData(vtk_image)
    contour.SetValue(0, 500)  # Adjust threshold as needed
    contour.Update()

    # Create a PyVista PolyData object for visualization
    surface = pv.wrap(contour.GetOutput())
    # Display the model using PyVista
    plotter = pv.Plotter()
    plotter.add_mesh(surface, smooth_shading=True)
    plotter.show()
