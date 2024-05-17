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
        self.stock: int = stock
        self.quantity: int = quantity
        self.position: Tuple[int, int] = position

    def use(self) -> None:
        if self.stock >= self.quantity:
            self.stock -= self.quantity
        else:
            raise ValueError(f"Insufficient stock for {self.name}")

    def check_stock(self) -> bool:
        return self.stock >= self.quantity

    def is_below_threshold(self, threshold: int = 20) -> bool:
        return self.stock < threshold


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

    def move_to(self, position: Tuple[int, int]) -> None:
        print(f"Moving from {self.current_position} to {position}")
        self.current_position = position

    def traverse_and_prepare(self, current_node: TreeNode) -> Optional[str]:
        if current_node.action and current_node.ingredient:
            ingredient: Ingredient = current_node.ingredient
            self.move_to(ingredient.position)
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


# Example initial stocks and positions
bowls = Ingredient("bowls", 80, 1, (650, 660))
bases = [
    Ingredient("arros",             20, 250, (610, 10)),
    Ingredient("arros Earth Mama",  20, 250, (640, 10)),
    Ingredient("quinoa",            20, 250, (670, 10))
]
proteins = [
    Ingredient("pollastre rostit",  16, 200, (450, 10)),
    Ingredient("gall dindi",        16, 200, (480, 10)),
    Ingredient("proteina vegetal",  16, 200, (510, 10)),
    Ingredient("vedella gallega",   16, 200, (540, 10)),
    Ingredient("salmo fumat",       16, 200, (570, 10))
]
toppings = [
    Ingredient("tomàquet cherry",   8, 100, (140, 10)),
    Ingredient("bolets shiitake",   8, 100, (170, 10)),
    Ingredient("moniato",           8, 100, (200, 10)),
    Ingredient("nous",              8, 100, (230, 10)),
    Ingredient("pinya fumada",      8, 100, (260, 10)),
    Ingredient("mango",             8, 100, (290, 10)),
    Ingredient("alvocat",           8, 100, (320, 10)),
    Ingredient("cigrons picants",   8, 100, (350, 10)),
    Ingredient("formatge fumat",    8, 100, (380, 10)),
    Ingredient("carbassa",          8, 100, (410, 10))
]
sauces = [
    Ingredient("crema vegetariana jalapeny",    6, 75, (10, 10)),
    Ingredient("crema vegetariana remolatxa",   6, 75, (40, 10)),
    Ingredient("crema tartufata",               6, 75, (70, 10)),
    Ingredient("crema chimichurri",             6, 75, (100, 10))
]

# Initialize the CooLex robot
cooLex = CooLex(bowls, bases, proteins, toppings, sauces)

# Example order
base_index = 0  # Arròs
protein_index = 1  # Gall dindi
topping_indices = [0, 3, 5]  # Tomàquet cherry, Nous, Mango
sauce_index = 2  # Crema de tartufata

# Prepare the bowl
result = cooLex.prepare_bowl(base_index, protein_index, topping_indices, sauce_index)
print(result)

# Print the schema of the nodes
# cooLex.print_schema()
