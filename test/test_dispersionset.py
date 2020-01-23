"""Tests for DispersionSet class."""

from testtools import unittest, TestCase, get_full_path
import swipp
import logging
logging.basicConfig(level=logging.DEBUG)


class Test_DispersionSet(TestCase):

    def setUp(self):
        self.full_path = get_full_path(__file__)

    # def test_from_geopsy(self):
    #     fname = self.full_path + "data/test_dc_mod2_ray2_lov2_shrt.txt"
    #     swipp.DispersionSet.from_geopsy(fname=fname)


    def test_init(self):
        # Instantiate DispersionCurve objects.
        frequency = [1, 2, 3]
        velocity = [4, 5, 6]
        ray = swipp.DispersionCurve(frequency=frequency, velocity=velocity)
        lov = swipp.DispersionCurve(frequency=frequency, velocity=velocity)

        # Rayleigh Alone
        ex_a = swipp.DispersionSet(identifier="Test", misfit=None,
                                   rayleigh={0: ray}, love=None)
        self.assertListEqual(velocity, ex_a.rayleigh[0].velocity.tolist())
        self.assertEqual("Test", ex_a.identifier)
        self.assertEqual(None, ex_a.misfit)

        # Love Alone
        ex_b = swipp.DispersionSet(identifier="Test", misfit=None,
                                   rayleigh=None, love={0: lov})
        self.assertListEqual(velocity, ex_b.love[0].velocity.tolist())

        # Rayleigh and Love
        ex_c = swipp.DispersionSet(identifier="Test", misfit=None,
                                   rayleigh={0: ray}, love={0: lov})
        self.assertListEqual(velocity, ex_c.rayleigh[0].velocity.tolist())
        self.assertListEqual(velocity, ex_c.love[0].velocity.tolist())

    def test_from_geopsy(self):
        myset = swipp.DispersionSet.from_geopsy(
            fname=self.full_path+"data/test_dc_mod2_ray2_lov2_shrt.txt")
        self.assertEqual(myset.misfit, 1.08851)
        self.assertEqual(myset.identifier, "149641")
        true_ray = {0: swipp.DispersionCurve([0.15, 64],
                                             [1/0.000334532972901842, 1/0.00917746839997367]),
                    1: swipp.DispersionCurve([0.479030947360446, 68],
                                             [1/0.000323646256288129, 1/0.00832719612771301])}
        true_lov = {0: swipp.DispersionCurve([0.11, 61],
                                             [1/0.0003055565316784, 1/0.00838314255586564]),
                    1: swipp.DispersionCurve([0.920128309893243, 69],
                                             [1/0.000305221889470528, 1/0.00828240730448549])}
        for test_key, test_value in myset.rayleigh.items():
            self.assertArrayEqual(true_ray[test_key].frequency, test_value.frequency)
            self.assertArrayEqual(true_ray[test_key].velocity, test_value.velocity)
        for test_key, test_value in myset.love.items():
            self.assertArrayEqual(true_lov[test_key].frequency, test_value.frequency)
            self.assertArrayEqual(true_lov[test_key].velocity, test_value.velocity)


if __name__ == "__main__":
    unittest.main()
