import unittest
import genome
import numpy as np
from xml.dom.minidom import getDOMImplementation



class GenomeTest(unittest.TestCase):
    def testClassExists(self):
        self.assertIsNotNone(genome.Genome)

    def testRandomGene(self):
        self.assertIsNotNone(genome.Genome.get_random_gene)

    def testRandomGeneNotNone(self):
        self.assertIsNotNone(genome.Genome.get_random_gene(5))

    def testRandomGeneHasValues(self):
        gene = genome.Genome.get_random_gene(5)
        #print("Random Gene:", gene)
        self.assertIsNotNone(gene[0])


    def testRandomGeneLength(self):
        gene = genome.Genome.get_random_gene(20)
        #print("Random Gene:", gene)
        self.assertEqual(len(gene), 20)

    def testRandomGeneIsNumpyArray(self):
        gene = genome.Genome.get_random_gene(20)
        #print("Random Gene:", gene)
        self.assertEqual(type(gene), np.ndarray)

    
    def testRandomeGenomeExists(self):
        data = genome.Genome.get_random_genome(20,5)
        self.assertIsNotNone(genome.Genome)
        self.assertIsNotNone(data)

    def testGeneSpecExist(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec)

    #Code added on 01-July-2026
    #Method to test the index of link length in the gene array
    def testGeneSpecHasLinkLength(self):
        #Spec is returning gene array
        spec = genome.Genome.get_gene_spec()
        #print("Specification of Gene:",spec)
        #test the index of link length in the gene array
        self.assertIsNotNone(spec["link-length"]["ind"])

    def testGeneSpecScale(self):
        spec = genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(20)
        #To pull value from gene using specs
        self.assertGreater(gene[spec["link-length"]["ind"]], 0)

#Test to check if the URDFLink class is working properly - Flat Link - Phase-1
    def testFlatLinks(self):
        links = [
            genome.URDFLink(name="A", parent_name=None,recur=1),
            genome.URDFLink(name="B", parent_name="A",recur=1),
            genome.URDFLink(name="C", parent_name="B",recur=2),
            genome.URDFLink(name="D", parent_name="C",recur=1)
        ]

        self.assertIsNotNone(links)

#Phase :2 : Generation of Expanded Links - Recursion - Phase-2
        def testExpandLinks(self):
            links = [
                genome.URDFLink(name="A", parent_name="None",recur=1),
                genome.URDFLink(name="B", parent_name="A",recur=1),
                genome.URDFLink(name="C", parent_name="B",recur=2),
                genome.URDFLink(name="D", parent_name="C",recur=1)
        ]
        expanded_links = [links[0]]  # Start with the root link
#Passing Parent Link, flat link and expanded link to the function to generate expanded links
        genome.Genome.expandlinks(links[0],links[0].name, links,expanded_links)
        #List Comprehension to get the names of the links in the expanded_links list
        names = [l.name +"  Parent Name:  " + str(l.parent_name) for l in expanded_links] 
        #['A  Parent Name:  None', 'B1  Parent Name:  A', 'C2  Parent Name:  B1', 'D3  Parent Name:  C2', 'C4  Parent Name:  B1', 'D5  Parent Name:  C4']
        print(names) 
        #Name of Expanded Links: ['A', 'B', 'C', 'D', 'C', 'D']
        #URDF can't have same link name, its unique name problem
        #Name of Expanded Links: ['A', 'B1', 'C2', 'D3', 'C4', 'D5']
        self.assertEqual(len(expanded_links), 6)  


    #Test Case for converting Genome [ numbers] into Dictionary for URDF Generation
    def testGeneToGeneDict(self):
        spec =genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(len(spec))
        gene_dict = genome.Genome.get_gene_dict(gene, spec)
        #Check if the gene_dict has the key "link-length" and its value is not None
        self.assertIn( "link-recurrence",gene_dict)

    def testGenomeToDict(self):
        spec =genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 3)
        #Dictionary of Genes for each gene in genome.
        genome_dicts = genome.Genome.get_genome_dicts(dna,spec)
        self.assertEqual(len(genome_dicts), 3)

    def testGetLinks(self):
        spec =genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 3)
        genome_dicts = genome.Genome.get_genome_dicts(dna,spec)
        links = genome.Genome.genome_to_links(genome_dicts)
        #Generation of flat links from genome dictionary, the number of links should be 3
        self.assertEqual(len(links), 3)

#Code added on 03-July-2026
#To generate link for XML File
    def testLinkToXML(self):
        #URDF class require three parameters to generate link, name, parent_name and recur, 
        #Remaining parameters are optional, if not provided, default values will be used.
        link = genome.URDFLink(name="A", parent_name="None",recur=1)
        domimpl = getDOMImplementation()
        adom = domimpl.createDocument(None, "robot", None)
        xml_str = link.to_link_xml(adom)
        print("Printing XML for Links", xml_str.toprettyxml())
        self.assertIsNotNone(xml_str)


#Generating Joint Element for XML File.

    def testJointElementToXML(self):
        #URDF class require three parameters to generate link, name, parent_name and recur, 
        #Remaining parameters are optional, if not provided, default values will be used.
        link = genome.URDFLink(name="A", parent_name="None",recur=1)
        domimpl = getDOMImplementation()
        adom = domimpl.createDocument(None, "robot", None)
        xml_str = link.to_joint_element(adom)
        print("Printing XML for Joint", xml_str.toprettyxml())
        self.assertIsNotNone(xml_str)

unittest.main()