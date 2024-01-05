import vtk

def ray_casting_rendering():
    # Load DICOM images
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName("digest_article")
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

def surface_rendering():
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
    
    return actor,renderer

def main():

    #Choose what are you want surface or ray 
    actor, renderer = surface_rendering()

    # Create a render window
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(640, 480)

    # Create an interactor and start rendering
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)

    interactor.Initialize()
    renderWindow.Render()
    interactor.Start()

if __name__ == "__main__":
    main()

