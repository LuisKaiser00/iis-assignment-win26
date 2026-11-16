# Assignment 2 — Integrated Intelligent Systems

Open `L02_Body_Motion_Problem_Tutorial_completed.ipynb` in JupyterLab with the working directory set to this folder.

## Submitted files
- `L02_Body_Motion_Problem_Tutorial_completed.ipynb` — solutions to E1–E6, Part 2 model explanation, executed reach and structural tests
- `robot.xacro` — main model and user-adjustable parameters
- `base.xacro`, `arm.xacro`, `gripper.xacro` — separate component definitions
- `robot.urdf` — expanded URDF for URDF-only visualization tools
- `urdf_background.html`, `urdf_handon.html` — original exercise instructions
- `expand_xacro.py` — tiny offline Xacro subset expander (for validation; not a replacement for ROS Xacro)

## How to use
In JupyterLab, upload the entire folder and run the notebook from within the folder. Standard ROS-based expansion: `xacro robot.xacro > robot.urdf`. In minimal Python-only environments: `python expand_xacro.py` creates the same example `robot.urdf` using a limited offline evaluator.

## Design assumptions
Arm has 3 revolute joints (shoulder, elbow, wrist), plus 2 prismatic finger joints. The gripper opens to 0.14 m, exceeding the carton width (0.10 m). Wrist-height IK targets are (x,z)=(0.55,0.40)m and (0.65,1.00)m. These x-distances are engineering choices because the handout only specified vertical heights. The robot is planar and fixed to a pedestal. Contact, sensing, collision-free motion, real grasping and fluid dynamics are **not** simulated.
