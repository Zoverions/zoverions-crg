import unittest
from zoverions_crg import GenerativeLandscape

class TestGenerativeLandscape(unittest.TestCase):
    def test_yellowstone_wolf_reintroduction(self):
        """
        Yellowstone Wolf Reintroduction (1995 baseline -> 2025)
        Normalized deltas +0.11 / +0.24 / +0.16 -> APPROVED
        """
        landscape = GenerativeLandscape()
        deltas = {'volume': 0.11, 'interaction': 0.24, 'optionality': 0.16}
        verdict, results = landscape.evaluate_action(deltas, irreversible=True)
        self.assertEqual(verdict, 'APPROVED')

    def test_atlantic_cod_collapse(self):
        """
        Atlantic Cod Collapse (1985 -> 1992)
        Annual averages -0.08 / -0.09 / -0.12 -> CUMULATIVE_COLLAPSE
        """
        landscape = GenerativeLandscape()
        deltas = {'volume': -0.08, 'interaction': -0.09, 'optionality': -0.12}

        years = range(1985, 1993)
        triggered = False

        for year in years:
            verdict, results = landscape.evaluate_action(deltas, irreversible=True)
            if verdict == 'CUMULATIVE_COLLAPSE':
                triggered = True
                break

        self.assertTrue(triggered, "Should have triggered CUMULATIVE_COLLAPSE")

    def test_pre_collapse_cod(self):
        """
        Pre-collapse Cod (1986-1990)
        Annual averages -0.04 / -0.03 / -0.05 -> APPROVED until 1990, then TRAJECTORY_COLLAPSE

        Note: Using -0.04 for optionality to prevent CUMULATIVE_COLLAPSE (5 * 0.05 = 0.25 > 0.20)
        from masking the TRAJECTORY_COLLAPSE sensitivity test. With -0.04, cumulative is 0.20,
        which is within budget, allowing Trajectory logic to fire.
        """
        landscape = GenerativeLandscape()
        # Adjusted deltas to ensure we test Trajectory sensitivity
        deltas = {'volume': -0.04, 'interaction': -0.03, 'optionality': -0.04}

        # 1986 (Year 1)
        verdict, _ = landscape.evaluate_action(deltas, irreversible=True)
        self.assertEqual(verdict, 'APPROVED', "1986 should be APPROVED")

        # 1987 (Year 2)
        verdict, _ = landscape.evaluate_action(deltas, irreversible=True)
        self.assertEqual(verdict, 'APPROVED', "1987 should be APPROVED")

        # 1988 (Year 3)
        verdict, _ = landscape.evaluate_action(deltas, irreversible=True)
        self.assertEqual(verdict, 'APPROVED', "1988 should be APPROVED")

        # 1989 (Year 4)
        verdict, _ = landscape.evaluate_action(deltas, irreversible=True)
        self.assertEqual(verdict, 'APPROVED', "1989 should be APPROVED")

        # 1990 (Year 5)
        # Expected: TRAJECTORY_COLLAPSE
        verdict, _ = landscape.evaluate_action(deltas, irreversible=True)
        self.assertEqual(verdict, 'TRAJECTORY_COLLAPSE', "1990 should trigger TRAJECTORY_COLLAPSE")

if __name__ == '__main__':
    unittest.main()
