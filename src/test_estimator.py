import unittest
from estimator import Impact,SevereImpact

class TestEstimator(unittest.TestCase):


    def test_covid19ImpactEstimator(self):
        data = {
                    "region": {
                            "name": "Africa",
                            "avgAge": 19.7,
                            "avgDailyIncomeInUSD": 5,
                            "avgDailyIncomePopulation": 0.71
                    },
                    "periodType": "months",
                    "timeToElapse": 5,
                    "reportedCases": 674,
                    "population": 66622705,
                    "totalHospitalBeds": 1380614
                }
        impact= Impact(data)
        server_impact = SevereImpact(data)
        self.assertEqual(impact.covid19ImpactEstimator(),6740)
        self.assertEqual(server_impact.covid19ImpactEstimator(),33700)
        self.assertEqual(server_impact.infectionByRequestedTime(),1348343430)
        self.assertEqual(server_impact.severeCasesByRequestedTime(),13434380)
        self.assertEqual(server_impact.availableHospitalBedsByRequestedTime(),13480)
        self.assertEqual(impact.casesForICUByRequestedTime(),1348343430380)
        self.assertNotEqual(server_impact.casesForVentilatorsByRequestedTime(),13480)
        self.assertNotEqual(server_impact.dollarsInFlight(),13480)


if __name__=='__main__':
    unittest.main()
