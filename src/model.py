import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os

current_dir = os.path.dirname(os.path.abspath(__file__))


class LinearRegression:
    """
    Implementation of a simple linear regression model.

    Attributes
    ----------
    weights : array_like
        The weights (or coefficients) of the linear regression model.
    """

    def __init__(self):
        self.weights = None

    @property
    def coef_(self):
        return self.weights

    def fit(self, X, y):
        """
        Trains the linear regression model using the given training data.

        Parameters
        ----------
        X : array_like
            The input feature matrix for training.
        y : array_like
            The target output vector for training.
        """
        # Adiciona uma coluna de uns para o termo bias
        X = np.hstack((np.ones((X.shape[0], 1)), X))

        # Calcula os pesos usando a fórmula dos mínimos quadrados
        self.weights = np.linalg.pinv(X.T @ X) @ X.T @ y

    def predict(self, X):
        """
        Makes predictions with the trained linear regression model.

        Parameters
        ----------
        X : array_like
            The input feature matrix for prediction.

        Returns
        -------
        array_like
            The predicted output vector.
        """
        # Adiciona uma coluna de uns para o termo bias
        X = np.hstack((np.ones((X.shape[0], 1)), X))

        return X @ self.weights


class SGDRegressor:
    """
    Implementation of a linear regressor using the Stochastic Gradient Descent (SGD) method.

    Parameters
    ----------
    learning_rate : float, default=0.01
        The learning rate for parameter update in SGD.
    max_iter : int, default=1000
        Maximum number of iterations for SGD.
    batch_size : int, default=20
        Batch size for each parameter update.
    tol : float, default=1e-3
        Tolerance for optimization. If the loss is less than `tol`, the algorithm stops.
    """

    def __init__(self, learning_rate=0.01, max_iter=1000, batch_size=20, tol=1e-3):
        self.learning_rate = learning_rate
        self.n_iters = max_iter
        self.batch_size = batch_size
        self.weights = None
        self.bias = None
        self.tol = tol

    @property
    def coef_(self):
        return self.weights

    @property
    def intercept_(self):
        return self.bias

    def compute_cost(self, X, y) -> float:
        """
        Computes the cost of the current prediction.

        Parameters
        ----------
        X : array_like
            Input samples.
        y : array_like
            Target values vector.

        Returns
        -------
        float
            The cost of the current prediction.
        """
        # Number of training examples
        m = X.shape[0]

        # Calculate the predicted values for all examples using vectorized operations
        predictions = np.dot(X, self.weights) + self.bias

        # Calculate the squared errors
        squared_errors = (predictions - y) ** 2

        # Calculate the total cost using vectorized operations
        return np.sum(squared_errors) / (2 * m)

    def fit(self, X, y):
        """
        Trains the model using Stochastic Gradient Descent.

        Parameters
        ----------
        X : array_like
            Input samples.
        y : array_like
            Target values vector.
        """
        n_samples, n_features = X.shape

        # Inicializa os parâmetros
        self.weights = np.zeros(n_features)
        self.bias = 0

        for i in range(self.n_iters):
            # Calcula as previsões
            y_predicted = np.dot(X, self.weights) + self.bias
            err = y_predicted - y
            m = len(X)

            # Calcula os gradientes
            dw = np.dot(X.T, err) / m
            db = np.sum(err) / m

            # Atualiza os parâmetros
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

            # Calcula o custo
            cost = self.compute_cost(X, y)
            print(f"Iteration: {i}, Cost: {cost}")

            if cost < self.tol:
                break

    def predict(self, X):
        """
        Makes predictions with the trained model.

        Parameters
        ----------
        X : array_like
            Input feature matrix.

        Returns
        -------
        array_like
            Model prediction vector.
        """
        return np.dot(X, self.weights) + self.bias


class StandardScaler:
    """
    This class standardizes features by removing the mean and scaling to unit variance.
    The standardization is performed using the Z-score normalization method.

    Attributes
    ----------
    mu_ : array, shape (n_features,)
        The mean value for each feature in the training set.
    sigma_ : array, shape (n_features,)
        The standard deviation for each feature in the training set.
    """

    def __init__(self) -> None:
        self.mu_ = None
        self.sigma_ = None

    @property
    def mean_(self):
        """
        Returns the mean value for each feature in the training set.

        Returns
        -------
        array, shape (n_features,)
            The mean value for each feature in the training set.
        """
        return self.mu_

    @property
    def scale_(self):
        """
        Returns the standard deviation for each feature in the training set.

        Returns
        -------
        array, shape (n_features,)
            The standard deviation for each feature in the training set.
        """
        return self.sigma_

    def fit(self, X):
        """
        Computes the mean and standard deviation of the input data for later scaling.

        Parameters
        ----------
        X : array-like, shape [n_samples, n_features]
            The input data to compute the mean and standard deviation.
        """
        self.mu_ = np.mean(X, axis=0)
        self.sigma_ = np.std(X, axis=0)
        return self

    def transform(self, X):
        """
        Scales the input data using the computed mean and standard deviation.

        Parameters
        ----------
        X (ndarray (m,n))     : input data, m examples, n features

        Returns
        -------
        X_norm (ndarray (m,n)): input normalized by column
        """
        epsilon = 1e-8  # Valor pequeno para evitar a divisão por zero
        return (X - self.mu_) / (self.sigma_ + epsilon)

    def fit_transform(self, X):
        """
        Computes the mean and standard deviation of the input data for later scaling
        and scales the input data using the computed mean and standard deviation.

        Parameters
        ----------
        X : array-like, shape [n_samples, n_features]
            The input data to scale.

        Returns
        -------
        X_tr : array-like, shape [n_samples, n_features]
            The scaled input data.
        """
        return self.fit(X).transform(X)


class PolynomialFeatures:
    """
    This class generates polynomial features up to a given degree.

    Parameters
    ----------
    degree : int, default=2
        The degree of the polynomial features.
    """

    def __init__(self, degree=2):
        self.degree = degree

    def fit_transform(self, X):
        """
        Fits the polynomial features to the given input data
        Transforms the given input data into polynomial features.

        Parameters
        ----------
        X : array_like
            The input data.

        Returns
        -------
        X_poly : array_like
            The polynomial features.
        """
        X_poly = X.copy()
        for _ in range(2, self.degree + 1):
            X_poly = np.hstack((X_poly, X**_))
        return X_poly


if __name__ == "__main__":
    # Carregar os dados do arquivo CSV
    data_file = os.path.join(
        current_dir, "..", "output", "times", "sorting_times_int.csv"
    )
    df = pd.read_csv(data_file)

    # Obter a lista de métodos de ordenação
    sorting_methods = df["Sorting Method"].unique()
    degree = 2
    poly = PolynomialFeatures(degree)
    scaler = StandardScaler()
    model = SGDRegressor(max_iter=10000, tol=1e-3)

    # Inicialize uma lista vazia para armazenar os DataFrames temporários
    dfs_to_concat = []

    # Para cada método de ordenação
    for method in sorting_methods:
        # Filtrar os dados para o método atual
        data = df[df["Sorting Method"] == method]

        X = data["Input Size"].values.reshape(-1, 1)
        y = data["Execution Time"].values

        # Transformar para características polinomiais
        X_poly = poly.fit_transform(X)
        X_poly = scaler.fit_transform(X_poly)
        print(X_poly)

        model.fit(X_poly, y)

        # Prever os valores y
        y_poly_pred = model.predict(X_poly)

        # Adicionar os valores previstos a lista
        dfs_to_concat.append(
            pd.DataFrame(
                {
                    "Sorting Method": [method] * len(X),
                    "Input Size": X.ravel(),
                    "Execution Time": y_poly_pred,
                }
            )
        )

        # Plotar os dados originais e a curva de regressão polinomial
        plt.figure()
        plt.scatter(X, y, color="blue")
        plt.plot(X, y_poly_pred, color="red")
        plt.title(f"Regressão Polinomial para {method}")
        plt.xlabel("Tamanho da Entrada")
        plt.ylabel("Tempo de Execução")
        plt.show()

    # Concatenar os DataFrames temporários em um único DataFrame
    prediction_df = pd.concat(dfs_to_concat, ignore_index=True)

    # Salvar o DataFrame em um arquivo CSV
    prediction_df.to_csv(r"output\model\sorting_times_int_predictions.csv", index=False)
