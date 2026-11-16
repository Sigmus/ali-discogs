import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_timing_sensitivity import timing_scenario


def band(source, digital):
    return {'target': 'Frozen source band', 'source_duration_seconds': source,
            'digital_duration_seconds': digital, 'source_duration_notes': []}


class TimingSensitivityTests(unittest.TestCase):
    def test_one_large_outlier_requires_many_close_bands(self):
        bands = [band(300,302) for _ in range(14)] + [band(207,142)]
        self.assertFalse(timing_scenario(bands, percentage=.2)['passes'])
        self.assertTrue(timing_scenario(bands, percentage=.35)['passes'])
        self.assertTrue(timing_scenario(bands, floor=15, consensus=True)['passes'])
        self.assertFalse(timing_scenario(bands[-2:], floor=15, consensus=True)['passes'])
        self.assertFalse(timing_scenario(bands+[band(207,142)], floor=15, consensus=True)['passes'])

    def test_total_absolute_error_cannot_cancel_between_bands(self):
        bands = [band(300,310) for _ in range(7)] + [band(300,290) for _ in range(7)] + [band(207,142)]
        self.assertFalse(timing_scenario(bands, floor=15, consensus=True)['passes'])
        self.assertFalse(timing_scenario([band(0,90)]*15, floor=15, consensus=True)['passes'])

    def test_unknown_durations_never_create_measured_support(self):
        result = timing_scenario([band(None,200)], floor=15, consensus=True)
        self.assertFalse(result['applicable'])
        self.assertEqual(result['timed_bands'],0)
