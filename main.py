from typing import Callable, List, Optional, Tuple

#####################################################
# Authors: Pol Rubio Borrego, Lea Cornelis Martínez #
# Date: 2024-05-17 #
#####################################################

class InsufficientStockError(Exception):
    pass

class TreeNode:
    def __init__(self, name: str, ingredient: Optional['Ingredient'] = None, action: Optional[Callable[[], None]] = None, stock_check: bool = False):
        self.name: str = name
        self.ingredient: Optional['Ingredient'] = ingredient
        self.action: Optional[Callable[[], None]] = action
        self.stock_check: bool = stock_check
        self.children: List['TreeNode'] = []

    def add_child(self, child_node: 'TreeNode') -> None:
        self.children.append(child_node)


class Ingredient:
    def __init__(self, name: str, stock: int, quantity: int, position: Tuple[int, int]):
        self.name: str = name
        self.total_stock: int = stock
        self.stock: int = stock
        self.quantity: int = quantity
        self.position: Tuple[int, int] = position

    def use(self) -> None:
        if self.stock >= self.quantity:
            self.stock -= self.quantity
            print(f"{self.name} used. Remaining stock: {self.stock} units ({round((self.stock / self.total_stock) * 100, 2)}%)")
        else:
            raise InsufficientStockError(f"Insufficient stock for {self.name}")

    def check_stock(self) -> bool:
        return self.stock >= self.quantity

    def is_below_threshold(self, threshold_percentage: float = 20.0) -> bool:
        return (self.stock / self.total_stock) * 100 < threshold_percentage


class CooLex:
    def __init__(self, bowls: Ingredient, bases: List[Ingredient], proteins: List[Ingredient], toppings: List[Ingredient], sauces: List[Ingredient]):
        self.bowls: Ingredient = bowls
        self.bases: List[Ingredient] = bases
        self.proteins: List[Ingredient] = proteins
        self.toppings: List[Ingredient] = toppings
        self.sauces: List[Ingredient] = sauces
        self.root: TreeNode = self.create_tree()
        self.initial_position: Tuple[int, int] = (310, 310)
        self.bowl_dispenser_position: Tuple[int, int] = (650, 660)
        self.final_position: Tuple[int, int] = (410, 610)
        self.current_position: Tuple[int, int] = self.initial_position
        self.total_distance: float = 0.0

    def create_tree(self) -> TreeNode:
        root = TreeNode("Start")

        bowl_node = TreeNode("Bowl", ingredient=self.bowls, action=self.bowls.use, stock_check=True)
        root.add_child(bowl_node)

        base_nodes = [TreeNode(base.name, ingredient=base, action=base.use, stock_check=True) for base in self.bases]
        bowl_node.children.extend(base_nodes)

        for base_node in base_nodes:
            protein_nodes = [TreeNode(protein.name, ingredient=protein, action=protein.use, stock_check=True) for protein in self.proteins]
            base_node.children.extend(protein_nodes)

            for protein_node in protein_nodes:
                topping_nodes = [TreeNode(topping.name, ingredient=topping, action=topping.use, stock_check=True) for topping in self.toppings]
                protein_node.children.extend(topping_nodes)

                for topping_node in topping_nodes:
                    sauce_nodes = [TreeNode(sauce.name, ingredient=sauce, action=sauce.use, stock_check=True) for sauce in self.sauces]
                    topping_node.children.extend(sauce_nodes)

        return root

    def move_to(self, ingredient: Ingredient) -> None:
        position = ingredient.position
        print(f"\nMoving to : {ingredient.name}")
        distance = self.distance(self.current_position, position)
        self.total_distance += distance
        print(f"Moving from {self.current_position} to {position} -- Distance: {round(distance, 2)} u.m.")
        self.current_position = position
    
    def distance(self, position1: Tuple[int, int], position2: Tuple[int, int]) -> float:
        return ((position1[0] - position2[0]) ** 2 + (position1[1] - position2[1]) ** 2) ** 0.5

    def traverse_and_prepare(self, next_node: TreeNode) -> None:
        if next_node.action and next_node.ingredient:
            ingredient: Ingredient = next_node.ingredient
            self.move_to(ingredient)
            next_node.action()
            if next_node.stock_check and ingredient.is_below_threshold():
                self.alert_stock(ingredient.name)
        self.current_node = next_node

    def prepare_bowl(self, base_index: int, protein_index: int, topping_indices: List[int], sauce_index: int) -> str:
        self.reset()

        base_node = self.root.children[0].children[base_index]
        protein_node = base_node.children[protein_index]
        topping_indices.sort(reverse=True)
        topping_nodes = [protein_node.children[i] for i in topping_indices]
        sauce_node = topping_nodes[0].children[sauce_index]

        path = [base_node, protein_node, *topping_nodes, sauce_node]
        
        self.move_to(Ingredient("Bowl Dispenser", 0, 0, self.bowl_dispenser_position))

        for node in path:
            self.traverse_and_prepare(node)

        self.move_to(Ingredient("Final Position", 0, 0, self.final_position))
        return "Bowl prepared successfully with the selected ingredients and a distance of " + str(round(self.total_distance, 2)) + " u.m."

    def alert_stock(self, ingredient_name: str) -> None:
        print(f"Alert: Stock of {ingredient_name} is below the threshold.")
        
    def reset(self):
        self.current_position = self.initial_position
        self.current_node = self.root
        self.total_distance = 0.0

def print_options(options: List[Ingredient]) -> None:
    for i, option in enumerate(options):
        print(f"{i + 1}. {option.name}")

def choose_option(options: List[Ingredient], message: str) -> int:
    print("\n")
    print(message)
    print_options(options)
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= len(options):
                return choice - 1
            else:
                print("Invalid choice. Please enter a valid option number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    bowls = Ingredient("bowls", 80, 1, (650, 660))
    bases = [
        Ingredient("Arròs",             20000, 250, (610, 10)),
        Ingredient("Arròs Earth Mama",  20000, 250, (640, 10)),
        Ingredient("Quinoa",            20000, 250, (670, 10))
    ]
    proteins = [
        Ingredient("Pollastre rostit al carbó",  300, 200, (450, 10)),
        Ingredient("Gall dindi fumat al carbó",  16000, 200, (480, 10)),
        Ingredient("Proteïna vegetal",           16000, 200, (510, 10)),
        Ingredient("Vedella gallega al carbó",   16000, 200, (540, 10)),
        Ingredient("Salmó fumat amb fusta",      16000, 200, (570, 10))
    ]
    toppings = [
        Ingredient("Tomàquet cherry",   8000, 100, (140, 10)),
        Ingredient("Bolets shiitake",   8000, 100, (170, 10)),
        Ingredient("Moniato",           8000, 100, (200, 10)),
        Ingredient("Nous",              8000, 100, (230, 10)),
        Ingredient("Pinya fumada",      8000, 100, (260, 10)),
        Ingredient("Mango",             8000, 100, (290, 10)),
        Ingredient("Alvocat",           8000, 100, (320, 10)),
        Ingredient("Cigrons picants",   8000, 100, (350, 10)),
        Ingredient("Formatge fumat",    8000, 100, (380, 10)),
        Ingredient("Carbassa",          8000, 100, (410, 10))
    ]
    sauces = [
        Ingredient("Crema vegetariana amb jalapeny i alfàbrega triturada",  6000, 75, (10, 10)),
        Ingredient("Crema vegetariana amb remolatxa",                       6000, 75, (40, 10)),
        Ingredient("Crema de tartufata amb bolets i tòfona negra",          6000, 75, (70, 10)),
        Ingredient("Crema de chimichurri amb suc de taronja",               6000, 75, (100, 10))
    ]

    cooLex = CooLex(bowls, bases, proteins, toppings, sauces)

    cont = 'YES'

    while cont == 'YES':
        base_index = choose_option(bases, "Choose a base:")
        protein_index = choose_option(proteins, "Choose a protein:")
        topping_indices = [choose_option(toppings, f"Choose topping {i + 1}:") for i in range(3)]
        sauce_index = choose_option(sauces, "Choose a sauce:")

        print("\n")
        print(f"Base: {bases[base_index].name}")
        print(f"Protein: {proteins[protein_index].name}")
        print("Toppings:")
        for i in topping_indices:
            print(f"  - {toppings[i].name}")
        print(f"Sauce: {sauces[sauce_index].name}")
        print("\n")

        try:
            result = cooLex.prepare_bowl(base_index, protein_index, topping_indices, sauce_index)
            print(result)
        except Exception as e:
            print("\nAn error occurred while preparing the bowl. Please try again.")
            print(f"Error: {e}")

        print("\n")
        cont = input("Do you want to prepare another bowl? (Yes/No): ").upper()
        while cont != 'YES' and cont != 'NO':
            cont = input("Invalid input. Please enter 'Yes' or 'No': ").upper()
        
        if cont == 'YES':
            print("\n")
            print("=============================================")
            print("\n")
    
    print("\nThank you for using CooLex! Have a nice day!")

if __name__ == "__main__":
    main()
