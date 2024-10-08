# -*- coding: utf-8 -*-
"""PR2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hf_TdKeqPoOJwuciwt46CpOl3kxvxO9z

<br>
<font>
<!-- <img src="https://cdn.freebiesupply.com/logos/large/2x/sharif-logo-png-transparent.png" alt="SUT logo" width=300 height=300 align=left class="saturate"> -->
<div dir=ltr align=center>
<img src="https://cdn.freebiesupply.com/logos/large/2x/sharif-logo-png-transparent.png" width=200 height=200>
<br>
<font color=0F5298 size=7>
Linear Algebra <br>
<font color=2565AE size=5>
Computer Engineering Department <br>
Spring 2024<br>
<font color=3C99D size=5>
Practical Assignment 2 <br>
<font color=696880 size=4>
<!-- <br> -->
Ashkan Majidi - Mahdi Alinejad - Keyhan Hodaei - Mohammad Mahdi Abedian - Mohammad Farhan Bahrami - Mohammadhossein salimi

____

# Personal Data
"""

student_number = '401106396'
first_name = 'mobina'
last_name = 'kochaknia'

"""# Introduction

In this assignment, you will implement some Algorithms and topics which you've already learned their theoretical foundations in the class. Note that **you are not allowed to use `numpy.linalg` functions in this notebook**.

Import your needed libraries here.
"""

import tester
import numpy as np
import math
import plotly.graph_objs as go
import matplotlib.pyplot as plt

# TODO: write your code here

"""# Q1: System of Equations (20 + 20 Points)

In this part, you are going to solve a system of equations using the Gauss-Jordan elimination method. You will also use the results to find the conic section that fits the given data points.

First, write a function that gets an augmented matrix as its input and then returns the results if the matrix could be solved using the Gauss-Jordan elimination method. If the matrix could not be solved, the function should return an appropriate error message.
"""

def solve(A, b):
    try:
        # Combine A and b to form the augmented matrix
        m = [row + [rhs] for row, rhs in zip(A, b)]

        # Convert m to echelon form
        h, w = len(m), len(m[0])
        for y in range(0, h):
            maxrow = y
            for y2 in range(y+1, h):    # Find max pivot
                if abs(m[y2][y]) > abs(m[maxrow][y]):
                    maxrow = y2
            m[y], m[maxrow] = m[maxrow], m[y]
            if m[y][y] == 0:     # Singular?
                return "The system of equations has no solution."
            for y2 in range(y+1, h):    # Eliminate column y
                c = m[y2][y] / m[y][y]
                for x in range(y, w):
                    m[y2][x] -= m[y][x] * c

        # Convert m to reduced row-echelon form
        for y in range(h-1, 0-1, -1):
            c = m[y][y]
            for y2 in range(0, y):
                for x in range(w-1, y-1, -1):
                    m[y2][x] -=  m[y][x] * m[y2][y] / c
            m[y][y] /= c
            for x in range(h, w):       # Normalize row y
                m[y][x] /= c

        # Extract solutions
        solutions = []
        for row in m:
            solutions.append(row[-1])
        return solutions

    except Exception as e:
        return f"An error occurred: {str(e)}"

"""Consider the [Ecliptic Coordinate System](https://en.wikipedia.org/wiki/Ecliptic_coordinate_system) in astronomy. The coordinates of a star in this system are given as $(\lambda, \beta)$, where $\lambda$ is the ecliptic longitude and $\beta$ is the ecliptic latitude.

We will give you the position vectors of an astronomical object with respect to a distant observer for five different [true anomalies](https://en.wikipedia.org/wiki/True_anomaly).

Consider the [Conic Sections](https://en.wikipedia.org/wiki/Conic_section) in mathematics. The general form of a conic section is given as $Ax^2 + Bxy + Cy^2 + Dx + Ey + F = 0$. Every orbit of astronomical objects (such as planets, asteroids, comets, etc.) is a conic section. Conic sections are classified into four types: ellipse, parabola, hyperbola, and circle.

Fit a surface to the given points.

Surface equation: $Ax + By+ Cz + D = 0$.
We take the value of C as one, and we obtain the values of A, B, and D using the following system of equations.

\begin{align*}
\sum_{i=1}^{N} z_i &= -B \sum_{i=1}^{N} y_i - A \sum_{i=1}^{N} x_i - D N \\
\sum_{i=1}^{N} z_i y_i &= -B \sum_{i=1}^{N} y_i^2 - A \sum_{i=1}^{N} x_i y_i - D \sum_{i=1}^{N} y_i \\
\sum_{i=1}^{N} z_i x_i &= -B \sum_{i=1}^{N} x_i y_i - A \sum_{i=1}^{N} x_i^2 - D \sum_{i=1}^{N} x_i
\end{align*}


"""

vectors = tester.vectors[0]
print(vectors)

import numpy as np

def surface_fit(vectors):
    # Calculate the sums needed for the system of equations
    x = vectors[:, 0]
    y = vectors[:, 1]
    z = vectors[:, 2]

    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_z = np.sum(z)
    sum_x2 = np.sum(x**2)
    sum_y2 = np.sum(y**2)
    sum_xy = np.sum(x*y)
    sum_xz = np.sum(x*z)
    sum_yz = np.sum(y*z)
    N = len(vectors)

    # Create the matrix and the right-hand side vector
    matrix = np.array([[sum_x2, sum_xy, sum_x],
                       [sum_xy, sum_y2, sum_y],
                       [sum_x,  sum_y,  N]])
    rhs = np.array([-sum_xz, -sum_yz, -sum_z])

    # Solve the system of equations
    A, B, D = np.linalg.solve(matrix, rhs)

    # We take the value of C as one
    C = 1.0

    return A, B, C, D

print(surface_fit(vectors))

"""### **From this cell to the end of Q1 Tasks are optional and have extra points.**

Retrieve the normal vector of the obtained surface.
"""

def get_normal_vector(A, B, C, D):
    # The normal vector of the surface is [A, B, C]
    return np.array([A, B, C])

A, B, C, D = surface_fit(vectors)
normal_vector = get_normal_vector(A, B, C, D)
print(normal_vector)

"""[Longitude of the Ascending Node](https://en.wikipedia.org/wiki/Longitude_of_the_ascending_node#:~:text=The%20longitude%20of%20the%20ascending,in%20a%20specified%20reference%20plane): The angle measured along the ecliptic plane from the [vernal equinox](https://en.wikipedia.org/wiki/Equinox) to the point where the orbit crosses the ecliptic plane from south to north.

[Inclination](https://en.wikipedia.org/wiki/Orbital_inclination): The angle between the orbital plane of a celestial body (such as a planet or satellite) and a reference plane, usually the ecliptic plane for objects in the solar system. It is measured in degrees and indicates how tilted the orbit is relative to the reference plane.

Find Inclination and Longitude of the Ascending Node of the orbit.
"""

import numpy as np

def get_inclination_and_longitude(normal_vector):
    # Normalize the normal vector
    normal_vector = normal_vector / np.linalg.norm(normal_vector)

    # Extract the components
    A, B, C = normal_vector

    # Calculate the inclination (in degrees)
    i = np.arccos(C) * 180 / np.pi

    # Calculate the longitude of the ascending node (in degrees)
    Ω = np.arctan2(-B, A) * 180 / np.pi

    # Make sure Ω is in the range [0, 360)
    if Ω < 0:
        Ω += 360

    return i, Ω

normal_vector = get_normal_vector(A, B, C, D)
i, Ω = get_inclination_and_longitude(normal_vector)
print(f"Inclination: {i} degrees")
print(f"Longitude of the Ascending Node: {Ω} degrees")

"""Find a translation vector to translate coordinates system to the orbit's plane and then translate the coordinate system."""

def translate(u, v):
    # The translation of vector u by vector v is u + v
    return u + v
translation_vector = get_translation_vector(A, B, C, D)
translation_vector = None
vectors = [translate(vector, translation_vector) for vector in vectors]

"""To align the xy plane of the coordinate system with the orbital plane, it needs to be rotated by an angle equal to `the ascending node longitude` around the `z-axis` and another rotation by an angle equal to the `orbital inclination` around the `x-axis`. First, write two functions to find the components of a vector in the rotated coordinate system around x and z axes, then find all vectors in the rotated coordinate system.<br>Hint: Use rotation matrices"""

# Some useful trigonometric functions
def cos(x):
    return math.cos(x * math.pi / 180)

def acos(x):
    return math.acos(x) * 180 / math.pi

def sin(x):
    return math.sin(x * math.pi / 180)

def asin(x):
    return math.asin(x) * 180 / math.pi

def tan(x):
    return math.tan(x * math.pi / 180)

def atan(x):
    return math.atan(x) * 180 / math.pi

def rotate_about_z(vector, x):
    #TODO: find the z-axis rotation matrix
    rotation_matrix = None
    #TODO: find the rotated vector by multiplying the rotation matrix and the vector
    return np.dot(rotation_matrix, vector)
def rotate_about_x(vector, x):
    #TODO: find the x-axis rotation matrix
    rotation_matrix = None
    #TODO: find the rotated vector by multiplying the rotation matrix and the vector
    return np.dot(rotation_matrix, vector)
def rotate_in_surface(vector):
    #TODO: find the vector in the rotated coordinate system
    u = None
    #TODO: return the vector in the rotated coordinate system
    return u - np.array([0, 0, u[2]])

#TODO: find all vectors in the rotated coordinate system
in_surface_vectors = None
print(in_surface_vectors)

"""General equation of conic sections is:
$Ax^2 + Bxy + Cy^2 + Dx + Ey + F = 0$<br>
Find the coefficients A, B, C, D, and E in such a way that they satisfy the given data points.<br>
consider that `F = 1`
"""

def find_conic(vectors):
    #TODO: use the conic section equation above to find the coefficients A, B, C, D, E
    #TODO: return the coefficients A, B, C, D, E, F
    pass
A, B, C, D, E, F = find_conic(in_surface_vectors)
print(find_conic(in_surface_vectors))

"""In the standard equation of a conic section, the coefficient B is equal to zero. To standardize the equation, rotate your coordinate system by an angle $\theta$ around the z-axis such that the following equation is satisfied:
$tan(2\theta) = \frac{B} {A - C}$<br>
Then, use the function you wrote to find the coefficients of the conic section.
"""

#TODO: find the rotation angle
rotation_angle = None
print(rotation_angle)
#TODO: rotate the vectors by the rotation angle around z-axis
rotated_vectors = None
print(find_conic(rotated_vectors))
A, B, C, D, E, F = find_conic(rotated_vectors)
#print your outputs (theta, A, C, D, E)

"""Assume $\Delta = B^2 - 4AC$<br>
If $\Delta < 0$, the conic section is ellipse or circle (for a circle, we have $A = C$).<br>
If $\Delta = 0$, the conic section is a parabola.<br>
If $\Delta > 0$, the conic section is a hyperbola.<br>
If you want to do any comparison between these coefficients, it's better to round their values to 8 decimal places and then compare them.<br>
|
Write a function that identifies the type of a conic section based on the values of A, B, and C.
"""

def conic_type(A, B, C):
    #TODO: find the value of delta, do the comparison and return the type of the conic section
    pass
orbit_type = conic_type(A, B, C)
print(orbit_type)

"""[Eccentricity](https://en.wikipedia.org/wiki/Eccentricity_(mathematics)): The eccentricity of a conic section is a parameter that determines the conic section's shape.<br>
For a circle, the eccentricity is 0.<br>
For a parabola, the eccentricity is 1.<br>
For an ellipse, the eccentricity is between 0 and 1.<br>
For a hyperbola, the eccentricity is greater than 1.<br><br>
An ellipse is denoted by the following equations:<br><br>
$\frac{(x-x_0)^2}{a^2} + \frac{(y-y_0)^2}{b^2} = 1$ (the ellipse is horizontal)<br>
$\frac{(y-y_0)^2}{a^2} + \frac{(x-x_0)^2}{b^2} = 1$ (the ellipse is vertical)<br><br>
The eccentricity of an ellipse is:<br><br>
$e = \sqrt{1 - \frac{b^2}{a^2}}$<br><br>
Where $a$ is the semi-major axis of the ellipse and $b$ is the semi-minor axis of the ellipse.<br><br><br>
A hyperbola is denoted by the following equations:<br><br>
$\frac{(x-x_0)^2}{a^2} - \frac{(y-y_0)^2}{b^2} = 1$ (the hyperbola is horizontal)<br>
$\frac{(y-y_0)^2}{a^2} - \frac{(x-x_0)^2}{b^2} = 1$ (the hyperbola is vertical)<br><br>
The eccentricity of a hyperbola is:<br><br>
$e = \sqrt{1 + \frac{b^2}{a^2}}$<br><br>
Where $a$ is the semi-major axis of the hyperbola and $b$ is the semi-minor axis of the hyperbola.<br><br><br>
A parabola is denoted by the following equations:<br><br>
$(x-x_0)^2 = 4a(y-y_0)$ (the parabola is horizontal)<br>
$(y-y_0)^2 = 4a(x-x_0)$ (the parabola is vertical)<br><br>
The eccentricity of a parabola is 1.<br>
Run the cell below to calculate the eccentricity of the orbit.
"""

def find_eccentricity(A, C):
    orbit_type = conic_type(A, 0, C)
    if orbit_type == "circle":
        return 0
    if orbit_type == "parabola":
        return 1
    if orbit_type == "ellipse":
        A = abs(A)
        C = abs(C)
        return (1 - (min(A, C) / max(A, C))) ** 0.5
    if A > 0:
        return math.sqrt(1 + A / -C)
    return math.sqrt(1 + C / -A)

e = round(find_eccentricity(A, C), 5)
print(e)

"""[Semi-major axis](https://en.wikipedia.org/wiki/Semi-major_and_semi-minor_axes): The semi-major axis of an orbit is its longest radius, denoted by $a$.<br>
Run the following cell to find the semi-major axis of the orbit.
"""

def find_semi_major_axis(A, C, D, E):
    if find_eccentricity(A, C) != 1:
        x0 = -D/(2 * A)
        y0 = -E / (2 * C)
        standard_vectors = [translate(vec, [x0, y0, 0]) for vec in rotated_vectors]
        A, B, C, D, E, F = find_conic(standard_vectors)
    e = find_eccentricity(A, C)
    if e == 0:
        return 1/math.sqrt(A)
    if e < 1:
        if abs(A) < abs(C):
            return math.sqrt(1 / A)
        return math.sqrt(1 / C)
    if e > 1:
        if A > 0:
            return math.sqrt(1 / A)
        else:
            return math.sqrt(1 / C)
    if abs(A) < abs(C):
        return abs(D / (4 * C))
    return abs(E / (4 * A))

a = round(find_semi_major_axis(A, C, D, E), 4)
print(a)

"""Locate the Sun and plot the orbit.<br>
Hint: The Sun is located at one of the foci of the orbit (if the orbit has two foci, choose one of them).
"""

f = plt.figure()
f.set_figwidth(10)
f.set_figheight(10)
plt.grid(color='lightgray',linestyle='--')
def axes():
    plt.axhline(0, alpha=.1)
    plt.axvline(0, alpha=.1)
if orbit_type == "ellipse" or orbit_type == "circle":
    b = a * (1- e ** 2) ** 0.5
    t = np.linspace(0, 2*math.pi, 100)
    plt.xlim([-1.2 * a, 1.2 * a])
    plt.ylim([-1.2 * a, 1.2 * a])
    plt.plot(a*np.cos(t) , b*np.sin(t), color = "green")
elif orbit_type == "parabola":
    x = np.linspace(0, 10 * a, 400)
    y = np.linspace(- 5 * a, 5 * a, 400)
    plt.xlim([-0.2 * a, 10.2 * a])
    plt.ylim([-5.2 * a, 5.2 * a])
    x, y = np.meshgrid(x, y)
    axes()
    plt.contour(x, y, (y**2 - 4*a*x), [0], colors='green')
else:
    b = a * math.sqrt(e ** 2 - 1)
    t = np.linspace(0, 2)
    plt.plot( a*np.cosh(t) , b*np.sinh(t) , color = "green")
    plt.plot( a*np.cosh(t) , -b*np.sinh(t) , color = "green")
    plt.plot( -a*np.cosh(t) , b*np.sinh(t) , color = "green")
    plt.plot( -a*np.cosh(t) , -b*np.sinh(t) , color = "green")
    plt.xlim([-1.2 * a * math.cosh(2), 1.2 * a* math.cosh(2)])
    plt.ylim([-1.2 * a * math.cosh(2), 1.2 * a * math.cosh(2)])

plt.plot(a * e,0,'ro', label = "sun")
plt.annotate("sun", (a * e, 0.04 * a), size = 20)
plt.show()

"""# Q2: Gram-Schmidt (40 Points)

The Gram-Schmidt process is a mathematical technique used to transform a set of linearly independent vectors into an orthogonal (or orthonormal) set of vectors. It is commonly used in linear algebra and numerical computations.

Now we want to implement Gram-Schmidt process so that given a set of linearly independent vectors $a_1, a_2, \cdots, a_k$, output should be orthonormal vectors $q_1, q_2, \cdots, q_k$ .
"""

def gram_schmidt(A: np.ndarray):
    """
    A: matrix with columns a_1, a_2, ..., a_k.
    output: matrix Q with columns q_1, q_2, ..., q_k.
    """
    Q = np.zeros_like(A, dtype=np.float64)
    for i in range(A.shape[1]):
        # Start with the i'th column of A
        q = A[:, i].astype(float)
        # Subtract the projections onto the previous vectors
        for j in range(i):
            q -= np.dot(Q[:, j], A[:, i]) * Q[:, j]
        # Normalize
        norm = np.linalg.norm(q)
        if norm < 1e-10:
            raise ValueError(f"Vector {i} is linearly dependent with previous vectors")
        else:
            Q[:, i] = q / norm
    return Q

A1 = np.array([[5, -1, 12, 3], [2, -15, 4, 9], [2, -2, 7, -4], [0, 8, 1, 11]])
A2 = np.array([[1, 2, 0], [8, 1, -6], [-3, 12, 1]])

B1 = gram_schmidt(A1)
B2 = gram_schmidt(A2)

print("test 1:")
tester.gram_schmidt_test(A1, B1)
print("test 2:")
tester.gram_schmidt_test(A2, B2)

"""Now we want to visualise this process in 3D space. The `vector_plot` function takes a list of vectors and visualizes them in 3D space. Here’s how it works:

Input Parameters:

- <strong>tvects:</strong> A list of vectors (each represented as a 3-tuple or array).<br>
- <strong>is_vect:</strong> A boolean flag indicating whether the input vectors are true vectors (default is True).<br>
- <strong>orig:</strong> The origin point (default is [0, 0, 0]).<br>

Steps:

- Create a 6-tuple array (coords) to store the coordinates of the vectors.
<br>
- For each vector in tvects:
<br><br>
Extract the first and second 3-tuples to represent the beginning and end points of the vector.<br>
Use Scatter3d from Plotly to create a vector visualization with appropriate coloring, size, and other properties.<br>
Add the vector to the data list.<br>
<br>
- Set the layout for the 3D plot.
<br>
- Create the figure and display it using fig.show().
"""

def vector_plot(tvects: np.ndarray, is_vect=True, orig=[0, 0, 0]):
    # Make a 6-tuple array for coords from the input vectors
    coords = [np.concatenate([orig, v]) for v in tvects]

    data = []
    for i, c in enumerate(coords):
        # Save first and second 3-tuple of each coord to have begin and end of each vector
        X, Y, Z = c[:3], c[3:], c[3:]
        # Make a vector by use Scatter3d in plotly.graph_objs with coloring and size and ... the vector
        vector = go.Scatter3d(x=[X[0], Y[0]], y=[X[1], Y[1]], z=[X[2], Z[2]],
                              marker=dict(size=[0, 3],
                                          color=['blue', 'blue']),
                              line=dict(width=6, color='blue'),
                              name='Vector')
        # Then save the vector in data[]
        data.append(vector)

    layout = go.Layout(margin=dict(l=4, r=4, b=4, t=4))
    fig = go.Figure(data=data, layout=layout)
    fig.show()

A = [[1, -1, 1], [1, 0, 1], [1, 1, 2]]

print("Plot of inital vectors\n")
vector_plot(A)

B = gram_schmidt(np.array(A))
print("Matrix of orthonormal vectors : \n", B)
vector_plot(B)

"""# Q3: Change of Basis (40 Points)

Consider vector $v_a$ in basis $a_1, a_2, \cdots, a_n \in \mathbb{R}^n$, We want to find its representation $v_b$ in basis $b_1, b_2, \cdots, b_n \in \mathbb{R}^n$. $A$ is a $n\times n$ matrix with columns $a_1, a_2, \cdots, a_n$, $B$ is a matrix with columns $b_1, b_2, \cdots, b_n$ and we have the following relation between them: $$Av_a = Bv_b$$
By knowing the above equation, Implement a function which takes representation of a $v_a$ in basis $A$ and returns its representation in basis $B$.
"""

def gauss_jordan(m):
    n = len(m)
    augmented_matrix = np.hstack([m, np.eye(n)])
    for i in range(n):
        if augmented_matrix[i][i] == 0:
            for j in range(i+1, n):
                if augmented_matrix[j][i] != 0:
                    augmented_matrix[[i, j]] = augmented_matrix[[j, i]]
                    break
        if augmented_matrix[i][i] == 0:
            raise ValueError("Matrix is singular and cannot be inverted.")

        augmented_matrix[i] = augmented_matrix[i] / augmented_matrix[i][i]
        for j in range(n):
            if i != j:
                augmented_matrix[j] = augmented_matrix[j] - \
                    augmented_matrix[i] * augmented_matrix[j][i]

    return augmented_matrix[:, n:]


def basis_change(va, A, B):
    va_in_standard = np.dot(A, va)
    B_inv = gauss_jordan(B)
    va_in_new_basis = np.dot(B_inv, va_in_standard)
    return va_in_new_basis

"""Use the below block to test your code."""

for s in range(1, 4):
    i = 3**s
    nA, mA = 3**s, 3**s
    nB, mB = 3**s, 3**s
    va = tester.vector_generator(i, 100)
    A = tester.matrix_generator(nA, mA, 10)
    B = tester.matrix_generator(nB, mB, 10)

    vb = basis_change(va, A, B)

    print("test " + str(s) + ": ")
    tester.change_of_basis_test(va, vb, A, B)

"""Now we want to visualize our vectors. Implement a funciton which its input is a set of vectors and it draws the vectors in gridline using matplotlib. Vectors must be shown as arrows and your grid should be like the grids shown below. [This matplotlib function](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.quiver.html) may be useful in your implementation.

"""

def plot_vectors(vectors):
    """
    vectors: list of vectors to plot.
    output: a gridline in which vectors are drawn as arrows.
    """
    # Create a grid
    scale = 2
    x = np.linspace(-scale, scale, 20)
    y = np.linspace(-scale, scale, 20)
    X, Y = np.meshgrid(x, y)

    # Plot gridlines
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')

    # Plot vectors as arrows
    for v in vectors:
        plt.arrow(0, 0, v[0], v[1], head_width=0.05, head_length=0.05, fc='red', ec='red')

    # Set axis limits
    plt.xlim(-scale, scale)
    plt.ylim(-scale, scale)

    # Add labels
    plt.xlabel('X')
    plt.ylabel('Y')

    # Show the plot
    plt.show()

"""Lets visualise two vector sets. these vectors are in standard basis."""

v1 = np.array([2,0])
v2 = np.array([0,1])
v3 = np.array([2,1])
vectors1 = [v1, v2, v3]

alpha = np.linspace(0, 2*np.pi, 41)
vectors2= list(zip(np.cos(alpha), np.sin(alpha)))

plot_vectors(vectors1)
plot_vectors(vectors2)

"""Change the basis of vector set 1 and 2 to basis $B_1$ and $B_2$ then visualize their representation in new basis."""

B1 = np.array([[1, 1], [1, -1]])
B2 = np.array([[2, 1], [1, 2]]) / 2

import numpy as np
import matplotlib.pyplot as plt

# Original vectors
v1 = np.array([2, 0])
v2 = np.array([0, 1])
v3 = np.array([2, 1])

# New basis vectors
B1 = np.array([[1, 1], [1, -1]])
B2 = np.array([[2, 1], [1, 2]]) / 2

# Transform vectors to new basis
v1_new_basis = np.dot(B1, v1)
v2_new_basis = np.dot(B1, v2)
v3_new_basis = np.dot(B1, v3)

# Plot original and transformed vectors
plt.figure(figsize=(8, 6))
plt.quiver(*v1_new_basis, angles='xy', scale_units='xy', scale=1, color='b', linestyle='--')
plt.quiver(*v2_new_basis, angles='xy', scale_units='xy', scale=1, color='g', linestyle='--')
plt.quiver(*v3_new_basis, angles='xy', scale_units='xy', scale=1, color='r', linestyle='--')
plt.xlim(-1, 3)
plt.ylim(-1, 3)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Vector Set 1 in New Basis')
plt.legend()
plt.grid()
plt.show()

def plot_vectors(vectors):
    """
    vectors: list of vectors to plot.
    output: a gridline in which vectors are drawn as arrows.
    """
    xs = [vector[0] for vector in vectors]
    ys = [vector[1] for vector in vectors]
    max_value = max(max(xs), max(ys), abs(min(xs)), abs(min(ys)))

    scale = max_value * 1.2

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.set_xlim(-scale, scale)
    ax.set_ylim(-scale, scale)
    ax.grid(True, which='both', linestyle='--')
    for vector in vectors:
        x, y = vector
        ax.arrow(0, 0, x, y, head_width=0.05*scale,head_length=0.1*scale, fc='blue', ec='blue')
    plt.show()

def invert_matrix(matrix):
    n = matrix.shape[0]
    augmented_matrix = np.hstack([matrix, np.eye(n)])
    for i in range(n):
        pivot_row = i
        for j in range(i + 1, n):
            if abs(augmented_matrix[j, i]) > abs(augmented_matrix[pivot_row, i]):
                pivot_row = j
        augmented_matrix[[i, pivot_row]] = augmented_matrix[[pivot_row, i]]
        augmented_matrix[i] /= augmented_matrix[i, i]
        for j in range(n):
            if i != j:
                augmented_matrix[j] -= augmented_matrix[i] * augmented_matrix[j, i]
    return augmented_matrix[:, n:]


alpha = np.linspace(0, 2*np.pi, 41)
vectors2= list(zip(np.cos(alpha), np.sin(alpha)))

new_vector_set_2 = basis_change(vectors2, B1, B2)

# Visualize the vectors in the new basis
plot_vectors(new_vector_set_2)