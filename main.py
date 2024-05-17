class TreeNode:
    def __init__(self, name, action=None, stock_check=False):
        self.name = name
        self.action = action
        self.stock_check = stock_check
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


class Ingredient:
    def __init__(self, name, stock, quantity):
        self.name = name
        self.stock = stock
        self.quantity = quantity

    def use(self):
        if self.stock >= self.quantity:
            self.stock -= self.quantity
        else:
            raise ValueError(f"Insufficient stock for {self.name}")

    def check_stock(self):
        return self.stock >= self.quantity

    def is_below_threshold(self, threshold=20):
        return self.stock < threshold


class CooLex:
    def __init__(self, bowls, bases, proteins, toppings, sauces):
        self.bowls = bowls
        self.bases = bases
        self.proteins = proteins
        self.toppings = toppings
        self.sauces = sauces
        self.root = self.create_tree()

    def create_tree(self):
        root = TreeNode("Start")

        # Bowl node
        bowl_node = TreeNode("Bowl", action=self.bowls.use, stock_check=True)
        root.add_child(bowl_node)

        # Base nodes
        base_nodes = [TreeNode(base.name, action=base.use, stock_check=True) for base in self.bases]
        bowl_node.children.extend(base_nodes)

        # Protein nodes
        for base_node in base_nodes:
            protein_nodes = [TreeNode(protein.name, action=protein.use, stock_check=True) for protein in self.proteins]
            base_node.children.extend(protein_nodes)

            # Topping nodes
            for protein_node in protein_nodes:
                topping_nodes = [TreeNode(topping.name, action=topping.use, stock_check=True) for topping in self.toppings]
                protein_node.children.extend(topping_nodes)

                # Sauce nodes
                for topping_node in topping_nodes:
                    sauce_nodes = [TreeNode(sauce.name, action=sauce.use, stock_check=True) for sauce in self.sauces]
                    topping_node.children.extend(sauce_nodes)

        return root

    def traverse_and_prepare(self, current_node):
        if current_node.action:
            try:
                current_node.action()
                if current_node.stock_check and current_node.action.im_self.is_below_threshold():
                    self.alert_stock(current_node.name)
            except ValueError as e:
                return str(e)

        for child in current_node.children:
            result = self.traverse_and_prepare(child)
            if result:
                return result

        return "Bowl prepared successfully."

    def prepare_bowl(self, base_index, protein_index, topping_indices, sauce_index):
        # Set the correct path based on indices
        base_node = self.root.children[0].children[base_index]
        protein_node = base_node.children[protein_index]
        topping_nodes = [protein_node.children[i] for i in topping_indices]
        sauce_node = topping_nodes[0].children[sauce_index]  # Assume same sauce for all toppings

        # Traverse the tree along the selected path
        result = self.traverse_and_prepare(self.root)
        return result

    def alert_stock(self, ingredient_name):
        print(f"Alert: Stock of {ingredient_name} is below the threshold.")


# Exemple d'estocs inicials
bowls = Ingredient("bowls", 100, 1)
bases = [Ingredient("arros", 100, 250), Ingredient("arros Earth Mama", 100, 250), Ingredient("quinoa", 100, 250)]
proteins = [Ingredient("pollastre rostit", 100, 200), Ingredient("gall dindi", 100, 200), Ingredient("proteina vegetal", 100, 200), Ingredient("vedella gallega", 100, 200), Ingredient("salmo fumat", 100, 200)]
toppings = [Ingredient("tomàquet cherry", 100, 100), Ingredient("bolets shiitake", 100, 100), Ingredient("moniato", 100, 100), Ingredient("nous", 100, 100), Ingredient("pinya fumada", 100, 100), Ingredient("mango", 100, 100), Ingredient("alvocat", 100, 100), Ingredient("cigrons picants", 100, 100), Ingredient("formatge fumat", 100, 100), Ingredient("carbassa", 100, 100)]
sauces = [Ingredient("crema vegetariana jalapeny", 100, 75), Ingredient("crema vegetariana remolatxa", 100, 75), Ingredient("crema tartufata", 100, 75), Ingredient("crema chimichurri", 100, 75)]

# Inicialitzar el robot CooLex
cooLex = CooLex(bowls, bases, proteins, toppings, sauces)

# Exemple de comanda
base_index = 0  # Arròs
protein_index = 1  # Gall dindi
topping_indices = [0, 3, 5]  # Tomàquet cherry, Nous, Mango
sauce_index = 2  # Crema de tartufata

# Preparar el bowl
result = cooLex.prepare_bowl(base_index, protein_index, topping_indices, sauce_index)
print(result)