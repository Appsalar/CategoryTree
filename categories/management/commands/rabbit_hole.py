from collections import deque, defaultdict

from django.core.management.base import BaseCommand

from categories.models import Category, Similarity


class Command(BaseCommand):
    help = "Finds longest rabbit hole and all rabbit islands"

    def handle(self, *args, **options):
        categories = Category.objects.values_list("id", flat=True)
        similarities = Similarity.objects.values_list("firstCategory_id", "secondCategory_id")

        adjacencyList = createAdjacencyList(categories, similarities)
        # print(adjacencyList)

        paths, distance = findLongestRabbitHole(adjacencyList)
        rabbitIslands = findRabbitIslands(adjacencyList)

        print(f"The longest rabbit hole length is {distance} and the possible holes are {paths}")
        print(f"Rabbit islands are: {rabbitIslands}")


# a rabbit hole is the shortest route from one Category to another
# and longest rabbit hole is a diameter in graph
def findLongestRabbitHole(adjacencyList):
    maxDistancePaths = set()
    maxDistance = 0

    for node in adjacencyList:
        paths, visited = bfsAllShortestPaths(adjacencyList, node)
        # print(paths, visited)
        paths = sum(paths.values(), [])  # flatten

        distance = max(visited.values())

        if distance > maxDistance:
            maxDistancePaths = set([tuple(sorted(path)) for path in paths if len(path) == distance])
            maxDistance = distance
        elif distance == maxDistance:
            maxDistancePaths |= set([tuple(sorted(path)) for path in paths if len(path) == distance])

    return maxDistancePaths, maxDistance


def bfsAllShortestPaths(adjacencyList, startNode):
    queue = deque([(startNode, 1)])
    visited = {startNode: 1}
    paths = defaultdict(list)
    paths[startNode] = [[startNode]]

    while queue:
        currentNode, currentDistance = queue.popleft()

        for node in adjacencyList[currentNode]:
            if node not in visited:
                visited[node] = currentDistance + 1
                queue.append((node, currentDistance + 1))
                paths[node] = [path + [node] for path in paths[currentNode]]
            elif visited[node] == currentDistance + 1:
                paths[node].extend([path + [node] for path in paths[currentNode]])

    return paths, visited


# a rabbit island is a connected component
def findRabbitIslands(adjacencyList):
    visited = set()
    components = []

    for node in adjacencyList:
        if node not in visited:
            component = []
            bfsTraversalFromNode(node, adjacencyList, visited, component)
            components.append(component)

    return components


def bfsTraversalFromNode(startNode, adjacencyList, visited, component):
    queue = deque([startNode])
    visited.add(startNode)

    while queue:
        current = queue.popleft()
        component.append(current)

        for node in adjacencyList[current]:
            if node not in visited:
                visited.add(node)
                queue.append(node)


def createAdjacencyList(nodes, edges):
    adjacencyList = {node: [] for node in nodes}

    for edge in edges:
        node1, node2 = edge
        # print(adjacencyList)
        adjacencyList[node1].append(node2)
        adjacencyList[node2].append(node1)

    return adjacencyList
