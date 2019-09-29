# from copy import deepcopy
from random import randrange


class StochasticSearch:

    def __init__(self, loss, initial_point_generator, movement_policy, validation_policy):
        self.loss = loss
        self.gen = initial_point_generator
        self.move = movement_policy
        self.valid = validation_policy
        self.sol = None
        self.steps = None
        self.cost = None
        self.trees = []  # list trees; tree = list of nodes; node = (v, loss(v))
        self.converged = False

    def search(self, min_loss=.1, n_steps=100):
        """training"""
        self.new_tree()
        # self.new_tree()

        for steps in range(1, n_steps):
            self.expand(0)

            # if self.model_loss() <= min_loss:
            #     break


        # print(self.model_loss())
        ...

    def __repr__(self):
        s = ''
        for i in self.trees:
            s += '\n'
            for j in i:
                s += str(j) + '\n'
        return s

    def __len__(self):
        return len(self.trees)

    def __getitem__(self, item):
        return self.trees[item]

    def new_tree(self):
        """create the root of a new tree"""
        v = self.gen()
        self.trees.append([(v, self.loss(v))])

    def branch(self, tree, depth):
        """create a branch of an existing tree from a node"""
        self.trees.append([self[tree][depth]])

    def branch_root(self, tree):
        """branch existing tree from root"""
        return self.branch(tree, 0)

    def branch_leaf(self, tree):
        """branch existing tree from leaf"""
        return self.branch(tree, -1)

    def tree_leaf(self, tree):
        """vector on the leaf of the tree"""
        return self[tree][-1][0]

    def delete_tree(self, tree):
        """delete a tree"""
        self.trees = [self[i] for i in range(len(self)) if i != tree]

    def tree_loss(self, tree):
        """loss of the leaf of the tree"""
        return self[tree][-1][1]

    def model_loss(self):
        """loss of the best tree"""
        return min(self.tree_loss(i) for i in self.trees)

    def append_to_tree(self, tree, v, loss):
        """add node to tree"""
        self.trees[tree].append((v, loss))

    def expand(self, tree):
        """try to find a better solution close to the leaf of the tree"""
        v = self.tree_leaf(tree)
        new = self.move(v)

        if self.valid(new):
            new_loss, old_loss = self.loss(new), self.tree_loss(tree)

            if new_loss <= old_loss:
                self.append_to_tree(tree, new, new_loss)


if __name__ == '__main__':

    def loss_(x):
        return sum(i ** 2 for i in x)


    def init_():
        return [randrange(-10, 10), randrange(-10, 10)]


    def move_(v):
        return [i + randrange(0, 2) * 2 - 1 for i in v]


    def valid_(_):
        return True


    S = StochasticSearch(loss_, init_, move_, valid_)
    S.search(min_loss=10)
    print(S)
