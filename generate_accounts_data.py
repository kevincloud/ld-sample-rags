"""
Generates ~130 demo text chunks for the Account Management RAG corpus.
Outputs: rag/data/accounts_chunks.json

Content types:
  PRODUCT           - account types and features
  FAQ               - common account management questions
  MARKET_COMMENTARY - trends in banking/accounts
  CLIENT_SCENARIO   - account management case studies
"""

import json
import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "data", "accounts_chunks.json")

PRODUCTS = [
    {
        "title": "Basic Checking Account",
        "text": (
            "A basic checking account is the foundation of everyday banking, used for deposits, bill payments, "
            "debit card purchases, ATM withdrawals, and check writing. Features vary by bank: some charge monthly "
            "maintenance fees ($5–$15) waivable with a minimum balance or direct deposit; others are fee-free. "
            "Most checking accounts include a debit card, mobile banking access, and overdraft options. "
            "Unlike savings accounts, checking accounts have no federal limit on the number of monthly "
            "transactions. FDIC insured up to $250,000 per depositor per institution. Best practice: "
            "maintain enough to cover monthly expenses plus a buffer; use direct deposit to waive fees; "
            "monitor the account weekly to catch unauthorized transactions or errors promptly."
        ),
        "metadata": {"product_type": "Checking", "tags": ["checking account", "debit card", "FDIC", "everyday banking", "direct deposit"]},
    },
    {
        "title": "High-Yield Savings Account (HYSA)",
        "text": (
            "A high-yield savings account (HYSA) offers significantly higher interest rates than traditional "
            "savings accounts. Online banks (Marcus by Goldman Sachs, Ally, SoFi, Marcus) typically offer "
            "4–5% APY versus 0.01–0.50% at traditional brick-and-mortar banks. HYSAs are FDIC insured and "
            "carry the same protections as any bank savings account. The rate is variable and will adjust "
            "when the Federal Reserve changes benchmark rates. Best uses: emergency funds (3–6 months of "
            "expenses), short-term savings goals (down payment, vacation), or parking cash awaiting investment. "
            "There are no monthly fees with most online HYSAs and no minimum balance requirements. "
            "Transfers to external accounts typically take 1–3 business days."
        ),
        "metadata": {"product_type": "Savings", "tags": ["HYSA", "high yield", "online bank", "emergency fund", "APY"]},
    },
    {
        "title": "Traditional Savings Account",
        "text": (
            "A traditional savings account at a brick-and-mortar bank provides a safe, FDIC-insured place "
            "to store money with easy in-branch access. Rates are typically much lower than online HYSAs — "
            "often 0.01–0.50% APY. Traditional savings accounts offer the convenience of same-branch "
            "cash transactions, teller assistance, and immediate fund availability without transfer delays. "
            "Monthly maintenance fees may apply if minimum balance requirements are not met. Historically, "
            "Regulation D limited savings account withdrawals to 6 per month, though this restriction was "
            "suspended by the Federal Reserve in 2020; many banks still enforce similar limits. "
            "Best for: customers who prefer in-branch banking, need frequent cash deposits, or want all "
            "accounts under one roof even at lower yields."
        ),
        "metadata": {"product_type": "Savings", "tags": ["savings account", "brick and mortar", "FDIC", "low yield", "traditional banking"]},
    },
    {
        "title": "Money Market Account (MMA)",
        "text": (
            "A money market account (MMA) combines features of checking and savings: it earns higher interest "
            "than a basic savings account (often competitive with HYSAs) while offering check-writing "
            "privileges and a debit card. MMAs typically require higher minimum balances ($1,000–$25,000+) "
            "to earn the best rates or avoid fees. They are FDIC insured up to $250,000. MMAs are "
            "appropriate for emergency funds that need to earn competitive interest while remaining "
            "immediately accessible via check or debit. Distinguish from money market funds (investment "
            "vehicles, not FDIC insured) — MMAs at banks are deposit accounts. When comparing to HYSAs: "
            "MMAs may offer check-writing that HYSAs typically don't, but HYSAs from online banks "
            "often offer the highest yields with the fewest restrictions."
        ),
        "metadata": {"product_type": "Savings", "tags": ["money market account", "MMA", "FDIC", "check writing", "high yield"]},
    },
    {
        "title": "Certificate of Deposit (CD)",
        "text": (
            "A CD is a time deposit that locks your funds at a fixed interest rate for a set term, ranging "
            "from 3 months to 5 years. In exchange for committing your funds, you receive a higher rate "
            "than a savings account. Current CD rates: 3-month (4.5–5.0%), 6-month (4.7–5.2%), 1-year "
            "(4.5–5.0%), 2-year (4.0–4.5%). CDs are FDIC insured. The key trade-off is illiquidity — "
            "early withdrawal penalties typically range from 3–12 months of interest depending on term. "
            "CD ladder strategy: divide savings across multiple CD terms (e.g., 1-year, 2-year, 3-year, "
            "4-year, 5-year) so that a portion matures annually, providing both yield and periodic "
            "liquidity. Bump-up CDs allow a one-time rate increase if rates rise; no-penalty CDs offer "
            "early withdrawal without penalty (at slightly lower rates)."
        ),
        "metadata": {"product_type": "CD", "tags": ["CD", "certificate of deposit", "fixed rate", "FDIC", "CD ladder"]},
    },
    {
        "title": "Interest Checking Account",
        "text": (
            "An interest-bearing checking account pays interest on the balance while maintaining full "
            "checking account functionality. Rates are typically lower than savings accounts (0.01–1.0% APY) "
            "but offer the convenience of unrestricted transactions with a small yield. Some rewards checking "
            "accounts (often at community banks and credit unions) pay 3–6% APY on balances up to a cap "
            "(typically $10,000–$25,000) if qualifying conditions are met each month: minimum number of "
            "debit card transactions, enrollment in e-statements, and an active direct deposit or ACH. "
            "These 'high-yield rewards checking' accounts can be excellent for emergency fund money "
            "that needs to be instantly accessible. The qualifying requirements can be burdensome for "
            "some users — evaluate whether you'll reliably meet them each month."
        ),
        "metadata": {"product_type": "Checking", "tags": ["interest checking", "rewards checking", "APY", "debit transactions", "high-yield checking"]},
    },
    {
        "title": "Joint Account",
        "text": (
            "A joint bank account is owned by two or more people, with all owners having equal rights to "
            "deposit, withdraw, and manage the account. Most joint accounts are structured as 'joint "
            "tenants with right of survivorship' (JTWROS) — upon one owner's death, the balance passes "
            "directly to the surviving owner(s) without going through probate. Joint accounts are common "
            "for spouses/partners, parents with minor children, and business partners. Each co-owner "
            "is individually FDIC insured up to $250,000 per co-owner per institution. Any owner can "
            "close the account or withdraw all funds without the other's consent — this creates legal "
            "and financial risk if the relationship sours. Adding a joint owner to an existing account "
            "typically requires the existing owner's presence and government-issued ID for the new owner."
        ),
        "metadata": {"product_type": "Account Structure", "tags": ["joint account", "JTWROS", "co-owner", "survivorship", "couples banking"]},
    },
    {
        "title": "Health Savings Account (HSA) — Banking Perspective",
        "text": (
            "An HSA is a tax-advantaged savings account exclusively for qualified medical expenses, "
            "available only to individuals enrolled in a High Deductible Health Plan (HDHP). From a "
            "banking perspective, HSAs function as a specialized savings or investment account: "
            "contributions are tax-deductible; earnings grow tax-free; withdrawals for qualified "
            "medical expenses are tax-free. 2024 contribution limits: $4,150 (individual), $8,300 "
            "(family). The funds roll over indefinitely — no 'use it or lose it.' HSA custodians "
            "(Fidelity HSA, Lively, HealthEquity, bank-administered HSAs) vary in investment options "
            "and fees. For banking customers, the HSA functions like a checking account for medical "
            "spending: debit card, online bill pay, and reimbursement for out-of-pocket expenses "
            "already paid. After age 65, withdrawals for any purpose are allowed (taxed as ordinary income)."
        ),
        "metadata": {"product_type": "Specialty Account", "tags": ["HSA", "health savings account", "HDHP", "tax advantaged", "medical expenses"]},
    },
    {
        "title": "Student Checking Account",
        "text": (
            "Student checking accounts are designed for high school and college students, offering "
            "features suited to limited income and developing financial habits. Common features: "
            "no monthly maintenance fee (for students up to age 24–26), no minimum balance requirement, "
            "mobile banking, and financial education tools. Major banks (Chase, Bank of America, Wells "
            "Fargo, TD Bank) all offer student-specific accounts. At age cutoff, accounts typically "
            "convert to standard checking (fees may apply). Best practices for student accounts: "
            "set up low-balance alerts to avoid overdrafts; use the bank's ATMs to avoid fees; "
            "enable direct deposit for payroll; avoid overdraft 'protection' services that charge $35 "
            "per transaction — opt-out and let transactions decline instead. Student accounts often "
            "automatically upgrade to a premium account when the student turns a certain age."
        ),
        "metadata": {"product_type": "Checking", "tags": ["student checking", "youth banking", "no fee", "college banking", "financial literacy"]},
    },
    {
        "title": "Business Checking Account",
        "text": (
            "A business checking account separates business finances from personal, which is essential "
            "for liability protection (especially for LLCs and corporations), tax preparation accuracy, "
            "and professional client interactions. Business accounts offer features not available in "
            "personal accounts: multiple signatories, payroll integration, merchant services, higher "
            "daily transaction limits, and cash deposit processing. Fees are typically higher than "
            "personal accounts: $15–$40/month, often waivable with minimum balances or transaction "
            "volume. Business accounts require an EIN (Employer Identification Number), business "
            "formation documents, and in-person account opening at most banks. Chase Business Complete "
            "Checking, Bank of America Business Advantage, and Novo (online, no monthly fee) are "
            "popular options. Online business banks (Mercury, Relay) offer no-fee modern interfaces "
            "with robust integrations."
        ),
        "metadata": {"product_type": "Business Account", "tags": ["business checking", "LLC", "EIN", "merchant services", "small business"]},
    },
    {
        "title": "Custodial Account (UTMA/UGMA)",
        "text": (
            "A custodial account (UTMA — Uniform Transfers to Minors Act, or UGMA — Uniform Gifts to "
            "Minors Act) is a brokerage or savings account opened by an adult for a minor. The adult "
            "acts as custodian and controls the account until the minor reaches the age of majority "
            "(18–21 depending on state). At that point, the minor gains full control with no restrictions. "
            "UTMA accounts can hold virtually any asset (cash, securities, real estate in some states); "
            "UGMA is limited to cash and securities. Tax treatment: earnings up to $1,300 are tax-free "
            "to the minor; the next $1,300 is taxed at the minor's rate; above $2,600 is taxed at the "
            "parent's rate ('kiddie tax'). Unlike 529 plans, funds can be used for anything — but this "
            "flexibility has less tax efficiency for education savings."
        ),
        "metadata": {"product_type": "Specialty Account", "tags": ["UTMA", "UGMA", "custodial account", "minor", "kiddie tax"]},
    },
    {
        "title": "Senior/Elder Banking Account",
        "text": (
            "Many banks offer accounts designed for customers aged 60–65 and older with features "
            "addressing common senior banking needs. Typical benefits: waived monthly fees regardless "
            "of balance, free checks, free money orders, no minimum balance, and free notary services. "
            "Some institutions offer dedicated senior banking specialists and elder financial abuse "
            "monitoring (flagging unusual transaction patterns). Important protections for seniors: "
            "designate a trusted contact person (TCP) — a person the bank can notify if they suspect "
            "financial exploitation, though the TPC cannot access accounts. Elder financial abuse is "
            "the most rapidly growing form of financial crime — over $3 billion annually stolen from "
            "seniors. Seniors should review account activity monthly, set up transaction alerts, "
            "and be extremely cautious about granting account access to family or caregivers."
        ),
        "metadata": {"product_type": "Specialty Account", "tags": ["senior banking", "elder banking", "financial abuse", "trusted contact", "fee waiver"]},
    },
    {
        "title": "Prepaid Debit Card / Reloadable Card",
        "text": (
            "Prepaid debit cards function like a debit card linked to a balance loaded onto the card "
            "rather than a bank account. They are available for purchase at retail stores and online. "
            "Major brands include NetSpend, Green Dot, and American Express Serve. FDIC insurance "
            "varies by product and card issuer — many prepaid cards are FDIC insured if certain "
            "conditions are met. Fees can be substantial: activation fees, monthly fees ($5–$10), "
            "reload fees, ATM fees, and inactivity fees. Prepaid cards serve populations without "
            "traditional bank accounts (unbanked households) but are typically more expensive than "
            "a basic checking account. Better alternatives for the unbanked: second-chance checking "
            "accounts, credit union accounts, and Bank On certified accounts (fee-free, feature-rich "
            "accounts available at participating banks and credit unions)."
        ),
        "metadata": {"product_type": "Alternative Banking", "tags": ["prepaid card", "unbanked", "debit card", "NetSpend", "Green Dot", "fees"]},
    },
    {
        "title": "Individual Retirement Account (IRA) — Banking Held",
        "text": (
            "Banks and credit unions offer IRA CDs and IRA savings accounts, providing FDIC-insured "
            "retirement savings options. A traditional IRA at a bank holds CDs or savings accounts "
            "rather than securities — providing capital preservation with no market risk but limited "
            "growth potential. IRA CDs lock in a fixed rate for the CD term within the IRA wrapper. "
            "These are appropriate for ultra-conservative investors near or in retirement who prioritize "
            "capital preservation over growth. Contribution limits: $7,000/year ($8,000 for 50+) in 2024. "
            "The trade-off vs. brokerage IRA: bank IRAs earn 4–5% currently (competitive in this rate "
            "environment) but historically underperform equity-invested IRAs over long periods. "
            "Best for the final 3–5 years before retirement when capital preservation is paramount."
        ),
        "metadata": {"product_type": "Retirement Account", "tags": ["IRA", "IRA CD", "retirement savings", "FDIC", "capital preservation"]},
    },
    {
        "title": "Overdraft Protection and Overdraft Lines of Credit",
        "text": (
            "When a transaction exceeds the available checking account balance, three things can happen: "
            "(1) Standard overdraft (opt-in required for debit/ATM): bank covers the transaction and "
            "charges an overdraft fee ($25–$35 per item). Many banks now offer no-fee overdraft up to "
            "a small amount ($10–$50). (2) Overdraft transfer: bank automatically transfers from a "
            "linked savings account. May have a per-transfer fee but is typically much cheaper than "
            "overdraft fees. (3) Overdraft line of credit: a pre-approved credit line linked to checking; "
            "interest accrues on amounts borrowed. (4) Decline: without coverage, the transaction is "
            "declined — safest option as it prevents debt but may cause embarrassment or returned "
            "payment fees from merchants. Best practice: opt out of standard overdraft for debit cards "
            "(transactions will simply decline), link a savings account for transfer protection, and "
            "set up low-balance alerts."
        ),
        "metadata": {"product_type": "Account Feature", "tags": ["overdraft", "overdraft protection", "NSF", "linked savings", "opt-out"]},
    },
    {
        "title": "Sweep Account",
        "text": (
            "A sweep account automatically 'sweeps' excess funds above a set threshold from a checking "
            "account into a higher-yielding account (savings, money market fund, or investment account) "
            "at the end of each business day, and pulls funds back when needed. This maximizes yield "
            "on idle cash without manual transfers. Business sweep accounts commonly move excess cash "
            "into Treasury funds or money market accounts overnight. For retail customers, sweep "
            "features are less common but available at some banks and brokerages — excess cash in a "
            "brokerage account may automatically sweep into a money market fund earning 4–5%. "
            "Sweep accounts are most valuable for businesses or high-balance individuals with large "
            "idle cash balances. The automation eliminates the need to manually move funds, ensuring "
            "no yield is left on the table."
        ),
        "metadata": {"product_type": "Account Feature", "tags": ["sweep account", "cash management", "money market", "idle cash", "business banking"]},
    },
    {
        "title": "Trust Account",
        "text": (
            "A bank trust account holds assets managed by a trustee for the benefit of a beneficiary "
            "according to the terms of a trust agreement. Banks with trust departments act as "
            "corporate trustees, managing assets and making distributions per the trust document. "
            "Revocable living trusts: the grantor maintains control during lifetime; trust assets "
            "avoid probate at death; the bank acts as trustee only after incapacity or death. "
            "Irrevocable trusts: assets are permanently transferred; useful for estate tax planning, "
            "Medicaid planning, and asset protection. Trust accounts are FDIC insured up to $250,000 "
            "per beneficiary (up to 5 beneficiaries = $1.25M coverage per owner per bank). "
            "Bank trust departments charge annual fees of 0.5–1.5% of assets. For trust accounts "
            "under $500,000, a directed trustee or self-directed trust may be more cost-effective."
        ),
        "metadata": {"product_type": "Specialty Account", "tags": ["trust account", "trustee", "revocable trust", "irrevocable trust", "estate planning"]},
    },
    {
        "title": "Brokered CD",
        "text": (
            "Brokered CDs are CDs purchased through a brokerage account (Fidelity, Schwab, Vanguard, "
            "TD Ameritrade) rather than directly from a bank. They offer several advantages over bank-direct "
            "CDs: (1) Higher yields — brokerages aggregate demand and negotiate better rates. (2) Secondary "
            "market liquidity — can be sold before maturity (at market price, which may be above or below "
            "par). (3) Multi-bank access — a single brokerage account can hold CDs from dozens of banks, "
            "each FDIC insured separately (up to $250,000 per bank). This makes it easy to maintain FDIC "
            "insurance on large cash balances. Risks: callable CDs (issuer can redeem early) may be "
            "called when rates fall. Non-callable CDs are preferable. FDIC insurance applies only to "
            "CDs from FDIC-insured banks — verify before purchasing."
        ),
        "metadata": {"product_type": "CD", "tags": ["brokered CD", "FDIC", "Fidelity", "Schwab", "secondary market", "multi-bank"]},
    },
    {
        "title": "Digital / Online-Only Banking Account",
        "text": (
            "Digital banks (neobanks) like Chime, Ally, Varo, Current, and Revolut operate entirely "
            "online with no physical branches. They typically offer: no monthly fees, no minimum balances, "
            "early direct deposit (2 days early), fee-free ATM access through networks, and competitive "
            "savings rates. Many provide features that traditional banks charge for: fee-free overdraft "
            "(Chime SpotMe), round-up savings, automatic savings tools, and real-time push notifications. "
            "Trade-offs: no in-branch cash deposits (some partner with retailers for cash deposits, often "
            "with a fee); limited product range (no mortgages, complex loans at the same institution); "
            "customer service is phone/chat only. For day-to-day banking, digital banks often provide "
            "superior value and user experience versus traditional banks, especially for fee-conscious "
            "customers."
        ),
        "metadata": {"product_type": "Digital Banking", "tags": ["neobank", "Chime", "Ally", "digital banking", "no fee", "online banking"]},
    },
    {
        "title": "529 Education Savings Account — Banking Perspective",
        "text": (
            "A 529 plan is a state-sponsored, tax-advantaged savings account for education expenses. "
            "From a banking/account management perspective, 529 plans function as investment accounts "
            "with account owner controls, beneficiary designations, and contribution/withdrawal management. "
            "Account owners choose investment options (typically age-based or fixed allocation funds). "
            "Contributions: no federal deduction, but 34+ states offer state income tax deductions. "
            "No income limits and no annual contribution limits (though gifts exceeding $18,000/year "
            "may have gift tax implications; 5-year superfunding allows $90,000 lump-sum contribution). "
            "Unused funds: can change beneficiary to another family member; since 2024, up to $35,000 "
            "can be rolled to a Roth IRA (lifetime limit). Account management: review asset allocation "
            "annually as beneficiary ages; update beneficiary if the original beneficiary won't use funds."
        ),
        "metadata": {"product_type": "Specialty Account", "tags": ["529", "education savings", "beneficiary", "superfunding", "Roth rollover"]},
    },
    {
        "title": "Second Chance Checking Account",
        "text": (
            "Second chance checking accounts are designed for individuals who have been denied traditional "
            "bank accounts due to negative history in ChexSystems or Early Warning Services (EWS). These "
            "are reporting agencies (like credit bureaus but for banking) where unpaid overdrafts, account "
            "abuse, or fraud are recorded. Second chance accounts typically come with no overdraft, "
            "limited features, and sometimes a monthly fee, but are FDIC insured and report positive "
            "behavior to ChexSystems. After 12 months of responsible use, many banks will upgrade to "
            "a standard checking account. Certified Bank On accounts (bankoncertification.org) are a "
            "high-quality option — low fees, core transaction features, no minimum balance. "
            "Credit unions often offer the best second-chance account terms. Clearing ChexSystems "
            "records requires disputing errors or waiting 5 years for negative items to age off."
        ),
        "metadata": {"product_type": "Checking", "tags": ["second chance", "ChexSystems", "unbanked", "Bank On", "banking access"]},
    },
    {
        "title": "FDIC Insurance — What It Covers and Its Limits",
        "text": (
            "FDIC (Federal Deposit Insurance Corporation) insurance protects depositors if an FDIC-insured "
            "bank fails. Coverage: $250,000 per depositor, per insured bank, per ownership category. "
            "Ownership categories include: single accounts, joint accounts ($500,000 per couple), "
            "retirement accounts (IRAs — $250,000 separately), trust accounts (per beneficiary), and "
            "business accounts. A depositor can have significantly more than $250,000 insured at one "
            "bank by using multiple ownership categories. FDIC insurance does NOT cover: investment "
            "products (stocks, bonds, mutual funds), even if sold at a bank; safe deposit box contents; "
            "annuities. Credit unions have equivalent coverage through NCUA (National Credit Union "
            "Administration). Since FDIC's creation in 1933, no depositor has ever lost a penny of "
            "insured deposits at an FDIC-insured bank."
        ),
        "metadata": {"product_type": "Account Protection", "tags": ["FDIC", "deposit insurance", "bank failure", "coverage limits", "ownership categories"]},
    },
    {
        "title": "Automated Savings Tools and Round-Up Features",
        "text": (
            "Automated savings features help customers save money without active effort. Round-up savings: "
            "each debit card purchase is rounded up to the nearest dollar, and the difference is transferred "
            "to savings (e.g., $3.75 purchase → $0.25 saved). Bank of America Keep the Change, Acorns, "
            "and Chime all offer this. Automated transfers: set recurring transfers from checking to "
            "savings on payday. Savings 'rules': apps like Qapital allow custom savings rules ("
            "'save $5 every time it rains,' 'save 10% of every deposit'). Round-up savings typically "
            "accumulate $150–$400/year — meaningful for small savers but not sufficient as a primary "
            "savings strategy. The behavioral impact is significant: the automation removes the decision "
            "point, making saving the default behavior. Even small automated savings create a habit and "
            "build the emergency fund foundation."
        ),
        "metadata": {"product_type": "Account Feature", "tags": ["automated savings", "round-up", "behavioral finance", "Bank of America", "Chime", "savings habit"]},
    },
    {
        "title": "Safe Deposit Box",
        "text": (
            "A safe deposit box is a secure, locked container rented from a bank, stored in the bank's vault. "
            "Sizes range from 2x5 inches to 10x10 inches or larger. Annual rental fees typically range "
            "from $25 to $200+ depending on size and bank. Contents are NOT FDIC insured — the bank is "
            "not liable for loss or damage unless due to bank negligence. Contents are also not covered "
            "by homeowner's insurance in most policies (a rider may be added). Best items for safe "
            "deposit boxes: original documents (birth certificates, Social Security cards, passports, "
            "property deeds, vehicle titles), jewelry, irreplaceable collectibles, physical cash for "
            "emergencies. Not appropriate for: items needed in an emergency (the box is inaccessible "
            "when the bank is closed), original will (executor must access after death), or items you "
            "need regular access to."
        ),
        "metadata": {"product_type": "Account Service", "tags": ["safe deposit box", "secure storage", "documents", "not FDIC insured", "bank vault"]},
    },
]

FAQS = [
    {
        "title": "How do I open a bank account?",
        "text": (
            "Opening a bank account requires: government-issued photo ID (driver's license, state ID, "
            "or passport), Social Security Number (or ITIN for non-citizens), initial deposit (varies "
            "by account — many online banks require $0), and a mailing address. In-branch opening: "
            "bring your ID and any required opening deposit. Most banks can open a new account in "
            "15–30 minutes. Online account opening: complete the application digitally, upload or "
            "photograph your ID, and fund via ACH transfer from another account. Instant approval "
            "is common for online banks. If you are denied due to ChexSystems history, ask about "
            "second-chance accounts or consider a credit union. Noncitizens with ITINs (Individual "
            "Taxpayer Identification Numbers) can open accounts at most major banks — bring ITIN, "
            "passport, and secondary ID."
        ),
        "metadata": {"category": "Account Opening", "tags": ["open account", "ID", "ChexSystems", "online account", "account opening requirements"]},
    },
    {
        "title": "What is the difference between available balance and actual balance?",
        "text": (
            "Your account has two balance figures: (1) Actual balance (ledger balance): the total of all "
            "posted transactions as of the end of the previous business day. (2) Available balance: "
            "the amount actually available for immediate use — the actual balance minus any holds on "
            "recent deposits or pending transactions. A hold reduces available balance before a deposit "
            "has fully cleared. A pending debit (card swipe at a restaurant that hasn't settled) "
            "reduces available balance immediately but may not yet be in the ledger balance. "
            "Always use available balance as your spending reference — making transactions based on "
            "actual balance while holds are outstanding can result in overdrafts. Most mobile banking "
            "apps clearly show both figures. Deposit holds typically last 1–2 business days for "
            "standard items, and up to 9 business days for new accounts or large deposits."
        ),
        "metadata": {"category": "Account Management", "tags": ["available balance", "ledger balance", "holds", "pending transactions", "overdraft"]},
    },
    {
        "title": "How long does a check deposit take to clear?",
        "text": (
            "Under the Expedited Funds Availability Act (EFAA), federal Reg CC rules govern when banks "
            "must make deposited funds available: (1) Cash and electronic payments: available next "
            "business day. (2) Government, cashier's, and certified checks: first $5,525 available "
            "next business day (full amount if deposited at the issuing bank). (3) Payroll checks and "
            "checks from the same bank: typically available next business day. (4) Personal and "
            "business checks: first $225 available same day, remainder by 2nd business day for "
            "established customers. Banks may place extended holds (up to 9 business days) on "
            "large deposits, new accounts, accounts with overdraft history, or when fraud is suspected. "
            "Mobile deposits may have longer hold periods than in-person deposits. The bank must notify "
            "you of any hold and provide the date funds will be available."
        ),
        "metadata": {"category": "Deposits", "tags": ["check hold", "funds availability", "Reg CC", "mobile deposit", "check clearing"]},
    },
    {
        "title": "How do I dispute a transaction on my account?",
        "text": (
            "To dispute an unauthorized or incorrect transaction: (1) Contact your bank immediately — "
            "by phone, in-branch, or through the mobile app's dispute function. For debit card "
            "transactions, the sooner you report, the better your protection. (2) For debit card "
            "fraud, federal Regulation E limits your liability: $0 if reported before any unauthorized "
            "use; $50 if reported within 2 business days; up to $500 if reported within 60 days of "
            "the statement; unlimited liability after 60 days. (3) For credit card disputes, the "
            "Fair Credit Billing Act (FCBA) provides strong protections — disputes must be filed "
            "within 60 days of the statement, and you're not required to pay the disputed amount "
            "while under investigation. (4) Keep records of all dispute communications. The bank "
            "must investigate and resolve within 10 business days (may extend to 45 days while "
            "crediting your account provisionally)."
        ),
        "metadata": {"category": "Dispute Resolution", "tags": ["dispute transaction", "unauthorized charge", "Regulation E", "FCBA", "fraud protection"]},
    },
    {
        "title": "What happens if my debit card is lost or stolen?",
        "text": (
            "Report a lost or stolen debit card to your bank immediately — by phone (24/7 fraud line) "
            "or through the mobile app (most apps allow instant card lock). The bank will cancel the "
            "card and issue a replacement (typically 3–7 business days; expedited shipping available). "
            "Liability protection: under Regulation E, if you report before unauthorized transactions "
            "occur, you have zero liability. If you report within 2 business days of learning the card "
            "is missing: maximum $50 liability. 2–60 days: maximum $500. After 60 days: potentially "
            "unlimited. Most banks offer $0 fraud liability policies that go beyond the legal "
            "minimums. While waiting for a replacement, use a different linked card, digital wallet "
            "(Apple Pay, Google Pay — uses tokenized virtual card number), or withdraw cash. "
            "Change your PIN and review recent transactions for any unauthorized activity."
        ),
        "metadata": {"category": "Card Management", "tags": ["lost card", "stolen card", "Regulation E", "fraud liability", "card replacement"]},
    },
    {
        "title": "What are bank account fees and how do I avoid them?",
        "text": (
            "Common bank fees include: Monthly maintenance fee ($5–$15): waived with direct deposit, "
            "minimum balance, or by choosing a no-fee account. Overdraft fee ($25–$35/item): opt-out "
            "of overdraft for debit; set up low-balance alerts; link a savings account for overdraft "
            "transfer. Out-of-network ATM fee ($2–$5 from your bank + operator fee): use in-network "
            "ATMs or choose a bank that reimburses ATM fees (Ally, Schwab, Charles Schwab Bank). "
            "Paper statement fee ($2–$5/month): enroll in e-statements. Wire transfer fee ($15–$30 "
            "outgoing): use ACH transfers for non-urgent payments. Safe deposit box fees: some accounts "
            "include free box access. Returned check fee ($25–$35): verify funds before writing checks. "
            "The most effective fee elimination strategy: choose an online bank or credit union with "
            "no monthly fee, enable direct deposit, and opt out of all optional overdraft services."
        ),
        "metadata": {"category": "Account Fees", "tags": ["bank fees", "monthly fee", "overdraft fee", "ATM fee", "fee avoidance"]},
    },
    {
        "title": "How do I set up direct deposit?",
        "text": (
            "Direct deposit allows your employer (or government benefit agency) to electronically deposit "
            "your paycheck directly into your bank account. To set up: (1) Obtain your bank's routing "
            "number and your account number — found on a check or in the mobile app/online banking. "
            "(2) Complete your employer's direct deposit authorization form — typically available through "
            "HR or the payroll portal. Enter your bank's routing number and your full account number. "
            "(3) Specify whether to deposit the full amount or split between accounts (e.g., $500 to "
            "savings, remainder to checking). Processing typically takes 1–2 pay cycles. Many benefits "
            "of direct deposit: faster than paper check, often available 1–2 days early at digital banks, "
            "triggers fee waivers on many accounts, and eliminates the risk of lost/stolen paper checks. "
            "For government benefits (Social Security, tax refunds), use the Treasury Direct form."
        ),
        "metadata": {"category": "Account Setup", "tags": ["direct deposit", "routing number", "account number", "payroll", "electronic deposit"]},
    },
    {
        "title": "What is a routing number and when do I need it?",
        "text": (
            "A bank routing number (ABA routing number) is a 9-digit code that identifies the financial "
            "institution where your account is held. It's used to direct electronic transfers to the "
            "correct bank. Where to find it: on the bottom-left of a check (the 9-digit number before "
            "your account number), in your online banking/mobile app, or on the bank's website. "
            "When you need your routing number: setting up direct deposit, linking external bank accounts, "
            "setting up ACH transfers, receiving wire transfers, filing taxes for direct deposit of refund, "
            "and authorizing electronic bill payments. Note: some banks have different routing numbers "
            "for wire transfers versus ACH transactions — verify which is needed. Foreign wire transfers "
            "also require a SWIFT/BIC code, not just a routing number."
        ),
        "metadata": {"category": "Account Basics", "tags": ["routing number", "ABA", "ACH", "wire transfer", "check"]},
    },
    {
        "title": "How do I transfer money between my own accounts?",
        "text": (
            "Transferring between your own accounts within the same bank: instant or same-day, typically "
            "free, done through online banking or mobile app. Transferring between accounts at different "
            "banks: (1) ACH transfer — link the external account (provide routing and account numbers, "
            "verify with micro-deposits), then initiate a transfer. Takes 1–3 business days, typically free. "
            "(2) Wire transfer — faster (same-day) but charges fees ($15–$30 outgoing). Use for large, "
            "time-sensitive transfers. (3) Zelle — for transfers to other people (not other personal "
            "accounts), instant and free. (4) Some banks offer instant transfers to linked external "
            "accounts for a small fee ($0.25–$10 depending on amount). Best practice: for recurring "
            "transfers (savings automation), set up a recurring ACH from checking to savings. Keep "
            "both account routing/account numbers in a secure location for future use."
        ),
        "metadata": {"category": "Transfers", "tags": ["account transfer", "ACH", "wire transfer", "external account", "linked account"]},
    },
    {
        "title": "How do I close a bank account?",
        "text": (
            "Before closing an account: (1) Update all direct deposits and automatic payments to a new "
            "account — list every payee and update them first. (2) Allow all pending transactions to "
            "clear — outstanding checks, scheduled payments, and ACH pulls can still hit the account "
            "after you close it. (3) Transfer all remaining funds. (4) To close: call customer service, "
            "visit a branch, or use online account closing (available at some banks). You'll need to "
            "provide ID and confirm your identity. Many banks will attempt to retain you — you're not "
            "obligated to provide a reason. If there's a remaining balance, request a check. "
            "Keep records of the account closing confirmation. If you simply stop using an account "
            "without formally closing it, dormancy fees may apply, and the account may eventually "
            "escheat (be turned over) to the state as unclaimed property."
        ),
        "metadata": {"category": "Account Management", "tags": ["close account", "account closure", "direct deposit update", "escheat", "automatic payments"]},
    },
    {
        "title": "What is ChexSystems and how does it affect me?",
        "text": (
            "ChexSystems is a consumer reporting agency (similar to a credit bureau, but for banking) "
            "that tracks negative banking history: unpaid overdrafts, returned checks, suspected fraud, "
            "and forced account closures. About 80% of banks check ChexSystems before opening new "
            "accounts. A negative ChexSystems record can prevent you from opening traditional bank "
            "accounts for up to 5 years (the maximum retention period). You are entitled to a free "
            "ChexSystems report annually (request at ChexSystems.com) and can dispute inaccurate "
            "information under the Fair Credit Reporting Act. To clear a record: pay outstanding "
            "balances owed to previous banks (may be negotiated); dispute errors; or request 'pay "
            "for delete' (the original bank removes the record upon settlement, though this isn't "
            "always granted). While negative records remain, second-chance accounts and Bank On "
            "certified accounts provide banking access."
        ),
        "metadata": {"category": "Banking Access", "tags": ["ChexSystems", "negative banking history", "second chance", "account denial", "consumer report"]},
    },
    {
        "title": "What is a debit card vs. a credit card?",
        "text": (
            "A debit card is linked directly to your checking account — when you use it, funds are "
            "immediately drawn from your balance. It uses your own money with no borrowing. "
            "A credit card is a revolving line of credit — you borrow from the issuer when making "
            "purchases, with the obligation to repay. If paid in full monthly, no interest is charged. "
            "Key differences: (1) Fraud protection: credit cards have stronger protections — under "
            "the Fair Credit Billing Act, liability is limited to $50 (most issuers offer $0 liability); "
            "debit card protections under Reg E are time-dependent and slightly weaker for delayed "
            "reporting. (2) Rewards: credit cards offer cash back, points, miles; most debit cards "
            "do not. (3) Credit building: credit card use is reported to bureaus; debit card use is not. "
            "(4) Spending control: debit cards prevent overspending beyond your balance; credit cards "
            "can facilitate overspending if not managed carefully."
        ),
        "metadata": {"category": "Account Basics", "tags": ["debit card", "credit card", "fraud protection", "Reg E", "credit building"]},
    },
    {
        "title": "How do I order checks and what are they used for?",
        "text": (
            "Personal checks are physical payment instruments that direct your bank to pay a specified "
            "amount to a named payee from your account. To order checks: contact your bank directly "
            "(often at a discount vs. check printing services), or use independent check printers "
            "(Checks Unlimited, Current, Costco checks) which are often cheaper and identical in "
            "function. Required information on checks: your name/address, bank routing number, "
            "account number. Checks are used for: rent payments (many landlords require checks), "
            "paying contractors, sending gifts, paying for services from vendors who don't accept "
            "cards, and any situation requiring a paper trail. Important check safety: never pre-sign "
            "blank checks; use gel ink pens (harder to wash); mail checks to trusted parties only; "
            "voided checks (for direct deposit setup) should be clearly marked 'VOID' in large letters "
            "across the check."
        ),
        "metadata": {"category": "Account Services", "tags": ["checks", "personal checks", "order checks", "voided check", "check safety"]},
    },
    {
        "title": "What is a certified check vs. a cashier's check?",
        "text": (
            "Both certified checks and cashier's checks are considered 'guaranteed funds' — the bank "
            "certifies that the funds are available, making them more trusted than personal checks. "
            "Certified check: the bank verifies that the account has sufficient funds and sets those "
            "funds aside (freezes them) to guarantee payment. The check is drawn on the customer's "
            "account. Cashier's check: the bank draws the check on its own funds — the bank is the "
            "payer, not the customer. Generally considered slightly more secure. Fees: $8–$15 per item "
            "at most banks; often free for premium account holders. Both are required for real estate "
            "closings, vehicle purchases, and other large transactions where personal checks aren't "
            "accepted. Beware of cashier's check scams: fraudulent cashier's checks are commonly used "
            "in overpayment scams — wait for funds to fully clear before releasing goods/services."
        ),
        "metadata": {"category": "Account Services", "tags": ["certified check", "cashier's check", "guaranteed funds", "real estate closing", "check scam"]},
    },
    {
        "title": "How does mobile check deposit work?",
        "text": (
            "Mobile check deposit allows you to deposit a check by photographing it with your smartphone "
            "through your bank's mobile app — no branch visit required. Process: open the app, select "
            "deposit, enter the amount, photograph the front and back of the check (endorse the back: "
            "signature + 'For Mobile Deposit Only'), and submit. Limits: most banks have daily and "
            "monthly limits for mobile deposit (typically $2,500–$10,000/day; higher for established "
            "accounts). Hold times: first $225 typically available immediately; remainder on next "
            "business day for established accounts; longer holds for large checks or new accounts. "
            "After submission: retain the physical check for 14–30 days until the deposit confirms, "
            "then shred or securely destroy it. Do NOT deposit the same check twice — this is considered "
            "check fraud. Sign 'For Mobile Deposit Only' to prevent the check from being re-deposited "
            "at a different institution."
        ),
        "metadata": {"category": "Digital Banking", "tags": ["mobile deposit", "remote deposit capture", "check deposit", "holds", "mobile banking"]},
    },
    {
        "title": "What should I do if I suspect fraudulent activity on my account?",
        "text": (
            "If you suspect fraud on your account: (1) Contact your bank immediately — call the number "
            "on the back of your card or the bank's 24/7 fraud hotline. Do not use phone numbers "
            "provided in suspicious emails or texts. (2) Ask the bank to freeze or lock your account "
            "and issue new cards with new numbers. (3) Review all recent transactions and identify "
            "all unauthorized items — report each one explicitly. (4) Change your online banking "
            "password, PIN, and any shared passwords. Enable two-factor authentication. (5) File "
            "a police report for significant fraud — your bank may require this for large claims. "
            "(6) Consider placing a credit freeze at all three bureaus if account information may "
            "have been compromised. (7) File a report with the FTC at IdentityTheft.gov for identity "
            "theft-related fraud. Banks must resolve most Regulation E complaints within 10 business "
            "days (or 45 days with provisional credit)."
        ),
        "metadata": {"category": "Security", "tags": ["fraud", "account compromise", "reporting fraud", "freeze account", "identity theft"]},
    },
    {
        "title": "What are money market accounts vs. money market funds?",
        "text": (
            "Money market account (MMA): a bank deposit account, FDIC insured, earns competitive interest, "
            "may include check-writing and debit card access. Rate is variable. Account balance is "
            "protected against loss. A bank deposit product, not an investment. "
            "Money market fund: a mutual fund that invests in short-term, high-quality debt securities "
            "(Treasury bills, commercial paper). NOT FDIC insured. Aims to maintain a $1.00 NAV "
            "(net asset value) but there's a theoretical risk of 'breaking the buck' (NAV falls below $1). "
            "Offered by investment companies (Vanguard, Fidelity, Schwab). Returns are generally "
            "similar to or slightly higher than bank MMAs. Available within brokerage accounts "
            "as a cash sweep vehicle. The distinction matters for safety: for FDIC protection, use "
            "a bank MMA. For potentially slightly higher yield in a brokerage account, money market "
            "funds are effective and extremely safe in practice."
        ),
        "metadata": {"category": "Account Types", "tags": ["money market account", "money market fund", "FDIC", "brokerage", "NAV"]},
    },
    {
        "title": "How do I add or remove an authorized user on my account?",
        "text": (
            "An authorized user (or signer) can make transactions on your account but generally has no "
            "ownership rights. To add: contact your bank by phone, in-branch, or online. You'll need "
            "the person's name and typically their Social Security Number (for identity verification). "
            "Authorized users receive their own debit card with their name. To remove: contact the bank "
            "directly; request cancellation of the authorized user's card. The primary account holder "
            "retains full control and responsibility. For joint accounts (full ownership), removal is "
            "more complex — in most states, both owners must agree to remove a joint owner, or the "
            "account must be closed and reopened. Authorized users are different from joint owners: "
            "authorized users cannot close the account, apply for overdraft, or make account changes — "
            "joint owners have full rights equal to the original owner."
        ),
        "metadata": {"category": "Account Management", "tags": ["authorized user", "joint account", "account access", "remove signer", "account holder"]},
    },
    {
        "title": "What is a 'hold' on a deposited check and how long does it last?",
        "text": (
            "A hold is a temporary restriction on deposited funds while the bank verifies the check will "
            "clear. Federal Regulation CC governs maximum hold periods. Situations that extend holds: "
            "(1) New account (open less than 30 days): up to 9 business days. (2) Large deposits "
            "(over $5,525): the amount above $5,525 may be held up to 7 business days. (3) Redeposited "
            "checks (previously returned). (4) Accounts with frequent overdrafts. (5) Reasonable doubt "
            "about collectability. The bank must provide written or electronic notice of any hold "
            "exceeding standard timeframes. Strategies to reduce holds: establish an account history "
            "before large deposits; visit a branch for large checks (tellers can sometimes reduce holds); "
            "use wire transfers for large, time-sensitive amounts; use cashier's checks for large real "
            "estate or vehicle transactions (first $5,525 next-day availability)."
        ),
        "metadata": {"category": "Deposits", "tags": ["check hold", "Regulation CC", "funds availability", "large deposit", "new account"]},
    },
    {
        "title": "What is a beneficiary designation on a bank account?",
        "text": (
            "A bank account beneficiary designation names who will receive the account balance upon the "
            "account owner's death. Accounts with beneficiaries designated are called POD (Payable on "
            "Death) or ITF (In Trust For) accounts. The designated beneficiary can claim the funds "
            "directly from the bank after the owner's death by presenting a death certificate and "
            "identification — bypassing probate entirely. This is a critical estate planning tool for "
            "bank accounts. Without a beneficiary: the account goes through probate (court-supervised "
            "distribution), which takes months and costs money. Keep beneficiary designations current — "
            "update after marriage, divorce, death of a named beneficiary, or birth of a child. "
            "You can name multiple beneficiaries with percentages, and contingent beneficiaries as a "
            "backup if the primary predeceases you. Review annually alongside your estate plan."
        ),
        "metadata": {"category": "Estate Planning", "tags": ["beneficiary", "POD", "payable on death", "probate", "estate planning"]},
    },
    {
        "title": "How do I protect my online banking account from fraud?",
        "text": (
            "Online banking security best practices: (1) Use a unique, strong password — at least 12 "
            "characters with a mix of letters, numbers, and symbols. Use a password manager "
            "(Bitwarden, 1Password). (2) Enable two-factor authentication (2FA) — SMS code, authenticator "
            "app, or biometric. Authenticator apps (Google Authenticator, Authy) are more secure than SMS. "
            "(3) Never click links in unsolicited emails or texts claiming to be your bank — go directly "
            "to the bank's website or app. (4) Only access banking on secure, private networks — avoid "
            "public Wi-Fi; use a VPN when necessary. (5) Enable login and transaction alerts. (6) "
            "Keep your devices and apps updated. (7) Log out of banking sessions when done. (8) "
            "Regularly review account activity. Bank impersonation scams are increasingly common — "
            "legitimate banks will never call asking for your password, OTP code, or to transfer "
            "funds to a 'safe account.'"
        ),
        "metadata": {"category": "Security", "tags": ["online banking security", "2FA", "phishing", "password", "bank impersonation"]},
    },
    {
        "title": "What is a wire transfer vs. ACH transfer?",
        "text": (
            "Wire transfer: an electronic transfer of funds through a network (Fedwire or SWIFT for "
            "international). Characteristics: same-day or next-day settlement, irrevocable (cannot "
            "be recalled once processed), fees of $15–$50 outgoing, faster and used for large/time-sensitive "
            "amounts. Best for: real estate closings, large business payments, international transfers. "
            "ACH (Automated Clearing House) transfer: processed in batches through the ACH network. "
            "Characteristics: 1–3 business days standard, some same-day ACH available, typically free "
            "or low-cost, can be reversed in certain cases. Best for: direct deposit, bill payments, "
            "regular bank-to-bank transfers, payroll. Key security difference: wire transfers are "
            "essentially irreversible and are the favored method for fraud/scams. Never wire funds "
            "to a party you don't fully trust and have independently verified. ACH has more reversibility "
            "protection."
        ),
        "metadata": {"category": "Transfers", "tags": ["wire transfer", "ACH", "Fedwire", "irrevocable", "transfer comparison"]},
    },
    {
        "title": "How do bank statements work and why should I review them?",
        "text": (
            "A bank statement is a monthly record of all account activity: deposits, withdrawals, "
            "fees, interest earned, and beginning/ending balances. Statements are available as "
            "paper mail (may have a fee) or electronically through online banking (free). "
            "Why review your statement: (1) Catch unauthorized transactions early — the sooner you "
            "report fraud under Reg E, the lower your liability. (2) Track spending patterns. "
            "(3) Identify recurring fees you may have forgotten about. (4) Verify that direct "
            "deposits, automatic payments, and expected checks have processed correctly. "
            "(5) Required for many financial applications (mortgage, rental, business loans). "
            "Best practice: review within 2–3 business days of statement generation — sets up the habit "
            "and catches issues while memory is fresh. At minimum, review monthly. Retain statements "
            "for 7 years for tax purposes (income records, deductible transactions)."
        ),
        "metadata": {"category": "Account Management", "tags": ["bank statement", "account review", "transaction monitoring", "Regulation E", "record keeping"]},
    },
    {
        "title": "What is NCUA insurance for credit unions?",
        "text": (
            "Credit union deposits are insured by the National Credit Union Administration (NCUA) through "
            "the National Credit Union Share Insurance Fund (NCUSIF) — the equivalent of FDIC insurance "
            "for credit unions. Coverage: $250,000 per member, per insured credit union, per account "
            "ownership category — identical to FDIC coverage amounts and categories. Coverage includes "
            "share drafts (checking), share savings (savings), money market shares, and CDs. All federal "
            "credit unions are required to have NCUA coverage. Most state-chartered credit unions "
            "also participate — verify by checking the NCUA's database or looking for the NCUA logo. "
            "Some state-chartered credit unions use private share insurance (ASI — American Share "
            "Insurance) instead of NCUA — this provides coverage but is not backed by the U.S. "
            "government. Since 1970, no insured credit union depositor has ever lost insured funds."
        ),
        "metadata": {"category": "Account Protection", "tags": ["NCUA", "credit union", "share insurance", "deposit insurance", "coverage"]},
    },
    {
        "title": "How do I change my address on a bank account?",
        "text": (
            "Updating your address with your bank is straightforward but important — failure to update "
            "can result in missed statements, tax documents (1099s), and replacement cards going to the "
            "wrong address. Methods to update: (1) Online banking: log in, go to Profile or Settings, "
            "update address. Most banks allow this with standard security verification. (2) Mobile app: "
            "similar process. (3) Phone: call customer service; you'll need to verify your identity. "
            "(4) Branch: in-person with government ID. Update all accounts at the same institution at "
            "once — each account (checking, savings, CDs, loans) may require separate updates at some "
            "banks. Also update: direct deposit with your employer (requires payroll form update), "
            "automatic payment vendors, the IRS (Form 8822 or on next tax return), state tax agencies, "
            "Social Security Administration, and the U.S. Postal Service."
        ),
        "metadata": {"category": "Account Management", "tags": ["address change", "account update", "mailing address", "online banking", "IRS notification"]},
    },
    {
        "title": "What is a money order and when should I use one?",
        "text": (
            "A money order is a prepaid payment instrument purchased for a specific amount, functioning "
            "like a guaranteed check. Sold by: banks and credit unions (typically $5–$10 fee), post "
            "offices (USPS, up to $1,000, $1.75–$2.20 fee), grocery stores, convenience stores, and "
            "Walmart (up to $1,000, $0.88 fee). Money orders are useful when: the recipient doesn't "
            "accept personal checks, you don't have a bank account, or you want to avoid sharing your "
            "bank account information. Safer than cash for mail payments. Limit per money order is "
            "typically $500–$1,000 (purchase multiples for larger amounts). Always keep your receipt — "
            "the receipt number allows you to track or replace a lost/stolen money order. Never purchase "
            "a money order to pay someone who says cash won't work — this is a common scam signal."
        ),
        "metadata": {"category": "Account Services", "tags": ["money order", "USPS", "payment instrument", "no bank account", "prepaid"]},
    },
    {
        "title": "How do I set up automatic bill pay?",
        "text": (
            "Automatic bill pay allows scheduled payments to be sent from your checking account without "
            "manual action each month. Two methods: (1) Bank-side bill pay: set up through your bank's "
            "online/mobile bill pay system. The bank sends a check or ACH to the payee. You control "
            "timing and amounts; easy to cancel from one place. (2) Biller-side autopay: the biller "
            "(utility, lender, insurer) pulls the payment from your account on the due date. Convenient "
            "but requires updating each biller when accounts change. Best practices: (1) Set up e-alerts "
            "for auto-pay confirmations. (2) Maintain a buffer balance above the auto-pay total. "
            "(3) Review auto-pay amounts annually — variable bills (utilities) may change. "
            "(4) When changing banks, update all autopays before closing the old account. "
            "Auto-pay discounts: many lenders offer 0.25% rate discount for enrollment."
        ),
        "metadata": {"category": "Account Management", "tags": ["automatic bill pay", "ACH", "autopay", "scheduled payments", "online banking"]},
    },
    {
        "title": "What is Zelle and how is it different from Venmo?",
        "text": (
            "Zelle is a bank-backed peer-to-peer payment service integrated directly into most major "
            "bank apps (Chase, Bank of America, Wells Fargo, and 1,700+ banks/credit unions). Transfers "
            "are instant and free, moving funds directly between U.S. bank accounts. Venmo (owned by "
            "PayPal), CashApp, and PayPal are separate apps that hold a balance within their platform "
            "before transfer to a bank. Key differences: (1) Zelle: instant bank-to-bank, no app "
            "balance, integrated in banking apps, no fees. (2) Venmo/CashApp: holds an in-app "
            "balance (not FDIC insured while held in app), social features, small fees for instant "
            "bank transfer (1.75%). (3) Security: ALL are for trusted contacts only — none offer buyer "
            "protection for purchases; scams are rampant. Never send Zelle/Venmo to strangers. "
            "Zelle specifically: transfers are irrevocable once sent; banks have limited ability to "
            "reverse payments even in clear fraud cases."
        ),
        "metadata": {"category": "Digital Payments", "tags": ["Zelle", "Venmo", "P2P payments", "instant transfer", "bank integrated"]},
    },
    {
        "title": "How do I dispute a bank fee?",
        "text": (
            "Bank fees are often negotiable, especially for long-standing customers with good histories. "
            "To dispute or request a waiver: (1) Contact customer service (phone, chat, or in-branch). "
            "Be polite and specific: name the fee, date, and reason you believe it should be waived "
            "(e.g., first overdraft, held check that caused an overdraft, fee charged in error). "
            "(2) Reference your account tenure and relationship (length of time as a customer, "
            "other products held). (3) If denied by a front-line representative, ask to speak with a "
            "supervisor. (4) If still denied and you believe the fee is erroneous, file a complaint "
            "with the CFPB (consumerfinance.gov). Banks often waive one overdraft fee per year as a "
            "courtesy — this is industry practice though not required. Credit unions and community "
            "banks tend to be more flexible with fee waivers than large national banks. Document "
            "the date, time, and representative's name for each interaction."
        ),
        "metadata": {"category": "Dispute Resolution", "tags": ["fee waiver", "overdraft fee", "customer service", "CFPB complaint", "bank fees"]},
    },
]

MARKET_COMMENTARY = [
    {
        "title": "The Death of Free Checking? Fee Trends in Retail Banking",
        "text": (
            "The era of universally free checking accounts at large banks is largely over, though "
            "competitive pressure from online banks and credit unions has kept fees in check. Monthly "
            "maintenance fees at major banks average $12–$15, typically waivable with minimum balances "
            "($1,500–$5,000) or direct deposit. The practical impact: approximately 75% of checking "
            "account holders avoid monthly fees through qualifying activities. However, overdraft fee "
            "revenue remains significant — banks earned over $5 billion in overdraft fees in 2023, "
            "down from $15+ billion in 2018 as regulatory pressure and competition from neo-banks "
            "have pushed banks to reduce and cap fees. Several large banks (Capital One, Ally, "
            "Discover, Citibank) have eliminated overdraft fees entirely. Community banks and credit "
            "unions continue to offer more favorable fee structures than large national banks."
        ),
        "metadata": {"period": "2024-2025", "topic": "Banking Fees", "tags": ["checking fees", "overdraft fees", "fee trends", "online banks", "consumer banking"]},
    },
    {
        "title": "The High-Yield Savings Account Revolution",
        "text": (
            "The Federal Reserve's 2022–2023 rate hike cycle transformed the savings account landscape. "
            "High-yield savings accounts at online banks moved from offering 0.50% APY in 2021 to "
            "5.0–5.50% by mid-2024 — the highest rates since 2007. This created massive consumer "
            "awareness of the yield gap between traditional banks (still offering 0.01–0.20% at many "
            "branches) and online alternatives. Deposits at online banks grew significantly as "
            "consumers moved funds in pursuit of yield. As the Fed begins cutting rates in 2025, "
            "HYSA rates will decline — currently 4.0–4.75% and trending down. The lesson: 'sticky' "
            "depositors who don't move funds to higher-yield accounts sacrifice significant income. "
            "The difference between 0.50% and 4.5% on a $50,000 emergency fund is $2,000/year — "
            "essentially free money for account-holders who pay attention."
        ),
        "metadata": {"period": "2024-2025", "topic": "Savings Rates", "tags": ["HYSA", "savings rates", "online banks", "deposit migration", "yield"]},
    },
    {
        "title": "Digital Banking Adoption: Who's Moving and Who's Staying",
        "text": (
            "U.S. digital banking adoption has accelerated dramatically — over 70% of Americans now "
            "primarily use mobile or online banking for daily account management. COVID-19 accelerated "
            "branch usage decline; branch visits per customer per year fell from 4.5 in 2019 to under "
            "2 in 2023. Neobanks (Chime, SoFi, Ally) have captured approximately 20 million primary "
            "banking relationships. Despite this, many consumers maintain traditional bank relationships "
            "for complex products (mortgages, business banking) while using digital banks for everyday "
            "transactions. Demographic split: under-35 consumers prefer digital-first banks for primary "
            "accounts; over-55 consumers prefer branch-accessible institutions. The big four banks "
            "(Chase, BofA, Wells Fargo, Citi) have invested heavily in digital capabilities, making "
            "them competitive with neobanks on most features while retaining branch network advantages."
        ),
        "metadata": {"period": "2024-2025", "topic": "Digital Banking", "tags": ["digital banking", "neobank", "mobile banking", "branch banking", "adoption"]},
    },
    {
        "title": "Deposit Insurance Awareness Post-SVB: What Consumers Should Know",
        "text": (
            "The 2023 failure of Silicon Valley Bank (SVB), Signature Bank, and First Republic Bank "
            "raised public awareness of FDIC deposit insurance limits for the first time in a generation. "
            "SVB had an unusual depositor base (tech startups) with many accounts far exceeding the "
            "$250,000 FDIC limit. The federal government's decision to guarantee all deposits (including "
            "uninsured) at SVB was extraordinary and not guaranteed to recur. Key consumer lessons: "
            "(1) Know your FDIC coverage — if you have more than $250,000 at a single bank, restructure "
            "ownership categories or use additional institutions. (2) Use the FDIC's BankFind Suite to "
            "verify your bank is FDIC-insured. (3) Brokered CDs at Fidelity/Schwab allow FDIC coverage "
            "across dozens of banks from one account. (4) Treasury bills are backed directly by the "
            "U.S. government — even safer than FDIC-insured deposits for large balances."
        ),
        "metadata": {"period": "2023-2025", "topic": "Deposit Insurance", "tags": ["FDIC", "SVB", "bank failure", "deposit insurance", "coverage limits"]},
    },
    {
        "title": "The Rise of Real-Time Payments (RTP) and FedNow",
        "text": (
            "Real-time payments are transforming U.S. money movement. Two major platforms: The Clearing "
            "House's RTP network (launched 2017, 300+ participating financial institutions) and the "
            "Federal Reserve's FedNow (launched July 2023, growing adoption). Both enable instant "
            "account-to-account transfers 24/7/365 — unlike ACH, which processes in batches during "
            "business hours. Consumer benefits: receive payroll, insurance claims, and tax refunds "
            "instantly; send emergency funds to family immediately. Business benefits: instant "
            "supplier payments, faster invoice settlement, improved cash flow visibility. Current "
            "limitation: both sender and receiver must be at participating financial institutions — "
            "not all banks are enrolled yet. Consumer applications are emerging: some banks offer "
            "FedNow-powered instant account transfers. By 2026, most major U.S. financial institutions "
            "are expected to participate in at least one real-time payment network."
        ),
        "metadata": {"period": "2024-2025", "topic": "Payment Systems", "tags": ["FedNow", "RTP", "real-time payments", "instant payments", "bank transfers"]},
    },
    {
        "title": "Open Banking and Account Aggregation: What It Means for Consumers",
        "text": (
            "Open banking allows consumers to securely share their financial data (with consent) across "
            "multiple financial services providers via standardized APIs. This enables tools like: "
            "budgeting apps (Mint, YNAB) that aggregate all accounts; comparison platforms that analyze "
            "your banking fees and suggest better products; lending platforms that use real bank data "
            "for more accurate underwriting. In the U.S., the CFPB's Personal Financial Data Rights "
            "Rule (Section 1033 of Dodd-Frank) is being implemented, requiring banks to provide "
            "consumer-authorized data access. Consumer rights: you have the right to authorize (and "
            "revoke) data sharing with third parties. Privacy consideration: carefully review what "
            "data you share and with whom — financial data is highly sensitive. Delete connections "
            "to apps you no longer use (typically through your bank's app or the aggregator's settings)."
        ),
        "metadata": {"period": "2024-2025", "topic": "Open Banking", "tags": ["open banking", "account aggregation", "CFPB 1033", "data sharing", "fintech"]},
    },
    {
        "title": "AI in Banking: Personalization, Fraud Detection, and Chatbots",
        "text": (
            "Artificial intelligence is reshaping retail banking in multiple dimensions. Fraud detection: "
            "ML models analyze transaction patterns in real-time, flagging unusual activity with "
            "significantly lower false positive rates than rule-based systems. Major banks prevent "
            "billions in fraud annually using AI. Personalization: AI analyzes spending patterns to "
            "offer personalized product recommendations, budgeting insights, and financial health scores. "
            "Customer service: AI chatbots handle routine inquiries (balance checks, transfer status, "
            "branch hours) — reducing wait times and operating costs. Predictive analytics: banks use "
            "AI to predict customer churn, identify at-risk borrowers before delinquency, and optimize "
            "cross-sell timing. Consumer concern: AI-driven decisions (loan denial, fraud flags) must "
            "be explainable under fair lending law. Banks must provide adverse action reasons even "
            "for AI-made decisions. Consumers can request reconsideration and human review."
        ),
        "metadata": {"period": "2025", "topic": "AI in Banking", "tags": ["AI", "fraud detection", "chatbot", "personalization", "banking technology"]},
    },
    {
        "title": "Bank Consolidation: What Mergers Mean for Your Accounts",
        "text": (
            "U.S. banking has seen continued consolidation — the number of FDIC-insured institutions "
            "has declined from over 10,000 in the 1990s to under 4,000 today. Recent notable mergers: "
            "JPMorgan Chase acquired First Republic Bank (2023); US Bank acquired Union Bank; TD Bank "
            "acquired several regional institutions. When your bank is acquired: (1) Your deposits "
            "remain FDIC insured. (2) Your account number, routing number, and terms may change after "
            "integration (typically 6–18 months). You'll receive advance notice. (3) Interest rates "
            "on savings products may change to reflect acquirer's rate environment. (4) Branch locations "
            "may be consolidated. Consumer rights in mergers: if loan terms are materially changed, "
            "you may have the right to pay off the loan without prepayment penalty. Review all "
            "communications from the acquiring institution carefully."
        ),
        "metadata": {"period": "2024-2025", "topic": "Banking Industry", "tags": ["bank merger", "acquisition", "First Republic", "banking consolidation", "FDIC"]},
    },
    {
        "title": "Credit Union vs. Bank: When to Choose Each",
        "text": (
            "Credit unions are member-owned, not-for-profit cooperatives. Banks are shareholder-owned, "
            "for-profit corporations. Key differences: (1) Rates: credit unions typically offer higher "
            "savings rates and lower loan rates than comparable banks — driven by not-for-profit status. "
            "(2) Fees: credit unions tend to have fewer and lower fees. (3) Membership: credit unions "
            "have field-of-membership requirements (employer, community, association-based) — though "
            "many have open membership for a nominal joining fee. (4) Branch/ATM access: large banks "
            "have broader networks; most credit unions participate in CO-OP ATM network (30,000 ATMs) "
            "and shared branching (5,600 locations). (5) Technology: large banks often have more "
            "sophisticated digital platforms. (6) Products: banks typically offer a broader product "
            "suite. Best strategy: use a credit union for savings and loans; use a large bank for "
            "full-service banking and advanced digital features."
        ),
        "metadata": {"period": "2025", "topic": "Banking Options", "tags": ["credit union", "bank comparison", "membership", "rates", "not-for-profit"]},
    },
    {
        "title": "Inflation's Impact on Bank Account Holders",
        "text": (
            "Inflation affects bank account holders in nuanced ways. Positive: higher inflation drove "
            "Federal Reserve rate hikes, which pushed HYSA and CD rates to 5%+ — the first meaningful "
            "positive real return on cash in over a decade. Negative: inflation erodes purchasing power "
            "of account balances over time — $10,000 in a checking account earning 0.01% loses real "
            "value at the rate of inflation. Account management implications for 2025: (1) Earn real "
            "returns on cash by using HYSAs or T-bills. (2) As the Fed cuts rates, lock in today's "
            "CD rates for 1–2 years before yields decline. (3) Minimize cash held in low-yield "
            "traditional savings accounts. (4) Budget adjustments: review automatic transfers "
            "and fixed savings targets — if inflation increased your monthly expenses, your savings "
            "rate may have inadvertently declined. Real return = nominal interest rate minus inflation."
        ),
        "metadata": {"period": "2024-2025", "topic": "Macroeconomics", "tags": ["inflation", "real return", "HYSA", "CD rates", "purchasing power"]},
    },
]

CLIENT_SCENARIOS = [
    {
        "title": "Case Study: Setting Up a Complete Banking System for a First Job",
        "text": (
            "Profile: Jordan, 22, just started first full-time job at $52,000. Currently has one "
            "checking account from college with minimal balance. Goal: set up a complete, functional "
            "banking system.\n\nRecommended setup: (1) Primary checking: choose a bank/credit union "
            "with direct deposit compatibility, fee-free checking, and a strong mobile app. "
            "(2) High-yield savings: open a separate HYSA (online bank offering 4–5% APY) for "
            "emergency fund. Keep $2,000 minimum in checking; build HYSA to $10,000–$15,000 (3 months "
            "of expenses). (3) Direct deposit: split deposit — $500 auto-transfer to HYSA each paycheck; "
            "remainder to checking. (4) Automate savings: set up recurring $100/month to a Roth IRA "
            "investment account. (5) Set up bill pay for rent, utilities, subscriptions. (6) Enable "
            "all transaction alerts. (7) Designate a beneficiary on all accounts. This system operates "
            "automatically, builds savings by default, and creates a clear separation between spending "
            "and savings money."
        ),
        "metadata": {"scenario_type": "Account Setup", "tags": ["first job", "banking setup", "direct deposit", "HYSA", "automation"]},
    },
    {
        "title": "Case Study: Recovering from Overdraft Spiral",
        "text": (
            "Profile: Carlos, 28, has been hit with 8 overdraft fees in the past 3 months ($280 total). "
            "Living paycheck to paycheck, the fees compound the problem.\n\nRoot cause analysis: "
            "Carlos has automatic bill payments with unpredictable timing relative to his biweekly "
            "paycheck. Solution plan: (1) Opt out of overdraft for debit card — transactions will "
            "simply decline rather than trigger fees. (2) Link a savings account as overdraft "
            "transfer source — most banks charge $0–$10/transfer versus $35/item. (3) Renegotiate "
            "bill due dates to align with payday — most utilities and credit card issuers allow "
            "this. (4) Set up a low-balance alert at $150. (5) Contact the bank and request "
            "a one-time courtesy waiver on recent fees — given his history, one or two may be "
            "refunded. (6) Request early direct deposit access (many banks now offer 2-day early "
            "access). Outcome: eliminating overdraft fees frees $280+ per quarter to begin "
            "building a checking account buffer."
        ),
        "metadata": {"scenario_type": "Overdraft Management", "tags": ["overdraft", "fees", "bill pay timing", "opt-out", "buffer"]},
    },
    {
        "title": "Case Study: Elderly Customer Protecting Against Financial Exploitation",
        "text": (
            "Profile: Eleanor, 79, lives alone and her daughter Susan (who lives in another state) "
            "is concerned about potential exploitation. Eleanor has been contacted by phone callers "
            "asking for bank information.\n\nProtective measures: (1) Add Susan as a 'trusted contact "
            "person' (TCP) on Eleanor's accounts — the bank can contact Susan if suspicious activity "
            "is observed, but Susan cannot access accounts. (2) Set up transaction alerts for all "
            "withdrawals over $100 sent to both Eleanor and Susan's email/phone. (3) Reduce the daily "
            "ATM withdrawal limit and daily debit purchase limit to amounts appropriate for Eleanor's "
            "typical spending. (4) Place a verbal password on the account so the bank knows to verify "
            "identity for any call-in requests. (5) Enroll in the bank's elder financial protection "
            "program. (6) Review and update all beneficiary designations. Warning signs of exploitation: "
            "unusual large withdrawals, new names on accounts, gift card purchases, and wire transfers "
            "to unknown parties."
        ),
        "metadata": {"scenario_type": "Elder Protection", "tags": ["elder financial abuse", "trusted contact", "transaction alerts", "protective measures", "senior banking"]},
    },
    {
        "title": "Case Study: Immigrant Family Opening First U.S. Bank Account",
        "text": (
            "Profile: The Ramirez family, recently arrived from Mexico. Two adults with ITINs (Individual "
            "Taxpayer Identification Numbers), no prior U.S. banking history, limited English. "
            "Goal: establish U.S. banking for direct deposit and bill payments.\n\n"
            "Account opening path: (1) Most major banks (Bank of America, Chase, Wells Fargo) and "
            "many credit unions accept ITIN + foreign passport + secondary ID. (2) Matrícula Consular "
            "(Mexican consular ID) is accepted by many banks. (3) Some banks have Spanish-speaking "
            "staff and Spanish-language banking interfaces. (4) Start with a basic checking account "
            "with no minimum balance and fee waiver through direct deposit. (5) Consider a joint "
            "account for both spouses. (6) After 6 months, request a secured credit card to begin "
            "building credit. (7) Be aware: wire transfers to Mexico have competitive rates through "
            "international banks versus remittance services (Western Union, Remitly may be cheaper "
            "for small amounts — compare fees). ITIN does not affect banking access."
        ),
        "metadata": {"scenario_type": "Immigrant Banking", "tags": ["ITIN", "immigrant banking", "Matrícula Consular", "account opening", "credit building"]},
    },
    {
        "title": "Case Study: College Student Building Financial Foundation",
        "text": (
            "Profile: Emma, 19, full-time college student. Works part-time (15 hrs/week, $1,200/month). "
            "Has a basic checking account but no savings.\n\nFoundation-building plan: (1) Open a "
            "student checking account with the university's partner bank for fee waivers and ATM "
            "access on campus. (2) Open a HYSA (Ally or Marcus) for a starter emergency fund — "
            "set up $100/month automatic transfer from each paycheck. Goal: $2,000 before graduation. "
            "(3) Build credit: apply for a student credit card (Discover it Student, Capital One "
            "SavorOne Student) — both have no annual fee and report to credit bureaus. Use only for "
            "one recurring subscription; pay in full monthly via autopay. (4) Avoid: payday apps "
            "(Earnin, Dave) that encourage cash advances; debit card overdraft (opt out); "
            "student loan disbursement in checking (transfer excess to HYSA immediately to avoid "
            "spending it). By graduation, Emma should have a good credit score (680+), an "
            "emergency fund, and zero credit card debt."
        ),
        "metadata": {"scenario_type": "Student Banking", "tags": ["college student", "student checking", "HYSA", "credit building", "financial foundation"]},
    },
    {
        "title": "Case Study: Small Business Owner Separating Personal and Business Finances",
        "text": (
            "Profile: David, 36, freelance consultant who has been operating under his SSN with no "
            "separate business account. Revenue: $130,000/year (sole proprietorship).\n\n"
            "Account separation plan: (1) Open a business checking account — even as a sole prop, "
            "separate accounts are essential for tax preparation, liability protection, and "
            "professional appearance. (2) LLC formation recommended ($50–$200 state filing) for "
            "liability protection; this requires a separate EIN and business account. (3) All "
            "client payments: invoice with business name, receive in business account. "
            "(4) Owner's draw: transfer a set 'salary' from business to personal account monthly. "
            "(5) Business savings: maintain 3 months of operating expenses in a business HYSA for "
            "cash flow buffer. (6) Tax reserves: transfer 25–30% of all income received to a "
            "dedicated tax savings account. (7) Accounting: connect business account to QuickBooks "
            "or Wave (free) for automated expense categorization. This clean separation transforms "
            "tax time from chaos to straightforward."
        ),
        "metadata": {"scenario_type": "Small Business", "tags": ["business account", "sole proprietorship", "LLC", "tax savings", "QuickBooks"]},
    },
    {
        "title": "Case Study: Managing Multiple Savings Goals with Buckets",
        "text": (
            "Profile: The Kim family, dual income, $145,000 combined. They have multiple savings goals: "
            "emergency fund ($20,000), home down payment ($80,000 over 3 years), vacation ($5,000/year), "
            "and car replacement ($15,000 in 2 years).\n\nBucket strategy: Rather than one savings "
            "account, use labeled savings buckets: (1) Emergency fund bucket: $20,000 in HYSA, "
            "fully funded — stop contributing, maintain. (2) Down payment bucket: $800/month "
            "auto-transfer to dedicated HYSA — reaches $80,000 in 3 years assuming 4.5% yield. "
            "(3) Vacation bucket: $420/month auto-transfer to separate savings account. "
            "(4) Car bucket: $625/month to separate account — reaches $15,000 in 2 years. "
            "Execution: many online banks (Ally, Capital One 360) allow multiple sub-accounts with "
            "custom names within one login. Seeing 'Down Payment Fund: $24,300' is more motivating "
            "than one undifferentiated savings balance. Each bucket is funded automatically "
            "on payday before discretionary spending."
        ),
        "metadata": {"scenario_type": "Savings Strategy", "tags": ["savings buckets", "multiple goals", "HYSA", "automation", "down payment"]},
    },
    {
        "title": "Case Study: Transitioning Elderly Parent's Finances to Family Management",
        "text": (
            "Profile: Robert, 75, beginning cognitive decline. His son Michael wants to help manage "
            "finances while preserving Robert's dignity and independence.\n\nAccount transition plan: "
            "(1) Durable power of attorney (DPOA): execute while Robert has legal capacity — this "
            "authorizes Michael to manage finances if Robert becomes incapacitated. The DPOA must "
            "be presented to each financial institution. (2) Joint account: add Michael as joint "
            "owner on checking account for bill payment oversight. (3) Trusted contact: add Michael "
            "as trusted contact on all accounts (doesn't require DPOA). (4) Online access: obtain "
            "online banking credentials with Robert's consent; set up view-only access if the bank "
            "allows. (5) Bill consolidation: set up automatic bill pay for recurring expenses to "
            "simplify. (6) Investment accounts: contact the financial institution with DPOA to "
            "manage investment accounts. Important: distinguish between 'convenience' joint accounts "
            "and estate planning — joint accounts pass outside the will and can create unintended "
            "inheritance consequences."
        ),
        "metadata": {"scenario_type": "Elder Account Management", "tags": ["power of attorney", "DPOA", "elder banking", "cognitive decline", "joint account"]},
    },
    {
        "title": "Case Study: Optimizing Cash Holdings as Interest Rates Change",
        "text": (
            "Profile: Linda, 52, has $85,000 in cash holdings across various accounts: $15,000 in "
            "a traditional savings account at 0.25%, $45,000 in a regular checking account, "
            "$25,000 in a 1-year CD purchased 8 months ago at 5.25% (maturing in 4 months).\n\n"
            "Optimization analysis: (1) Transfer $40,000 from the 0.25% savings and low-yield checking "
            "to a HYSA (currently 4.5% APY) — opportunity cost of inaction: $1,700/year in foregone "
            "interest. (2) When the CD matures in 4 months: with rates declining, consider a 2-year "
            "CD to lock in current rates (approximately 4.25–4.5%) before rates fall further, "
            "if those funds won't be needed. (3) Maintain $10,000 in liquid HYSA for near-term needs. "
            "(4) Consider laddering the CD maturity: split the $25,000 into a 1-year ($12,500) and "
            "2-year ($12,500) CD to maintain some rate-lock benefit while ensuring periodic liquidity. "
            "Annual income improvement from optimization: $1,500–$2,000."
        ),
        "metadata": {"scenario_type": "Cash Management", "tags": ["HYSA", "CD", "rate optimization", "cash management", "yield maximization"]},
    },
    {
        "title": "Case Study: Victim of Account Takeover Fraud",
        "text": (
            "Profile: Jennifer, 41, discovered $4,200 was wire-transferred from her checking account "
            "to an unknown party. She received an email from her bank (actually a phishing email) "
            "that led her to log in on a fraudulent site, capturing her credentials.\n\n"
            "Immediate response: (1) Call the bank's fraud line immediately — banks have wire recall "
            "procedures that are most effective within 24 hours. The FBI's IC3 (Internet Crime "
            "Complaint Center) wire recall process may assist. (2) Bank must investigate a Reg E "
            "claim — wire transfers may have different protections than ACH; provide all details "
            "of the phishing incident. (3) Change all banking passwords immediately; enable 2FA on "
            "all financial accounts. (4) File an FTC complaint at IdentityTheft.gov and a local "
            "police report. (5) Place a credit freeze at all three bureaus. (6) Review all accounts "
            "for additional unauthorized activity. (7) CFPB complaint if the bank refuses to "
            "reimburse. Outcome: wire recalls succeed approximately 50% of the time; account "
            "takeover fraud with documented phishing significantly improves the bank's liability."
        ),
        "metadata": {"scenario_type": "Fraud Recovery", "tags": ["account takeover", "wire fraud", "phishing", "Reg E", "fraud recovery"]},
    },
    {
        "title": "Case Study: FDIC Coverage Planning for Large Deposit",
        "text": (
            "Profile: The Chen family received $750,000 from the sale of a family business. They "
            "need to keep funds liquid for 12 months while deciding on long-term investments.\n\n"
            "FDIC coverage strategy: $750,000 exceeds the $250,000 single-account limit at any one "
            "bank. Options to insure the full amount: (1) Use multiple ownership categories at one bank: "
            "Individual checking ($250K), Joint account with spouse ($500K — $250K per owner). "
            "Total coverage: $750K at one bank. (2) Spread across multiple banks: $250K at three "
            "different FDIC-insured institutions. (3) Brokered CD ladder through Fidelity or Schwab: "
            "purchase CDs from 10 different banks ($75K each), all FDIC insured separately, earning "
            "competitive rates. This is the most elegant solution. (4) Treasury bills: backed directly "
            "by U.S. government — no $250K limit. Purchase through TreasuryDirect or brokerage. "
            "For 12-month liquidity, the brokered CD ladder or T-bills provide both safety and "
            "yield during the holding period."
        ),
        "metadata": {"scenario_type": "Large Deposit Management", "tags": ["FDIC", "large deposit", "brokered CD", "Treasury bills", "coverage planning"]},
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
