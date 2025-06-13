from random import randint, random

class Genome:
    def __init__(self, data=None):
        if data is None:
            self.data = [randint(0, 255) for _ in range(10)]
        else:
            self.data = data

    def mutate(self, mutation_rate=0.1):
        for i in range(len(self.data)):
            if random() < mutation_rate:
                self.data[i] = randint(0, 255)
    
    def copy(self):
        return Genome(self.data.copy())
    
    def to_color(self):
        return (self.data[0], self.data[1], self.data[2])
    
    def to_shape(self):
        return self.data[3] % 3

    def to_behavior(self):
        return {
            "aggression": self.data[7] / 255,
            "curiosity": self.data[8] / 255,
            "social": self.data[9] / 255,
        }

    def to_stats(self):
        return {
            "speed": self.data[4] / 255,
            "vision": 1 + self.data[5] % 4 + 1,
            "energy": self.data[6] / 20 * 100 ,

        }