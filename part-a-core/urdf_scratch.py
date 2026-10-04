import pybullet as p
import pybullet_data
try:
    p.connect(p.GUI)
    p.setPhysicsEngineParameter(enableFileCaching=0)
    plane_shape = p.createCollisionShape(p.GEOM_PLANE)
    floor = p.createMultiBody(plane_shape, plane_shape)
    p.setGravity(0,0,-5)
    print(pybullet_data.getDataPath())
    robot2 = p.loadURDF(
        r"C:\Users\SherazPervaiz\AI-26\Week-7\101.urdf"
    )
    p.setRealTimeSimulation(1)
    input("Press Enter to exit...")
except Exception as e:
    print("ERROR:", e)
    input("Press Enter to close...")