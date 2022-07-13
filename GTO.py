import math, pandas, random, warnings, functions as u, numpy as np
warnings.filterwarnings('ignore')


class GTOClass:
    Silverback_Score = None
    Silverback = None
    convergence_curve = None

    # statistical data for objetive function
    difference_umbral = None
    test = None
    criteria = None
    selected = None

    datatype = float

    def execGTO(self, X, pop_size, max_iter, variables_no, upper_bound, lower_bound):
        # initialize Silverback
        self.Silverback = np.array([])
        self.Silverback_Score = 1000000

        self.convergence_curve = np.zeros(max_iter)
        for i in range(1, pop_size):
            try:
                Pop_Fit = self.ObjectiveFunction(X[i, :])
                if Pop_Fit < self.Silverback_Score and not np.isnan(X[i, :]).any():
                    self.Silverback_Score = Pop_Fit
                    self.Silverback = X[i, :]
            except Exception as e:
                continue

        GX = np.copy(X)
        lb = np.ones((1, variables_no)) * lower_bound
        ub = np.ones((1, variables_no)) * upper_bound

        # Controlling parameter
        p = 0.5
        Beta = 7
        w = 0.8

        # Main loop
        for It in range(1, max_iter):
            a = (math.cos(2 * random.random()) + 1) * (1 - It / max_iter)
            C = a * (2 * random.random() - 1)

            # Exploration:
            for i in range(1, pop_size):
                if np.random.uniform(0, 1) < p:
                    GX[i, :] = (ub - lb) * random.random() + lb
                else:
                    if np.random.uniform(0, 1) >= 0.5:
                        # Z = np.random.uniform(-a, a, variables_no)
                        Z = u.get_random_data_r(self.selected, variables_no)
                        H = Z * X[i, :]
                        GX[i, :] = (random.random() - a) * X[random.randint(0, pop_size - 1), :] + C * H
                    else:
                        GX[i, :] = X[i, :] - C * (
                                C * (X[i, :] - GX[random.randint(0, pop_size - 1), :]) + random.random() * (
                                X[i, :] - GX[random.randint(0, pop_size - 1), :]))

            GX = self.BoundaryCheck(GX, lower_bound, upper_bound)

            # Group formation operation
            for i in range(1, pop_size):
                try:
                    New_Fit = self.ObjectiveFunction(GX[i, :])
                    if New_Fit < Pop_Fit and not np.isnan(GX[i, :]).any():
                        Pop_Fit = New_Fit
                        X[i, :] = GX[i, :]

                    if New_Fit < self.Silverback_Score and not np.isnan(GX[i, :]).any():
                        self.Silverback_Score = New_Fit
                        self.Silverback = GX[i, :]
                except Exception as e:
                    continue

            # Exploitation:
            for i in range(1, pop_size):
                try:
                    if a >= w:
                        g = 2 ** C
                        delta = np.power(np.power(abs(np.mean(GX, axis=0)), g), (1 / g))
                        GX[i, :] = np.power(np.multiply(delta, C), (X[i, :] - self.Silverback)) + X[i, :]
                    else:
                        GX[i, :] = self.Silverback - (self.Silverback * (2 * r1 - 1) - X[i, :] * (2 * r1 - 1)) * (Beta * h)
                except Exception as e:
                    continue

            GX = self.BoundaryCheck(GX, lower_bound, upper_bound)
            for i in range(0, pop_size - 1):
                try:
                    New_Fit = self.ObjectiveFunction(GX[i, :])
                    if New_Fit < Pop_Fit and not np.isnan(GX[i, :]).any():
                        Pop_Fit = New_Fit
                        X[i, :] = GX[i, :]

                    if New_Fit < self.Silverback_Score and not np.isnan(GX[i, :]).any():
                        self.Silverback_Score = New_Fit
                        self.Silverback = GX[i, :]
                except Exception as e:
                    continue

            self.convergence_curve[It] = self.Silverback_Score
            return self.Silverback

    def BoundaryCheck(self, X, lb, ub):
        for i in range(1, len(X)):  # desde 1 hasta el primer tamaño de la matriz
            FU = X[i, :] > ub
            FL = X[i, :] < lb
            X[i, :] = (X[i, :] * np.logical_not(np.logical_and(FU, FL))) + ub * FU + lb * FL
        return X

    def setStatisticData(self, _difference_umbral, _test, _criteria, _datatype, _selected):
        self.difference_umbral = _difference_umbral
        self.test = _test
        self.criteria = _criteria
        self.datatype = _datatype
        self.selected = _selected

    def ObjectiveFunction(self, x):
        selected_distribution = u.getDistributionInfo([x], [self.datatype], self.difference_umbral, self.test, self.criteria)
        if 'Repeated' in selected_distribution[0]['dist'][0]: return -1000000
        return selected_distribution[0][self.test]

    # N double
    # dim double
    # ub array
    # lb double
    def initialization(self, N, dim, ub, lb):
        Boundary_no = ub.shape[1] if hasattr(ub, "__len__") else 1
        X = np.random.randn(N, dim) * (ub - lb) + lb
        if Boundary_no > 1:
            for i in range(1, X.ndim):
                ub_i = ub(i)
                lb_i = lb(i)
                X[i, :] = np.random.randn(N, 1) * (ub_i - lb_i) + lb_i
        return X
