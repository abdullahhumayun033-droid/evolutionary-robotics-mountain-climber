#Code added on 06-July-2026
import pybullet as p
class Simulation():
    def __init__(self):

#p.Direct will run physics Engine offline in multi-processor
        self.physicsClientId = p.connect(p.GUI)
        
    #Pybullet update physics engine 240 time per second: 
    #2400 is 10 sec of simulation
    def run_creature(self, cr, iteration=2400):
        pid = self.physicsClientId
        p.resetSimulation(physicsClientId=pid)
        #x,z,y
        p.setGravity (0,0,-10,physicsClientId=pid)
        p.setPhysicsEngineParameter(enableFileCaching=0,physicsClientId=pid)

        plane_shape = p.createCollisionShape(p.GEOM_PLANE, physicsClientId=pid)
        floor = p.createMultiBody(plane_shape, plane_shape, physicsClientId=pid)
        xml_file = 'temp_06_July.urdf'
        xml_str = cr.to_xml()
        #Writing XML file to Disk
        with open(xml_file, 'w') as f:
            f.write(xml_str)
        
        #Load the XML file back
        cid = p.loadURDF(xml_file, physicsClientId=pid)
        p.resetBasePositionAndOrientation(cid,[0,0,3],[0,0,1,0],physicsClientId=pid)

        #Running Step Simulation 2400 times
        for step in range(iteration):
            p.stepSimulation(physicsClientId=pid)
            #To update motor after every 24 steps [ 1/10th of a second]
            
            if step%24==0:
                self.update_motors(cid=cid, cr=cr)

            #getBasePositionAndOrientation() is function defined in pybullet which return position 
            #and orientation
            pos, orn = p.getBasePositionAndOrientation(cid, physicsClientId=pid)
            cr.update_position(pos)
            #if step>0:
             #   print(cr.last_position[2]) #Displaying y position
                
                #print ("Updating the simulation after 24 steps", count)

    
    #Update Motor Function
    def update_motors(self, cid, cr):
        """
        cid is the id in the physics engine
        cr is the creature object
        """
        #For Loop is iterating over all the joints in creature - XML file
        for jid in range(p.getNumJoints(cid,physicsClientId = self.physicsClientId)):
       
        #Get motor for that particular Joint
            m = cr.get_motors()[jid]
            p.setJointMotorControl2(cid, jid , 
                        controlMode = p.VELOCITY_CONTROL,
                        targetVelocity =m.get_output(), force = 5,
                        physicsClientId = self.physicsClientId)
