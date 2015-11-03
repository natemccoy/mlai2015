# Python code for MLAI lectures.

# import the time model to allow python to pause.
import time
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from IPython.display import display, clear_output, HTML


##########          Week 1          ##########
def hyperplane_coordinates(w, b, plot_limits):
    """Helper function for plotting the decision boundary of the perceptron."""
    if abs(w[1])>abs(w[0]):
        # If w[1]>w[0] in absolute value, plane is likely to be leaving tops of plot.
        x0 = plot_limits['x']
        x1 = -(b + x0*w[0])/w[1]
    else:
        # otherwise plane is likely to be leaving sides of plot.
        x1 = plot_limits['y']
        x0 = -(b + x1*w[1])/w[0]
    return x0, x1

def init_perceptron_plot(f, ax, x_plus, x_minus, w, b, x_select):
    """Initialise a plot for showing the perceptron decision boundary."""

    h = {}

    ax[0].set_aspect('equal')
    # Plot the data again
    ax[0].plot(x_plus[:, 0], x_plus[:, 1], 'rx')
    ax[0].plot(x_minus[:, 0], x_minus[:, 1], 'go')
    plot_limits = {}
    plot_limits['x'] = np.asarray(ax[0].get_xlim())
    plot_limits['y'] = np.asarray(ax[0].get_ylim())
    x0, x1 = hyperplane_coordinates(w, b, plot_limits)
    strt = -b/w[1]

    h['arrow'] = ax[0].arrow(0, strt, w[0], w[1]+strt, head_width=0.2)
    # plot a line to represent the separating 'hyperplane'
    h['plane'], = ax[0].plot(x0, x1, 'b-')
    ax[0].set_xlim(plot_limits['x'])
    ax[0].set_ylim(plot_limits['y'])
    ax[0].set_xlabel('$x_0$', fontsize=fontsize)
    ax[0].set_ylabel('$x_1$', fontsize=fontsize)
    h['iter'] = ax[0].set_title('Update 0')

    h['select'], = ax[0].plot(x_select[0], x_select[1], 'ro', markersize=10)

    bins = 15
    f_minus = np.dot(x_minus, w)
    f_plus = np.dot(x_plus, w)
    ax[1].hist(f_plus, bins, alpha=0.5, label='+1', color='r')
    ax[1].hist(f_minus, bins, alpha=0.5, label='-1', color='g')
    ax[1].legend(loc='upper right')
    return h

def update_perceptron_plot(h, f, ax, x_plus, x_minus, i, w, b, x_select):
    """Update plots after decision boundary has changed."""
    # Helper function for updating plots
    h['select'].set_xdata(x_select[0])
    h['select'].set_ydata(x_select[1])
    # Re-plot the hyper plane 
    plot_limits = {}
    plot_limits['x'] = np.asarray(ax[0].get_xlim())
    plot_limits['y'] = np.asarray(ax[0].get_ylim())
    x0, x1 = hyperplane_coordinates(w, b, plot_limits)
    strt = -b/w[1]
    h['arrow'].remove()
    del(h['arrow'])
    h['arrow'] = ax[0].arrow(0, strt, w[0], w[1]+strt, head_width=0.2)
    
    h['plane'].set_xdata(x0)
    h['plane'].set_ydata(x1)

    h['iter'].set_text('Update ' + str(i))
    ax[1].cla()
    bins = 15
    f_minus = np.dot(x_minus, w)
    f_plus = np.dot(x_plus, w)
    ax[1].hist(f_plus, bins, alpha=0.5, label='+1', color='r')
    ax[1].hist(f_minus, bins, alpha=0.5, label='-1', color='g')
    ax[1].legend(loc='upper right')

    display(f)
    clear_output(wait=True)
    if i<3:
        time.sleep(0.5)
    else:
        time.sleep(.25)   
    return h

def init_regression_plot(f, ax, x, y, m_vals, c_vals, E_grid, m_star, c_star, fontsize=20):
    """Function to plot the initial regression fit and the error surface."""
    h = {}
    levels=[0, 0.5, 1, 2, 4, 8, 16, 32, 64]
    h['cont'] = ax[0].contour(m_vals, c_vals, E_grid, levels=levels) # this makes the contour plot on axes 0.
    plt.clabel(h['cont'], inline=1, fontsize=15)
    ax[0].set_xlabel('$m$', fontsize=fontsize)
    ax[0].set_ylabel('$c$', fontsize=fontsize)
    h['msg'] = ax[0].set_title('Error Function', fontsize=fontsize)

    # Set up plot
    h['data'], = ax[1].plot(x, y, 'r.', markersize=10)
    ax[1].set_xlabel('$x$', fontsize=fontsize)
    ax[1].set_ylabel('$y$', fontsize=fontsize)
    ax[1].set_ylim((-9, -1)) # set the y limits of the plot fixed
    ax[1].set_title('Best Fit', fontsize=fontsize)

    # Plot the current estimate of the best fit line
    x_plot = np.asarray(ax[1].get_xlim()) # get the x limits of the plot for plotting the current best line fit.
    y_plot = m_star*x_plot + c_star
    h['fit'], = ax[1].plot(x_plot, y_plot, 'b-', linewidth=3)
    return h

def update_regression_plot(h, f, ax, m_star, c_star, iteration):
    """Update the regression plot with the latest fit and position in error space."""
    ax[0].plot(m_star, c_star, 'g*')
    x_plot = np.asarray(ax[1].get_xlim()) # get the x limits of the plot for plo
    y_plot = m_star*x_plot + c_star
    
    # show the current status on the plot of the data
    h['fit'].set_ydata(y_plot)
    h['msg'].set_text('Iteration '+str(iteration))
    display(f)
    clear_output(wait=True)
    time.sleep(0.25) # pause between iterations to see update
    return h

##########           Weeks 4 and 5           ##########
class LM():
    """Linear model
    :param X: input values
    :type X: numpy.ndarray
    :param y: target values
    :type y: numpy.ndarray
    :param basis: basis function 
    :param type: function"""

    def __init__(self, X, y, basis, num_basis, **kwargs):
        "Initialise"
        self.X = X
        self.y = y
        self.num_data = y.shape[0]
        self.sigma2 = 1.
        self.basis = basis
        self.num_basis = num_basis
        self.basis_args = kwargs
        self.Phi = basis(X, num_basis=num_basis, **kwargs)

    def update_QR(self):
        "Perform the QR decomposition on the basis matrix."
        self.Q, self.R = np.linalg.qr(self.Phi)

    def fit(self):
        """Minimize the objective function with respect to the parameters"""
        self.update_QR()
        self.w_star = sp.linalg.solve_triangular(self.R, np.dot(self.Q.T, self.y))
        self.update_sum_squares()
        self.sigma2=self.sum_squares/self.num_data

    def predict(self, X):
        """Return the result of the prediction function."""
        return np.dot(self.basis(X, self.num_basis, **self.basis_args), self.w_star)
        
    def update_f(self):
        """Update values at the prediction points."""
        self.f = np.dot(self.Phi, self.w_star)
        
    def update_sum_squares(self):
        """Compute the sum of squares error."""
        self.update_f()
        self.sum_squares = ((self.y-self.f)**2).sum()
        
    def objective(self):
        """Compute the objective function."""
        self.update_sum_squares()
        return self.sum_squares

    def log_likelihood(self):
        """Compute the log likelihood."""
        self.update_sum_squares()
        return -self.num_data/2.*np.log(np.pi*2.)-self.num_data/2.*np.log(self.sigma2)-self.sum_squares/(2.*self.sigma2)

class BLM():
    """Bayesian Linear model
    :param X: input values
    :type X: numpy.ndarray
    :param y: target values
    :type y: numpy.ndarray
    :param alpha: Scale of prior on parameters
    :type alpha: float
    :param sigma2: Noise variance
    :type sigma2: float
    :param basis: basis function 
    :param type: function"""

    def __init__(self, X, y, alpha, sigma2, basis, num_basis, **kwargs):
        "Initialise"
        self.X = X
        self.y = y
        self.num_data = y.shape[0]
        self.sigma2 = sigma2
        self.alpha = alpha
        self.basis = basis
        self.num_basis = num_basis
        self.basis_args = kwargs
        self.Phi = basis(X, num_basis=num_basis, **kwargs)

    def update_QR(self):
        "Perform the QR decomposition on the basis matrix."
        self.Q, self.R = np.linalg.qr(np.vstack([self.Phi, self.alpha*np.eye(self.num_basis)]))

    def fit(self):
        """Minimize the objective function with respect to the parameters"""
        self.update_QR()
        self.mu_w = sp.linalg.solve_triangular(self.R, np.dot(self.Q[:self.y.shape[0], :].T, self.y))
        self.update_sum_squares()

    def predict(self, X):
        """Return the result of the prediction function."""
        return np.dot(self.basis(X, self.num_basis, **self.basis_args), self.mu_w)
        
    def update_f(self):
        """Update values at the prediction points."""
        self.f_bar = np.dot(self.Phi, self.mu_w)
        #self.f_var = np.dot(self.Phi, 

    def update_sum_squares(self):
        """Compute the sum of squares error."""
        self.update_f()
        self.sum_squares = ((self.y-self.f_bar)**2).sum()
        
    def objective(self):
        """Compute the objective function."""
        self.update_sum_squares()
        return self.sum_squares

    def log_likelihood(self):
        """Compute the log likelihood."""
        self.update_sum_squares()
        return -self.num_data/2.*np.log(np.pi*2.)-self.num_data/2.*np.log(self.sigma2)-self.sum_squares/(2.*self.sigma2)
    

def polynomial(x, num_basis=4, data_limits=[-1., 1.]):
    "Polynomial basis"
    centre = data_limits[0]/2. + data_limits[1]/2.
    span = data_limits[1] - data_limits[0]
    z = x - centre
    z = 2*z/span
    Phi = np.zeros((x.shape[0], num_basis))
    for i in range(num_basis):
        Phi[:, i:i+1] = z**i
    return Phi

def radial(x, num_basis=4, data_limits=[-1., 1.]):
    "Radial basis constructed using exponentiated quadratic form."
    if num_basis>1:
        centres=np.linspace(data_limits[0], data_limits[1], num_basis)
        width = (centres[1]-centres[0])/2.
    else:
        centres = np.asarray([data_limits[0]/2. + data_limits[1]/2.])
        width = (data_limits[1]-data_limits[0])/2.
    
    Phi = np.zeros((x.shape[0], num_basis))
    for i in range(num_basis):
        Phi[:, i:i+1] = np.exp(-0.5*((x-centres[i])/width)**2)
    return Phi

def fourier(x, num_basis=4, data_limits=[-1., 1.]):
    "Fourier basis"
    tau = 2*np.pi
    span = float(data_limits[1]-data_limits[0])
    Phi = np.zeros((x.shape[0], num_basis))
    for i in range(num_basis):
        count = float((i+1)//2)
        frequency = count/span
        if i % 2:
            Phi[:, i:i+1] = np.sin(tau*frequency*x)
        else:
            Phi[:, i:i+1] = np.cos(tau*frequency*x)
    return Phi

def plot_basis(basis, x_min, x_max, fig, ax, loc, text, diagrams='./diagrams', fontsize=20):
    """Plot examples of the basis vectors."""
    x = np.linspace(x_min, x_max, 100)[:, None]

    Phi = basis(x, num_basis=3)

    ax.plot(x, Phi[:, 0], '-', color=[1, 0, 0], linewidth=3)
    ylim = [-2, 2]
    ax.set_ylim(ylim)
    plt.sca(ax)
    plt.yticks([-2, -1, 0, 1, 2])
    plt.xticks([-1, 0, 1])
    ax.text(loc[0][0], loc[0][1],text[0], horizontalalignment='center', fontsize=fontsize)
    ax.set_xlabel('$x$', fontsize=fontsize)
    ax.set_ylabel('$\phi(x)$', fontsize=fontsize)

    plt.savefig(diagrams + '/' + basis.__name__ + '_basis1.svg')

    ax.plot(x, Phi[:, 1], '-', color=[1, 0, 1], linewidth=3)
    ax.text(loc[1][0], loc[1][1], text[1], horizontalalignment='center', fontsize=fontsize)

    plt.savefig(diagrams + '/' + basis.__name__ + '_basis2.svg')

    ax.plot(x, Phi[:, 2], '-', color=[0, 0, 1], linewidth=3)
    ax.text(loc[2][0], loc[2][1], text[2], horizontalalignment='center', fontsize=fontsize)

    plt.savefig(diagrams + '/' + basis.__name__ + '_basis3.svg')

    w = np.random.normal(size=(3, 1))
    
    f = np.dot(Phi,w)
    ax.cla()
    a, = ax.plot(x, f, color=[0, 0, 1], linewidth=3)
    ax.plot(x, Phi[:, 0], color=[1, 0, 0], linewidth=1) 
    ax.plot(x, Phi[:, 1], color=[1, 0, 1], linewidth=1)
    ax.plot(x, Phi[:, 2], color=[0, 0, 1], linewidth=1) 
    ylim = [-4, 3]
    ax.set_ylim(ylim)
    plt.sca(ax)
    plt.xticks([-1, 0, 1]) 
    ax.set_xlabel('$x$', fontsize=fontsize) 
    ax.set_ylabel('$f(x)$', fontsize=fontsize)
    t = []
    for i in range(w.shape[0]):
        t.append(ax.text(loc[i][0], loc[i][1], '$w_' + str(i) + ' = '+ str(w[i]) + '$', horizontalalignment='center', fontsize=fontsize))

    plt.savefig(diagrams + '/' + basis.__name__ + '_function1.svg')

    w = np.random.normal(size=(3, 1)) 
    f = np.dot(Phi,w) 
    a.set_ydata(f)
    for i in range(3):
        t[i].set_text('$w_' + str(i) + ' = '+ str(w[i]) + '$')
    plt.savefig(diagrams + '/' + basis.__name__ + '_function2.svg')


    w = np.random.normal(size=(3, 1)) 
    f = np.dot(Phi, w) 
    a.set_ydata(f)
    for i in range(3):
        t[i].set_text('$w_' + str(i) + ' = '+ str(w[i]) + '$')
    plt.savefig(diagrams + '/' + basis.__name__ + '_function3.svg')


    
def plot_marathon_fit(model, data_limits, fig, ax, x_val=None, y_val=None, objective=None, diagrams='./diagrams', fontsize=20, objective_ylim=None, prefix='olympic'):
    "Plot fit of the marathon data alongside error."
    ax[0].cla()
    ax[0].plot(model.X, model.y, 'o', color=[1, 0, 0], markersize=6, linewidth=3)
    if x_val is not None and y_val is not None:
        ax[0].plot(x_val, y_val, 'o', color=[0, 1, 0], markersize=6, linewidth=3)
        
    ylim = ax[0].get_ylim()

    x_pred = np.linspace(data_limits[0], data_limits[1], 130)[:, None]
    y_pred = model.predict(x_pred)
    
    ax[0].plot(x_pred, y_pred, color=[0, 0, 1], linewidth=2)
    ax[0].set_xlabel('year', fontsize=fontsize)
    ax[0].set_ylim(ylim)
    plt.sca(ax[0])

    xlim = ax[0].get_xlim()

    if objective is not None:
        max_basis = len(objective)
        ax[1].plot(range(max_basis), objective, 'o', color=[1, 0, 0], markersize=6, linewidth=3)
        if objective is not None:
            ax[1].set_ylim(objective_ylim)
        ax[1].set_xlim([-1, max_basis])
        ax[1].set_xlabel('polynomial order', fontsize=fontsize)

    file_name = prefix + '_' + model.__class__.__name__ + '_' + model.basis.__name__ + str(model.num_basis) + '.svg'
    plt.savefig(diagrams + '/' +file_name)

    
##########          Week 12          ##########
class GP():
    def __init__(self, X, y, sigma2, kernel, **kwargs):
        self.K = compute_kernel(X, X, kernel, **kwargs)
        self.X = X
        self.y = y
        self.sigma2 = sigma2
        self.kernel = kernel
        self.kernel_args = kwargs
        self.update_inverse()
    
    def update_inverse(self):
        # Preompute the inverse covariance and some quantities of interest
        ## NOTE: This is not the correct *numerical* way to compute this! It is for ease of use.
        self.Kinv = np.linalg.inv(self.K+self.sigma2*np.eye(self.K.shape[0]))
        # the log determinant of the covariance matrix.
        self.logdetK = np.linalg.det(self.K+self.sigma2*np.eye(self.K.shape[0]))
        # The matrix inner product of the inverse covariance
        self.Kinvy = np.dot(self.Kinv, self.y)
        self.yKinvy = (self.y*self.Kinvy).sum()

        
    def log_likelihood(self):
        # use the pre-computes to return the likelihood
        return -0.5*(self.K.shape[0]*np.log(2*np.pi) + self.logdetK + self.yKinvy)
    
    def objective(self):
        # use the pre-computes to return the objective function 
        return -self.log_likelihood()


def posterior_f(self, X_test):
    K_star = compute_kernel(self.X, X_test, self.kernel, **self.kernel_args)
    A = np.dot(self.Kinv, K_star)
    mu_f = np.dot(A.T, y)
    C_f = K_starstar - np.dot(A.T, K_star)
    return mu_f, C_f

def update_inverse(self):
    # Perform Cholesky decomposition on matrix
    self.R = sp.linalg.cholesky(self.K + self.sigma2*self.K.shape[0])
    # compute the log determinant from Cholesky decomposition
    self.logdetK = 2*np.log(np.diag(self.R)).sum()
    # compute y^\top K^{-1}y from Cholesky factor
    self.Rinvy = sp.linalg.solve_triangular(self.R, self.y)
    self.yKinvy = (self.Rinvy**2).sum()
    
    # compute the inverse of the upper triangular Cholesky factor
    self.Rinv = sp.linalg.solve_triangular(self.R, np.eye(self.K.shape[0]))
    self.Kinv = np.dot(self.Rinv, self.Rinv.T)
    
def compute_kernel(X, X2, kernel, **kwargs):
    K = np.zeros((X.shape[0], X2.shape[0]))
    for i in np.arange(X.shape[0]):
        for j in np.arange(X2.shape[0]):
            K[i, j] = kernel(X[i, :], X2[j, :], **kwargs)
        
    return K
    
def exponentiated_quadratic(x, x_prime, variance, lengthscale):
    "Exponentiated quadratic covaraince function."
    squared_distance = ((x-x_prime)**2).sum()
    return variance*np.exp((-0.5*squared_distance)/lengthscale**2)        
