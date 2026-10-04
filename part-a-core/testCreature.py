import unittest
import creature
import pybullet as p
import genome

class TestCreature(unittest.TestCase):
    def testcreatureExist(self):
        self.assertIsNotNone(creature.Creature)

    #Test to check if the Creature class is working properly - Flat Link - Phase-1
    def testCreatureGetFlatLinks(self):
        #Create a creature object with 4 genes
        c = creature.Creature(gene_count=4)
        #Get the flat links of the creature
        links = c.get_flat_links()
        self.assertEqual(len(links), 4)
        print("Flat Links in Creature Class is working properly. Number of links:", len(links))


    #Test to check if the Creature class is working properly - Expanded Link - Phase-2
    """
    def testExpLinks(self):
        #Create a creature object with 4 genes
        
            c = creature.Creature(gene_count=4)
            #Get the flat links of the creature
            links = c.get_flat_links()
            exp_links = c.get_expanded_links()
            print("Expanded Links in Creature Class is working properly. Number of links:", len(exp_links))
            self.assertGreaterEqual(len(links), len(exp_links))
    """
    #To Test if URDF file is generated properly from the Creature class
    def testToXML(self):
        c = creature.Creature(gene_count=4)
        c.get_expanded_links()
        xml_str = c.to_xml()
        with open('103.urdf', 'w') as f:
            f.write('<?xml version="1.0"?>' + "\n" +xml_str)
        self.assertIsNotNone(xml_str)
        print("XML generation in Creature Class is working properly. XML String:", xml_str)

    #Loading the 103.urdf file in pybyllet to check if the URDF file is valid and can be loaded in pybullet
    """
    def testLoadXML(self):
        c = creature.Creature(gene_count=20)
        xml_str = c.to_xml()
        with open('104.urdf', 'w') as f:
            f.write(xml_str)
        print("File 103.urdf is generated and saved in the current directory.")
        p.connect(p.GUI)
        cid = p.loadURDF(r'/Users/syedabdullahhumayun/Downloads/Robot/104.urdf')

        print("URDF file is loaded in pybullet. Client ID:", cid)
        p.setRealTimeSimulation(1)
        input("Press Enter to exit...")
        self.assertIsNotNone(cid)
    
    #Testing the overlap of child problem
    def testRadial(self):
        links = [
            #Code should show one parent link :A, two child links B connected to A, two big long links 
            #should be shown
                genome.URDFLink(name="A", parent_name="None",recur=1),
                #Setting up rotation of 0.75 and lenght of 1.0
                genome.URDFLink(name="B", parent_name="A",recur=6,joint_origin_rpy_1=0.75,link_length=5.0),
                ]
        c = creature.Creature(gene_count=2)
        c.flat_links = links
        c.get_expanded_links()
        xml_str = c.to_xml()
        with open('105.urdf', 'w') as f:
            f.write('<?xml version="1.0"?>' + "\n" +xml_str)
        #self.assertIsNotNone(xml_str)

        p.connect(p.GUI)
        cid = p.loadURDF(r'/Users/syedabdullahhumayun/Downloads/Robot/105.urdf')

        print("URDF file is loaded in pybullet. Client ID:", cid)
        p.setRealTimeSimulation(1)
        input("Press Enter to exit...")
        self.assertIsNotNone(cid)

"""
    #Writing code to test motor
    def testMotor(self):
        m = creature.Motor(0.1, 0.5, 0.5)
        self.assertIsNotNone(m)

#Writing test for get_output method for Pulse Wave
    def testMotorVal(self):
        m = creature.Motor(0.1, 0.5, 0.5)
        print("Value of M  in Pulse Wave",m)
        self.assertEqual(m.get_output(),1)


#Writing test for get_output method for Sine Wave
    def testMotorVal2(self):
        m = creature.Motor(0.6, 0.5, 0.5)
        m.get_output()
        print("Value of M  in Sine Wave",m)
        m.get_output()
        print("Value of M  in Sine Wave",m)

        self.assertGreater(m.get_output(),0)


    def testCMot(self):
        c = creature.Creature(gene_count = 4)
        ls = c.get_expanded_links()
        ms = c.get_motors()
        self.assertEqual(len(ls)-1, len(ms))

unittest.main()