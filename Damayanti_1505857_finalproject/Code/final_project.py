import vtk
dir_ = r"CTDATA"

# Read data
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(dir_)
reader.Update()

renWin = vtk.vtkRenderWindow()
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)



# Create colour transfer function
colorFunc = vtk.vtkColorTransferFunction()
colorFunc.AddRGBPoint(-3024, 0.0, 0.0, 0.0)
colorFunc.AddRGBPoint(-77, 0.54902, 0.25098, 0.14902)
colorFunc.AddRGBPoint(94, 0.882353, 0.603922, 0.290196)
colorFunc.AddRGBPoint(179, 1, 0.937033, 0.954531)
colorFunc.AddRGBPoint(260, 0.615686, 0, 0)
colorFunc.AddRGBPoint(3071, 0.827451, 0.658824, 1)

# Create opacity transfer function
alphaChannelFunc = vtk.vtkPiecewiseFunction()
alphaChannelFunc.AddPoint(-3024, 0.0)
alphaChannelFunc.AddPoint(-77, 0.0)
alphaChannelFunc.AddPoint(94, 0.29)
alphaChannelFunc.AddPoint(179, 0.55)
alphaChannelFunc.AddPoint(260, 0.84)
alphaChannelFunc.AddPoint(3071, 0.875)

# Instantiate necessary classes and create VTK pipeline
volume = vtk.vtkVolume()
ren = vtk.vtkRenderer()
ren.SetViewport(0,0,0.6,1)
ren.SetBackground(0.1,0.2,0.4)



ren.AddVolume(volume)

RGB_tuples = [(1, 0, 0), (0, 1, 0), (0, 0, 1)] # define colors for plane outline


# Define volume mapper
volumeMapper = vtk.vtkSmartVolumeMapper()  
volumeMapper.SetInputConnection(reader.GetOutputPort())

# Define volume properties
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetScalarOpacity(alphaChannelFunc)
volumeProperty.SetColor(colorFunc)
volumeProperty.ShadeOn()

# Set the mapper and volume properties
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)
volume.Update()

renWin.AddRenderer(ren)
renWin.Render()



mapToColors = vtk.vtkImageMapToColors()
mapToColors.SetInputConnection(reader.GetOutputPort(0))
mapToColors.Update()

# A picker is used to get information about the volume
picker = vtk.vtkCellPicker()
picker.SetTolerance(0.005)

# Define plane widget
planeWidgetX = vtk.vtkImagePlaneWidget() 

 

# Set plane properties

planeWidgetX.SetInputConnection(mapToColors.GetOutputPort(0))
planeWidgetX.SetPlaneOrientation(0)
planeWidgetX.DisplayTextOn()
planeWidgetX.SetSliceIndex(100)
planeWidgetX.SetPicker(picker)
planeWidgetX.SetColorMap(mapToColors)
planeWidgetX.SetKeyPressActivationValue("x")
planeWidgetX.GetPlaneProperty().SetColor(RGB_tuples[0])



# Place plane widget and set interactor

planeWidgetX.SetCurrentRenderer(ren)
planeWidgetX.SetInteractor(iren)
planeWidgetX.PlaceWidget()

planeWidgetX.On()


#code for sliced portion
image = planeWidgetX.GetResliceOutput()
image.Modified()

actor = vtk.vtkImageActor()
actor.GetMapper().SetInputData(image) 
actor.Update()

# Place plane widget and set interactor

 

# Add the volume to the renderer
ren2 = vtk.vtkRenderer()
ren2.SetBackground(0,0,0)



ren2.AddActor(actor)
ren2.SetViewport(0.6,0.5,1,1)
ren2.ResetCamera()



renWin.AddRenderer(ren2)

renWin.Render()

# Set plane properties

planeWidgetY = vtk.vtkImagePlaneWidget()
planeWidgetY.SetInputConnection(mapToColors.GetOutputPort(0))
planeWidgetY.SetPlaneOrientation(1)
planeWidgetY.DisplayTextOn()
planeWidgetY.SetSliceIndex(100)
planeWidgetY.SetPicker(picker)
planeWidgetY.SetColorMap(mapToColors)
planeWidgetY.SetKeyPressActivationValue("y")
prop2 = planeWidgetY.GetPlaneProperty()
prop2.SetColor(1, 1, 0)
# Place plane widget and set interactor

planeWidgetY.SetCurrentRenderer(ren)
planeWidgetY.SetInteractor(iren)
planeWidgetY.PlaceWidget()
planeWidgetY.On()


#code for sliced portion
image2 = planeWidgetY.GetResliceOutput()
image2.Modified()

actor2 = vtk.vtkImageActor()
actor2.GetMapper().SetInputData(image2) 
actor2.Update()

ren3 = vtk.vtkRenderer()
ren3.SetBackground(0,0,0)



ren3.AddActor(actor2)
ren3.SetViewport(0.6,0,1,0.7)
ren3.ResetCamera()



renWin.AddRenderer(ren3)

renWin.Render()

#X and Y axes plane sliders
def slider_callback(obj, evt):
    #global image2, actor2
    value = obj.GetRepresentation().GetValue()
    planeWidgetX.SetSliceIndex(int(value))
    planeWidgetX.UpdatePlacement()
    renWin.Render()

def slider_callback2(obj, evt):
    #global image2, actor2
    value = obj.GetRepresentation().GetValue()
    planeWidgetY.SetSliceIndex(int(value))
    planeWidgetY.UpdatePlacement()
    renWin.Render()

sliderRep = vtk.vtkSliderRepresentation2D()
sliderWidget = vtk.vtkSliderWidget()

sliderRep.SetMinimumValue(0)
sliderRep.SetMaximumValue(200)
sliderRep.SetValue(50)
sliderRep.SetTitleText("X-Axis")
sliderRep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRep.GetPoint1Coordinate().SetValue(0.0,0.1)
sliderRep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRep.GetPoint2Coordinate().SetValue(0.2, 0.1)
sliderRep.SetSliderLength(0.0001)
sliderRep.SetSliderWidth(0.02)
sliderRep.SetEndCapLength(0.02)
sliderRep.SetTubeWidth(0.005)
sliderWidget.SetInteractor(iren)
sliderWidget.SetRepresentation(sliderRep)
sliderWidget.EnabledOn()
sliderWidget.AddObserver("InteractionEvent", slider_callback)


sliderRep2 = vtk.vtkSliderRepresentation2D()
sliderWidget2 = vtk.vtkSliderWidget()

sliderRep2.SetMinimumValue(0)
sliderRep2.SetMaximumValue(200)
sliderRep2.SetValue(50)
sliderRep2.SetTitleText("Y-Axis")
sliderRep2.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRep2.GetPoint1Coordinate().SetValue(0.3,0.1)
sliderRep2.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRep2.GetPoint2Coordinate().SetValue(0.5, 0.1)
sliderRep2.SetSliderLength(0.0001)
sliderRep2.SetSliderWidth(0.02)
sliderRep2.SetEndCapLength(0.02)
sliderRep2.SetTubeWidth(0.005)


sliderWidget2.SetInteractor(iren)
sliderWidget2.SetRepresentation(sliderRep2)
sliderWidget2.EnabledOn()
sliderWidget2.AddObserver("InteractionEvent", slider_callback2)



ren3.ResetCamera()
renWin.AddRenderer(ren3)
renWin.Render()

# Render the scene
renWin.SetSize(800,800)

renWin.Render()
iren.Initialize()
iren.Start()


