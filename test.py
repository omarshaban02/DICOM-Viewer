
import vtk

# Load DICOM images
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName("digest_article")
reader.Update()
# Apply Marching Cubes to extract isosurface
marchingCubes = vtk.vtkMarchingCubes()
marchingCubes.SetInputConnection(reader.GetOutputPort())
marchingCubes.SetValue(0, 90)  # Adjust isovalue as needed

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

renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.SetSize(640, 480)

# Create an interactor and start rendering
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderWindow)


interactor.Initialize()
renderWindow.Render()
interactor.Start()