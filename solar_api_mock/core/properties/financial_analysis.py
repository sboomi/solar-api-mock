from pydantic import Field

from solar_api_mock.core.properties.base import SchemaProperties
from solar_api_mock.core.properties.common import MoneyProperties


class FinancialDetailsProperties(SchemaProperties):
    """Details of a financial analysis.

    Some of these details are already stored at
    higher levels (e.g., out of pocket cost).
    Total money amounts are over a lifetime period
    defined by the panel_lifetime_years field
    in SolarPotential.

    Note: The out of pocket cost of purchasing the
    panels is given in the out_of_pocket_cost field
    in CashPurchaseSavings."""

    lifetimeSrecTotal: MoneyProperties = Field(
        description="Amount of money the user will receive from Solar Renewable Energy Credits over the panel lifetime; this applies if the user buys (with or without a loan) the panels.",
    )
    costOfElectricityWithoutSolar: MoneyProperties = Field(
        description="Total cost of electricity the user would have paid over the lifetime period if they didn't install solar.",
    )
    utilityIncentive: MoneyProperties = Field(
        description="Amount of money available from utility incentives; this applies if the user buys (with or without a loan) the panels.",
    )
    netMeteringAllowed: bool = Field(
        description="Whether net metering is allowed.",
    )
    stateIncentive: MoneyProperties = Field(
        description="Amount of money available from state incentives; this applies if the user buys (with or without a loan) the panels.",
    )
    percentageExportedToGrid: float = Field(
        description="The percentage (0-100) of solar electricity production we assumed was exported to the grid, based on the first quarter of production. This affects the calculations if net metering is not allowed.",
    )
    initialAcKwhPerYear: float = Field(
        description="How many AC kWh we think the solar panels will generate in their first year.",
    )
    remainingLifetimeUtilityBill: MoneyProperties = Field(
        description="Utility bill for electricity not produced by solar, for the lifetime of the panels.",
    )
    solarPercentage: float = Field(
        description="Percentage (0-100) of the user's power supplied by solar. Valid for the first year but approximately correct for future years.",
    )
    federalIncentive: MoneyProperties = Field(
        description="Amount of money available from federal incentives; this applies if the user buys (with or without a loan) the panels.",
    )


class SavingsOverTimeProperties(SchemaProperties):
    """Financial information that's shared between different
    financing methods."""

    presentValueOfSavingsLifetime: MoneyProperties = Field(
        description="Using the assumed discount rate, what is the present value of the cumulative lifetime savings?",
    )
    presentValueOfSavingsYear20: MoneyProperties = Field(
        description="Using the assumed discount rate, what is the present value of the cumulative 20-year savings?",
    )
    savingsYear20: MoneyProperties = Field(
        description="Savings in the first twenty years after panel installation.",
    )
    financiallyViable: bool = Field(
        description="Indicates whether this scenario is financially viable. Will be false for scenarios with poor financial viability (e.g., money-losing).",
    )
    savingsLifetime: MoneyProperties = Field(
        description="Savings in the entire panel lifetime.",
    )
    savingsYear1: MoneyProperties = Field(
        description="Savings in the first year after panel installation.",
    )


class LeasingSavingsProperties(SchemaProperties):
    """Cost and benefit of leasing a particular configuration of solar panels with a particular electricity usage."""

    savings: SavingsOverTimeProperties = Field(
        description="How much is saved (or not) over the lifetime period.",
    )
    leasesSupported: bool = Field(
        description="Whether leases are supported in this juristiction by the financial calculation engine. If this field is false, then the values in this message should probably be ignored. This is independent of `leases_allowed`: in some areas leases are allowed, but under conditions that aren't handled by the financial models.",
    )
    annualLeasingCost: MoneyProperties = Field(
        description="Estimated annual leasing cost.",
    )
    leasesAllowed: bool = Field(
        description="Whether leases are allowed in this juristiction (leases are not allowed in some states). If this field is false, then the values in this message should probably be ignored.",
    )


class CashPurchaseSavingsProperties(SchemaProperties):
    """Cost and benefit of an outright purchase of a
    particular configuration of solar panels with a
    particular electricity usage."""

    rebateValue: MoneyProperties = Field(
        description="The value of all tax rebates.",
    )
    savings: "SavingsOverTimeProperties" = Field(
        description="How much is saved (or not) over the lifetime period.",
    )
    upfrontCost: MoneyProperties = Field(
        description="Initial cost after tax incentives: it's the amount that must be paid during first year. Contrast with `out_of_pocket_cost`, which is before tax incentives.",
    )
    outOfPocketCost: MoneyProperties = Field(
        description="Initial cost before tax incentives: the amount that must be paid out-of-pocket. Contrast with `upfront_cost`, which is after tax incentives.",
    )
    paybackYears: float = Field(
        description="Number of years until payback occurs. A negative value means payback never occurs within the lifetime period.",
    )


class FinancedPurchaseSavingsProperties(SchemaProperties):
    """Cost and benefit of using a loan to buy a
    particular configuration of solar panels with a
    particular electricity usage."""

    annualLoanPayment: MoneyProperties = Field(
        description="Annual loan payments.",
    )
    rebateValue: MoneyProperties = Field(
        description="The value of all tax rebates (including Federal Investment Tax Credit (ITC)).",
    )
    savings: SavingsOverTimeProperties = Field(
        description="How much is saved (or not) over the lifetime period.",
    )
    loanInterestRate: float = Field(
        description="The interest rate on loans assumed in this set of calculations.",
    )


class FinancialAnalysisProperties(SchemaProperties):
    """Analysis of the cost and benefits of the optimum solar
    layout for a particular electric bill size."""

    defaultBill: bool = Field(
        description="Whether this is the bill size selected to be the default bill for the area this building is in. Exactly one `FinancialAnalysis` in `BuildingSolarPotential` should have `default_bill` set.",
        default=None,
    )
    panelConfigIndex: int = Field(
        description="Index in solar_panel_configs of the optimum solar layout for this bill size. This can be -1 indicating that there is no layout. In this case, the remaining submessages will be omitted.",
    )
    financialDetails: FinancialDetailsProperties = Field(
        description="Financial information that applies regardless of the financing method used.",
        default=None,
    )
    cashPurchaseSavings: CashPurchaseSavingsProperties = Field(
        description="Cost and benefit of buying the solar panels with cash.",
        default=None,
    )
    monthlyBill: MoneyProperties = Field(
        description="The monthly electric bill this analysis assumes.",
    )
    averageKwhPerMonth: float = Field(
        description="How much electricity the house uses in an average month, based on the bill size and the local electricity rates.",
    )
    leasingSavings: LeasingSavingsProperties = Field(
        description="Cost and benefit of leasing the solar panels.", default=None
    )
    financedPurchaseSavings: FinancedPurchaseSavingsProperties = Field(
        description="Cost and benefit of buying the solar panels by financing the purchase.",
        default=None,
    )
