import unittest
from pyvvo.equipment import capacitor
import os
import pandas as pd
import numpy as np

# Handle pathing.
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
CAPACITORS = os.path.join(THIS_DIR, 'query_capacitors.csv')


class CapacitorSinglePhaseTestCase(unittest.TestCase):
    """Basic property tests for CapacitorSinglePhase."""

    def setUp(self):
        """Create CapacitorSinglePhase object."""
        self.cap = \
            capacitor.CapacitorSinglePhase(name='cap1', mrid='1', phase='c',
                                           state='OpEn', name_prefix='cap_')

    def test_name_prefix(self):
        self.assertEqual('cap_', self.cap.name_prefix)

    def test_name(self):
        """Ensure the prefix was added to the name."""
        self.assertEqual(self.cap.name, 'cap_cap1')

    def test_mrid(self):
        self.assertEqual('1', self.cap.mrid)

    def test_phase(self):
        """Lower case phase should be cast to upper case."""
        self.assertEqual('C', self.cap.phase)

    def test_state(self):
        """State should be cast to upper case."""
        self.assertEqual('OPEN', self.cap.state)

    def test_state_none(self):
        """None is a valid state to initialize a capacitor."""
        cap = \
            capacitor.CapacitorSinglePhase(name='cap1', mrid='1', phase='c',
                                           state=None, name_prefix='cap_')
        self.assertIsNone(cap.state)

    def test_repr(self):
        self.assertEqual(str(self.cap), self.cap.name)


class CapacitorSinglePhaseBadInputsTestCase(unittest.TestCase):
    """Test bad inputs to CapacitorSinglePhase"""

    def test_name_prefix_bad_type(self):
        self.assertRaises(TypeError, capacitor.CapacitorSinglePhase,
                          name='cap', mrid='1', phase='A', state='OPEN',
                          name_prefix=1)

    def test_name_bad_type(self):
        self.assertRaises(TypeError, capacitor.CapacitorSinglePhase,
                          name=[1, 2, 3], mrid='1', phase='A', state='OPEN',
                          name_prefix='blah')

    def test_mrid_bad_type(self):
        self.assertRaises(TypeError, capacitor.CapacitorSinglePhase,
                          name='1', mrid={'a': 1}, phase='A', state='OPEN',
                          name_prefix='blah')

    def test_phase_bad_type(self):
        self.assertRaises(TypeError, capacitor.CapacitorSinglePhase,
                          name='1', mrid='1', phase=7, state='OPEN',
                          name_prefix='blah')

    def test_phase_bad_value(self):
        self.assertRaises(ValueError, capacitor.CapacitorSinglePhase,
                          name='1', mrid='1', phase='N', state='OPEN',
                          name_prefix='blah')

    def test_state_bad_type(self):
        self.assertRaises(TypeError, capacitor.CapacitorSinglePhase,
                          name='1', mrid='1', phase='c', state=True,
                          name_prefix='blah')

    def test_state_bad_value(self):
        self.assertRaises(ValueError, capacitor.CapacitorSinglePhase,
                          name='1', mrid='1', phase='b', state='stuck',
                          name_prefix='blah')


class InitializeControllableCapacitors(unittest.TestCase):
    """Test initialize_controllable_capacitors"""

    def setUp(self):
        self.df = pd.read_csv(CAPACITORS)
        self.caps = capacitor.initialize_controllable_capacitors(self.df)

    def test_length(self):
        """There should be 10-1=9 capacitors, because one capacitor is
        not controllable"""
        self.assertEqual(len(self.caps), 9)

    def test_is_capacitor(self):
        """Ensure each result is indeed a SinglePhaseCapacitor."""

        for _, cap in self.caps.items():
            self.assertIsInstance(cap, capacitor.CapacitorSinglePhase)

    def test_multi_phase_capacitor(self):
        """Not supporting multi-phase controllable capacitors until
        necessary to."""
        df = self.df.copy(deep=True)
        df.loc[3, 'phs'] = np.nan

        self.assertRaises(NotImplementedError,
                          capacitor.initialize_controllable_capacitors,
                          df=df)

    def test_value(self):
        self.assertEqual(
            self.caps['capbank1c'].mrid,
            self.df[self.df['name'] == 'capbank1c']['mrid'].iloc[0])


if __name__ == '__main__':
    unittest.main()
