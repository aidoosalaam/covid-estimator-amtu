import math

class Impact(object):

    def __init__(self, data):
        if data is not None:
            self.data = data
            self.periodType = data["periodType"]
            self.timeToElapse = data["timeToElapse"]
            self.reportedCases = data["reportedCases"]
            self.population = data["population"]
            self.totalHospitalBeds = data["totalHospitalBeds"]
            self.region_name = data["region"]["name"]
            self.region_avgAge = data["region"]["avgAge"]
            self.region_avgDailyIncomeInUSD = data["region"]["avgDailyIncomeInUSD"]
            self.region_avgDailyIncomePopulation = data["region"]["avgDailyIncomePopulation"]

    def covid19ImpactEstimator(self):
        return math.trunc(math.trunc(self.reportedCases * 10))


    def infectionByRequestedTime(self):
        period_type = self.periodType.lower()
        time_to_elapse = 0
        if period_type == "weeks":
                time_to_elapse = math.trunc(self.timeToElapse * 7)
        elif period_type == "months":
                time_to_elapse = math.trunc(self.timeToElapse * 30)
        else:
            time_to_elapse = math.trunc(self.timeToElapse)

        power = time_to_elapse//3
        infection_by_req_time = math.trunc(self.covid19ImpactEstimator() * (2**power))
        return infection_by_req_time

    def severeCasesByRequestedTime(self):
        return math.trunc(0.15 * self.infectionByRequestedTime())

    def availableHospitalBedsByRequestedTime(self):
        hospitalBedsByRequestedTime = math.trunc((0.35 * self.totalHospitalBeds) - self.severeCasesByRequestedTime())
        return hospitalBedsByRequestedTime

    def casesForICUByRequestedTime(self):
        casesForICUByRequestedTime = math.trunc(0.05 * self.infectionByRequestedTime())
        return casesForICUByRequestedTime

    def casesForVentilatorsByRequestedTime(self):
        casesForVentilatorsByRequestedTime = math.trunc(0.02 * self.infectionByRequestedTime())
        return casesForVentilatorsByRequestedTime

    def dollarsInFlight(self):
        dollarsInFlight = math.trunc((self.infectionByRequestedTime() * self.region_avgDailyIncomePopulation * self.region_avgDailyIncomeInUSD)// self.timeToElapse)
        return dollarsInFlight


class SevereImpact(Impact):

    def covid19ImpactEstimator(self):
        return math.trunc(self.reportedCases * 50)


    def infectionByRequestedTime(self):
        period_type = self.periodType.lower()
        time_to_elapse = 0
        if period_type == "weeks":
                time_to_elapse = math.trunc(self.timeToElapse * 7)
        elif period_type == "months":
                time_to_elapse = math.trunc(self.timeToElapse * 30)
        else:
            time_to_elapse = math.trunc(self.timeToElapse)

        power = time_to_elapse//3
        infection_by_req_time = math.trunc(self.covid19ImpactEstimator() * (2**power))
        return infection_by_req_time

    def severeCasesByRequestedTime(self):
        return math.trunc(0.15 * self.infectionByRequestedTime())

    def availableHospitalBedsByRequestedTime(self):
        hospitalBedsByRequestedTime = math.trunc((0.35 * self.totalHospitalBeds) - self.severeCasesByRequestedTime())
        return hospitalBedsByRequestedTime

    def casesForICUByRequestedTime(self):
        casesForICUByRequestedTime = math.trunc(0.05 * self.infectionByRequestedTime())
        return casesForICUByRequestedTime

    def casesForVentilatorsByRequestedTime(self):
        casesForVentilatorsByRequestedTime = math.trunc(0.02 * self.infectionByRequestedTime())
        return casesForVentilatorsByRequestedTime

    def dollarsInFlight(self):
        dollarsInFlight = math.trunc((self.infectionByRequestedTime() * self.region_avgDailyIncomePopulation * self.region_avgDailyIncomeInUSD)// self.timeToElapse)
        return dollarsInFlight


def covidEstimator(data):
    impact = Impact(data)
    severe_impact = SevereImpact(data)
    data = {
            "data" : data,
            "Impact":{
                "currentlyInfected" : impact.infectionByRequestedTime(),
                "severeCasesByRequestedTime" : impact.severeCasesByRequestedTime(),
                "hospitalBedsByRequestedTime" : impact.availableHospitalBedsByRequestedTime(),
                "casesForICUByRequestedTime" : impact.casesForICUByRequestedTime(),
                "casesForVentilatorsByRequestedTime" : impact.casesForVentilatorsByRequestedTime(),
                "dollarsInFlight" : impact.dollarsInFlight()
            },
            "SevereImpact":{
                "currentlyInfected" : severe_impact.infectionByRequestedTime(),
                "severeCasesByRequestedTime" : severe_impact.severeCasesByRequestedTime(),
                "hospitalBedsByRequestedTime" : severe_impact.availableHospitalBedsByRequestedTime(),
                "casesForICUByRequestedTime" : severe_impact.casesForICUByRequestedTime(),
                "casesForVentilatorsByRequestedTime" : severe_impact.casesForVentilatorsByRequestedTime(),
                "dollarsInFlight" : severe_impact.dollarsInFlight()
            }
    }
    return data

def estimator(data):
    return covidEstimator(data)