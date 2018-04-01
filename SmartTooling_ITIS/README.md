<h1>Valve leak detection for ITIS in the SmartTooling project.</h1>
<h2>Challenge</h2>
<p>Inspection of valves for leaks at high pressure puts operators in dangerous environments. During the test the valve can be under pressure up to 2000 bar. The inspection by a robot overcomes this issue. After the testing the robot should show the location of detected leaks to the operator.</p>
<h2>Solution</h2>
<p>The UR robot can be shown the path to follow beforehand. During testing the leak detector can send a digital input to the robot controller when a leak is detected.</p>
<p>A separate thread on the UR controller can detect the incoming signals from the leak detector and store the current robot pose and sent these poses to the Python program running on an external controller over socket communication.</p>
<p>When testing is finished the robot should show the operator the locations of the detected leaks by moving to the stored locations where leaks were detected. The difficulty here is to avoid collisions between robot and valve while moving to these leak positions. A solution could be to roughly follow the same path as the path that was taught for inspection since this path was taught by the opeator and is known to be collision free. To record this path a third thread on de UR controller sends robot poses at fixed time intervals to the python program on the external controller.</p>
<p>The python program will read and store both types of robot poses (time triggered and leak triggered) chronologically in a list. Besides the pose values (x, y, z, a, b, c) the messages from the UR robot also contains a &lsquo;leak flag&rsquo; to indicate whether the pose represents a leak position or not.</p>
<p>When the leak test is finished and the operator chooses to view the detected leaks, the UR controller will ask poses one at a time from the external controller. The robot will then:</p>
<ul>
<li>Move to the received pose and</li>
<li>Check the value of the &lsquo;leak flag&rsquo; and depending the value of the &lsquo;leak flag&rsquo;
<ul>
<li>ask for the next pose or</li>
<li>wait for the operator to confirm the leak has been marked and then move to the next pose.</li>
</ul>
</li>
</ul>
