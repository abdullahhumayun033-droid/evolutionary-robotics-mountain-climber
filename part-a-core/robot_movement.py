#Pybullet Documenation: https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA/edit?tab=t.0#heading=h.2ye70wns7io3
import pybullet as p
import pybullet_data

try:
    p.connect(p.GUI)

    p.setPhysicsEngineParameter(enableFileCaching=0)

    plane_shape = p.createCollisionShape(p.GEOM_PLANE)
    floor = p.createMultiBody(plane_shape, plane_shape)

    p.setGravity(0,0,-9.81)

    print(pybullet_data.getDataPath())

    robot2 = p.loadURDF(
        r"C:\Users\SherazPervaiz\AI-26\URDF and RobotMovement\102.urdf"
    )

    p.setRealTimeSimulation(1)
    #Putting Robot at x,y,x =0,0,1 - Slightly in the Air
    #Orientaiton in 4D = 0,0,0,1
    p.resetBasePositionAndOrientation(robot2, [0, 0, 2], [0, 0, 0, 1])
    #Adding Motor Control to the Joint
    #Joint Index = 0 (First Joint), Control Mode = VELOCITY_CONTROL, Target Velocity = 1.0
    #Robot is moving slightly 
    #Speed Control of the Robot of first joint
    p.setJointMotorControl2(robot2, 0, p.VELOCITY_CONTROL, targetVelocity=0.9)
    #Speed Control of the Robot of second joint
    p.setJointMotorControl2(robot2, 1, p.VELOCITY_CONTROL, targetVelocity=0.9)

    #p.setJointMotorControl2(robot2, 0, p.VELOCITY_CONTROL, targetVelocity=0.1, force=10)

    #Moving the Robot to a specific position
    #p.setJointMotorControl2(robot2, 0, p.POSITION_CONTROL, targetVelocity=10,targetPosition=0.5)

    input("Press Enter to exit...")

except Exception as e:
    print("ERROR:", e)
    input("Press Enter to close...")