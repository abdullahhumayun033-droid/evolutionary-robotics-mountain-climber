import pybullet as p
import pybullet_data as pd
import time
import creature
p.connect(p.GUI)
p.setPhysicsEngineParameter(enableFileCaching=0)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)
p.setGravity(0,0,-10)
c = creature.Creature(gene_count = 5)
with open('test.urdf' , 'w') as f:
    c.get_expanded_links()
    f.write(c.to_xml())
#Loading the generated XML
cid = p.loadURDF(r'/Users/syedabdullahhumayun/Downloads/Robot/test.urdf')


p.setRealTimeSimulation(1)

#Setting creature to start from 0,0,0
#Code added on 06-July-2026
c.update_position([0,0,0])
#0,0,3 is slighthly above the ground: z,x,y
p.resetBasePositionAndOrientation(cid,[0,0,3],[0,0,1,0])
while True:
    for jid in range(p.getNumJoints(cid)):
       
        #Get motor for that particular Joint
        m = c.get_motors()[jid]
        p.setJointMotorControl2(cid, jid , 
                    controlMode = p.VELOCITY_CONTROL,
                    targetVelocity =m.get_output(), force = 5)
    
    #Update the Motor after every 10th of a second. Motor will keep running and 
    #speed will be changed after every 10th of second
    p.stepSimulation()
    pos, orn = p.getBasePositionAndOrientation(cid)
    c.update_position(pos)
    print("Distance Travelled",c.get_distance_travelled())
    time.sleep(0.1)

input("Press Enter to exit...")

