"""Independent arithmetic oracles. These are NOT M-Tools implementation tests."""
from decimal import Decimal as D, ROUND_CEILING
from math import asin, exp, log, sqrt, ceil
from statistics import NormalDist
import unittest


class ReferenceCalculations(unittest.TestCase):
    def test_qt01_cac(self):
        self.assertEqual(D(2000) / 20, D(100))

    def test_qt02_roas(self):
        self.assertEqual(D(3000) / 1000, D(3))

    def test_qt03_margin(self):
        margin = D(10000) - 6000
        self.assertEqual((margin, margin / 10000, margin / 100), (D(4000), D('.4'), D(40)))

    def test_qt04_break_even(self):
        self.assertEqual((D(4000) / (100 - 60)).to_integral_value(rounding=ROUND_CEILING), D(100))
        self.assertEqual((D(4001) / 40).to_integral_value(rounding=ROUND_CEILING), D(101))

    def test_qt05_price_scenarios(self):
        def profit(price, volume, cost, fixed):
            return (D(price) - cost) * volume - fixed
        self.assertEqual(profit(90, 150, 60, 2000) - profit(100, 100, 60, 2000), D(500))

    def test_qt06_funnel(self):
        self.assertEqual((D(40)/100, D(20)/40, D(20)/100), (D('.4'), D('.5'), D('.2')))

    def test_qt07_churn(self):
        churn = D(10) / 100
        self.assertEqual((churn, 1-churn), (D('.1'), D('.9')))

    def test_qt08_sample(self):
        z = NormalDist().inv_cdf(.975)
        raw = z*z*.5*.5/.05**2
        self.assertEqual(ceil(raw), 385)
        adjusted = ceil(1000*raw/(999+raw))
        self.assertEqual((adjusted, ceil(adjusted/.5)), (278, 556))

    def test_qt09_gap(self):
        self.assertEqual((D(70)-100, (D(70)-100)/100), (D(-30), D('-.3')))

    def test_qt10_romi(self):
        self.assertEqual((D(1500)-500)/500, D(2))

    def test_qt11_media(self):
        self.assertEqual((D(200)/10000, D(100)/200, 1000*D(100)/10000, D(100)/10), (D('.02'), D('.5'), D(10), D(10)))

    def test_qt12_tam(self):
        self.assertEqual(1000*4*D(50), D(200000))

    def test_qt13_normal_power_reference(self):
        h = abs(2*asin(sqrt(.15))-2*asin(sqrt(.10)))
        normal = NormalDist()
        critical = normal.inv_cdf(.975)
        approx = ceil(2*(critical + normal.inv_cdf(.8))**2/h**2)
        def power(group_n):
            shift = h*sqrt(group_n/2)
            return normal.cdf(-critical-shift) + 1-normal.cdf(critical-shift)
        self.assertEqual(approx, 681)
        self.assertGreaterEqual(power(681), .8)
        self.assertLess(power(680), .8)

    def test_qt14_ltv(self):
        ltv = sum(D(v)/(1+D(0))**t for t,v in enumerate((40,30),1))
        self.assertEqual((ltv, ltv-D(20), ltv/20), (D(70), D(50), D('3.5')))

    def test_qt15_payback(self):
        def crossing(cac, values):
            total = D(0)
            if cac == 0:
                return 0
            for t, value in enumerate(values,1):
                total += D(value)
                if total >= cac:
                    return t
            return None
        self.assertEqual(crossing(D(100), [40,40,40]), 3)
        self.assertIsNone(crossing(D(100), [20,20]))
        self.assertEqual(crossing(D(0), []), 0)
        self.assertEqual(D(100)/40, D('2.5'))

    def test_weighted_score(self):
        self.assertEqual(D('.8')*D('.6')+D('.2')*D('.4'), D('.56'))
        self.assertEqual(D('.4')*D('.6')+D('.9')*D('.4'), D('.60'))

    def test_gabor_granger(self):
        prices = [D(100), D(120), D(150)]
        demand = [D('.8'), D('.6'), D('.4')]
        self.assertEqual([x*y for x,y in zip(prices,demand)], [D(80),D(72),D(60)])
        self.assertEqual([(x-80)*y for x,y in zip(prices,demand)], [D(16),D(24),D(28)])

    def test_bass(self):
        m,p,q=1000,.03,.38
        def cumulative(t):
            e=exp(-(p+q)*t)
            return m*(1-e)/(1+(q/p)*e)
        series=[cumulative(t) for t in range(13)]
        self.assertAlmostEqual(series[0],0)
        self.assertTrue(all(a<=b<=m for a,b in zip(series,series[1:])))
        self.assertAlmostEqual(sum(b-a for a,b in zip(series,series[1:])),series[-1])
        self.assertAlmostEqual(log(q/p)/(p+q),6.192619,places=5)

    def test_preference_ideal(self):
        def preference(x,y):
            return 10+2*x+4*y-x*x-y*y
        self.assertEqual((D(2)/(2*1),D(4)/(2*1)),(D(1),D(2)))
        self.assertGreater(preference(1,2), preference(0,0))

    def test_mental_availability(self):
        self.assertEqual((D(60)/100,D(120)/60),(D('.6'),D(2)))
        self.assertEqual((D(60)/100)*(D(120)/60),D('1.2'))

    def test_linear_optimization_oracle(self):
        objective,x,y=max((3*x+2*y,x,y) for x in range(3) for y in range(5) if x+y<=4)
        self.assertEqual((objective,x,y),(10,2,2))

    def test_effect_and_budget(self):
        self.assertEqual(D(30)/100-D(20)/100,D('.1'))
        self.assertEqual(D(60)+50-100,D(10))


if __name__ == '__main__':
    unittest.main(verbosity=2)
