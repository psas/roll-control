#!/usr/bin/env python
import lv2
import unittest
from math import fabs


class TestLV2(unittest.TestCase):

    def test_CL_zero_a(self):
        for velocity in range(0,500,100):
            cl = lv2.C_L(0, velocity)
            self.assertEqual(cl, 0.0)

    def test_CL(self):
        for velocity in range(0,500,100):
            for angle in range(0,15,2):
                cl = lv2.C_L(angle, velocity)
                self.assertLess(cl, 1.0)

    def test_lift_zero_a(self):
        for velocity in range(0,500,100):
            for altitude in range(0,10000,1000):
                lift = lv2.lift(0, velocity, altitude)
                self.assertEqual(lift, 0.0)

    def test_lift_zero_v(self):
        for angle in range(0,15,2):
            for altitude in range(0,10000,1000):
                lift = lv2.lift(angle, 0, altitude)
                self.assertEqual(lift, 0.0)

    def test_lift_case0(self):
        lift = lv2.lift(1, 200, 4000)
        self.assertAlmostEqual(lift,  0.7533, places=4)

    def test_lift_case1(self):
        lift = lv2.lift(1, 330, 4000)
        self.assertAlmostEqual(lift,  2.61987, places=4)

    def test_lift_case2(self):
        lift = lv2.lift(13, 60, 4000)
        self.assertAlmostEqual(lift,  1.05606, places=4)

    def test_aa_zero_a(self):
        for velocity in range(0,500,100):
            for altitude in range(0,10000,1000):
                aa = lv2.angular_accel(0, altitude, velocity, 1)
                self.assertEqual(aa, 0.0)

    def test_aa_case0(self):
        aa = lv2.angular_accel(0.5, 3000, 300, 5)
        self.assertAlmostEqual(aa, 272.8236256, places=4)

    def test_aa_case1(self):
        aa = lv2.angular_accel(13, 4000, 100, 20)
        self.assertAlmostEqual(aa, 742.1556022, places=4)

    def test_aa_pos(self):
        aa = lv2.angular_accel(13, 4000, 100, 20)
        self.assertGreater(aa, 10)

    def test_aa_neg(self):
        aa = lv2.angular_accel(-13, 4000, 100, 20)
        self.assertLess(aa, 10)

    def test_servo(self):
        alpha = lv2.servo(5, 0.135)
        self.assertEqual(alpha, 5)
        alpha = lv2.servo(4, 0.136)
        self.assertEqual(alpha, 5)

    def test_servo_15(self):
        alpha = lv2.servo(34, 0.135)
        self.assertEqual(alpha, 15)

    def test_servo_neg15(self):
        alpha = lv2.servo(-34, 0.135)
        self.assertEqual(alpha, -15)

    def test_reverselookup(self):

        for test_alpha in range(1, 15):
            for alt in range(100,10000, 500):
                for vel in range(50, 400, 50):
                    for t in range(30):
                        aa = lv2.angular_accel(test_alpha, alt, vel, t)
                        alpha  = lv2.estimate_alpha(aa, alt, vel, t)

                        # not worse than 5% error:
                        percent_diff = (fabs(alpha - test_alpha)/test_alpha)*100.0
                        self.assertLess(percent_diff, 5)


if __name__ == '__main__':
    unittest.main()
