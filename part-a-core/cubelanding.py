#Install Python version 3.12 but not above to install pybullet
#pip install pybullet
#Download python 3.12 from https://www.python.org/downloads/windows/
#Install Visual Studio Build Tools from https://visualstudio.microsoft.com/visual-cpp-build-tools/
#When the installer opens:
#Select "Desktop development with C++"
#Make sure these are checked:
#MSVC v143 (or latest) C++ Build Tools
#Windows 10/11 SDK
#C++ CMake tools for Windows (optional but recommended)

import pybullet as p
p.connect(p.GUI)
#Important: We need to create seperate gemometry for visual and collission shapes. 
#Otherwise, the visual and collision shapes will be linked together and we won't be able to move them independently.
#It will create 2D plane which can be placed in the environment.
plane_shape = p.createCollisionShape(p.GEOM_PLANE)
#createMultibody is build in function to combine multiple geometries combined
#Connected together in different ways. 
#Floor_shape for visual geometry and floor_shapre for collission geometry.
floor = p.createMultiBody(plane_shape, plane_shape)
p.setGravity(0,0,-9.81)
#Start the simulation in real time. This will allow us to see the box fall down due to gravity.
#Now the shape will be perfect cube. 
p.setRealTimeSimulation(1)
input("Press Enter to exit...")
