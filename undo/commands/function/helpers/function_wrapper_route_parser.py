# with help from: https://medium.com/@wshanshan/intro-to-python-ast-module-bbd22cd505f7
# but stolen form: https://deepsource.com/blog/python-asts-by-building-your-own-linter
# heart emoji, Tushar, a true hero
import ast
from io import StringIO
import sys

class RouteVisitor(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.route_list = [] # Now it's unique to this instance


    def parse_handler(self, file_path):
        if not file_path.exists():
            return

        with open(file_path) as f:
            code = f.read()

        # go parse the file and extract the routes from the standard place
        tree = ast.parse(code)
        self.visit(tree)


    def generic_visit(self, node):
        if isinstance(node, ast.If):
            # print(ast.dump(node))
            self.capture_route(node)

        super().generic_visit(node)

    def capture_route(self, node):
        # test for the signature
        # if req["route_key"] == "ANY /route_key"
        
        # test this is a comparison (x = y) not a constant (e.g. it isn't "if True")
        if not isinstance(node.test, ast.Compare):
            return

        # check the left of the operator is an list/dict
        # from which a property is being accessed - "subscripted", i guess
        # (e.g. it's req["route_key"] == .. rather than req == ...)
        compare = node.test
        if not isinstance(compare.left, ast.Subscript):
            return
        
        # check if that subscriptable, is against a variable called "req"
        subscript = compare.left
        if not isinstance(subscript.value, ast.Name) or subscript.value.id != "req":
            return

        # check if the slice - the index we are retreiving from that subscriptable
        # is the route_key
        # (beware, Python 3.8 expresses this differently, so leaving in this conversion)
        subslice = subscript.slice
        if isinstance(subslice, ast.Index): subslice = subslice.value
        if not isinstance(subslice, ast.Constant) or subslice.value != "route_key":
            return

        # check that it's doing an equals comparison operation
        if len(compare.ops) != 1 or not isinstance(compare.ops[0], ast.Eq):
            return

        # make sure it's comparing it to a constant, not a variable
        # then grab that variable cuz that's our route, baby, we did it!
        if isinstance(compare.comparators[0], ast.Constant):
            route_key = compare.comparators[0].value
            self.route_list.append(route_key)

        return route_key
