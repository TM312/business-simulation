#import libraries

import pandas as pd
import numpy as np
import random, math, datetime




def updateVars(T, cityFeeRates, marketShare, repairCosts, chargingCosts, usagePrice, basePrice, bRiderShare, bRiderGrowth, scootersInitial, keepScooterRideRatio, custSupportCosts, avgLifespanScooter, scooterCosts):
  
    #clearing previously calculated epoch values for the variables
    chargedRatio.clear()
    repairedRatio.clear()
    functioningScooterRatio.clear()
    avgTripDur.clear()
    avgFare.clear()
    availability.clear()
    insuranceCosts.clear()
    creditCardFees.clear()
    grossRevRide.clear()
    usage.clear()
    scootRideRatio.clear()
    avgRidesDayScoot.clear()
    opCosts.clear()
    depreciation.clear()
    movAvgDepreciation.clear()
    cityFees.clear()
    proFormaContribution.clear()
    monthlyEarnings.clear()
    scooters.clear()
    scootersInUse.clear()
    functioningScooters.clear()
    avgScootDistance.clear()
    movAvgUsage.clear()
    movAvgAvgTripDur.clear()

    usageMultiplicator = cosValues[month-1:month+T-1]
    contraRev = [0.44] * T
    if cityFeeRates == True:
        cityFeesA, cityFeesD = 0, 0
    else:
        cityFeesA, cityFeesD = 10, 1

    # formats the xAxis of the plots to contain listMonths
    fmtr = ticker.IndexFormatter(listMonths[month:month+T])

    #calculating the values for each epoch t in time horizont T and appending them to a list
    for t in range(T):
        popBerlin.append(int(popBerlinInitial + popBerlinGrowthFactor * t))

        if bRiderGrowth == "flat":
            bRider.append(int(bRiderShare * popBerlin[-1] * marketShare))
        elif bRiderGrowth == "linear":
            # linear user growth (growth per month: 10% of users in starting month)
            bRider.append(int(bRiderShare * marketShare *
                              (popBerlin[-1] + t * 0.1 * popBerlin[0])))
        else:
            # exponential user growth 10%-MoM
            bRider.append(
                int(bRiderShare*1.1**t * popBerlin[-1] * marketShare))

        #average trip duration in min; estimation; #makes sure that avgTripDurMin <= avgTripDur <= avgTripDurMax
        if t == 0:
            avgTripDur.append(avgTripDurDefault)
        else:
            avgTripDur.append(round(min(avgTripDurMax, max(avgTripDurMin, avgTripDurDefault * (1 +
                                                                                               + avgTripDurBasePriceElasticity *
                                                                                               ((basePrice - basePriceDefault)/basePriceDefault)
                                                                                               + avgTripDurUsagePriceElasticity * ((usagePrice - usagePriceDefault)/usagePriceDefault))
                                                           )), 2))

        if avgTripDur[-1] <= avgTripDurMin:
            avgTripDur[-1] = avgTripDurMin

        selectionAvgTripDur = min(windowAvgTripDur, len(avgTripDur))
        y = np.ones(selectionAvgTripDur,)/selectionAvgTripDur
        movAvgAvgTripDur.append(
            sum([a*b for a, b in zip(avgTripDur[-selectionAvgTripDur:], y)]))

        #avg fare
        # gross revenue per ride
        avgFare.append(round(movAvgAvgTripDur[-1] * usagePrice + basePrice, 2))

        #other costs per ride
        insuranceCosts.append(0.05)  # in $
        creditCardFees.append(round(0.1 * avgFare[-1], 2))  # in $

        #scooter ratios
        chargedRatio.append(round(min(1, chargingWeightCharged * chargingCosts / chargingCostsMax -
                                      avgTripDurWeightCharged * (movAvgAvgTripDur[-1]-avgTripDurDefault)/avgTripDurDefault), 3))
        repairedRatio.append(round(repairCosts / repairCostsMax, 3))
        functioningScootRatioMin = int(
            max(0, (-1 + repairedRatio[-1] + chargedRatio[-1]) * 100))
        functioningScootRatioMax = int(
            min(repairedRatio[-1], chargedRatio[-1]) * 100)
        functioningScootRatioMean = (
            functioningScootRatioMin + functioningScootRatioMax) / 2
        #functioningScooterRatio.append(round(random.randint(functioningScootRatioMin, abs(functioningScootRatioMax))/100,3)) #repairCosts and chargingCosts are independent features
        # repairCosts and chargingCosts are independent features
        functioningScooterRatio.append(round(functioningScootRatioMean/100, 3))

        #number of scooters and scooter to (1000) rider ratio
        initialScootRideRatio = scootersInitial / bRider[0] * 1000


        if keepScooterRideRatio == True:
            scooters.append(int(initialScootRideRatio/1000 * bRider[-1]))
        else:
            scooters.append(scootersInitial)

        #Scooters per 1000 users
        scootRideRatio.append(round(scooters[-1] / bRider[-1] * 1000, 2))

        #scooter availability
        #functioning scooters
        functioningScooters.append(
            int(functioningScooterRatio[-1] * scooters[-1]))

        #avg scooters in use per minute:
        if t == 0:
            scootersInUse.append(int(min(
                functioningScooters[-1], bRider[-1] * movAvgAvgTripDur[-1] * usageDefault / usageHours)))
        else:
            scootersInUse.append(int(min(
                functioningScooters[-1], bRider[-1] * movAvgAvgTripDur[-1] * movAvgUsage[-1] / usageHours)))

        #avg free scooters at any time (between 06:00 - 23:59)
        remainingScooters = functioningScooters[-1] - scootersInUse[-1]
        if remainingScooters == 0:
            avgScootDistance.append(
                int(0.5 * math.sqrt((berlinCoveredArea/1)/pi) * 1000))  # in m

        else:
            avgScootDistance.append(
                int(0.5 * math.sqrt((berlinCoveredArea/remainingScooters)/pi) * 1000))  # in m

        #print("\navgScootDistance: " + str(avgScootDistance))
        #print("remainingScooters: " + str(remainingScooters))

        #usage
        if avgFare[-1] >= avgFareDefault:
            usageAvgFareElasticity = ((1.5 * usageDefault - usageDefault) / usageDefault) / (
                (basePriceMin - avgFareDefault) / avgFareDefault)
        else:
            usageAvgFareElasticity = ((5 * usageDefault - usageDefault) / usageDefault) / (
                (basePriceMin - avgFareDefault) / avgFareDefault)

        usage.append(round(min(usageMax,
                               max(usageMin,
                                   usageMultiplicator[t] * usageDefault *
                                   (1 +
                                    usageAvgFareElasticity *
                                    ((avgTripDurDefault * usagePrice +
                                      basePrice) - avgFareDefault)/avgFareDefault
                                       + usageCustSupportCostElasticity *
                                       (custSupportCosts - custSupportCostsDefault) /
                                    custSupportCostsDefault
                                       + usageAvgScootDistanceWeightElasticity *
                                       (avgScootDistance[-1] - avgScootDistanceDefault) /
                                    avgScootDistanceDefault
                                    )
                                   )), 2))

        selectionUsage = min(windowUsage, len(usage))
        y = np.ones(selectionUsage,)/selectionUsage
        movAvgUsage.append(
            sum([a*b for a, b in zip(usage[-selectionUsage:], y)]))

        #average number of rides per day per scooter
        if usageMultiplicator == 0:
            avgRidesDayScoot.append(0)
        else:
            avgRidesDayScoot.append(round(
                min(usageHours/avgTripDur[-1], bRider[-1] * movAvgUsage[-1] / scooters[-1]), 3))

        #city fees per ride
        if usageMultiplicator == 0:
            depreciation.append(0)
            cityFees.append(0)
        else:
            cityFees.append(
                round((cityFeesA/365 + cityFeesD)/avgRidesDayScoot[-1], 3))
            depreciation.append(
                scooterCosts / (avgLifespanScooter * avgRidesDayScoot[-1]))

        #depreciation costs per scooter per ride (straight line depreciation)
        """
        The (learned) moving average models more realistic for accounting purposes and is more robust against oscillations. 
        Therefore, "depreciation" will be removed from the plots in subsequent states. 
        However, currently it is still plotted to allow for better detection of unrealistic model behavior. 
        """
        selection = min(windowDepreciation, len(depreciation))
        y = np.ones(selection,)/selection
        movAvgDepreciation.append(
            sum([a*b for a, b in zip(depreciation[-selection:], y)]))

        # operational costs per ride
        opCosts.append(round(contraRev[t] + repairCosts + chargingCosts +
                             custSupportCosts + insuranceCosts[-1] + creditCardFees[-1] + cityFees[-1], 2))

        #pro Forma Contribution per Ride
        proFormaContribution.append(
            round(avgFare[-1] - opCosts[-1] - movAvgDepreciation[-1], 2))

        #earnings per month
        monthlyEarnings.append(
            round(proFormaContribution[-1] * avgRidesDayScoot[-1] * scooters[-1] * 30.5, 2))





return        
{"inputs": {"T": T,
            "marketShare": marketShare,
            "cityFeeRates": cityFeeRates,
            "repairCosts": repairCosts,
            "chargingCosts": chargingCosts,
            "usagePrice": usagePrice,
            "basePrice": basePrice,
            "bRiderShare": bRiderShare,
            "bRiderGrowth": bRiderGrowth,
            "scootersInitial": scootersInitial,
            "keepScooterRideRatio": keepScooterRideRatio,
            "custSupportCosts": custSupportCosts,
            "avgLifespanScooter": avgLifespanScooter,
            "scooterCosts": scooterCosts},
 "outputs": {"bRider": bRider,
             "avgTripDur": avgTripDur,
             "avgFare": avgFare,
             "movAvgAvgTripDur": movAvgAvgTripDur,
             "insuranceCosts": insuranceCosts,
             "creditCardFees": creditCardFees,
             "chargedRatio": chargedRatio,
             "repairedRatio": repairedRatio,
             "functioningScooterRatio": functioningScooterRatio,
             "initialScootRideRatio": initialScootRideRatio,
             "scooters": scooters,
             "scootRideRatio": scootRideRatio,
             "functioningScooters": functioningScooters,
             "scootersInUse": scootersInUse,
             "avgScootDistance": avgScootDistance,
             "usage": usage,
             "movAvgUsage": movAvgUsage,
             "avgRidesDayScoot": avgRidesDayScoot,
             "cityFees": cityFees,
             "opCosts": opCosts,
             "depreciation": depreciation,
             "movAvgDepreciation": movAvgDepreciation,
             "proFormaContribution": proFormaContribution,
             "monthlyEarnings": monthlyEarnings
             }}
