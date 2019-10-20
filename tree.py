from enum import Enum
from graphviz import Source


class Sex(Enum):
    male = "M"
    female = "F"


class Individual:
    '''Builds up an individual and their relationships.'''

    def __init__(self, info):
        self.firstname = info['firstname']
        self.surname = info['surname']
        self.sex = info['sex']
        self.dob = info['dob']
        self.name = self.firstname+ self.surname
        self.children = []
        self.siblings = []
        self.mother = ''
        self.father= ''
        self.partner = ''

    def __str__(self):
        return self.name

    def getPartner(self, person):
        if person.children:
            for child in children:
                if self.sex == Sex.female:
                    partner = child.getFather
                else:
                    partner = child.getMother

    def setMother(self, mother):
        self.mother = mother
        if not self in mother.children:
            mother.addChild(self)

    def setFather(self, father):
        self.father = father
        if not self in father.children:
            father.addChild(self)

    def isParent(self):
        return self.children

    def addChild(self, child):
        self.children.append(child)
        if not child.mother and self.sex == Sex.female:
            child.setMother(self)
        if not child.father and self.sex == Sex.male:
            child.setFather(self)

    def addSibling(self, sibling):
        self.siblings.append(sibling)
        if not self in sibling.siblings:
            sibling.addSiblings(self)

    def addPartner(self, partner):
        self.partner = partner
        if not partner.partner == self:
            partner.addPartner(self)

    def graphviz(self):
        label = self.firstname+self.surname
        colour = 'rosybrown1' if self.sex == Sex.female else 'skyblue2'
        node = ['label="' + label + '"']
        node.append('style=filled')
        node.append('fillcolor=' + colour)
        return self.name + '[' + ','.join(node) + ']\n'


class Family:
    """Builds up the whole family together"""

    everyone= {}

    def addPerson(self, person):
        key = person.name
        self.everyone[key] = person

    def getPerson(self, name):
        for person in self.everyone.values():
            if person.name == name or person.firstname == name or person.surname == name:
                return person
        return None


    def outputTree(self):
        tree = ('digraph {\n' + \
              '\tnode [shape=box];\n')

        for person in self.everyone.values():
            tree = tree + "\t" + person.graphviz()

        for person in self.everyone.values():
            if person.partner :
                tree = tree + '\t{ rank=same ' + person.name + ' ' + person.partner.name+' } \n \t' + person.name + ' -> ' +  person.partner.name + ';\n'
            if person.children:
                for c in person.children:
                    tree = tree + "\t" + person.name + ' -> ' + c.name+ ';\n'
        tree = tree+ ('')

        tree = tree+ ('}')
        return tree


def main():
    family = Family()
    mother = Individual({'firstname': 'Mother', 'surname': 'test', 'sex': Sex.female, 'dob' : '03/09/1987'})
    father =Individual({'firstname': 'Father', 'surname': 'test', 'sex': Sex.male, 'dob' : '23/10/1988'})
    child = Individual({'firstname': 'Child', 'surname': 'test', 'sex': Sex.female, 'dob' : '11/01/2010'})
    father.addChild(child)
    mother.addChild(child)
    mother.addPartner(father)
    family.addPerson(mother)
    family.addPerson(father)
    family.addPerson(child)

    tree = family.outputTree()
    print(tree)
    s = Source(tree, filename="test.gv", format="png")
    s.view()

if __name__ == '__main__':
    main()
