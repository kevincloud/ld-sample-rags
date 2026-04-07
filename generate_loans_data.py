"""
Generates ~130 demo text chunks for the Loans & Credit RAG corpus.
Outputs: rag/data/loans_chunks.json

Content types:
  PRODUCT       - loan and credit products
  FAQ           - common borrower questions
  MARKET_COMMENTARY - rate environment, lending trends
  CLIENT_SCENARIO   - borrower case studies
"""

import json
import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "data", "loans_chunks.json")

PRODUCTS = [
    {
        "title": "30-Year Fixed-Rate Mortgage",
        "text": (
            "A 30-year fixed-rate mortgage is the most popular home loan in the United States. The interest rate "
            "is locked for the entire 30-year term, providing payment certainty and protection against rising rates. "
            "Monthly principal and interest payments remain constant, though escrow amounts for property taxes and "
            "insurance may change annually. As of 2025, 30-year fixed rates typically range from 6.5–7.5% depending "
            "on credit score, down payment, and lender. Borrowers with credit scores above 740 and 20% down payment "
            "receive the most favorable rates. The primary advantage is predictable payments and long amortization "
            "reducing monthly obligations. The trade-off is paying more total interest over the life of the loan "
            "versus shorter-term options."
        ),
        "metadata": {"product_type": "Mortgage", "risk_level": "Low", "tags": ["mortgage", "30-year", "fixed rate", "home purchase"]},
    },
    {
        "title": "15-Year Fixed-Rate Mortgage",
        "text": (
            "A 15-year fixed-rate mortgage offers a significantly lower interest rate than the 30-year equivalent — "
            "typically 0.5–0.75% lower — and builds equity much faster. Monthly payments are higher (approximately "
            "40–50% more than a comparable 30-year loan), but total interest paid over the life of the loan is "
            "roughly half. For example, a $400,000 mortgage at 6.5% over 30 years costs approximately $510,000 "
            "in interest; the same loan at 5.75% over 15 years costs approximately $197,000 in interest. "
            "Best suited for borrowers with strong income who prioritize building equity quickly and minimizing "
            "total borrowing costs. Requires higher qualification income due to larger monthly payment."
        ),
        "metadata": {"product_type": "Mortgage", "risk_level": "Low", "tags": ["mortgage", "15-year", "fixed rate", "equity building"]},
    },
    {
        "title": "Adjustable-Rate Mortgage (ARM)",
        "text": (
            "An adjustable-rate mortgage (ARM) has an initial fixed-rate period followed by periodic adjustments "
            "tied to a market index (typically SOFR). Common ARM structures are 5/1, 7/1, and 10/1, where the "
            "first number is the fixed period in years and the second is the adjustment frequency. Initial rates "
            "are typically 0.5–1.5% lower than 30-year fixed rates. After the fixed period, rates adjust annually "
            "subject to caps: typically 2% per adjustment and 5–6% lifetime cap above the initial rate. ARMs are "
            "most appropriate for borrowers who plan to sell or refinance before the adjustment period begins, "
            "or for jumbo loan borrowers where the initial rate savings are most significant."
        ),
        "metadata": {"product_type": "Mortgage", "risk_level": "Moderate", "tags": ["mortgage", "ARM", "adjustable rate", "short-term"]},
    },
    {
        "title": "FHA Loan",
        "text": (
            "FHA loans are government-backed mortgages insured by the Federal Housing Administration, designed "
            "to help lower-income and first-time homebuyers access homeownership. Key features: minimum 3.5% down "
            "payment with a credit score of 580+; 10% down required for scores 500–579. FHA loans require both "
            "an upfront mortgage insurance premium (MIP) of 1.75% of the loan amount and an annual MIP of 0.55–1.05% "
            "depending on loan term and LTV. Unlike conventional PMI, FHA MIP typically lasts the life of the loan "
            "for down payments under 10%. FHA loans have loan limits that vary by county. They are most valuable "
            "for buyers with credit scores in the 580–680 range who cannot afford a 20% down payment."
        ),
        "metadata": {"product_type": "Mortgage", "risk_level": "Low", "tags": ["FHA", "government loan", "first-time buyer", "low down payment"]},
    },
    {
        "title": "VA Home Loan",
        "text": (
            "VA loans are mortgage loans guaranteed by the U.S. Department of Veterans Affairs, available to "
            "eligible active-duty service members, veterans, and surviving spouses. Key benefits: no down payment "
            "required, no private mortgage insurance (PMI), competitive interest rates (typically 0.25–0.5% below "
            "conventional), and no prepayment penalty. VA loans do have a funding fee (1.25–3.3% of loan amount "
            "depending on down payment and usage) that can be rolled into the loan. There is no maximum loan "
            "amount for eligible veterans with full entitlement. VA loans require a VA appraisal and the property "
            "must meet VA minimum property requirements. This benefit can be used multiple times."
        ),
        "metadata": {"product_type": "Mortgage", "risk_level": "Low", "tags": ["VA loan", "veteran", "no down payment", "military"]},
    },
    {
        "title": "Home Equity Line of Credit (HELOC)",
        "text": (
            "A HELOC is a revolving line of credit secured by your home equity, functioning similarly to a credit "
            "card with your home as collateral. Borrowers can draw funds during the draw period (typically 10 years), "
            "paying interest only on the amount drawn. After the draw period, the repayment period begins (typically "
            "20 years) during which no new draws are allowed and principal plus interest must be repaid. HELOCs "
            "typically have variable rates tied to the Prime Rate plus a margin. Maximum borrowing is usually "
            "80–90% of home value minus outstanding mortgage balance. HELOCs are best for ongoing or unpredictable "
            "expenses (home renovations, education costs, business needs). Risk: your home is collateral — "
            "failure to repay can result in foreclosure."
        ),
        "metadata": {"product_type": "Home Equity", "risk_level": "Moderate", "tags": ["HELOC", "home equity", "revolving credit", "variable rate"]},
    },
    {
        "title": "Home Equity Loan",
        "text": (
            "A home equity loan (also called a second mortgage) provides a lump sum at a fixed interest rate, "
            "repaid over a set term (5–30 years). Unlike a HELOC, the rate is fixed at origination, providing "
            "payment certainty. Borrowers can typically access up to 80–85% of home value minus the outstanding "
            "first mortgage. Interest may be tax-deductible if used for home improvement (consult a tax advisor). "
            "Home equity loans are best for large, one-time expenses where a fixed amount and fixed payment are "
            "preferred: home renovations, debt consolidation, or major purchases. Current rates are typically "
            "Prime + 1–3%, and since the loan is secured by real estate, rates are significantly lower than "
            "unsecured personal loans."
        ),
        "metadata": {"product_type": "Home Equity", "risk_level": "Moderate", "tags": ["home equity loan", "second mortgage", "fixed rate", "lump sum"]},
    },
    {
        "title": "Personal Loan (Unsecured)",
        "text": (
            "An unsecured personal loan provides a fixed lump sum with a fixed interest rate and fixed monthly "
            "payment over a set term (typically 1–7 years). Because no collateral is required, rates are higher "
            "than secured loans — typically 6–36% APR depending on credit score and income. Borrowers with "
            "excellent credit (750+) may qualify for rates as low as 6–10%; those with fair credit may see rates "
            "of 20–36%. Common uses: debt consolidation (replacing high-rate credit card debt), major purchases, "
            "medical expenses, or home improvement without home equity. Unlike credit cards, personal loans have "
            "a defined payoff timeline and fixed payments, making budgeting straightforward. No prepayment "
            "penalty with most lenders."
        ),
        "metadata": {"product_type": "Personal Loan", "risk_level": "Varies", "tags": ["personal loan", "unsecured", "debt consolidation", "fixed payment"]},
    },
    {
        "title": "Auto Loan — New Vehicle",
        "text": (
            "New auto loans are installment loans to finance the purchase of a new vehicle, typically offered by "
            "banks, credit unions, and captive finance companies (manufacturer financing arms). Terms typically "
            "range from 24–84 months; 60–72 months is most common. Interest rates for new vehicles are lower than "
            "used due to better collateral value — currently averaging 5–8% for well-qualified borrowers. "
            "Manufacturer-sponsored promotional financing (0–1.9% APR) is periodically available on select models. "
            "Key metrics: keep total monthly car payment (principal, interest, insurance) below 15% of gross "
            "monthly income. Avoid terms exceeding 60 months as they increase total interest and the risk of "
            "being 'underwater' (owing more than the car's value)."
        ),
        "metadata": {"product_type": "Auto Loan", "risk_level": "Low-Moderate", "tags": ["auto loan", "new car", "installment loan", "vehicle financing"]},
    },
    {
        "title": "Auto Loan — Used Vehicle",
        "text": (
            "Used auto loans finance pre-owned vehicles and typically carry higher interest rates than new auto "
            "loans due to the higher collateral risk (used vehicles depreciate faster and are harder to value). "
            "Rates for used vehicles average 7–15% for qualified borrowers. Lenders often restrict loan terms "
            "and amounts based on vehicle age and mileage — many won't finance vehicles over 10 years old or "
            "with more than 100,000 miles. A pre-approval from your bank or credit union before visiting a "
            "dealer gives you negotiating leverage and protection against dealer-inflated financing. "
            "Credit unions typically offer significantly lower rates on used auto loans than banks — "
            "worth comparing before financing."
        ),
        "metadata": {"product_type": "Auto Loan", "risk_level": "Moderate", "tags": ["auto loan", "used car", "installment loan", "credit union"]},
    },
    {
        "title": "Student Loan — Federal Direct Subsidized",
        "text": (
            "Federal Direct Subsidized Loans are available to undergraduate students with demonstrated financial "
            "need. The government pays the interest while the borrower is enrolled at least half-time, during the "
            "6-month grace period after leaving school, and during deferment periods. For 2024–2025, the interest "
            "rate is fixed at 6.53% for undergraduates. Annual limits range from $3,500–$5,500 depending on "
            "year in school, with an aggregate limit of $23,000. These are the best federal loan option due to "
            "the interest subsidy. Repayment typically begins 6 months after graduation. Access to income-driven "
            "repayment plans and Public Service Loan Forgiveness (PSLF) makes them flexible. "
            "Always exhaust subsidized loan eligibility before taking unsubsidized loans."
        ),
        "metadata": {"product_type": "Student Loan", "risk_level": "Low", "tags": ["student loan", "federal", "subsidized", "undergraduate"]},
    },
    {
        "title": "Student Loan — Federal Direct Unsubsidized",
        "text": (
            "Federal Direct Unsubsidized Loans are available to undergraduate and graduate students regardless "
            "of financial need. Unlike subsidized loans, interest accrues during all periods, including while "
            "enrolled. For 2024–2025, rates are 6.53% for undergraduates and 8.08% for graduate students. "
            "Annual limits for dependent undergraduates are $5,500–$7,500 (combined with subsidized). Graduate "
            "students can borrow up to $20,500/year with an aggregate limit of $138,500. Borrowers can choose "
            "to pay interest while in school to prevent capitalization. Like all federal loans, unsubsidized "
            "loans offer income-driven repayment, deferment, forbearance, and potential loan forgiveness. "
            "Always preferred over private student loans due to federal protections and flexible repayment."
        ),
        "metadata": {"product_type": "Student Loan", "risk_level": "Low-Moderate", "tags": ["student loan", "federal", "unsubsidized", "graduate"]},
    },
    {
        "title": "Private Student Loan",
        "text": (
            "Private student loans are offered by banks, credit unions, and specialized lenders (Sallie Mae, "
            "Earnest, College Ave) and should be considered only after exhausting federal loan options. Rates "
            "are either fixed or variable (tied to SOFR) and depend heavily on creditworthiness — ranging from "
            "4–15%+ APR. Unlike federal loans, private loans typically lack income-driven repayment options, "
            "deferment flexibility, or forgiveness programs. A creditworthy cosigner (usually a parent) can "
            "significantly reduce the interest rate. Private loans are best for filling the gap after federal "
            "loans, grants, and scholarships are maximized. Borrowing rule of thumb: total student loan debt "
            "should not exceed your expected first-year salary after graduation."
        ),
        "metadata": {"product_type": "Student Loan", "risk_level": "Moderate-High", "tags": ["student loan", "private", "cosigner", "variable rate"]},
    },
    {
        "title": "Credit Card — Rewards (Travel)",
        "text": (
            "Travel rewards credit cards earn points or miles on purchases, redeemable for airline tickets, hotel "
            "stays, and travel statement credits. Premium travel cards (Chase Sapphire Reserve, Amex Platinum) "
            "charge annual fees of $550–$695 but offer benefits such as airport lounge access, travel credits, "
            "and elevated earning rates (2–5x on travel and dining). Mid-tier travel cards (Chase Sapphire "
            "Preferred, Capital One Venture) charge $95–$250 with strong rewards rates and sign-up bonuses "
            "of 60,000–100,000 points. APRs typically range from 20–30% — rewards are only beneficial if the "
            "balance is paid in full each month. The economics favor heavy travelers who can maximize the "
            "travel credits and lounge benefits."
        ),
        "metadata": {"product_type": "Credit Card", "risk_level": "Variable", "tags": ["credit card", "travel rewards", "points", "miles", "annual fee"]},
    },
    {
        "title": "Credit Card — Cash Back",
        "text": (
            "Cash back credit cards return a percentage of purchases as cash rewards — either as a flat rate "
            "(e.g., 2% on everything) or tiered (5% on rotating categories, 1–2% on all else). Best flat-rate "
            "cards include the Citi Double Cash (2% back) and the Fidelity Visa (2% back to Fidelity accounts). "
            "Best category cards include the Chase Freedom Flex and Discover it. Cards with no annual fee are "
            "most appropriate for average spenders; annual fee cards make sense for heavy spenders who will "
            "exceed the breakeven. Cash back cards are the simplest reward structure — no worrying about "
            "point values or redemption complexity. APRs of 20–30% mean carrying a balance eliminates all "
            "rewards value and then some."
        ),
        "metadata": {"product_type": "Credit Card", "risk_level": "Variable", "tags": ["credit card", "cash back", "rewards", "no annual fee"]},
    },
    {
        "title": "Business Term Loan",
        "text": (
            "A business term loan provides a lump sum of capital repaid over a fixed term (1–10 years) at "
            "a fixed or variable rate. Used for business expansion, equipment purchase, real estate, or "
            "working capital. SBA 7(a) loans (up to $5M) are government-guaranteed and offer longer terms "
            "and lower down payments than conventional business loans. Conventional business term loans from "
            "banks typically require 2+ years in business, strong revenue, and good personal/business credit. "
            "Rates vary widely: SBA loans are typically Prime + 2.25–2.75%; conventional bank loans range "
            "from 6–15%. Online lenders (Kabbage, OnDeck) offer faster approval but at significantly higher "
            "rates (15–80% APR). For established businesses, bank and SBA loans offer the best rates."
        ),
        "metadata": {"product_type": "Business Loan", "risk_level": "Moderate", "tags": ["business loan", "SBA", "term loan", "small business"]},
    },
    {
        "title": "Business Line of Credit",
        "text": (
            "A business line of credit (LOC) is a revolving credit facility that allows a business to draw "
            "funds up to a pre-approved limit as needed and repay on a flexible schedule, paying interest "
            "only on the drawn balance. Unsecured lines typically have lower limits ($10K–$250K) and higher "
            "rates; secured lines (backed by accounts receivable, inventory, or real estate) offer higher "
            "limits and lower rates. Business LOCs are ideal for managing cash flow gaps, covering seasonal "
            "inventory needs, or handling unexpected expenses. Unlike term loans, the revolving structure "
            "provides ongoing access to capital without reapplying. Most require annual renewal. "
            "Best for businesses with consistent revenue who need flexible access to working capital."
        ),
        "metadata": {"product_type": "Business Loan", "risk_level": "Moderate", "tags": ["business line of credit", "working capital", "revolving", "cash flow"]},
    },
    {
        "title": "Construction Loan",
        "text": (
            "A construction loan is a short-term, high-interest loan used to finance the building of a new home "
            "or major renovation. Unlike a mortgage, funds are disbursed in stages (draws) as construction "
            "milestones are completed. During construction, borrowers typically pay interest-only on drawn "
            "amounts. Terms are usually 12–18 months. Upon completion, the construction loan converts to a "
            "permanent mortgage (construction-to-permanent loan) or is paid off with a new mortgage. "
            "Rates are typically 1–2% above standard mortgage rates due to higher risk. Lenders require "
            "detailed construction plans, contracts, and builder qualifications. Reserves of 10–20% of project "
            "cost are typically required for contingencies."
        ),
        "metadata": {"product_type": "Mortgage", "risk_level": "Moderate-High", "tags": ["construction loan", "new construction", "short-term", "draw schedule"]},
    },
    {
        "title": "Debt Consolidation Loan",
        "text": (
            "A debt consolidation loan combines multiple high-interest debts (credit cards, medical bills, "
            "personal loans) into a single loan at a lower interest rate, simplifying repayment and "
            "potentially reducing total interest paid. For example, consolidating $25,000 of credit card "
            "debt at 22% APR into a personal loan at 10% over 5 years saves approximately $12,000 in "
            "interest and reduces monthly payment. Key considerations: (1) The loan should have a lower rate "
            "than the debts being consolidated. (2) Avoid using the consolidation loan as a license to "
            "re-accumulate credit card debt. (3) Secured consolidation loans (using home equity) offer lower "
            "rates but risk your home. (4) Term matters — longer terms lower payments but increase total "
            "interest even at a lower rate."
        ),
        "metadata": {"product_type": "Personal Loan", "risk_level": "Low-Moderate", "tags": ["debt consolidation", "credit card debt", "interest savings", "simplification"]},
    },
    {
        "title": "Payday Alternative Loan (PAL)",
        "text": (
            "Payday Alternative Loans (PALs) are small-dollar loans offered by federal credit unions as a "
            "regulated, affordable alternative to predatory payday loans. PAL I: amounts of $200–$1,000, "
            "terms of 1–6 months, maximum APR of 28%, application fee up to $20. PAL II: amounts up to "
            "$2,000, terms up to 12 months, same 28% rate cap. To qualify, borrowers must have been credit "
            "union members for at least one month. By contrast, typical payday loans carry APRs of 300–600%. "
            "PALs are designed for members facing short-term cash flow emergencies. Credit unions also "
            "typically provide financial counseling alongside PALs to address the root cause of the "
            "cash flow stress and prevent repeat borrowing."
        ),
        "metadata": {"product_type": "Small Dollar Loan", "risk_level": "Low", "tags": ["PAL", "credit union", "small dollar", "payday alternative", "emergency"]},
    },
    {
        "title": "Jumbo Mortgage",
        "text": (
            "A jumbo mortgage is a home loan exceeding the conforming loan limits set by the FHFA — $766,550 "
            "for most U.S. counties in 2024 ($1,149,825 in high-cost areas). Because jumbo loans cannot be "
            "purchased by Fannie Mae or Freddie Mac, they carry slightly higher rates and stricter qualification "
            "requirements. Typical requirements: credit score 700+, 10–20% down payment, debt-to-income ratio "
            "below 43%, 12 months cash reserves. Jumbo rates are often within 0.25–0.5% of conforming rates "
            "for well-qualified borrowers. Jumbo loans are most common in high-cost metro areas (New York, "
            "San Francisco, Los Angeles). Large bank portfolio lenders (Chase, Wells Fargo, Bank of America) "
            "and specialty mortgage lenders are the primary sources."
        ),
        "metadata": {"product_type": "Mortgage", "risk_level": "Low-Moderate", "tags": ["jumbo mortgage", "high-cost", "large loan", "conforming limit"]},
    },
    {
        "title": "Reverse Mortgage (HECM)",
        "text": (
            "A Home Equity Conversion Mortgage (HECM) is a federally insured reverse mortgage available to "
            "homeowners aged 62 and older. It allows seniors to convert home equity into cash (lump sum, "
            "monthly payments, or line of credit) without selling the home or making monthly mortgage payments. "
            "The loan balance grows over time as interest accrues and becomes due when the homeowner sells, "
            "moves out permanently, or passes away. No monthly payment is required, but borrowers must "
            "maintain the home, pay property taxes, and keep homeowner's insurance current. Upfront costs "
            "include MIP (2% of home value) and origination fees. HECMs are appropriate for asset-rich, "
            "cash-poor retirees who want to age in place and supplement retirement income."
        ),
        "metadata": {"product_type": "Reverse Mortgage", "risk_level": "Moderate", "tags": ["reverse mortgage", "HECM", "senior", "home equity", "retirement income"]},
    },
    {
        "title": "Secured Credit Card",
        "text": (
            "A secured credit card requires a cash deposit (typically $200–$2,000) that serves as the credit "
            "limit and collateral. It functions exactly like a regular credit card for purchases, and the "
            "account activity is reported to all three credit bureaus — making it an effective credit-building "
            "tool. After 12–18 months of responsible use (on-time payments, low utilization), most issuers "
            "will graduate the account to an unsecured card and return the deposit. The Discover it Secured "
            "and Capital One Platinum Secured are top-rated options. Best for: those with no credit history, "
            "students, recent immigrants, or those rebuilding after financial setbacks. Avoid secured cards "
            "with high annual fees or monthly fees that eat into the deposit."
        ),
        "metadata": {"product_type": "Credit Card", "risk_level": "Low", "tags": ["secured credit card", "credit building", "credit score", "deposit", "starter card"]},
    },
    {
        "title": "USDA Rural Development Loan",
        "text": (
            "USDA loans are zero-down-payment mortgages guaranteed by the U.S. Department of Agriculture for "
            "properties in eligible rural and suburban areas. Key features: no down payment required, "
            "competitive rates (often below FHA), lower mortgage insurance than FHA. Two upfront costs: "
            "1% guarantee fee (can be rolled into loan) and 0.35% annual fee. Income limits apply — "
            "typically 115% of the area median income. Property must be located in a USDA-eligible area "
            "(use USDA's eligibility map). Credit requirements are flexible — scores as low as 640 are "
            "typically accepted. USDA loans are an excellent option for moderate-income buyers purchasing "
            "in suburban or rural areas who qualify geographically and by income."
        ),
        "metadata": {"product_type": "Mortgage", "risk_level": "Low", "tags": ["USDA loan", "rural", "zero down payment", "government loan", "suburban"]},
    },
    {
        "title": "Medical Loan / Healthcare Financing",
        "text": (
            "Medical loans are personal loans designated for healthcare expenses — elective procedures, "
            "dental work, fertility treatments, or managing large medical bills. Providers include banks, "
            "online lenders, and specialized healthcare finance companies (CareCredit, Alphaeon Credit). "
            "CareCredit offers promotional deferred-interest financing (0% if paid within 6–24 months) for "
            "medical and dental procedures at participating providers. Important: deferred interest means "
            "all interest accrues during the promotional period and is charged retroactively if the balance "
            "isn't paid in full — not the same as true 0% APR. Standard medical loans from banks/credit "
            "unions at fixed rates are often more transparent. Always negotiate with the provider first — "
            "hospitals frequently offer interest-free payment plans."
        ),
        "metadata": {"product_type": "Personal Loan", "risk_level": "Moderate", "tags": ["medical loan", "healthcare financing", "CareCredit", "deferred interest", "dental"]},
    },
]

FAQS = [
    {
        "title": "What credit score do I need to get a mortgage?",
        "text": (
            "Credit score requirements vary by loan type. Conventional loans (backed by Fannie/Freddie) require "
            "a minimum 620, but scores below 740 may result in higher rates through loan-level price adjustments "
            "(LLPAs). Scores of 760+ typically receive the best conventional pricing. FHA loans accept scores as "
            "low as 580 (3.5% down) or 500 (10% down). VA loans have no official minimum but most lenders require "
            "620+. USDA loans typically require 640+. Jumbo loans usually require 700+. Beyond the minimum, every "
            "20-point improvement in credit score can mean meaningful rate improvements — improving from 680 to "
            "720 on a $400,000 mortgage could save $50–$100/month. Checking and correcting credit report errors "
            "before applying is one of the highest-ROI actions a prospective borrower can take."
        ),
        "metadata": {"category": "Mortgage", "tags": ["credit score", "mortgage qualification", "FICO", "conventional", "FHA"]},
    },
    {
        "title": "What is the debt-to-income ratio and why does it matter?",
        "text": (
            "Debt-to-income (DTI) ratio is the percentage of your gross monthly income that goes toward debt "
            "payments. Lenders use it to assess your ability to manage monthly payments. Two versions: "
            "Front-end DTI (housing ratio): monthly housing costs ÷ gross monthly income. Usually should be "
            "below 28%. Back-end DTI (total debt ratio): all monthly debt payments ÷ gross monthly income. "
            "Most conventional lenders want back-end DTI below 43%; FHA allows up to 57% with compensating "
            "factors. Example: $5,000 gross monthly income, $1,200 housing payment, $500 in other debt = "
            "34% back-end DTI. To improve DTI before applying: pay down or eliminate smaller debts, increase "
            "income (including a co-borrower), or choose a less expensive property."
        ),
        "metadata": {"category": "Mortgage", "tags": ["DTI", "debt-to-income", "qualification", "income", "mortgage"]},
    },
    {
        "title": "What is the difference between pre-qualification and pre-approval?",
        "text": (
            "Pre-qualification is an informal estimate based on self-reported income, assets, and debts — no "
            "credit pull, no document verification. It gives a rough sense of what you might borrow but carries "
            "little weight with sellers. Pre-approval is a conditional commitment from a lender to lend a "
            "specific amount based on verified income, assets, employment, and a hard credit pull. A pre-approval "
            "letter is typically valid for 60–90 days and demonstrates serious buying intent to sellers. "
            "In competitive markets, sellers often won't consider offers without a pre-approval letter. "
            "A 'verified pre-approval' or 'underwritten pre-approval' goes one step further — the file is "
            "reviewed by an underwriter before you find a property, making the commitment even stronger. "
            "Always obtain pre-approval before home shopping."
        ),
        "metadata": {"category": "Mortgage", "tags": ["pre-approval", "pre-qualification", "home buying", "mortgage process"]},
    },
    {
        "title": "How does my credit score affect my interest rate?",
        "text": (
            "Your credit score has a direct, significant impact on the interest rate you're offered. Lenders "
            "use risk-based pricing — higher risk (lower score) = higher rate. For a conventional mortgage, "
            "a borrower with a 760 score might be offered 6.75%; the same loan with a 680 score might cost "
            "7.50%. That 0.75% difference on a $350,000 mortgage means paying $162 more per month and "
            "$58,000 more in interest over 30 years. For auto loans, a 720 credit score might get 5.5% while "
            "a 580 score might get 15–18%. For credit cards, the difference between excellent and fair credit "
            "can mean 15% vs. 28% APR. Before any major borrowing, review your credit reports at "
            "AnnualCreditReport.com and dispute any errors."
        ),
        "metadata": {"category": "Credit", "tags": ["credit score", "interest rate", "risk-based pricing", "FICO", "credit impact"]},
    },
    {
        "title": "What is APR vs. interest rate?",
        "text": (
            "The interest rate is the cost of borrowing the principal, expressed as an annual percentage. "
            "APR (Annual Percentage Rate) is a broader measure that includes the interest rate plus other "
            "loan costs (origination fees, discount points, mortgage broker fees, certain closing costs), "
            "expressed as an annual rate. APR is always equal to or higher than the stated interest rate. "
            "For mortgages, APR is most useful for comparing loans with different fee structures — a loan "
            "with a lower rate but high fees might have a higher APR than a loan with a slightly higher rate "
            "and no fees. For credit cards, APR and interest rate are the same (no additional fees in the "
            "rate). For short-term loans or payday loans, APR is extremely high because fees are annualized "
            "over a short period."
        ),
        "metadata": {"category": "Credit Basics", "tags": ["APR", "interest rate", "fees", "mortgage comparison", "total cost"]},
    },
    {
        "title": "What is PMI and how can I avoid it?",
        "text": (
            "Private Mortgage Insurance (PMI) is required by conventional lenders when the down payment is "
            "less than 20% of the home's purchase price. PMI protects the lender (not the borrower) against "
            "default. Cost: typically 0.5–1.5% of the loan amount annually, added to monthly payments. "
            "On a $350,000 loan, PMI might add $146–$438/month. PMI is NOT permanent — it can be removed when "
            "the loan balance reaches 80% of the original appraised value (you can request removal) and must "
            "be automatically canceled at 78% LTV. Ways to avoid PMI: put 20% down; use a piggyback loan "
            "(80/10/10 structure — 80% first mortgage, 10% second, 10% down); choose an FHA loan (though "
            "FHA has its own MIP); or use a lender-paid PMI option (rate increase in exchange for no PMI)."
        ),
        "metadata": {"category": "Mortgage", "tags": ["PMI", "private mortgage insurance", "20% down", "LTV", "removal"]},
    },
    {
        "title": "What is loan-to-value ratio (LTV)?",
        "text": (
            "Loan-to-value (LTV) ratio is the loan amount divided by the property's appraised value, expressed "
            "as a percentage. Example: $320,000 loan on a $400,000 home = 80% LTV. LTV is one of the most "
            "important factors in mortgage qualification and pricing. Higher LTV = more risk for the lender = "
            "higher rates and/or required PMI. 80% LTV (20% down) is the threshold below which PMI is not "
            "required on conventional loans. For HELOCs and home equity loans, lenders look at combined LTV "
            "(CLTV) — the total of all liens divided by appraised value. Most HELOC lenders cap at 80–90% "
            "CLTV. LTV also affects refinancing: borrowers with LTV above 97% typically cannot refinance "
            "without bringing cash to closing or using special programs."
        ),
        "metadata": {"category": "Mortgage", "tags": ["LTV", "loan-to-value", "equity", "PMI", "refinancing"]},
    },
    {
        "title": "When should I refinance my mortgage?",
        "text": (
            "Refinancing replaces your existing mortgage with a new one, typically to lower your rate, change "
            "the loan term, or access equity. The traditional 'refinance rule' was to only refi if you could "
            "lower your rate by 1% or more, but a better framework is the break-even analysis: total closing "
            "costs ÷ monthly savings = months to break even. Example: $4,000 in closing costs / $200/month "
            "savings = 20 months to break even. If you plan to stay in the home 20+ months, refinancing makes "
            "sense. Additional considerations: don't restart a 30-year term if you're already 10 years in — "
            "consider a 20-year refi instead. Avoid cash-out refinancing to fund depreciating assets or "
            "lifestyle expenses. Rates must fall meaningfully (typically 0.5–1%+) to justify refinancing costs "
            "given current high rate environment."
        ),
        "metadata": {"category": "Mortgage", "tags": ["refinancing", "break-even", "rate reduction", "closing costs", "mortgage"]},
    },
    {
        "title": "How do I build credit from scratch?",
        "text": (
            "Building credit with no history requires starting with beginner-friendly products and practicing "
            "responsible habits. Best starting path: (1) Become an authorized user on a parent's or spouse's "
            "credit card — their positive history can instantly appear on your credit report. (2) Open a "
            "secured credit card ($200–$500 deposit) — use for small purchases, pay in full each month. "
            "(3) Apply for a credit-builder loan from a credit union — the loan funds are held in a savings "
            "account while you make payments, released at the end, and reported to bureaus throughout. "
            "(4) After 6–12 months of on-time payments, apply for a starter unsecured card. Credit score "
            "factors: payment history (35%), utilization (30%), length of history (15%), mix (10%), "
            "new inquiries (10%). The fastest single action is reducing credit card utilization below 10%."
        ),
        "metadata": {"category": "Credit Building", "tags": ["credit building", "no credit", "secured card", "credit-builder loan", "credit score"]},
    },
    {
        "title": "What happens if I miss a loan payment?",
        "text": (
            "Missing a loan payment triggers a sequence of consequences depending on how late the payment is. "
            "1–29 days late: most lenders charge a late fee (typically $25–$40 or 5% of payment) but do not "
            "report to credit bureaus. 30+ days late: reported to all three credit bureaus — a 30-day late "
            "can drop a 780 credit score by 90–110 points. 60, 90, 120+ days late: progressively more damage "
            "and increased risk of loan acceleration, collections, or repossession (auto) or foreclosure "
            "(mortgage). Actions if you can't make a payment: contact the lender immediately — many offer "
            "hardship programs, deferment, or forbearance before the payment is late. It's almost always "
            "better to call proactively than to miss a payment silently."
        ),
        "metadata": {"category": "Loan Management", "tags": ["missed payment", "late payment", "credit impact", "delinquency", "forbearance"]},
    },
    {
        "title": "What is the difference between a fixed and variable interest rate?",
        "text": (
            "A fixed interest rate stays constant for the entire loan term, providing payment predictability "
            "and protection against rising rates. A variable (adjustable) rate changes periodically based on "
            "a market benchmark (Prime Rate, SOFR). Variable rates start lower than fixed rates — reflecting "
            "the borrower absorbing interest rate risk. Over time, variable rates may rise or fall. Fixed rates "
            "are best when rates are low (lock in the low rate) or when you value payment certainty. Variable "
            "rates can be advantageous when rates are high (you benefit if they fall), for short-term loans "
            "where the variable period doesn't have time to rise significantly, or when you expect to pay "
            "off the loan early. Mortgages, auto loans, and student loans are commonly available in both types."
        ),
        "metadata": {"category": "Credit Basics", "tags": ["fixed rate", "variable rate", "adjustable", "interest rate", "loan comparison"]},
    },
    {
        "title": "What is a credit utilization ratio?",
        "text": (
            "Credit utilization ratio is the percentage of your available revolving credit that you're currently "
            "using. It's calculated per card and in aggregate across all cards. Example: $3,000 balance on a "
            "$10,000 limit card = 30% utilization. This single factor accounts for 30% of your FICO score — "
            "the second most important factor after payment history. Utilization above 30% begins to hurt your "
            "score; above 50% causes significant damage. The optimal utilization is 1–9% (not 0%). Strategies "
            "to improve utilization: pay balances before the statement closing date (when issuers report to "
            "bureaus); request credit limit increases; open an additional card (increases available credit); "
            "pay down balances. Utilization is not a permanent mark — unlike late payments, reducing utilization "
            "improves your score within the next billing cycle."
        ),
        "metadata": {"category": "Credit", "tags": ["credit utilization", "credit score", "FICO", "revolving credit", "credit card balance"]},
    },
    {
        "title": "What is the difference between a hard and soft credit inquiry?",
        "text": (
            "A hard inquiry (hard pull) occurs when a lender checks your credit as part of a lending decision "
            "— mortgage, auto loan, credit card application. Each hard pull typically reduces your score by "
            "3–7 points and remains on your report for 2 years (impacts score for 12 months). Multiple "
            "mortgage or auto loan hard pulls within a 14–45 day window are treated as a single inquiry by "
            "FICO (rate shopping protection). A soft inquiry occurs when you check your own credit, employers "
            "run background checks, or lenders pre-screen for offers — these do NOT affect your credit score. "
            "Checking your own credit through Credit Karma, Experian, or your bank's free credit score tool "
            "is always a soft pull. Never avoid monitoring your credit out of fear of a score impact."
        ),
        "metadata": {"category": "Credit", "tags": ["hard inquiry", "soft inquiry", "credit pull", "credit score", "rate shopping"]},
    },
    {
        "title": "Can I pay off a loan early? Are there prepayment penalties?",
        "text": (
            "Most loans in the U.S. do not have prepayment penalties, but it depends on the loan type and "
            "lender. Auto loans, personal loans, student loans, and most modern mortgages have no prepayment "
            "penalty. Some older mortgage products and certain lender programs may have a prepayment penalty "
            "for early payoff within the first 2–5 years. Always check your loan agreement before making "
            "large extra payments. When making extra principal payments: specify they should be applied to "
            "principal (not future payments). For mortgages, extra principal payments reduce the loan "
            "balance, saving interest over the life of the loan, but do not reduce the required monthly "
            "payment (unlike bi-weekly payment programs). The decision to pay off low-interest debt early "
            "vs. investing depends on your risk tolerance and expected investment returns."
        ),
        "metadata": {"category": "Loan Management", "tags": ["prepayment", "early payoff", "extra payment", "prepayment penalty", "principal"]},
    },
    {
        "title": "What is loan forbearance vs. deferment?",
        "text": (
            "Both forbearance and deferment temporarily pause or reduce required loan payments during financial "
            "hardship, but they differ in how interest is handled. Deferment (primarily federal student loans): "
            "payments paused, and interest does NOT accrue on subsidized loans (it does on unsubsidized). "
            "Forbearance: payments paused or reduced, but interest continues to accrue on all loan types and "
            "is typically capitalized (added to principal) at the end. Mortgage forbearance (as seen widely "
            "during COVID-19): missed payments are not forgiven — they must be repaid, either immediately, "
            "in a repayment plan, or through a loan modification extending the term. Contact your servicer "
            "proactively — forbearance agreements protect your credit. The impact on your credit: typically "
            "does not affect credit score if granted as a formal program, but should be confirmed with lender."
        ),
        "metadata": {"category": "Loan Management", "tags": ["forbearance", "deferment", "hardship", "student loan", "mortgage relief"]},
    },
    {
        "title": "What is a co-signer on a loan?",
        "text": (
            "A co-signer is a person who agrees to be equally responsible for repaying a loan if the primary "
            "borrower cannot. Co-signers are typically used when the primary borrower has insufficient credit "
            "history, too-low credit score, or inadequate income to qualify independently. The co-signer's "
            "credit and income are considered in the approval decision and they may secure a better rate. "
            "Critically: the loan appears on the co-signer's credit report and counts against their DTI ratio "
            "— affecting their ability to borrow for themselves. If the primary borrower misses payments, "
            "the co-signer's credit is damaged. Some lenders allow co-signer release after a certain number "
            "of on-time payments. Co-signing is a significant financial commitment and should only be done "
            "for borrowers whose repayment ability you trust completely."
        ),
        "metadata": {"category": "Loan Basics", "tags": ["co-signer", "co-borrower", "credit", "qualification", "liability"]},
    },
    {
        "title": "What is a loan origination fee?",
        "text": (
            "A loan origination fee is charged by a lender to cover the cost of processing a new loan "
            "application — underwriting, document preparation, and administrative costs. It's typically "
            "expressed as a percentage of the loan amount: 0.5–1% for mortgages, and can be higher for "
            "personal loans or business loans. On a $350,000 mortgage, a 1% origination fee is $3,500. "
            "Origination fees may be paid upfront at closing or rolled into the loan balance. Some lenders "
            "advertise 'no-origination-fee' loans but compensate with a higher interest rate. When comparing "
            "loan offers, use APR (which includes fees) rather than just the interest rate. On a Loan "
            "Estimate form, origination charges are listed in Section A of the Closing Costs section."
        ),
        "metadata": {"category": "Loan Costs", "tags": ["origination fee", "closing costs", "mortgage fees", "APR", "loan comparison"]},
    },
    {
        "title": "What is amortization?",
        "text": (
            "Amortization is the process of paying off a loan through scheduled, regular payments over time. "
            "Each payment is split between interest and principal. Early in the loan, most of the payment goes "
            "toward interest; as the balance decreases, more goes toward principal. Example: On a $300,000 "
            "mortgage at 7%, first payment: approximately $1,896 — $1,750 interest, $146 principal. After "
            "15 years: approximately $1,896 — $1,050 interest, $846 principal. An amortization schedule "
            "shows every payment breakdown over the loan's life. This explains why extra principal payments "
            "early in a mortgage save disproportionately large amounts of total interest — you're reducing "
            "the principal on which future interest is calculated. Making one extra payment per year can "
            "shorten a 30-year mortgage by 4–6 years."
        ),
        "metadata": {"category": "Loan Basics", "tags": ["amortization", "principal", "interest", "mortgage payment", "payoff schedule"]},
    },
    {
        "title": "What is a credit freeze and how do I use it?",
        "text": (
            "A credit freeze (security freeze) restricts access to your credit reports, preventing new credit "
            "accounts from being opened in your name — the most powerful protection against identity theft. "
            "Freezing is free at all three bureaus (Equifax, Experian, TransUnion) and can be done online, "
            "by phone, or by mail. Freezing does not affect your credit score, existing credit accounts, "
            "or your ability to check your own credit. When you need to apply for new credit, temporarily "
            "lift the freeze with a PIN — typically takes only minutes online. After the application, "
            "refreeze all three bureaus. Consider also freezing ChexSystems (used by banks) and "
            "NCTUE (telecommunications). Everyone should have a credit freeze — it's free and the only "
            "downside is needing to lift it briefly when applying for credit."
        ),
        "metadata": {"category": "Credit Protection", "tags": ["credit freeze", "identity theft", "security freeze", "Equifax", "Experian", "TransUnion"]},
    },
    {
        "title": "What is the difference between a charge-off and a collection account?",
        "text": (
            "A charge-off occurs when a creditor writes off a debt as uncollectable (typically after 120–180 "
            "days of non-payment). Despite the name, the debt is NOT forgiven — it is still legally owed. "
            "The creditor either retains the account in-house for collection or sells it to a debt collection "
            "agency (at which point it may appear as both a charge-off from the original creditor AND a new "
            "collection account). Both charge-offs and collection accounts severely damage credit scores and "
            "remain on credit reports for 7 years from the date of first delinquency. Options for dealing "
            "with them: pay in full (doesn't remove but shows resolved), negotiate a settlement for less "
            "than owed, or negotiate 'pay for delete' (some collectors will remove the account upon payment, "
            "though original creditors rarely agree to this)."
        ),
        "metadata": {"category": "Credit Repair", "tags": ["charge-off", "collection", "credit repair", "debt", "credit report"]},
    },
    {
        "title": "What is the CFPB and how does it protect borrowers?",
        "text": (
            "The Consumer Financial Protection Bureau (CFPB) is a federal agency created by the Dodd-Frank "
            "Act (2010) to protect consumers in financial markets. It regulates banks, credit unions, "
            "mortgage servicers, payday lenders, debt collectors, and other financial companies. Key "
            "protections: enforces Truth in Lending Act (TILA) requiring clear disclosure of loan terms; "
            "enforces Fair Debt Collection Practices Act (FDCPA) limiting debt collector behavior; "
            "the mortgage Know Before You Owe rule standardized Loan Estimates and Closing Disclosures. "
            "Consumers can submit complaints directly to the CFPB (consumerfinance.gov) — companies are "
            "required to respond within 15 days. The CFPB maintains a public database of consumer "
            "complaints that is searchable. It's one of the most effective tools for resolving disputes "
            "with financial institutions."
        ),
        "metadata": {"category": "Consumer Rights", "tags": ["CFPB", "consumer protection", "complaint", "TILA", "FDCPA"]},
    },
    {
        "title": "What is LTV and CLTV?",
        "text": (
            "LTV (Loan-to-Value) is the ratio of a single mortgage to the property's appraised value. "
            "CLTV (Combined Loan-to-Value) is the ratio of ALL liens on a property (first mortgage + "
            "second mortgage + HELOC) to the appraised value. Example: $300,000 first mortgage + $50,000 "
            "HELOC on a $400,000 home = 87.5% CLTV. CLTV is used by second mortgage and HELOC lenders "
            "to determine how much additional lending they're comfortable with. Most HELOC lenders cap "
            "at 80–90% CLTV. For rate and terms, lenders use LTV; for maximum qualifying loan amount "
            "when a second lien exists, they use CLTV. In foreclosure, the first mortgage lender is paid "
            "first — the higher the CLTV, the less equity buffer exists for the second lien holder, "
            "explaining why second mortgage rates are higher."
        ),
        "metadata": {"category": "Mortgage", "tags": ["LTV", "CLTV", "home equity", "HELOC", "second mortgage"]},
    },
    {
        "title": "What is a balloon payment?",
        "text": (
            "A balloon payment is a large, lump-sum payment due at the end of a loan term — typically much "
            "larger than the regular periodic payments. Balloon loans have lower monthly payments (often "
            "calculated on a 30-year amortization) but require full payoff after a shorter term (5–7 years). "
            "At the balloon due date, borrowers must pay off the balance in full, refinance, or sell the "
            "property. Balloon mortgages are uncommon today after the 2008 financial crisis but still "
            "appear in commercial real estate lending. Business loans may also have balloon structures. "
            "Risk: if property values fall or credit tightens at the balloon date, refinancing may be "
            "difficult. Borrowers should have a clear plan for addressing the balloon payment well before "
            "its due date."
        ),
        "metadata": {"category": "Loan Basics", "tags": ["balloon payment", "balloon mortgage", "commercial real estate", "refinancing risk"]},
    },
    {
        "title": "How does bankruptcy affect my ability to get a loan?",
        "text": (
            "Bankruptcy is a federal legal process that eliminates or restructures debt. Chapter 7 "
            "(liquidation) stays on your credit report for 10 years; Chapter 13 (reorganization/repayment "
            "plan) for 7 years. Post-bankruptcy mortgage waiting periods: FHA loan — 2 years after Chapter 7 "
            "discharge; 1 year into Chapter 13 repayment (with court approval). Conventional loan — 4 years "
            "after Chapter 7; 2 years after Chapter 13 discharge. VA loan — 2 years after Chapter 7. "
            "During the waiting period, rebuilding credit is critical: secured credit card, credit-builder "
            "loan, on-time payments. A bankruptcy doesn't permanently disqualify you from borrowing — "
            "lenders look at the totality of the post-bankruptcy credit picture. Working with a housing "
            "counselor during the waiting period significantly improves outcomes."
        ),
        "metadata": {"category": "Credit Repair", "tags": ["bankruptcy", "Chapter 7", "Chapter 13", "credit recovery", "mortgage waiting period"]},
    },
    {
        "title": "What is a home appraisal and why is it required?",
        "text": (
            "A home appraisal is an independent assessment of a property's fair market value performed by "
            "a licensed appraiser. Lenders require appraisals on purchase and refinance mortgages to ensure "
            "the collateral (the home) is worth at least the loan amount. The appraiser evaluates the "
            "property's condition, features, and comparable sales (comps) in the area. Cost: $400–$700 "
            "for a typical single-family home. If the appraisal comes in below the purchase price, options "
            "include: renegotiate the purchase price, make up the difference in cash, challenge the "
            "appraisal with additional comps (reconsideration of value), or walk away using the appraisal "
            "contingency. Automated Valuation Models (AVMs) may be accepted for low-LTV refinances, "
            "reducing or eliminating the need for a full appraisal."
        ),
        "metadata": {"category": "Mortgage", "tags": ["appraisal", "home value", "LTV", "purchase price", "comps"]},
    },
    {
        "title": "What is a Loan Estimate and Closing Disclosure?",
        "text": (
            "The Loan Estimate (LE) is a standardized 3-page form provided within 3 business days of "
            "submitting a mortgage application. It details the loan terms, projected monthly payments, "
            "and closing costs estimates. The Closing Disclosure (CD) is the final version provided at "
            "least 3 business days before closing, with actual figures. Borrowers should compare LE to CD "
            "carefully — some fees are not allowed to change (origination fees) while others can change "
            "within limits (title insurance) or without limit (prepaid interest). These forms were "
            "standardized by the CFPB's Know Before You Owe rule to make mortgage comparison shopping "
            "easier. Always obtain Loan Estimates from at least 2–3 lenders before proceeding — comparison "
            "shopping on mortgages typically saves $1,500–$3,000+ in fees."
        ),
        "metadata": {"category": "Mortgage Process", "tags": ["Loan Estimate", "Closing Disclosure", "TRID", "closing costs", "mortgage shopping"]},
    },
    {
        "title": "What is interest capitalization on student loans?",
        "text": (
            "Interest capitalization occurs when unpaid accrued interest is added to the principal balance "
            "of a loan — you then pay interest on a higher balance going forward. For federal student loans, "
            "capitalization occurs at the end of deferment, forbearance, and income-driven repayment (IDR) "
            "periods (though SAVE plan has changed some rules). Example: $50,000 in unsubsidized loans at "
            "6.5% with 4 years of school deferment = $13,000 in accrued interest. If capitalized, the new "
            "balance is $63,000, and future interest accrues on that higher balance. Strategies to avoid "
            "capitalization: pay interest while in school (even small amounts help); choose repayment plans "
            "that cap interest; request subsidized loans first; refinance private loans at lower rates "
            "after graduating with strong income."
        ),
        "metadata": {"category": "Student Loans", "tags": ["capitalization", "student loan", "interest accrual", "deferment", "income-driven repayment"]},
    },
    {
        "title": "What are closing costs and how much should I expect to pay?",
        "text": (
            "Closing costs are the fees paid at the closing of a real estate transaction, separate from the "
            "down payment. They typically total 2–5% of the loan amount. Major categories: "
            "Lender fees ($500–$2,500+): origination fee, application fee, underwriting fee. "
            "Third-party fees: title insurance ($500–$2,500), appraisal ($400–$700), attorney fees "
            "(where required), pest inspection. "
            "Prepaid items: homeowners insurance (1 year), property taxes (2–6 months), prepaid interest. "
            "Strategies to reduce closing costs: negotiate lender fees, shop for title insurance, ask "
            "for seller concessions (seller pays some closing costs), or use a 'no-closing-cost mortgage' "
            "(rate increase in exchange for lender covering costs — better for short holding periods). "
            "First-time buyer programs in many states provide closing cost assistance."
        ),
        "metadata": {"category": "Mortgage Process", "tags": ["closing costs", "mortgage fees", "title insurance", "prepaid", "seller concessions"]},
    },
    {
        "title": "What is a FICO score vs. VantageScore?",
        "text": (
            "FICO Score and VantageScore are the two main credit scoring models used in the U.S. FICO (Fair "
            "Isaac Corporation) was created in 1989 and is used in 90%+ of lending decisions; there are "
            "multiple FICO versions (FICO 8, FICO 9, FICO 10, FICO Auto, FICO Bankcard) tailored to "
            "different loan types. VantageScore was created by the three credit bureaus in 2006 and is "
            "commonly shown by free credit monitoring services (Credit Karma, Chase Credit Journey). Both "
            "score on a 300–850 scale using similar factors, but weights differ slightly. "
            "VantageScore can score consumers with as little as 1 month of credit history; FICO requires "
            "6 months. Your VantageScore and FICO score may differ by 20–50 points — lenders use FICO, so "
            "obtain your FICO score (free at Experian, Discover, American Express) for the most relevant "
            "pre-application assessment."
        ),
        "metadata": {"category": "Credit Basics", "tags": ["FICO", "VantageScore", "credit score", "Credit Karma", "scoring model"]},
    },
    {
        "title": "What is a rate lock on a mortgage?",
        "text": (
            "A rate lock is a lender's guarantee to hold a specific interest rate for a borrower for a set "
            "period (typically 30–60 days) while the loan is processed. Rate locks protect against rate "
            "increases during the loan process. If rates fall after locking, most standard locks cannot be "
            "renegotiated — but 'float-down' options allow refinancing to a lower rate for an additional "
            "fee. Lock periods: 30 days is standard for a smooth purchase transaction; 45–60 days provides "
            "more buffer for complex deals or new construction. Longer locks cost more (lender charges a "
            "premium for holding the rate longer). If your lock expires before closing, you must extend "
            "(at additional cost) or relock at current market rates. Never miss a lock expiration without "
            "requesting an extension in advance."
        ),
        "metadata": {"category": "Mortgage Process", "tags": ["rate lock", "interest rate protection", "float-down", "lock expiration", "closing timeline"]},
    },
    {
        "title": "What is mortgage escrow?",
        "text": (
            "Mortgage escrow is an account managed by the lender/servicer that holds funds for property "
            "taxes and homeowners insurance, disbursing them when bills come due. At closing, borrowers "
            "typically prepay 2–6 months of property tax and insurance into the escrow account. Thereafter, "
            "the monthly mortgage payment includes the escrow portion (1/12 of annual property tax + "
            "1/12 of annual insurance premium). Servicers must maintain a cushion but cannot hold more "
            "than 2 months of escrow payments. Annual escrow analysis compares actual vs. estimated costs "
            "— if actual costs were higher, a 'shortage' requires a lump-sum payment or higher monthly "
            "escrow. If lower, a 'surplus' is refunded. Most lenders require escrow for loans with "
            "LTV above 80%. Borrowers with 20% equity may request escrow waiver (lender may charge a fee)."
        ),
        "metadata": {"category": "Mortgage", "tags": ["escrow", "property tax", "homeowners insurance", "mortgage payment", "escrow analysis"]},
    },
    {
        "title": "How does student loan income-driven repayment work?",
        "text": (
            "Income-driven repayment (IDR) plans cap federal student loan payments at a percentage of "
            "discretionary income. The main plans are: SAVE (Saving on a Valuable Education) — newest plan, "
            "payments capped at 5–10% of discretionary income (5% for undergrad only); PAYE (Pay As You "
            "Earn) — 10% of discretionary income; IBR (Income-Based Repayment) — 10–15% depending on when "
            "borrowed; ICR (Income-Contingent Repayment). After 20–25 years of qualifying payments, "
            "remaining balances are forgiven (though forgiven amounts may be taxable). For borrowers pursuing "
            "Public Service Loan Forgiveness (PSLF), IDR is required — forgiveness occurs after 10 years "
            "of qualifying payments (120 payments) in a public service job. IDR enrollment is free and done "
            "through StudentAid.gov."
        ),
        "metadata": {"category": "Student Loans", "tags": ["IDR", "income-driven repayment", "SAVE", "PSLF", "loan forgiveness"]},
    },
    {
        "title": "What is a second mortgage?",
        "text": (
            "A second mortgage is any lien on a property that is subordinate to the first (primary) mortgage. "
            "Common second mortgage types: home equity loans (lump sum, fixed rate) and HELOCs (revolving, "
            "variable rate). Because the second mortgage lender is paid after the first mortgage lender in "
            "foreclosure, second mortgages carry higher interest rates to compensate for this subordinate "
            "position. When refinancing a first mortgage, the second mortgage lender must either be paid off "
            "or grant 'subordination' (agree to remain in second position on the new first mortgage). "
            "Piggyback loans (80/10/10) use a second mortgage to avoid PMI when down payment is less than "
            "20%. Interest on second mortgages is deductible only if used for home improvement."
        ),
        "metadata": {"category": "Home Equity", "tags": ["second mortgage", "HELOC", "home equity", "subordination", "piggyback"]},
    },
    {
        "title": "What is a USURY law?",
        "text": (
            "Usury laws are state regulations that cap the maximum interest rate lenders can charge on "
            "loans. These laws were designed to protect borrowers from predatory lending. However, a 1978 "
            "Supreme Court ruling (Marquette National Bank v. First of Omaha) allowed nationally chartered "
            "banks to charge the interest rates permitted in their home state — effectively gutting state "
            "usury limits for credit cards. This is why credit card companies are often chartered in "
            "Delaware or South Dakota (which have no rate caps). State usury laws still apply to some "
            "non-bank lenders and certain loan types. Payday lenders, however, operate in many states "
            "under special small-loan exemptions with APRs of 300–600%. Several states have passed "
            "rate caps specifically targeting payday loans (36% APR cap)."
        ),
        "metadata": {"category": "Consumer Rights", "tags": ["usury", "interest rate cap", "consumer protection", "payday lending", "state law"]},
    },
    {
        "title": "What is the difference between a mortgage servicer and the original lender?",
        "text": (
            "The lender (originator) provides the funds for a mortgage at closing. The servicer collects "
            "monthly payments, manages the escrow account, handles customer service, processes payoff "
            "requests, and manages delinquency/loss mitigation. Often the originator and servicer are the "
            "same company, but most mortgages are sold on the secondary market shortly after origination — "
            "the loan's ownership and servicing rights can be sold separately. It's common for a mortgage's "
            "servicer to change one or more times over its life. When a servicer change occurs, borrowers "
            "must receive a Notice of Transfer at least 15 days before the transfer. You must then direct "
            "payments to the new servicer. Your loan terms cannot change when servicing is transferred. "
            "All qualified written requests and complaints must be directed to the servicer, not the owner."
        ),
        "metadata": {"category": "Mortgage", "tags": ["mortgage servicer", "loan servicing", "secondary market", "servicer transfer", "escrow"]},
    },
]

MARKET_COMMENTARY = [
    {
        "title": "2025 Mortgage Rate Outlook: When Will Rates Come Down?",
        "text": (
            "Mortgage rates reached their highest levels since 2000 in October 2023 (7.79% for 30-year fixed) "
            "before moderating. As of early 2025, 30-year fixed rates hover in the 6.5–7.0% range. The path "
            "forward depends primarily on Federal Reserve policy and inflation data. Our base case: 2–3 Fed "
            "rate cuts of 25 bps each in 2025 should gradually reduce the 10-year Treasury yield (to which "
            "mortgage rates are closely tied), bringing 30-year rates toward 6.0–6.5% by year-end. Mortgage "
            "rates typically lag Fed cuts by 2–4 months. The housing market remains constrained by the "
            "'lock-in effect' — existing homeowners with 3% mortgages are reluctant to sell. This keeps "
            "inventory low and prices supported even as affordability is strained. Prospective buyers should "
            "not wait for 3–4% rates, which are unlikely; rates in the 5.5–6.5% range are more realistic."
        ),
        "metadata": {"period": "2025", "topic": "Mortgage Rates", "tags": ["mortgage rates", "Federal Reserve", "2025 outlook", "housing market"]},
    },
    {
        "title": "Auto Loan Market: Affordability Squeeze Tightens",
        "text": (
            "The auto loan market faces significant affordability headwinds in 2025. Vehicle prices remain "
            "elevated despite easing from 2022 peaks — the average new vehicle transaction price exceeds "
            "$47,000. Combined with 7–9% auto loan rates (versus 3–4% in 2021), the average monthly payment "
            "for a new vehicle now exceeds $700. Delinquency rates on auto loans have risen, particularly "
            "for subprime borrowers, reaching levels not seen since 2010. The market is bifurcating: "
            "prime borrowers (720+ scores) face manageable terms; subprime borrowers face rates of 15–25% "
            "and tight credit. Used vehicle prices have normalized somewhat after the COVID-era shortage. "
            "Strategies for consumers: consider a 3–5 year old certified pre-owned vehicle; put more down "
            "to reduce loan amount; use a credit union for financing; and avoid 84-month terms."
        ),
        "metadata": {"period": "2025", "topic": "Auto Lending", "tags": ["auto loans", "vehicle prices", "delinquency", "affordability", "subprime"]},
    },
    {
        "title": "Credit Card Debt Reaches Record Levels",
        "text": (
            "U.S. consumer credit card debt surpassed $1.2 trillion in 2024, a record high, according to "
            "Federal Reserve data. The average credit card interest rate hit a record 22–23% APR, the highest "
            "since data collection began. Delinquency rates are rising, particularly among younger borrowers "
            "(ages 18–39) and lower-income households who used credit to offset pandemic savings depletion "
            "and inflation-driven cost of living increases. The concentration of debt is concerning: the top "
            "10% of cardholders carry balances averaging $9,500+. The practical advice remains unchanged: "
            "pay in full monthly to avoid interest entirely; if carrying a balance, pursue 0% balance "
            "transfer offers (typically 15–21 months), negotiate rates, or consolidate with a personal loan. "
            "Credit card debt at 22% is an immediate financial emergency."
        ),
        "metadata": {"period": "2024-2025", "topic": "Consumer Credit", "tags": ["credit card debt", "delinquency", "APR", "consumer debt", "record high"]},
    },
    {
        "title": "Student Loan Landscape Post-COVID Forbearance",
        "text": (
            "The COVID-19 federal student loan payment pause lasted over 3 years (March 2020 – September 2023) "
            "before payments resumed. The restart has created significant borrower adjustment challenges — "
            "approximately 20% of borrowers were in 'on-ramp' status (late payments not reported to credit "
            "bureaus) through September 2024. The Biden administration's broad student loan forgiveness plan "
            "was blocked by the Supreme Court, but targeted forgiveness programs continue: PSLF, borrower "
            "defense, and IDR account adjustments (giving credit for prior non-qualifying payments). The "
            "SAVE plan faces legal challenges in 2025. Borrowers should: verify their enrollment in the "
            "optimal repayment plan, check eligibility for PSLF if in public service, and ensure their "
            "contact information is current with their servicer to avoid missing critical notices."
        ),
        "metadata": {"period": "2024-2025", "topic": "Student Loans", "tags": ["student loans", "payment restart", "SAVE plan", "PSLF", "forgiveness"]},
    },
    {
        "title": "The Rise of Buy Now, Pay Later (BNPL) and Regulatory Response",
        "text": (
            "Buy Now, Pay Later (BNPL) services (Affirm, Klarna, Afterpay, PayPal Pay Later) have grown "
            "explosively, with over 100 million U.S. users. The most common product: pay-in-4 (four "
            "equal payments over 6 weeks, typically interest-free). Longer-term BNPL loans carry interest "
            "rates of 10–36% APR. Concerns: BNPL is largely unregulated at the federal level; purchases "
            "are not consistently reported to credit bureaus (can't build credit); easy approval can "
            "enable overspending; multiple simultaneous BNPL commitments can create hidden debt loads. "
            "In 2024, the CFPB issued guidance treating BNPL like credit cards for key consumer "
            "protections. For consumers: use BNPL only for planned purchases you'd have made anyway; "
            "never use for impulse purchases; track all BNPL obligations as real debt obligations."
        ),
        "metadata": {"period": "2024-2025", "topic": "Fintech Lending", "tags": ["BNPL", "buy now pay later", "Affirm", "Klarna", "consumer debt", "regulation"]},
    },
    {
        "title": "Home Equity Lending Surge as Homeowners Tap Accumulated Equity",
        "text": (
            "U.S. homeowners collectively hold approximately $30 trillion in home equity — near record "
            "levels after years of home price appreciation. The 'lock-in effect' (homeowners reluctant to "
            "sell and give up 3% mortgages) means many are accessing equity through HELOCs and home equity "
            "loans instead of selling. HELOC originations have increased significantly, as homeowners fund "
            "renovations, college costs, and debt consolidation while keeping their low first mortgage. "
            "Key consideration: HELOC rates are variable (typically Prime + 0–2.5%, currently 7.5–10.5%) "
            "and will reprice downward as the Fed cuts rates. Home equity lending is appropriate for home "
            "improvements that increase property value or replacing higher-rate debt. Using home equity "
            "to fund lifestyle expenses or depreciating assets (cars, vacations) is inadvisable — you "
            "risk your home as collateral."
        ),
        "metadata": {"period": "2025", "topic": "Home Equity", "tags": ["HELOC", "home equity", "lock-in effect", "home renovation", "equity tap"]},
    },
    {
        "title": "Credit Score Migration: How Scores Have Shifted Post-Pandemic",
        "text": (
            "The COVID-19 pandemic paradoxically improved aggregate U.S. credit scores. Stimulus payments, "
            "enhanced unemployment benefits, and loan forbearance programs reduced delinquencies and "
            "allowed many consumers to pay down debt. The average FICO score reached a record 718 in 2021. "
            "Since then, scores have declined modestly as forbearance programs ended, consumer debt "
            "increased, and delinquencies rose. The distribution has bifurcated: homeowners and those "
            "who locked in low debt rates in 2020–2021 have strong credit profiles; renters and recent "
            "borrowers face higher rates and more financial stress. For lenders, this creates underwriting "
            "challenges — traditional score-based models may not fully capture the post-pandemic credit "
            "environment. Alternative data (rental payments, utility payments) is increasingly being "
            "incorporated into underwriting."
        ),
        "metadata": {"period": "2024-2025", "topic": "Credit Markets", "tags": ["credit scores", "FICO", "post-pandemic", "credit quality", "alternative data"]},
    },
    {
        "title": "SBA Lending Trends: Small Business Access to Capital",
        "text": (
            "SBA loan volume has remained strong, supporting small business recovery and growth. SBA 7(a) "
            "loans (up to $5M for working capital, equipment, real estate) and 504 loans (for major fixed "
            "assets and real estate) are the primary products. The SBA's Express loan (up to $500,000, "
            "36-hour turnaround decision) has become increasingly popular for urgent needs. Rising rates "
            "have increased small business borrowing costs — SBA 7(a) rates are Prime + 2.25–2.75% (capped), "
            "currently placing them at 9.5–11%. Community Development Financial Institutions (CDFIs) "
            "provide an important alternative for underserved small businesses that don't meet bank "
            "criteria. Online alternative lenders (OnDeck, Kabbage) offer fast capital but at high rates — "
            "appropriate only when traditional financing is unavailable and the business ROI clearly "
            "exceeds the borrowing cost."
        ),
        "metadata": {"period": "2025", "topic": "Business Lending", "tags": ["SBA", "small business", "7a loan", "504 loan", "CDFI", "business lending"]},
    },
    {
        "title": "Impact of AI on Loan Underwriting and Approval",
        "text": (
            "Artificial intelligence and machine learning are transforming loan underwriting across all "
            "product categories. Traditional models relied heavily on FICO scores and debt-to-income ratios. "
            "AI models analyze thousands of variables — including alternative data like rental payment "
            "history, bank transaction patterns, and employment data — to improve approval rates for "
            "thin-file or non-traditional borrowers. Lenders like Upstart, ZestFinance, and increasingly "
            "large banks are deploying AI underwriting. Benefits: more accurate risk assessment, faster "
            "decisions (seconds vs. days), and greater access for underserved borrowers. Concerns: "
            "algorithmic bias can perpetuate or amplify discrimination against protected classes. "
            "Regulators (OCC, CFPB) are increasing scrutiny of AI models for fair lending compliance. "
            "For consumers: AI-underwritten loans from reputable lenders are legitimate — evaluate based "
            "on APR and terms, not the underlying technology."
        ),
        "metadata": {"period": "2025", "topic": "Fintech Lending", "tags": ["AI", "underwriting", "machine learning", "alternative data", "fair lending"]},
    },
    {
        "title": "Interest Rate Environment: Impact on Refinancing Activity",
        "text": (
            "Mortgage refinancing activity has been at multi-decade lows since rates rose above 6% in 2022. "
            "The 'refinanceable universe' — borrowers with existing mortgages at rates above current market "
            "levels — has shrunk significantly from the peak of 2021. Most homeowners locked in mortgages "
            "at 2.5–3.5% in 2020–2021 and have no mathematical incentive to refinance at current 6.5–7% "
            "rates. As rates gradually decline toward 5.5–6%, a new wave of refinancing activity will "
            "emerge — primarily for borrowers who purchased in 2023–2024 at 7%+ rates. Cash-out "
            "refinancing has remained more active than rate-and-term refinancing for homeowners with "
            "substantial equity who need liquidity. For lenders, the focus has shifted heavily toward "
            "purchase originations and home equity products to replace refinancing volume."
        ),
        "metadata": {"period": "2025", "topic": "Mortgage Market", "tags": ["refinancing", "mortgage market", "lock-in effect", "cash-out refi", "originations"]},
    },
    {
        "title": "Predatory Lending: Identifying and Avoiding Scams",
        "text": (
            "Predatory lending involves unfair, deceptive, or abusive loan terms that harm borrowers. "
            "Common predatory practices: (1) Payday loans — 300–600% APR for 2-week loans with "
            "automatic rollover trapping borrowers in debt cycles. (2) Rent-to-own — extremely expensive "
            "way to acquire goods, often with hidden fees. (3) Advance-fee loan scams — require upfront "
            "payment before 'releasing' loan funds; legitimate lenders never do this. (4) Equity stripping — "
            "encouraging homeowners to repeatedly refinance, extracting fees each time while increasing "
            "loan balance. (5) Balloon loan fraud — burying balloon payment terms in fine print. "
            "Warning signs: pressure to sign immediately, vague or missing paperwork, lender focuses "
            "only on monthly payment not total cost. Verify any lender through your state's banking "
            "regulator and NMLS Consumer Access (for mortgage companies)."
        ),
        "metadata": {"period": "2025", "topic": "Consumer Protection", "tags": ["predatory lending", "payday loans", "scam", "advance fee", "consumer protection"]},
    },
    {
        "title": "The HELOC Rate Opportunity as Fed Cuts Continue",
        "text": (
            "HELOCs are uniquely positioned to benefit from the Federal Reserve's rate-cutting cycle. Unlike "
            "fixed-rate home equity loans, HELOC rates are variable and directly tied to the Prime Rate "
            "(currently Fed Funds Rate + 3%). Every 25 basis point Fed rate cut immediately flows through "
            "to HELOC rates. With 2–3 cuts expected in 2025, HELOC rates that currently sit around 8–10% "
            "could fall to 7–8.5% by year-end. For homeowners contemplating home equity borrowing, a HELOC "
            "in a declining rate environment may outperform a fixed-rate home equity loan locked in at "
            "today's higher rates. The tradeoff: variable rate risk if the rate-cutting cycle stalls. "
            "A common strategy: use a HELOC for the flexibility and convert to a fixed-rate home equity "
            "loan if rates begin rising again."
        ),
        "metadata": {"period": "2025", "topic": "Home Equity", "tags": ["HELOC", "Prime Rate", "Federal Reserve", "rate cuts", "home equity strategy"]},
    },
]

CLIENT_SCENARIOS = [
    {
        "title": "Case Study: First-Time Homebuyer with 5% Down in a Competitive Market",
        "text": (
            "Profile: Keisha, 29, first-time homebuyer earning $72,000. She has saved $18,000 (5% of a "
            "$360,000 target purchase price) and a credit score of 695.\n\n"
            "Loan options analysis: (1) Conventional loan with 5% down: requires PMI (~$110/month), "
            "rate approximately 7.25% (score below 720 triggers LLPAs). Monthly P&I: $2,337 + PMI. "
            "(2) FHA loan: 3.5% down ($12,600), rate ~6.90%, but MIP adds $165/month permanently. "
            "PMI removes at 78% LTV; FHA MIP typically stays for life of loan. (3) State first-time buyer "
            "program: many states offer down payment assistance (2–5% grants or deferred loans) and "
            "below-market rates for qualifying income levels. Recommended path: check state HFA programs "
            "first. If unavailable, FHA with a plan to refinance to conventional once equity reaches 20% "
            "and credit improves above 720 (which removes PMI exposure). Pre-approval before house hunting "
            "is essential in competitive markets."
        ),
        "metadata": {"scenario_type": "First-Time Buyer", "tags": ["first-time buyer", "FHA", "down payment assistance", "PMI", "mortgage"]},
    },
    {
        "title": "Case Study: Debt Consolidation — Breaking the Credit Card Cycle",
        "text": (
            "Profile: Marcus, 38, $91,000 salary. Credit card balances: $8,000 at 24%, $5,500 at 21%, "
            "$3,200 at 19%. Minimum payments: $535/month. Paying minimums only would cost $12,000+ in "
            "interest and take 15+ years to pay off.\n\n"
            "Consolidation analysis: Marcus qualifies for a personal loan of $17,000 at 11.5% APR "
            "over 36 months. Monthly payment: $558/month — only $23 more than current minimums, but "
            "pays off in 3 years versus 15+, saving over $9,000 in interest. Critical next step: "
            "after consolidating, do NOT use the freed-up credit card capacity for new purchases. "
            "Either close the cards (slight credit score impact) or keep with zero balance. "
            "Root cause analysis: identify what drove the debt accumulation — budget shortfall, "
            "lifestyle inflation, emergency spending. Address root cause to prevent recurrence. "
            "The consolidation buys time and saves interest; behavior change creates lasting improvement."
        ),
        "metadata": {"scenario_type": "Debt Consolidation", "tags": ["credit card debt", "personal loan", "debt consolidation", "interest savings"]},
    },
    {
        "title": "Case Study: Refinancing Decision in a High-Rate Environment",
        "text": (
            "Profile: The Nguyen family purchased their home in October 2023 with a 30-year fixed mortgage "
            "at 7.75% ($425,000 loan). Current balance: $419,000. Current market rate: 6.8%.\n\n"
            "Refinance analysis: Current payment (P&I): $3,025. New payment at 6.8%: $2,750. Monthly "
            "savings: $275. Closing costs estimate: $6,800. Break-even: 6,800 ÷ 275 = 24.7 months. "
            "Decision: If they plan to stay in the home 25+ months, refinancing makes sense now. "
            "Should they wait for lower rates? If rates fall to 6.0% in 12 months, savings jump to "
            "$450/month with similar closing costs — break-even under 16 months. Risk of waiting: "
            "rates could stay flat or rise. Recommendation: Set a rate target (6.0–6.25%) with an "
            "alert through their lender. Refinance when the break-even period falls below 18 months "
            "for their planning horizon."
        ),
        "metadata": {"scenario_type": "Refinancing", "tags": ["refinancing", "break-even", "mortgage rate", "rate lock", "decision analysis"]},
    },
    {
        "title": "Case Study: Auto Loan Negotiation and Financing Strategy",
        "text": (
            "Profile: Priya, 31, needs to replace her car. Target vehicle: 2022 certified pre-owned "
            "sedan, dealer asking price $28,500. Her credit score: 748. Current savings: $4,500 for down.\n\n"
            "Financing strategy: (1) Get pre-approved by her credit union before visiting the dealer. "
            "Credit union offers 5.9% for 60 months on used vehicles for her score. (2) Dealer financing "
            "offer: 8.4% for 72 months (lower payment looks attractive but 72 months on a used car is "
            "high risk). Credit union 60-month: $456/month, total cost $27,360 in interest. Dealer "
            "72-month: $433/month, total interest $8,576. Same vehicle, $5,200 more in total interest. "
            "(3) Negotiate the price first (treat as cash deal), then introduce financing. Dealer "
            "markup on financing is profit center. Final result: negotiated price to $26,800, used "
            "credit union financing at 5.9% / 60 months = $434/month. Saved $3,700 on price + $5,000+ "
            "in interest versus dealer offer."
        ),
        "metadata": {"scenario_type": "Auto Loan", "tags": ["auto loan", "credit union", "negotiation", "dealer financing", "used car"]},
    },
    {
        "title": "Case Study: Managing Student Loans as a New Graduate",
        "text": (
            "Profile: Daniela, 25, just graduated with $48,000 in federal student loans (mix of "
            "subsidized and unsubsidized). Starting salary: $58,000 as a healthcare administrator. "
            "Employer: nonprofit hospital.\n\n"
            "Strategic analysis: Daniela qualifies for PSLF — working for a nonprofit 501(c)(3). "
            "Optimal strategy: (1) Enroll in the SAVE income-driven repayment plan immediately. "
            "At $58,000 income, SAVE payment ≈ $125/month (versus $520/month on standard repayment). "
            "(2) Make 120 qualifying payments (10 years) while working for the nonprofit. (3) Remaining "
            "balance forgiven tax-free under PSLF. Total paid: ~$15,000 over 10 years versus $62,000+ "
            "on standard repayment — a $47,000+ benefit. Critical: certify employment annually, keep "
            "records meticulously, and verify loans are Direct Loans (not FFEL). The PSLF opportunity "
            "dramatically changes the financial calculus versus aggressive repayment."
        ),
        "metadata": {"scenario_type": "Student Loan Strategy", "tags": ["student loans", "PSLF", "SAVE plan", "nonprofit", "forgiveness strategy"]},
    },
    {
        "title": "Case Study: HELOC for Home Renovation — Smart vs. Risky Uses",
        "text": (
            "Profile: The Morrison family, home value $520,000, mortgage balance $240,000. They want "
            "$60,000 for a kitchen renovation. Considering HELOC at current Prime + 1% = 9.5%.\n\n"
            "Analysis: CLTV after HELOC: ($240K + $60K) / $520K = 57.7% — well within lender limits. "
            "The kitchen renovation is projected to add $40,000–$50,000 to home value (kitchen "
            "renovations typically return 60–80% of cost). Net economic position: spends $60K, "
            "adds ~$45K in value, pays interest on $60K at 9.5% = $475/month in interest-only payments. "
            "This is a reasonable use of home equity. What NOT to do: using HELOC to buy a car "
            "(loses home as collateral for a depreciating asset), fund vacations, or pay off credit "
            "cards without addressing spending behavior. Rate outlook: with Fed cuts expected, HELOC "
            "rate may fall to 8–8.5% in 2025 — consider drawing in tranches aligned with construction "
            "milestones rather than all at once to minimize interest carry."
        ),
        "metadata": {"scenario_type": "HELOC Use", "tags": ["HELOC", "home renovation", "home equity", "collateral risk", "renovation ROI"]},
    },
    {
        "title": "Case Study: Credit Recovery After Foreclosure",
        "text": (
            "Profile: Robert, 45, went through foreclosure 3 years ago after job loss. Current credit "
            "score: 612 (recovering). Renting, stable job for 2 years at $85,000. Goal: buy a home again.\n\n"
            "Timeline and strategy: FHA loan is available 3 years after foreclosure with score 580+ — "
            "Robert just crossed the waiting period. However, score of 612 gives a higher FHA rate "
            "and higher MIP. Better path: wait 12–18 more months to: (1) Hit the 4-year mark for "
            "conventional loan eligibility (requires 7-year wait only for certain cases). (2) Improve "
            "score to 660+ through continued positive history. (3) Save for 10% down (reduces FHA MIP). "
            "Credit improvement actions: open secured card if none exists; keep utilization under 10%; "
            "add a credit-builder loan. With 12 months of effort, projecting score to 660–680 reduces "
            "borrowing costs by $150–$200/month versus applying today. Patience pays."
        ),
        "metadata": {"scenario_type": "Credit Recovery", "tags": ["foreclosure recovery", "credit repair", "FHA", "waiting period", "credit building"]},
    },
    {
        "title": "Case Study: Small Business Owner Navigating SBA Loan Application",
        "text": (
            "Profile: Elena, 42, owns a 4-year-old catering business generating $380,000 annual revenue "
            "with consistent profitability. Needs $150,000 for commercial kitchen expansion.\n\n"
            "Loan options: (1) SBA 7(a) loan: $150,000, 10-year term, rate = Prime + 2.25% (currently "
            "~10.75%). Monthly payment: ~$2,000. SBA guarantee reduces lender risk, improving approval "
            "odds for business without significant real estate collateral. (2) Conventional business "
            "term loan: possible if the business has strong cash flow, but may require more collateral. "
            "(3) SBA 504 if the expansion involves real estate or equipment over $150K. "
            "Application preparation: 2 years business tax returns, year-to-date P&L and balance sheet, "
            "personal tax returns (3 years), business plan, equipment quotes. Elena's strong revenue "
            "and 4-year operating history make her a solid candidate. Apply through an SBA Preferred "
            "Lender for fastest processing (no SBA review step)."
        ),
        "metadata": {"scenario_type": "Business Lending", "tags": ["SBA loan", "small business", "7a", "business expansion", "catering"]},
    },
    {
        "title": "Case Study: Jumbo Mortgage for High-Value Home Purchase",
        "text": (
            "Profile: Dr. Alex Kim, 44, physician earning $450,000. Purchasing a $1.2M home, planning "
            "20% down ($240,000). Loan amount: $960,000 — well above the $766,550 conforming limit.\n\n"
            "Jumbo loan analysis: Jumbo rates are currently 6.75–7.25% for well-qualified borrowers. "
            "Dr. Kim's credit score (790), stable income, and 20% down make him highly qualified. "
            "Monthly P&I at 7.0% / 30-year: $6,391. Total monthly with taxes/insurance/HOA: ~$8,500. "
            "DTI check: $8,500 / ($450,000 / 12) = 22.7% — strong. Options: (1) 30-year fixed jumbo "
            "at 7.0%. (2) 10/1 ARM at 6.25% — saves $445/month for 10 years; appropriate if planning "
            "to pay off aggressively or sell within 10 years. (3) Bank portfolio programs from private "
            "banks often offer favorable jumbo terms for high-net-worth clients (relationship pricing). "
            "Recommendation: Shop private bank programs alongside traditional jumbo — relationship "
            "pricing can save 0.25–0.5% for clients with significant deposits or investment assets."
        ),
        "metadata": {"scenario_type": "Jumbo Mortgage", "tags": ["jumbo mortgage", "high-value home", "physician loan", "ARM vs fixed", "private bank"]},
    },
    {
        "title": "Case Study: VA Loan for Veteran Home Purchase",
        "text": (
            "Profile: Sergeant James Webb, 32, honorably discharged after 8 years of active service. "
            "Starting civilian career at $78,000. No down payment saved. Credit score: 680.\n\n"
            "VA loan eligibility: James has full VA entitlement. With no down payment requirement "
            "and no PMI, VA financing is clearly superior. At 680 credit score, VA rate approximately "
            "6.90% (slightly higher than prime VA rates due to score). Purchase price target: $320,000. "
            "Monthly P&I: $2,114. VA funding fee: 2.15% ($6,880, can be financed into loan). "
            "Compared to FHA: no monthly MIP saves $165/month; no down payment requirement saves $11,200 "
            "(3.5% FHA minimum). Recommendation: (1) Obtain VA Certificate of Eligibility (COE) through "
            "VA.gov or a VA-approved lender. (2) Work with a VA-experienced lender and real estate agent. "
            "(3) Consider improving credit score to 720+ before closing — each 20-point improvement "
            "can lower rate by 0.125–0.25% on a $320,000 loan."
        ),
        "metadata": {"scenario_type": "VA Loan", "tags": ["VA loan", "veteran", "military", "no down payment", "COE"]},
    },
    {
        "title": "Case Study: Reverse Mortgage for Asset-Rich, Cash-Poor Retiree",
        "text": (
            "Profile: Dorothy, 74, widowed homeowner. Home value: $480,000, no mortgage. Monthly Social "
            "Security: $1,650. Monthly expenses: $3,200. Savings: $42,000. Gap: $1,550/month.\n\n"
            "HECM analysis: At age 74, Dorothy qualifies for a significant HECM reverse mortgage. "
            "Principal limit (maximum borrowing): approximately $250,000–$280,000 based on age, home "
            "value, and current rates. Options: (1) Monthly tenure payments: approximately $900–$1,100/month "
            "for life — closes most of the income gap. (2) Line of credit: flexible, and the unused "
            "portion grows at the interest rate — creates an expanding reserve. (3) Combination. "
            "Key protections: federally insured; cannot owe more than home value; can remain in home "
            "for life as long as taxes and insurance are maintained. Upfront costs: ~$10,000–$15,000 "
            "(MIP, origination, closing costs). Required counseling with a HUD-approved counselor "
            "before proceeding — highly recommended to involve family in this decision."
        ),
        "metadata": {"scenario_type": "Reverse Mortgage", "tags": ["reverse mortgage", "HECM", "retiree", "home equity", "income gap"]},
    },
    {
        "title": "Case Study: Managing Multiple Student Loan Servicers After Graduation",
        "text": (
            "Profile: Tyler, 24, graduated with $92,000 in federal student loans across multiple "
            "Direct Loan servicers after several servicer transfers. Confused by multiple login "
            "portals, unsure of repayment options.\n\n"
            "Simplification strategy: (1) Consolidate all federal loans into a single Direct "
            "Consolidation Loan through StudentAid.gov — one servicer, one payment, one portal. "
            "Note: consolidation resets PSLF payment count (applies average weighted term), so "
            "evaluate carefully if pursuing PSLF. (2) Enroll in SAVE plan — at $55,000 starting "
            "salary, payment ≈ $192/month (versus $950+ on standard). (3) Enroll in autopay: "
            "0.25% rate reduction on federal loans. (4) Set annual income recertification calendar "
            "reminder. (5) If Tyler is NOT pursuing PSLF or IDR forgiveness, aggressive standard "
            "repayment on $92K may cost $62,000 in interest — consider refinancing private loans "
            "separately if any exist at lower rates (but never refinance federal loans to private "
            "if pursuing PSLF)."
        ),
        "metadata": {"scenario_type": "Student Loan Management", "tags": ["student loan consolidation", "servicer", "SAVE plan", "autopay", "IDR"]},
    },
    {
        "title": "Case Study: Credit Card Churning — Maximizing Rewards Responsibly",
        "text": (
            "Profile: Jennifer, 34, data analyst earning $110,000. Excellent credit (790 score), "
            "no credit card debt, pays in full monthly. Spending: $3,500/month. Interested in "
            "maximizing credit card rewards.\n\n"
            "Strategy: Jennifer is an ideal candidate for rewards optimization. (1) Core setup: "
            "Chase Sapphire Preferred ($95/year) for dining/travel at 3x; Chase Freedom Unlimited "
            "for 1.5x on everything else; Chase Freedom Flex for 5x rotating categories. "
            "(2) Annual sign-up bonus rotation: new card 1–2x/year for 60,000–100,000 point bonuses "
            "(minimum spend $3,000–$5,000 within 90 days — achieved naturally with existing spending). "
            "(3) Transfer partners: Chase Ultimate Rewards points transfer 1:1 to United, Southwest, "
            "Hyatt — extraordinary value for premium travel. Risk management: never spend beyond "
            "normal budget to chase bonuses; set autopay for full statement balance; cancel cards "
            "with annual fees before renewal if benefits don't justify cost. Estimated annual value: "
            "$1,200–$2,500 in travel rewards."
        ),
        "metadata": {"scenario_type": "Rewards Optimization", "tags": ["credit card rewards", "churning", "Chase", "travel points", "responsible use"]},
    },
]


def build_chunks():
    chunks = []
    for item in PRODUCTS:
        chunks.append({"content_type": "PRODUCT", "title": item["title"], "text": item["text"], "metadata": item["metadata"]})
    for item in FAQS:
        chunks.append({"content_type": "FAQ", "title": item["title"], "text": item["text"], "metadata": item["metadata"]})
    for item in MARKET_COMMENTARY:
        chunks.append({"content_type": "MARKET_COMMENTARY", "title": item["title"], "text": item["text"], "metadata": item["metadata"]})
    for item in CLIENT_SCENARIOS:
        chunks.append({"content_type": "CLIENT_SCENARIO", "title": item["title"], "text": item["text"], "metadata": item["metadata"]})
    return chunks


if __name__ == "__main__":
    import os as _os
    _os.makedirs(_os.path.dirname(OUTPUT_PATH), exist_ok=True)
    chunks = build_chunks()
    counts = {}
    for c in chunks:
        counts[c["content_type"]] = counts.get(c["content_type"], 0) + 1
    print("Chunk counts by content type:")
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")
    print(f"  TOTAL: {len(chunks)}")
    with open(OUTPUT_PATH, "w") as f:
        json.dump(chunks, f, indent=2)
    print(f"\nWrote {len(chunks)} chunks to {OUTPUT_PATH}")
