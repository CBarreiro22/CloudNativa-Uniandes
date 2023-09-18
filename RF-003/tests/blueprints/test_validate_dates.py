import unittest
from datetime import datetime, timedelta

from src.blueprints.rf003 import validate_dates
from src.erros.errors import ivalid_dates

ISO_FORMATTER = "%Y-%m-%dT%H:%M:%S.%fZ"
class TestValidateDates(unittest.TestCase):

    def test_validate_dates_valid(self):
        fecha_actual = datetime.now() + timedelta(days=1)
        planned_start_date = fecha_actual.strftime(ISO_FORMATTER)
        planned_end_date = fecha_actual + timedelta(days=10)
        # Test with valid dates
        json_data = {
            "plannedStartDate": f"{planned_start_date}",
            "plannedEndDate": "2024-09-18T19:15:13.047930Z"
        }
        self.assertIsNone(validate_dates(json_data))

    def test_validate_dates_invalid_start_date(self):
        # Test with invalid start date
        json_data = {
            "plannedStartDate": "2022-09-18T19:15:13.047930Z",
            "plannedEndDate": "2024-09-18T19:15:13.047930Z"
        }

        with self.assertRaises(ivalid_dates):
            validate_dates(json_data)



if __name__ == '__main__':
    unittest.main()
