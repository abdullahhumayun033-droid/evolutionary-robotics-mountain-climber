
import numpy as np
import copy

class Genome():
    @staticmethod

    def get_random_gene(length):
        #Generating random gene for generation of genome 
        gene = np.array([np.random.random() for _ in range(length)])
        return gene

    @staticmethod
    def get_random_genome(gene_length, gene_count):
        genome =[Genome.get_random_gene(gene_length) for _ in range(gene_count)]
        #print ("Random Genome Generated from Gene",genome)
        return genome

#Code added on 01-July-2026
#Implementing Genome Specs: Generate Descriptor or Dictionary from param.txt file
#We have now have a working random genome generator and a basic genome specification.
#The gene specs will be used to generate set of links and joints later on.
#specification.

    @staticmethod
    def get_gene_spec():
        #Scale is definining how much the gene can vary. 
        #For example, if the scale is 1, then the gene can vary from 0 to 1. 
        #If the scale is 0.5, then the gene can vary from 0 to 0.5.
        gene_spec = {"link-shape":{"scale":1},
            "link-length": {"scale":1},
            "link-radius": {"scale":1},
            "link-recurrence": {"scale":4}, #Can have upto 4 links in a robot in recurrsion
            "link-mass": {"scale":1},
            "joint-type": {"scale":1},
            "joint-parent":{"scale":1},
            "joint-axis-xyz": {"scale":1},
            "joint-origin-rpy-1":{"scale":np.pi * 2}, #Control rotation in radians.
            "joint-origin-rpy-2":{"scale":np.pi * 2}, #Control rotation in radians.
            "joint-origin-rpy-3":{"scale":np.pi * 2}, #Control rotation in radians.
            "joint-origin-xyz-1":{"scale":1}, #How far the joint is from parent link in x,y,z direction. This is the offset of the joint from the parent link.
            "joint-origin-xyz-2":{"scale":1},
            "joint-origin-xyz-3":{"scale":1},
            "control-waveform":{"scale":1},
            "control-amp":{"scale":0.25}, #Maximum speed of motor
            "control-freq":{"scale":1} #Maximum frequency of motor
            }
        
        
        ind = 0
        for key in gene_spec.keys():
            gene_spec[key]["ind"] = ind
            ind = ind + 1
        return gene_spec

    #Function to convert genome [ numbers ] into URDF Dictionary for URDF Generation
    @staticmethod
    def get_gene_dict(gene,spec):
        gdict = {}
        for key in spec:
            #To pull value from gene using specs
            ind = spec[key]["ind"]
            scale = spec[key]["scale"]
            gdict[key] = gene[ind] * scale
        return gdict

    @staticmethod
    def get_genome_dicts(genome,spec):
        gdicts = []
        for gene in genome:
            gdicts.append(Genome.get_gene_dict(gene,spec))
        return gdicts

#Code added on 02-July-2026
    @staticmethod
    def genome_to_links(gdicts):
        link_ind = 0
        #Name of First Link
        parent_names = [str(link_ind)]
        links = []
        for gdict in gdicts:
            link_ind = link_ind + 1
            link_name = str(link_ind)
            #From Gene Spec
            parent_ind = gdict["joint-parent"] * len(parent_names)
            recur = gdict["link-recurrence"]
            parent_name=parent_names[int(parent_ind)]
            #Calling constructor of URDFLink class to create link object
            link = URDFLink(name=link_name,
                            parent_name=parent_name,
                            recur=recur+1,
                            link_length=gdict["link-length"], 
                            link_radius=gdict["link-radius"], 
                            link_mass=gdict["link-mass"],
                            joint_type=gdict["joint-type"],
                            joint_parent=gdict["joint-parent"],
                            joint_axis_xyz=gdict["joint-axis-xyz"],
                            joint_origin_rpy_1=gdict["joint-origin-rpy-1"],
                            joint_origin_rpy_2=gdict["joint-origin-rpy-2"],
                            joint_origin_rpy_3=gdict["joint-origin-rpy-3"],
                            joint_origin_xyz_1=gdict["joint-origin-xyz-1"],
                            joint_origin_xyz_2=gdict["joint-origin-xyz-2"],
                            joint_origin_xyz_3=gdict["joint-origin-xyz-3"],
                            control_waveform=gdict["control-waveform"],
                            control_amp=gdict["control-amp"],
                            control_freq=gdict["control-freq"])
            links.append(link)
            #First available Parent Name is added to the list of parent names for next link 
            #to be created.
            if link_ind != 0:# don't re-add the first link
                parent_names.append(link_name)
            link_ind = link_ind + 1

        # now just fix the first link so it links to nothing and avoid
        #Double parent name for the first link. This is important for URDF generation.
        links[0].parent_name = "None"
        return links
                    

#Writing Phase 2 to generate expanded links from Flat links to be used in URDF generation.

    @staticmethod
    def expandlinks(parent_link, uniq_parent_name,flat_links, exp_links):
        #It will return child of the parent link, in the beginning it will return A and so on.   
        children = [link for link in flat_links if link.parent_name == parent_link.name]
        sibling_ind = 1
        print("Parent:", parent_link.name)

        for link in flat_links:
                print(link.name, "parent =", link.parent_name)
        for c in children:
            for i in range(int(c.recur)):
                sibling_ind = sibling_ind +  1
                c_copy=copy.copy(c)
                c_copy.parent_name = uniq_parent_name
                #Unique name for the link to avoid duplicate names in URDF
                uniq_name = c_copy.name + str(len(exp_links)) 
                c_copy.name = uniq_name
                #Links will have proper sibling index to rotate
                c_copy.sibling_ind = sibling_ind
                exp_links.append(c_copy)
                Genome.expandlinks(c,uniq_name,flat_links,exp_links)

#Class to handle URDF Link and Joint generation from genome. 
#This class will be used to generate the URDF file from the genome.

#Code added on 02-July-2026
class URDFLink():
    def __init__(self, name, parent_name, recur, 
                link_length=0.1, 
                link_radius=0.1, 
                link_mass=0.1,
                joint_type=0.1,
                joint_parent=0.1,
                joint_axis_xyz=0.1,
                joint_origin_rpy_1=0.1,
                joint_origin_rpy_2=0.1,
                joint_origin_rpy_3=0.1,
                joint_origin_xyz_1=0.1,
                joint_origin_xyz_2=0.1,
                joint_origin_xyz_3=0.1,
                control_waveform=0.1,
                control_amp=0.1,
                control_freq=0.1):
        self.name = name
        self.parent_name = parent_name
        self.recur = recur 
        self.link_length=link_length 
        self.link_radius=link_radius
        self.link_mass=link_mass
        self.joint_type=joint_type
        self.joint_parent=joint_parent
        self.joint_axis_xyz=joint_axis_xyz
        self.joint_origin_rpy_1=joint_origin_rpy_1
        self.joint_origin_rpy_2=joint_origin_rpy_2
        self.joint_origin_rpy_3=joint_origin_rpy_3
        self.joint_origin_xyz_1=joint_origin_xyz_1
        self.joint_origin_xyz_2=joint_origin_xyz_2
        self.joint_origin_xyz_3=joint_origin_xyz_3
        self.control_waveform=control_waveform
        self.control_amp=control_amp
        self.control_freq=control_freq
        self.sibling_ind = 1 #Solving Children Problem: Default value of sibling is one

#Adding function to generate link tag for XML
    def to_link_xml(self, adom):
        #         <link name="base_link">
        #     <visual>
        #       <geometry>
        #         <cylinder length="0.6" radius="0.25"/>
        #       </geometry>
        #     </visual>
        #     <collision>
        #       <geometry>
        #         <cylinder length="0.6" radius="0.25"/>
        #       </geometry>
        #     </collision>
        #     <inertial>
        # 	    <mass value="0.25"/>
        # 	    <inertia ixx="0.0003" iyy="0.0003" izz="0.0003" ixy="0" ixz="0" iyz="0"/>
        #     </inertial>
        #   </link>
  
        link_tag = adom.createElement("link")
        link_tag.setAttribute("name", self.name)
        vis_tag = adom.createElement("visual")
        geom_tag = adom.createElement("geometry")
        cyl_tag = adom.createElement("cylinder")
        cyl_tag.setAttribute("length", str(self.link_length))
        cyl_tag.setAttribute("radius", str(self.link_radius))
        
        geom_tag.appendChild(cyl_tag)
        vis_tag.appendChild(geom_tag)
        link_tag.appendChild(vis_tag)
        #return link_tag.toprettyxml()
        
        coll_tag = adom.createElement("collision")
        c_geom_tag = adom.createElement("geometry")
        c_cyl_tag = adom.createElement("cylinder")
        c_cyl_tag.setAttribute("length", str(self.link_length))
        c_cyl_tag.setAttribute("radius", str(self.link_radius))
        
        c_geom_tag.appendChild(c_cyl_tag)
        coll_tag.appendChild(c_geom_tag)
        
        #     <inertial>
        # 	    <mass value="0.25"/>
        # 	    <inertia ixx="0.0003" iyy="0.0003" izz="0.0003" ixy="0" ixz="0" iyz="0"/>
        #     </inertial>
        inertial_tag = adom.createElement("inertial")
        mass_tag = adom.createElement("mass")
        # pi r^2 * height
        mass = np.pi * (self.link_radius * self.link_radius) * self.link_length
        mass_tag.setAttribute("value", str(mass))
        inertia_tag = adom.createElement("inertia")
        # <inertia ixx="0.0003" iyy="0.0003" izz="0.0003" ixy="0" ixz="0" iyz="0"/>
        inertia_tag.setAttribute("ixx", "0.03")
        inertia_tag.setAttribute("iyy", "0.03")
        inertia_tag.setAttribute("izz", "0.03")
        inertia_tag.setAttribute("ixy", "0")
        inertia_tag.setAttribute("ixz", "0")
        inertia_tag.setAttribute("iyx", "0")
        inertial_tag.appendChild(mass_tag)
        inertial_tag.appendChild(inertia_tag)
        

        link_tag.appendChild(vis_tag)
        link_tag.appendChild(coll_tag)
        link_tag.appendChild(inertial_tag)
        
        return link_tag

    #XML for Joint Tag in XML
    def to_joint_element(self, adom):
        #           <joint name="base_to_sub2" type="revolute">
        #     <parent link="base_link"/>
        #     <child link="sub_link2"/>
        #     <axis xyz="1 0 0"/>
        #     <limit effort="10" upper="0" lower="10" velocity="1"/>
        #     <origin rpy="0 0 0" xyz="0 0.5 0"/>
        #   </joint>
        joint_tag = adom.createElement("joint")
        joint_tag.setAttribute("name", self.name + "_to_" + self.parent_name)
        if self.joint_type >= 0.5:
            joint_tag.setAttribute("type", "revolute")
        else:
            joint_tag.setAttribute("type", "fixed")
        parent_tag = adom.createElement("parent")
        parent_tag.setAttribute("link", self.parent_name)
        child_tag = adom.createElement("child")
        child_tag.setAttribute("link", self.name)
        axis_tag = adom.createElement("axis")
        if self.joint_axis_xyz <= 0.33:
            axis_tag.setAttribute("xyz", "1 0 0")
        if self.joint_axis_xyz > 0.33 and self.joint_axis_xyz <= 0.66:
            axis_tag.setAttribute("xyz", "0 1 0")
        if self.joint_axis_xyz > 0.66:
            axis_tag.setAttribute("xyz", "0 0 1")
        
        limit_tag = adom.createElement("limit")
        # effort upper lower velocity
        limit_tag.setAttribute("effort", "1")
        limit_tag.setAttribute("upper", "-3.1415")
        limit_tag.setAttribute("lower", "3.1415")
        limit_tag.setAttribute("velocity", "1")
        # <origin rpy="0 0 0" xyz="0 0.5 0"/>
        #Parameter to link to be placed relative to parent link. 
        #This is the offset of the joint from the parent link.
        orig_tag = adom.createElement("origin")
        
        #To double check the rotation of the joint,
        #we can use the sibling index to multiply the rotation. This will ensure that the joint is 
        #rotated correctly relative to its parent link.
        #Rotation will increase if there more siblings (value of sibling_ind is more)
        rpy1 = self.joint_origin_rpy_1 * self.sibling_ind 
        rpy = str(rpy1) + " " + str(self.joint_origin_rpy_2) + " " + str(self.joint_origin_rpy_3)
        
        orig_tag.setAttribute("rpy", rpy)
        xyz = str(self.joint_origin_xyz_1) + " " + str(self.joint_origin_xyz_2) + " " + str(self.joint_origin_xyz_3)
        orig_tag.setAttribute("xyz", xyz)

        joint_tag.appendChild(parent_tag)
        joint_tag.appendChild(child_tag)
        joint_tag.appendChild(axis_tag)
        joint_tag.appendChild(limit_tag)
        joint_tag.appendChild(orig_tag)
        return joint_tag
            
    