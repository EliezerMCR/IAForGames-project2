# decision_tree.py

# Nodo de condición
class DecisionNode:
    def __init__(self, condition, true_branch, false_branch):
        self.condition = condition  # Función que devuelve True o False
        self.true_branch = true_branch  # Nodo hijo si la condición es True
        self.false_branch = false_branch  # Nodo hijo si la condición es False

    def evaluate(self):
        if self.condition():
            return self.true_branch.evaluate()
        else:
            return self.false_branch.evaluate()

# Nodo de acción


class ActionNode:
    def __init__(self, action):
        self.action = action  # Función que ejecuta la acción

    def evaluate(self):
        return self.action()
