# Pololu AltIMU-10 v5 Gyro, Accelerometer, Compass, and Altimeter

To read gyroscope angles, a Madgwick filter is used in our Orientation class.

Simply put, call the ```get_roll_pitch_and_yaw_in_degrees()``` function from the Orientation class as follows:

```python
from pololuAltIMUv5.orientation import Orientation

orientation_interface = Orientation()
roll, pitch, yaw = orientation_interface.get_roll_pitch_and_yaw_in_degrees()

```