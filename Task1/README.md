# IC2122 Task1: Forward Kinematics
Students are required to control the UR3 joint angle to make UR3's end-effector arrive at the specific points. In the process, students can understand the relationship between the joint angle and end-effector. Also, students have a better understanding of forward kinematics.

## 1. Controlling UR3 joint angle
Students can control the joint angle by pressing the keys of the keybroad or clicking the button on the output panel.

**Keybroad control**
---------------------------
- Joint:    (+),(-)     
(+): add 1 degree to the specific joint angle
(+): subtract 1 degree to the specific joint angle
- Joint1:   (Q),(W)
- Joint2:   (A),(S)
- Joint3:   (Z),(X)
- Joint4:   (E),(R)
- Joint5:   (D),(F)
- Joint6:   (C),(V)

Gripper (RG2):
- (T):  Open the RG2
- (Y):  Clsoe the RG2

Pose:
- (L):   Return all of the joint angles as 0 degrees (return pose)

**Panel control**
---------------------------
![image](https://github.com/Summer-Lo/IC2122_Robot_Lab/tree/IC2122/Task1/images/Task1_panel.png)
This panel displays the joint number and corresponding joint angle which is similar to the UR3 controlling panel. Also, the target's position and orientation is displayed at the bottom part. Besides, there are some buttons that can be clicking and activating corresponding actions.
- Joint Name:   Display at the Left-side which is similar with the real UR3 user panel.
- Joint Angle:  Display at the Right-side which unit is degree.

- (<<): Subtract 5 degrees to the corresponding joint angle
- (<):  Subtract 1 degrees to the corresponding joint angle
- (>>): Add 5 degrees to the corresponding joint angle
- (>):  Add 1 degrees to the corresponding joint angle

- "Return Pose (L)":    Return all of the joint angles as 0 degrees (return pose)
- "Open RG2 (Y)":       Open the RG2
- "Close RG2 (Y)":      Close the RG2

- "Joint Angle Configuration (input joint angle at administrator)":  Students can set the joint angle to the corresponding joint by entering the value of joint angle (degree) in the administrator terminal after clicking this button

At the bottom part, there are some information of the UR3's End-effector (Tip).
- Position:         X, Y, Z
- Orientation:      Alpha, Beta, Gamma

## 2. Student Activities
**Activity 1**
---------------------------
Students should practice controlling the joint angle. Please mark down your result which will be useful for another activity.

**Activity 2**
---------------------------
Applying the knowledge and result from the previous activity, students should enter the joint angles to make the end-effector arrive at a specific position by clicking "Joint Angle Configuration (input joint angle at administrator)" button.

## 3. Task Step
- Step 1:   Practicing the joint angle control.
- Step 2:   Observing the relationship between joint angle and end-effector (Forward Kinematics).
- Step 3:   Controlling the end-effector to arrive at Point 1 (different colors of blocks) by clicking or pressing the button and keyboard.
- Step 4:   Repeating the previous step for arriving at Point 2.
- Step 5:   Pressing the "Joint Angle Configuration (input joint angle at administrator)" button to set the joint angle directly for arriving at point 3. 