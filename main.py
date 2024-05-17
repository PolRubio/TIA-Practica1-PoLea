from typing import Callable, List, Optional, Tuple

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
            raise ValueError(f"Insufficient stock for {self.name}")

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
        self.final_position: Tuple[int, int] = (410, 610)
        self.current_position: Tuple[int, int] = self.initial_position

    def create_tree(self) -> TreeNode:
        root = TreeNode("Start")

        # Bowl node
        bowl_node = TreeNode("Bowl", ingredient=self.bowls, action=self.bowls.use, stock_check=True)
        root.add_child(bowl_node)

        # Base nodes
        base_nodes = [TreeNode(base.name, ingredient=base, action=base.use, stock_check=True) for base in self.bases]
        bowl_node.children.extend(base_nodes)

        # Protein nodes
        for base_node in base_nodes:
            protein_nodes = [TreeNode(protein.name, ingredient=protein, action=protein.use, stock_check=True) for protein in self.proteins]
            base_node.children.extend(protein_nodes)

            # Topping nodes
            for protein_node in protein_nodes:
                topping_nodes = [TreeNode(topping.name, ingredient=topping, action=topping.use, stock_check=True) for topping in self.toppings]
                protein_node.children.extend(topping_nodes)

                # Sauce nodes
                for topping_node in topping_nodes:
                    sauce_nodes = [TreeNode(sauce.name, ingredient=sauce, action=sauce.use, stock_check=True) for sauce in self.sauces]
                    topping_node.children.extend(sauce_nodes)

        return root

    def move_to(self, ingredient: Ingredient) -> None:
        position = ingredient.position
        print(f"\nMoving to ingredient: {ingredient.name}")
        print(f"Moving from {self.current_position} to {position} -- Distance: {round(self.distance(self.current_position, position), 2)} u.m.")
        self.current_position = position
    
    def distance(self, position1: Tuple[int, int], position2: Tuple[int, int]) -> float:
        return ((position1[0] - position2[0]) ** 2 + (position1[1] - position2[1]) ** 2) ** 0.5

    def traverse_and_prepare(self, current_node: TreeNode) -> Optional[str]:
        if current_node.action and current_node.ingredient:
            ingredient: Ingredient = current_node.ingredient
            self.move_to(ingredient)
            try:
                current_node.action()
                if current_node.stock_check and ingredient.is_below_threshold():
                    self.alert_stock(ingredient.name)
            except ValueError as e:
                return str(e)

        for child in current_node.children:
            result = self.traverse_and_prepare(child)
            if result:
                return result

        return None

    def prepare_bowl(self, base_index: int, protein_index: int, topping_indices: List[int], sauce_index: int) -> str:
        # Reset current position to initial position
        self.current_position = self.initial_position

        # Set the correct path based on indices
        base_node = self.root.children[0].children[base_index]
        protein_node = base_node.children[protein_index]
        topping_nodes = [protein_node.children[i] for i in topping_indices]
        sauce_node = topping_nodes[0].children[sauce_index]  # Assume same sauce for all toppings

        # Traverse the tree along the selected path
        result = self.traverse_and_prepare(self.root)
        if result:
            return result

        # Move to final position
        self.move_to(self.final_position)
        return "Bowl prepared successfully."

    def alert_stock(self, ingredient_name: str) -> None:
        print(f"Alert: Stock of {ingredient_name} is below the threshold.")

    def print_schema(self, node: Optional[TreeNode] = None, indent: str = "") -> None:
        if node is None:
            node = self.root
        print(f"{indent}{node.name}")
        for child in node.children:
            self.print_schema(child, indent + "  ")

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
        Ingredient("Pollastre rostit al carbó",  16000, 200, (450, 10)),
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

    base_index = choose_option(bases, "Choose a base:")
    protein_index = choose_option(proteins, "Choose a protein:")
    topping_count = int(input("\nEnter the number of toppings you want to add: "))
    topping_indices = [choose_option(toppings, f"Choose topping {i + 1}:") for i in range(topping_count)]
    sauce_index = choose_option(sauces, "Choose a sauce:")

    # Print the ingredients chosen
    print("\n")
    print(f"Base: {bases[base_index].name}")
    print(f"Protein: {proteins[protein_index].name}")
    print("Toppings:")
    for i in topping_indices:
        print(f"  - {toppings[i].name}")
    print(f"Sauce: {sauces[sauce_index].name}")
    print("\n")


    result = cooLex.prepare_bowl(base_index, protein_index, topping_indices, sauce_index)
    print(result)

if __name__ == "__main__":
    main()
