using System;
using System.Collections.Generic;
using System.Text.Json;

namespace App.Business.Services.Pmg
{
    public class PmgTariffCalculatorService
    {
        private const decimal InpatientBaseRate = 8735.00m;
        private const decimal OutpatientBaseRate = 155.00m;
        private const decimal MountainMultiplier = 1.25m;

        public decimal CalculateInpatient(string dsgCode, decimal weightCoef, int packageNumber, bool isMountain)
        {
            decimal rate = InpatientBaseRate * weightCoef;
            decimal coef = (packageNumber == 4) ? 0.60m : 0.55m;
            decimal tariff = rate * coef;
            if (isMountain) tariff *= MountainMultiplier;
            return Math.Round(tariff, 2);
        }

        public decimal CalculateOutpatient(int classNumber, decimal classCoef, bool isMountain)
        {
            decimal tariff = OutpatientBaseRate * classCoef;
            if (isMountain) tariff *= MountainMultiplier;
            return Math.Round(tariff, 2);
        }
    }
}
