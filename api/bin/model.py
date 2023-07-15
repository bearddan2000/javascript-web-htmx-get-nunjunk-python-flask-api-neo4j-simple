from py2neo import Graph, Node, Relationship
from datetime import datetime
import os
import uuid

class DbModel():
    
    def __init__(self) -> None:
        self.seed()

    def connect(self) -> Graph:
        url = 'bolt://db:7687'
        username = os.environ['NEO4J_AUTH'].split('/')[0]
        password = os.environ['NEO4J_AUTH'].split('/')[1]

        return Graph(url + '/neo4j/', auth=(username, password))

    def decorate_result(self, cipher) -> dict:
        res = self.connect().run(cipher).data()
        return {'results': res}

    def match(self, where:str = None) -> dict:
        cipher: list = []
        cipher.append("MATCH(n:Dog) - [:BREED_OF] -> (b:Breed)")
        cipher.append("MATCH(n:Dog) - [:COLOR_OF] -> (c:Color)")
        if where is not None:
            cipher.append(where)
        cipher.append("RETURN DISTINCT n.name AS name, b.breed AS breed, c.color AS color")
        return self.decorate_result(" ".join(cipher))

    def get_all(self) -> list:
        return self.match()
    
    def filter_by_name(self, name):
        where: str = f"WHERE n.name = '{name}'"        
        return self.match(where)
    
    def filter_by_breed(self, name):
        where: str = f"WHERE b.breed = '{name}'"        
        return self.match(where)
    
    def filter_by_color(self, name):
        where: str = f"WHERE c.color = '{name}'"        
        return self.match(where)

    def seed_create(self, graph: Graph, node_name: str, lst: list):
        for val in lst:
            node = Node(node_name, id=str(uuid.uuid4()), name=val)
            graph.create(node)

    def seed(self):
        dog_list = [
            {'name': 'Fido', 'breed': [0], 'color': [2]}, 
            {'name': 'Perro', 'breed': [1], 'color': [0,1]}, 
            {'name': 'Chien', 'breed': [1], 'color': [2]}, 
            {'name': 'Hund', 'breed': [0], 'color': [0]} 
        ]
        breed_list = [
            Node('Breed', id=str(uuid.uuid4()), breed='Bulldog'), 
            Node('Breed', id=str(uuid.uuid4()), breed='Shepard')
        ]
        color_list = [
            Node('Color', id=str(uuid.uuid4()), color='Black'), 
            Node('Color', id=str(uuid.uuid4()), color='Brown'),
            Node('Color', id=str(uuid.uuid4()), color='White')
        ]
        graph=self.connect()

        for val in dog_list:
            dog = Node('Dog', id=str(uuid.uuid4()), name=val['name'])
            graph.create(dog)
            for breed in val['breed']:
                breed_rel = Relationship(dog, 'BREED_OF', breed_list[breed])
                graph.create(breed_rel)
            for color in val['color']:
                color_rel = Relationship(dog, 'COLOR_OF', color_list[color])
                graph.create(color_rel)