import genome
from xml.dom.minidom import getDOMImplementation
from enum import Enum
import numpy as np

#Code added on 03-July && 04-July-2026
#Writing Motor enum class
class MotorType(Enum):
    PULSE = 1
    SINE = 2

#Writing Motor class to control movement
class Motor:
    def __init__(self,control_waveform, control_amp,control_freq):

        if control_waveform <=0.5:
            self.motor_type = MotorType.PULSE # Enum class
            print("Pulse Wave")
        else:
            self.motor_type = MotorType.SINE
            print("Sine Wave")
        self.amp = control_amp
        self.freq  = control_freq
        self.phase = 0

#Code added on 03-July && 04-July-2026
    def get_output(self):
                #Higher the frequency then more the phase get updated
                #When phase is going to 2pi then it will get back to 0 again
        self.phase = (self.phase + self.freq ) % (np.pi*2)
        #Checking for Pulse Wave Form
        if self.motor_type == MotorType.PULSE:
            if self.phase < np.pi:
                output = 1
            else:
                output = -1

        #Checking for Pulse Wave Form
        if self.motor_type == MotorType.SINE:
            output = np.sin(self.phase)
        return output


class Creature:
    def __init__(self, gene_count):
        #Generating DNA for the creature using genome class
        self.spec = genome.Genome.get_gene_spec()
        self.dna = genome.Genome.get_random_genome(len(self.spec),gene_count)
        self.flat_links=None
        self.motors=None
        #Change on 06-July-2026
        self.get_flat_links()
        self.get_expanded_links()
        #to measure the distance travelled from initial to last position
        self.start_position = None
        self.last_position = None



    #Convert DNA into flat links
    def get_flat_links(self):
        gdicts=genome.Genome.get_genome_dicts(self.dna,self.spec)
        self.flat_links = genome.Genome.genome_to_links(gdicts)
        return self.flat_links


    def get_expanded_links(self):
        self.get_flat_links()
        exp_links = [self.flat_links[0]] #To include Root link in the expanded links
        genome.Genome.expandlinks(self.flat_links[0],self.flat_links[0].name,
                                                    self.flat_links,exp_links)
        self.exp_links=exp_links
        return self.exp_links

    #Method to convert the creature into XML format for URDF generation
    def to_xml(self):
        self.get_expanded_links()

        domimpl = getDOMImplementation()
        adom = domimpl.createDocument(None, "robot", None)

        robot_tag = adom.documentElement

        for link in self.exp_links:
            robot_tag.appendChild(link.to_link_xml(adom))

        first = True
        for link in self.exp_links:
            if first:
                first = False
                continue
            robot_tag.appendChild(link.to_joint_element(adom))

        robot_tag.setAttribute("name", "pepe")
        return robot_tag.toprettyxml()
        
#Code added on 03-July && 04-July-2026
    #Method for creature to get Motor
    def get_motors(self):
        #Root link does not need Motor as it is not connected to any link
            if self.motors ==None:
                motors = []
                # Loop will run from second node to total lenght, excluding root
                for i in range (1, len(self.exp_links)):
                    l = self.exp_links[i]
                    m = Motor (l.control_waveform, l.control_amp, l.control_freq)
                    motors.append(m)
                self.motors = motors
            return self.motors

    #Code added on 06-July-2026
    #Function to calculate how far a creature is moved
    def update_position(self,pos):
        if self.start_position == None:
            self.start_position = pos
        else:
            self.last_position = pos

    #Method to find out how much distance object has travelled
    def get_distance_travelled(self):
        p1=np.array(self.start_position)
        p2=np.array(self.last_position)
        #Using Euclidean distance to measure 
        return np.linalg.norm(p1-p2)