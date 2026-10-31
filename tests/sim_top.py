import os
import sys
from pathlib import Path

import cocotb
from cocotb.triggers import Timer
from cocotb_tools.runner import get_runner

# set up and begin verilog simulation
def sim_top_runner():

    sim = os.getenv("SIM", "icarus")

    proj_path = Path(__file__).resolve().parent.parent
    sys.path.append(str(proj_path / "tests"))

    source_code = [proj_path / "hdl" / "top_module.sv"]

    runner = get_runner(sim)
    runner.build(
        sources=source_code,
        hdl_toplevel="top_module",
        always=False
    )

    runner.test(
        hdl_toplevel="top_module", test_module="gui"
    )


# call to begin verilog simulation
if __name__ == "__main__":
    sim_top_runner()
