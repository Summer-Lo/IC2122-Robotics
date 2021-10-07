# IC2122 Task2: Inverse Kinematics
Students are required to control the target position and orientation to make UR3's end-effector arrive at the specific points. In the process, students can understand the importance end-effector's position and orientation. Also, students have a better understanding of inverse kinematics.

## 2. Controlling UR3
Students can control target poisiton and orientation. Adopting the inverse kinematics, the end-effector will be attracted to arrive the position and orientaiotn of the target.

**Keybroad control (Joint angle control Disabled)**
---------------------------
Joint Angle control is disabled at this task.

Gripper (RG2):
- (T):  Open the RG2
- (Y):  Clsoe the RG2

Pose:
- (L):  Return the target position and orientation as the original value. (return pose)

Target:
- (I):  Set the target's position and orientation.
- (P):  Set the target's position.
- (O):  Set the target's orientation.

**Panel control (Joint angle control Disabled)**
---------------------------
Joint Angle control is disabled at this task.

![image](https://github.com/Summer-Lo/IC2122_Robot_Lab/tree/IC2122/Task2/images/Task2_panel.png)
This panel displays the joint number and corresponding joint angle which is similar to the UR3 controlling panel. Also, the target's position and orientation is displayed at the bottom part. Besides, there are some buttons that can be clicked and activatied corresponding actions.
- Joint Name:   Display at the Left-side which is similar with the real UR3 user panel.
- Joint Angle:  Display at the Right-side which unit is degree.


- "Return Pose (L)":        Return the target position and orientation as the original value. (return pose)
- "Open RG2 (Y)":           Open the RG2
- "Close RG2 (Y)":          Close the RG2

At the bottom part, there are some information of the UR3's End-effector (Tip), and button for achieving the inverse kinematics.
- Position:                 X, Y, Z
- Orientation:              Alpha, Beta, Gamma

Below buttons are required to input the value at the administrator terminal.
- "Set Target (I)":         Set the target's position and orientation.
- "Set Position (P)":       Set the target's position.
- "Set Orientation (O)":    Set the target's orientation.

## 3. Task Step
- Step 1:   Praticing for setting the target position.
- Step 2:   Observing the relationship between joint angle and end-effector (Inverse Kinematics).
- Step 3:   Measuring and finding out the position of the point in V-REP.
- Step 4:   Setting the target's position for arriving at the point.
- Step 5:   Observing the angle of gipper whether it is suitable to grip the blocks.
- Step 6:   Setting the target's orientation for gripper the block vertically.
- Steo 7:   Repeating the previous step for arriving at another point.


# IC2122 Task2.1: Inverse Kinematics
Students should observe the inverse kinematics solution and joint angle conbination.

**Keybroad control (Joint angle control Disabled)**
---------------------------
Same as the previous task.
**Panel control (Joint angle control Disabled)**
---------------------------
Joint Angle control is disabled at this task.

![image](https://github.com/Summer-Lo/IC2122_Robot_Lab/tree/IC2122/Task2/images/Task2.1_panel.png)

Same as the previous part.

Solution: Below three solution displayed different joint angle conbination for arriving the same position and orientation.

"Solution 1":   The First conbination of inverse kinematics
"Solution 2":   The Second conbination of inverse kinematics
"Solution 3":   The Third conbination of inverse kinematics



## 3. Task Step
- Step 1:   Clicking the "Solution 1" button and observe the result
- Step 2:   Clicking the "Solution 2" button and observe the result
- Step 3:   Clicking the "Solution 3" button and observe the result
- Step 4:   Discussing the result and observation.
