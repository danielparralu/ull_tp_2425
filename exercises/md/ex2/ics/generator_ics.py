import numpy as np


G = 4.302e-6  # kpc km^2/s^2
G = 1


class ic:
    def __init__(
        self,
        sim_name,
        dt=0.01,
        dt_out=0.1,
        t_end=15,
        epsilon=None,
        theta=1,
    ):

        self.file_name = 'ics/ic_' + sim_name + '.txt'
        self.sim_name = sim_name
        self.dt = dt
        self.dt_out = dt_out
        self.t_end = t_end
        self.theta = theta
        self.epsilon = epsilon

        self.X = np.empty((0, 7))

        self.components = True

    def uni_sphere(self, N, R, M_total, V_max, xyz_0):
        r = np.random.uniform(0, R, size=N)
        theta = np.random.uniform(0, np.pi, size=N)
        phi = np.random.uniform(0, 2 * np.pi, size=N)

        x = r * np.sin(theta) * np.cos(phi) + xyz_0[0]
        y = r * np.sin(theta) * np.sin(phi) + xyz_0[1]
        z = r * np.cos(theta) + xyz_0[2]

        m = np.ones_like(r) * M_total / len(r)

        v_x = -V_max * np.sin(theta) * np.cos(phi)
        v_y = -V_max * np.sin(theta) * np.sin(phi)
        v_z = -V_max * np.cos(theta)

        X = np.column_stack([m, x, y, z, v_x, v_y, v_z])

        self.X = np.vstack([self.X, X])
        self.L = 2 * R

    def exp_disk(self, N, R_d, z_scale, M_disk):
        r = np.random.exponential(scale=R_d, size=N)
        angles = np.random.uniform(0, 2 * np.pi, size=N)
        x = r * np.cos(angles)
        y = r * np.sin(angles)
        z = np.random.normal(scale=z_scale, size=N)

        m = np.ones_like(r) * M_disk / len(r)
        M = np.empty_like(r)
        for i in range(len(r)):
            M[i] = np.sum(m[r <= r[i]])
            r_others = np.sqrt(
                self.X[:, 1] ** 2 + self.X[:, 2] ** 2 + self.X[:, 3] ** 2
            )
            M[i] = M[i] + np.sum(self.X[:, 0][r_others <= r[i]])

        v_circ = np.sqrt(G * M / r)

        v_x = -v_circ * np.sin(angles)
        v_y = v_circ * np.cos(angles)
        v_z = np.random.normal(scale=10, size=N)

        X = np.column_stack([m, x, y, z, v_x, v_y, v_z])

        self.X = np.vstack([self.X, X])
        self.L = 2 * R_d

    def save_file(self):
        self.N = len(self.X)
        if self.epsilon is None:
            factor = 0.1
            self.epsilon = factor * self.L / self.N ** (1 / 3)
        with open(self.file_name, 'w') as f:
            f.write("! Simulation name:\n")
            f.write(f"{self.sim_name}\n\n")

            f.write("! Time step:\n")
            f.write(f"{self.dt}\n\n")

            f.write("! Output time step:\n")
            f.write(f"{self.dt_out}\n\n")

            f.write("! Final time:\n")
            f.write(f"{self.t_end}\n\n")

            f.write("! Number of particles:\n")
            f.write(f"{self.N}\n\n")

            f.write("! Theta:\n")
            f.write(f"{self.theta}\n\n")

            f.write("! Epsilon (softening length):\n")
            f.write(f"{self.epsilon}\n\n")

            f.write("! Positions (x,y,z) (each line, a particle):\n")
            positions = self.X[:, 1:4]
            np.savetxt(f, positions, fmt="%.10f", delimiter=", ")
            f.write("\n")

            f.write("! Velocity (vx, vy, vz) (each line, a particle):\n")
            velocities = self.X[:, 4:7]
            np.savetxt(f, velocities, fmt="%.10f", delimiter=", ")
            f.write("\n")

            f.write("! Mass (each line, a particle):\n")
            masses = self.X[:, 0]
            np.savetxt(f, masses, fmt="%.10f")


if __name__ == "__main__":

    file_name = input("Enter the file name: ")
    theta = float(input("Enter theta: "))
    dt = float(input("Enter dt: "))
    dt_out = float(input("Enter dt_out: "))
    t_end = float(input("Enter t_end: "))

    ics = ic(file_name, theta=theta, dt=dt, dt_out=dt_out, t_end=t_end)

    num_unispheres = int(input("Enter the number of uniform spheres: "))
    for i in range(num_unispheres):
        print(f"Enter parameters for unisphere {i+1}:")
        N = int(input("  Enter N (particle numbers): "))
        R = float(input("  Enter R (maximum radius of the unisphere): "))
        M_total = float(input("  Enter M_total (total mass of the sphere): "))
        V_max = float(
            input(
                "  Enter V_max (maximum velocity in magnitude of a particle in the sphere): "
            )
        )
        xyz_0 = (
            float(input("  Enter x0: ")),
            float(input("  Enter y0: ")),
            float(input("  Enter z0: ")),
        )
        ics.uni_sphere(N, R, M_total, V_max, xyz_0)

    ics.save_file()
