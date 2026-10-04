import creature


class Population():
    def __init__(self, pop_size, gene_count):
         self.creature = [creature.Creature(gene_count=gene_count) for i in range(pop_size)]
         print("Generated 10 creatures from creature class", self.creature)