import nn

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(self.w, x)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        if(nn.as_scalar(self.run(x)) >= 0):
            return 1
        else:
            return -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        whether_false = True
        batch_size = 1
        while whether_false:
            whether_false = False
            for x, y in dataset.iterate_once(batch_size):##travel all the data point to update the w
                pred = self.get_prediction(x) # get pred pred
                real_y = nn.as_scalar(y)
                if pred != real_y:   #if pred != true label
                    direction = nn.Constant(real_y * x.data)
                    self.w.update(direction, 1)
                    whether_false = True

class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.lr = 0.1
        self.w1 = nn.Parameter(1, 128)   #set two layer parameters
        self.b1 = nn.Parameter(1, 128)
        self.w2 = nn.Parameter(128, 1)
        self.b2 = nn.Parameter(1, 1)
        self.params = [self.w1, self.b1, self.w2, self.b2]

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        ##We just set a simple two layer
        ##f(x) = relu(x*w_1 + b_1)*w_2 + b_2
        first_layer = nn.ReLU(nn.AddBias(nn.Linear(x, self.w1), self.b1))
        output_layer = nn.AddBias(nn.Linear(first_layer, self.w2), self.b2)
        return output_layer

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        #get the pred_value to calculate the loss
        pred = self.run(x)
        return nn.SquareLoss(pred, y)
    
    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        batch_size = 50
        loss = 100
        while loss >= 0.02: ##finish condition
            for x, y in dataset.iterate_once(batch_size):#trabel a batch everytime
                loss = self.get_loss(x, y)
                grads = nn.gradients(loss, self.params)
                loss = nn.as_scalar(loss)
                for i in range(len(self.params)):             ##travel all the parameters and update
                    self.params[i].update(grads[i], -self.lr) ##gradient descent

class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.lr = 0.1
        self.w1 = nn.Parameter(784, 128)   #set three layer parameters
        self.b1 = nn.Parameter(1, 128)
        self.w2 = nn.Parameter(128, 64)
        self.b2 = nn.Parameter(1, 64)
        self.w3 = nn.Parameter(64, 10)      ##the output should be 10 dimension
        self.b3 = nn.Parameter(1, 10)
        self.params = [self.w1, self.b1, self.w2, self.b2, self.w3, self.b3]

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        first_layer = nn.ReLU(nn.AddBias(nn.Linear(x, self.w1), self.b1))
        second_layer = nn.ReLU(nn.AddBias(nn.Linear(first_layer, self.w2), self.b2))
        output_layer = nn.AddBias(nn.Linear(second_layer, self.w3), self.b3)
        return output_layer

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        pred = self.run(x)
        return nn.SoftmaxLoss(pred, y) ##softmax loss

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        batch_size = 50
        loss = 100
        validate_accuracy = 0
        while validate_accuracy <= 0.98: ##finish condition
            for x, y in dataset.iterate_once(batch_size):#trabel a batch everytime
                loss = self.get_loss(x, y)
                grads = nn.gradients(loss, self.params)
                loss = nn.as_scalar(loss)
                for i in range(len(self.params)):             ##travel all the parameters and update
                    self.params[i].update(grads[i], -self.lr) ##gradient descent
            validate_accuracy = dataset.get_validation_accuracy()

class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.lr = 0.06
        self.w1 = nn.Parameter(self.num_chars, 128)   #set three layer parameters
        self.b1 = nn.Parameter(1, 128)
        self.w2 = nn.Parameter(self.num_chars, 128)
        self.b2 = nn.Parameter(1, 128)
        self.w3 = nn.Parameter(128, 5)      ##the output should be 5 dimension
        self.b3 = nn.Parameter(1, 5)
        self.h = nn.Parameter(128, 128)
        self.params = [self.w1, self.b1, self.w2, self.b2, self.w3, self.b3, self.h]
        

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        ##Initialize f_intitial(x0)
        h_i = nn.ReLU(nn.AddBias(nn.Linear(xs[0], self.w1), self.b1))
        #travel all the char in xs to update the h_i
        for char in xs[1:]: 
            h_i = nn.ReLU(nn.AddBias(nn.Add(nn.Linear(char, self.w2), nn.Linear(h_i, self.h)), self.b2))
        #final h_i to get the output
        output_layer = nn.AddBias(nn.Linear(h_i, self.w3), self.b3)
        return output_layer

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        pred = self.run(xs)
        return nn.SoftmaxLoss(pred, y) ##softmax loss

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        batch_size = 20
        loss = 100
        validate_accuracy = 0
        while validate_accuracy <= 0.81: ##finish condition
            for x, y in dataset.iterate_once(batch_size):#trabel a batch everytime
                loss = self.get_loss(x, y)
                grads = nn.gradients(loss, self.params)
                loss = nn.as_scalar(loss)
                for i in range(len(self.params)):             ##travel all the parameters and update
                    self.params[i].update(grads[i], -self.lr) ##gradient descent
            validate_accuracy = dataset.get_validation_accuracy()
