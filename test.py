import vtk

# Load DICOM images
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName("digest_article")
reader.Update()

# Create a renderer and render window
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.SetSize(640, 480)

# Create an interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderWindow)

# Initialize the interactor
interactor.Initialize()

# Function to switch between surface and ray casting rendering
def toggle_rendering(obj, event):
    if actor.GetVisibility():
        actor.SetVisibility(False)
        volume.SetVisibility(True)
        renderer.ResetCamera()  # Reset camera for better view of the volume
    else:
        actor.SetVisibility(True)
        volume.SetVisibility(False)

# Create a text actor to display instructions
textActor = vtk.vtkTextActor()
textActor.SetTextScaleModeToNone()
textActor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
textActor.SetPosition(0.1, 0.9)
textActor.GetTextProperty().SetFontSize(18)
textActor.GetTextProperty().SetColor(1.0, 1.0, 1.0)
textActor.SetInput("Press 'S' to switch between the two moods")

# Add the text actor to the renderer
renderer.AddActor(textActor)

# Create an observer for keypress events
def keypress(obj, event):
    key = interactor.GetKeySym()
    if key == "s" or key == "S":
        toggle_rendering(None, None)

# Add the observer for keypress events
interactor.AddObserver("KeyPressEvent", keypress)

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

# Create a volume mapper and property for ray casting rendering
volumeMapper = vtk.vtkSmartVolumeMapper()
volumeMapper.SetInputConnection(reader.GetOutputPort())

volumeProperty = vtk.vtkVolumeProperty()
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

# Set up ray casting properties (you may need to adjust these based on your data)
colorFunc = vtk.vtkColorTransferFunction()
colorFunc.AddRGBPoint(0, 0.0, 0.0, 0.0)
colorFunc.AddRGBPoint(255, 1.0, 1.0, 1.0)

scalarOpacity = vtk.vtkPiecewiseFunction()
scalarOpacity.AddPoint(0, 0.0)
scalarOpacity.AddPoint(255, 1.0)

volumeProperty.SetColor(colorFunc)
volumeProperty.SetScalarOpacity(scalarOpacity)
volumeProperty.ShadeOn()

# Add the actor and volume to the renderer (initially only the actor is visible)
renderer.AddActor(actor)
renderer.AddVolume(volume)
volume.SetVisibility(False)

# Start rendering
renderWindow.Render()
interactor.Start()

