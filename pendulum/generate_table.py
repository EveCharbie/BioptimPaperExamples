from time import time

import numpy as np
from bioptim import Solver

from .pendulum.ocp import prepare_ocp


def generate_table(out):
    root_path = "/".join(__file__.split("/")[:-1])
    model_path = root_path + "/models/MassPoint_pendulum.bioMod"
    np.random.seed(0)

    # IPOPT
    ocp = prepare_ocp(biorbd_model_path=model_path)
    solver = Solver.IPOPT()
    solver.set_linear_solver("ma57")
    solver.set_print_level(0)

    # --- Solve the program --- #
    tic = time()
    sol = ocp.solve(solver=solver)
    toc = time() - tic
    sol_merged = sol.merge_phases()

    out.nx = sol_merged.states["all"].shape[0]
    out.nu = sol_merged.controls["all"].shape[0]
    out.ns = sol_merged.ns[0]
    out.solver.append(out.Solver("Ipopt"))
    out.solver[0].n_iteration = sol.iterations
    out.solver[0].cost = sol.cost
    out.solver[0].convergence_time = toc
    out.solver[0].compute_error_single_shooting(sol, 1)
