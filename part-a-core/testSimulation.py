#Code added on 06-July-2026
import unittest
import simulation
import creature
import os
import population

class TestSim(unittest.TestCase):
    def testSimExists(self):
        sim = simulation.Simulation()
        self.assertIsNotNone(sim)

    #Checking for multiple Physics Engine (clientid)
    def testSimId(self):
        sim = simulation.Simulation()
        self.assertIsNotNone(sim.physicsClientId)

    #Test to run the creature
    def testRun(self):
        sim = simulation.Simulation()
        #cr = creature.Creature(gene_count=3)
        self.assertIsNotNone(sim.run_creature)

    #Test to check if creature is written to disk
    def testRunXML(self):
        sim = simulation.Simulation()
        cr = creature.Creature(gene_count=3)
        sim.run_creature(cr)
        #To verify URDF file written to the disk
        self.assertTrue(os.path.exists('temp_06_July.urdf'))


        #Test to check if creature position is changed during simulation or not
    def testRunPos(self):
        sim = simulation.Simulation()
        cr = creature.Creature(gene_count=3)
        sim.run_creature(cr)
        
        print("Creature Start Position", cr.start_position)
        print("Creature Last Position", cr.last_position)

        #3D position of the robot's base link: (x, y, z)
        #x = left/right (or forward/backward depending on your world orientation)
        #y = sideways
        #z = height above the world origin
        #(1.3820470119809255e-20, 1.76722871828601e-21, -0.00017361111111111112) mean:
        #x ≈ 0.0,y ≈ 0.0,z ≈ -0.00017
        #robot starts approximately at: 0,0,0

        #Last Position:(0.025488429377183566,  -0.006671690235010319,  -136.74819217342397)
        #x = 0.0255 m,y = -0.0067 m,z = -136.75 m
        #The robot moved 2.5 cm in the x-direction.
        #It moved 0.67 cm in the negative y-direction.
        #It fell 136.75 meters below the world origin

        #To return true if start position and last position is not same and creature has moved
        self.assertNotEqual(cr.start_position, cr.last_position)

    def testDist(self):
        sim = simulation.Simulation()
        cr = creature.Creature(gene_count=3)
        sim.run_creature(cr)
        dist = cr.get_distance_travelled()
        print("Distance: " , dist)
        #To return true if distance travelled is greater than 0
        self.assertGreater(dist,0)

    #Fitness Function is distance travelled.
    def testPop(self):
        pop = population.Population(pop_size=100, gene_count=3)
        sim = simulation.Simulation()

        for cr in pop.creature:
            sim.run_creature(cr)

        dists = [cr.get_distance_travelled() for cr in pop.creature]
        print ("distance" , dists)
        self.assertIsNotNone(dists)

    

unittest.main()