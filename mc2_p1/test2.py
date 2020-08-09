import unittest
import datetime as dt
import marketsim_editedv4

class MyTestCase(unittest.TestCase):

    def test_orders_short(self):
        portvals = marketsim_editedv4.compute_portvals(orders_file = "./orders/orders-short.csv", start_val=1000000)
        final_portfolio_value = portvals.ix[-1,:][0]
        final_portfolio_dataframe_length = len(portvals)

        expected_value = 998035.0
        self.assertAlmostEqual(expected_value, final_portfolio_value, 4, "Final portfolio value is {} incorrect. Expected {}".format(final_portfolio_value, expected_value), delta=None)

        expected_value = 11
        self.assertEqual(expected_value, final_portfolio_dataframe_length, "Final portfolio dataframe length {} is incorrect. Expected {}".format(final_portfolio_dataframe_length, expected_value))


    def test_orders(self):
        portvals = marketsim_editedv4.compute_portvals(orders_file = "./orders/orders.csv", start_val=1000000)
        final_portfolio_value = portvals.ix[-1,:][0]
        final_portfolio_dataframe_length = len(portvals)

        expected_value = 1133860.0
        self.assertAlmostEqual(expected_value, final_portfolio_value, 4, "Final portfolio value is {} incorrect. Expected {}".format(final_portfolio_value, expected_value), delta=None)

        expected_value = 240
        self.assertEqual(expected_value, final_portfolio_dataframe_length, "Final portfolio dataframe length {} is incorrect. Expected {}".format(final_portfolio_dataframe_length, expected_value))


    def test_orders2(self):
        portvals = marketsim_editedv4.compute_portvals(orders_file = "./orders/orders2.csv", start_val=1000000)
        final_portfolio_value = portvals.ix[-1,:][0]
        final_portfolio_dataframe_length = len(portvals)

        expected_value = 1078752.6
        self.assertAlmostEqual(expected_value, final_portfolio_value, 4, "Final portfolio value is {} incorrect. Expected {}".format(final_portfolio_value, expected_value), delta=None)

        expected_value = 232
        self.assertEqual(expected_value, final_portfolio_dataframe_length, "Final portfolio dataframe length {} is incorrect. Expected {}".format(final_portfolio_dataframe_length, expected_value))



    def test_orders3(self):
        portvals = marketsim_editedv4.compute_portvals(orders_file = "./orders/orders3.csv", start_val=1000000)
        final_portfolio_value = portvals.ix[-1,:][0]
        final_portfolio_dataframe_length = len(portvals)

        expected_value = 1050160.0
        self.assertAlmostEqual(expected_value, final_portfolio_value, 4, "Final portfolio value is {} incorrect. Expected {}".format(final_portfolio_value, expected_value), delta=None)

        expected_value = 141
        self.assertEqual(expected_value, final_portfolio_dataframe_length, "Final portfolio dataframe length {} is incorrect. Expected {}".format(final_portfolio_dataframe_length, expected_value))



    def test_orders_01(self):
        portvals = marketsim_editedv4.compute_portvals(orders_file = "./orders/orders-01.csv", start_val=1000000)
        final_portfolio_value = portvals.ix[-1,:][0]
        final_portfolio_dataframe_length = len(portvals)

        expected_value = 1115569.2
        self.assertAlmostEqual(expected_value, final_portfolio_value, 4, "Final portfolio value is {} incorrect. Expected {}".format(final_portfolio_value, expected_value), delta=None)

        expected_value = 245
        self.assertEqual(expected_value, final_portfolio_dataframe_length, "Final portfolio dataframe length {} is incorrect. Expected {}".format(final_portfolio_dataframe_length, expected_value))


    def test_orders_03(self):
        portvals = marketsim_editedv4.compute_portvals(orders_file = "./orders/orders-03.csv", start_val=1000000)
        final_portfolio_value = portvals.ix[-1,:][0]
        final_portfolio_dataframe_length = len(portvals)

        expected_value = 857616.0
        self.assertAlmostEqual(expected_value, final_portfolio_value, 4, "Final portfolio value is {} incorrect. Expected {}".format(final_portfolio_value, expected_value), delta=None)

        expected_value = 240
        self.assertEqual(expected_value, final_portfolio_dataframe_length, "Final portfolio dataframe length {} is incorrect. Expected {}".format(final_portfolio_dataframe_length, expected_value))


    def test_orders_04(self):
        portvals = marketsim_editedv4.compute_portvals(orders_file = "./orders/orders-04.csv", start_val=1000000)
        final_portfolio_value = portvals.ix[-1,:][0]
        final_portfolio_dataframe_length = len(portvals)

        expected_value = 923545.4
        self.assertAlmostEqual(expected_value, final_portfolio_value, 4, "Final portfolio value is {} incorrect. Expected {}".format(final_portfolio_value, expected_value), delta=None)

        expected_value = 233
        self.assertEqual(expected_value, final_portfolio_dataframe_length, "Final portfolio dataframe length {} is incorrect. Expected {}".format(final_portfolio_dataframe_length, expected_value))


    def test_orders_05(self):
        portvals = marketsim_editedv4.compute_portvals(orders_file = "./orders/orders-05.csv", start_val=1000000)
        final_portfolio_value = portvals.ix[-1,:][0]
        final_portfolio_dataframe_length = len(portvals)

        expected_value = 1415563.0
        self.assertAlmostEqual(expected_value, final_portfolio_value, 4, "Final portfolio value is {} incorrect. Expected {}".format(final_portfolio_value, expected_value), delta=None)

        expected_value = 296
        self.assertEqual(expected_value, final_portfolio_dataframe_length, "Final portfolio dataframe length {} is incorrect. Expected {}".format(final_portfolio_dataframe_length, expected_value))


    def test_orders_06(self):
        portvals = marketsim_editedv4.compute_portvals(orders_file = "./orders/orders-06.csv", start_val=1000000)
        final_portfolio_value = portvals.ix[-1,:][0]
        final_portfolio_dataframe_length = len(portvals)

        expected_value = 894604.3
        self.assertAlmostEqual(expected_value, final_portfolio_value, 4, "Final portfolio value is {} incorrect. Expected {}".format(final_portfolio_value, expected_value), delta=None)

        expected_value = 210
        self.assertEqual(expected_value, final_portfolio_dataframe_length, "Final portfolio dataframe length {} is incorrect. Expected {}".format(final_portfolio_dataframe_length, expected_value))



    def test_orders_07(self):
        portvals = marketsim_editedv4.compute_portvals(orders_file = "./orders/orders-07.csv", start_val=1000000)
        final_portfolio_value = portvals.ix[-1,:][0]
        final_portfolio_dataframe_length = len(portvals)

        expected_value = 1106563.3
        self.assertAlmostEqual(expected_value, final_portfolio_value, 4, "Final portfolio value is {} incorrect. Expected {}".format(final_portfolio_value, expected_value), delta=None)

        expected_value = 237
        self.assertEqual(expected_value, final_portfolio_dataframe_length, "Final portfolio dataframe length {} is incorrect. Expected {}".format(final_portfolio_dataframe_length, expected_value))


    def test_orders08(self):
        portvals = marketsim_editedv4.compute_portvals(orders_file = "./orders/orders-08.csv", start_val=1000000)
        final_portfolio_value = portvals.ix[-1,:][0]
        final_portfolio_dataframe_length = len(portvals)

        expected_value = 1074884.1
        self.assertAlmostEqual(expected_value, final_portfolio_value, 4, "Final portfolio value is {} incorrect. Expected {}".format(final_portfolio_value, expected_value), delta=None)

        expected_value = 229
        self.assertEqual(expected_value, final_portfolio_dataframe_length, "Final portfolio dataframe length {} is incorrect. Expected {}".format(final_portfolio_dataframe_length, expected_value))


    def test_orders_09(self):
        portvals = marketsim_editedv4.compute_portvals(orders_file = "./orders/orders-09.csv", start_val=1000000)
        final_portfolio_value = portvals.ix[-1,:][0]
        final_portfolio_dataframe_length = len(portvals)

        expected_value = 1067710.0
        self.assertAlmostEqual(expected_value, final_portfolio_value, 4, "Final portfolio value is {} incorrect. Expected {}".format(final_portfolio_value, expected_value), delta=None)

        expected_value = 37
        self.assertEqual(expected_value, final_portfolio_dataframe_length, "Final portfolio dataframe length {} is incorrect. Expected {}".format(final_portfolio_dataframe_length, expected_value))


    def test_orders_10(self):
        portvals = marketsim_editedv4.compute_portvals(orders_file = "./orders/orders-10.csv", start_val=1000000)
        final_portfolio_value = portvals.ix[-1,:][0]
        final_portfolio_dataframe_length = len(portvals)

        expected_value = 1050160.0
        self.assertAlmostEqual(expected_value, final_portfolio_value, 4, "Final portfolio value is {} incorrect. Expected {}".format(final_portfolio_value, expected_value), delta=None)

        expected_value = 141
        self.assertEqual(expected_value, final_portfolio_dataframe_length, "Final portfolio dataframe length {} is incorrect. Expected {}".format(final_portfolio_dataframe_length, expected_value))


    def test_orders_11(self):
        portvals = marketsim_editedv4.compute_portvals(orders_file = "./orders/orders-11.csv", start_val=1000000)
        final_portfolio_value = portvals.ix[-1,:][0]
        final_portfolio_dataframe_length = len(portvals)

        expected_value = 1078670.0
        self.assertAlmostEqual(expected_value, final_portfolio_value, 4, "Final portfolio value is {} incorrect. Expected {}".format(final_portfolio_value, expected_value), delta=None)

        expected_value = 37
        self.assertEqual(expected_value, final_portfolio_dataframe_length, "Final portfolio dataframe length {} is incorrect. Expected {}".format(final_portfolio_dataframe_length, expected_value))


    def test_orders_12(self):
        portvals = marketsim_editedv4.compute_portvals(orders_file = "./orders/orders-12.csv", start_val=1000000)
        final_portfolio_value = portvals.ix[-1,:][0]
        final_portfolio_dataframe_length = len(portvals)

        expected_value = 1050160.0
        self.assertAlmostEqual(expected_value, final_portfolio_value, 4, "Final portfolio value is {} incorrect. Expected {}".format(final_portfolio_value, expected_value), delta=None)

        expected_value = 240
        self.assertEqual(expected_value, final_portfolio_dataframe_length, "Final portfolio dataframe length {} is incorrect. Expected {}".format(final_portfolio_dataframe_length, expected_value))


    def test_orders_leverage(self):
        portvals = marketsim_editedv4.compute_portvals(orders_file = "./orders/orders-leverage.csv", start_val=1000000)
        final_portfolio_value = portvals.ix[-1,:][0]
        final_portfolio_dataframe_length = len(portvals)

        expected_value = 1087919.23
        self.assertAlmostEqual(expected_value, final_portfolio_value, 4, "Final portfolio value is {} incorrect. Expected {}".format(final_portfolio_value, expected_value), delta=None)

        expected_value = 232
        self.assertEqual(expected_value, final_portfolio_dataframe_length, "Final portfolio dataframe length {} is incorrect. Expected {}".format(final_portfolio_dataframe_length, expected_value))


    def test_orders_leverage_1(self):
        portvals = marketsim_editedv4.compute_portvals(orders_file = "./orders/orders-leverage-1.csv", start_val=1000000)
        final_portfolio_value = portvals.ix[-1,:][0]
        final_portfolio_dataframe_length = len(portvals)

        expected_value = 1050160.0
        self.assertAlmostEqual(expected_value, final_portfolio_value, 4, "Final portfolio value is {} incorrect. Expected {}".format(final_portfolio_value, expected_value), delta=None)

        expected_value = 106
        self.assertEqual(expected_value, final_portfolio_dataframe_length, "Final portfolio dataframe length {} is incorrect. Expected {}".format(final_portfolio_dataframe_length, expected_value))


    def test_orders_leverage_2(self):
        portvals = marketsim_editedv4.compute_portvals(orders_file = "./orders/orders-leverage-2.csv", start_val=1000000)
        final_portfolio_value = portvals.ix[-1,:][0]
        final_portfolio_dataframe_length = len(portvals)

        expected_value = 1074650.0
        self.assertAlmostEqual(expected_value, final_portfolio_value, 4, "Final portfolio value is {} incorrect. Expected {}".format(final_portfolio_value, expected_value), delta=None)

        expected_value = 37
        self.assertEqual(expected_value, final_portfolio_dataframe_length, "Final portfolio dataframe length {} is incorrect. Expected {}".format(final_portfolio_dataframe_length, expected_value))


    def test_orders_leverage_3(self):
        portvals = marketsim_editedv4.compute_portvals(orders_file = "./orders/orders-leverage-3.csv", start_val=1000000)
        final_portfolio_value = portvals.ix[-1,:][0]
        final_portfolio_dataframe_length = len(portvals)

        expected_value = 1050160.0
        self.assertAlmostEqual(expected_value, final_portfolio_value, 4, "Final portfolio value is {} incorrect. Expected {}".format(final_portfolio_value, expected_value), delta=None)

        expected_value = 141
        self.assertEqual(expected_value, final_portfolio_dataframe_length, "Final portfolio dataframe length {} is incorrect. Expected {}".format(final_portfolio_dataframe_length, expected_value))



if __name__ == '__main__':
    unittest.main()
