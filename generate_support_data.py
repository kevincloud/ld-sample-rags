"""
Generates ~130 demo text chunks for the Customer Support RAG corpus.
Outputs: rag/data/support_chunks.json

Content types:
  PRODUCT           - support services and tools available to customers
  FAQ               - common customer support questions across all banking topics
  MARKET_COMMENTARY - trends in banking customer service and support
  CLIENT_SCENARIO   - customer support case studies
"""

import json
import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "data", "support_chunks.json")

PRODUCTS = [
    {
        "title": "24/7 Phone Banking Support",
        "text": (
            "Phone banking support provides customers with live agent access around the clock for "
            "urgent banking needs. Services available via phone: account balance inquiries, "
            "transaction disputes, lost/stolen card reporting, fraud alerts, fund transfers, "
            "bill pay assistance, and general account questions. Most major banks maintain "
            "dedicated 24/7 fraud hotlines separate from general customer service. Average "
            "hold times vary: large banks typically 3–12 minutes during peak hours; credit "
            "unions often shorter. Tips for efficient phone support: have your account number "
            "and SSN last four digits ready; call from the phone number on file for faster "
            "identity verification; use the fraud/emergency line for card issues (skip the "
            "main queue); listen carefully to menu options to reach the right department. "
            "Phone banking is still the preferred channel for complex, time-sensitive, or "
            "emotionally sensitive issues where real human interaction is valuable."
        ),
        "metadata": {"product_type": "Support Channel", "tags": ["phone banking", "24/7 support", "customer service", "fraud hotline", "live agent"]},
    },
    {
        "title": "Online Banking Help Center",
        "text": (
            "The online banking help center is a self-service portal accessible through the "
            "bank's website and mobile app, providing 24/7 access to support resources. "
            "Typical features: searchable FAQ database, step-by-step task guides (how to "
            "set up direct deposit, order checks, dispute a transaction), video tutorials, "
            "secure message center for non-urgent inquiries, and chat access. The help center "
            "allows customers to resolve most routine questions without calling. Best practices: "
            "use the search bar with specific terms (e.g., 'mobile deposit limit' rather than "
            "'deposit'); check the help center before calling — many questions are faster to "
            "resolve online. The secure message center typically receives responses within "
            "1–3 business days and provides a written record of support interactions. "
            "Online banking help is available at any hour — especially valuable for questions "
            "outside business hours."
        ),
        "metadata": {"product_type": "Support Channel", "tags": ["help center", "self-service", "FAQ", "secure message", "online banking"]},
    },
    {
        "title": "Live Chat Support",
        "text": (
            "Live chat support connects customers with bank representatives through real-time "
            "text messaging via the bank's website or mobile app. Growing channel: most major "
            "banks now offer live chat during extended hours (often 7 AM–11 PM daily). "
            "Best for: quick questions, account inquiries, navigating the app, and situations "
            "where you want a written record of the interaction. Limitations: identity "
            "verification via chat may be more complex; complex issues or those requiring "
            "document review are better handled by phone or branch. Many banks now deploy "
            "AI chatbots for initial interaction — these handle common queries (balance, "
            "payment status, branch hours) instantly and route complex issues to human agents. "
            "Save chat transcripts: most bank chat platforms allow you to email yourself a "
            "transcript — do this for any dispute, complaint, or promise made by the representative "
            "so you have a record."
        ),
        "metadata": {"product_type": "Support Channel", "tags": ["live chat", "chatbot", "real-time support", "written record", "AI chatbot"]},
    },
    {
        "title": "Branch Banking Services",
        "text": (
            "Bank branches provide in-person services for transactions and needs that require "
            "face-to-face interaction or physical documents. Services available in-branch: "
            "account opening, cashier's checks and money orders, notary services, safe deposit "
            "box access, large cash deposits/withdrawals, loan applications, mortgage consultations, "
            "wire transfer initiation, complex account changes (adding joint owners, trust accounts), "
            "and dispute resolution. Branch visits are best for: opening new accounts, "
            "applying for loans, resolving complex disputes, large cash transactions, "
            "and estate/trust matters. Appointment scheduling: for loans and complex matters, "
            "schedule in advance — walk-in availability varies by branch and time. "
            "Branch hours: typically Monday–Friday 9 AM–5 PM, Saturday limited hours; "
            "closed Sundays and federal holidays. Use the bank's app or website to find "
            "nearest branch, check hours, and book appointments."
        ),
        "metadata": {"product_type": "Support Channel", "tags": ["branch", "in-person banking", "teller", "banker", "full-service"]},
    },
    {
        "title": "Mobile Banking App Support Features",
        "text": (
            "Modern banking apps include robust self-service and support features. Key support "
            "capabilities within apps: card lock/unlock (instantly freeze a card if misplaced), "
            "transaction dispute initiation, account alerts setup (balance, transaction, login), "
            "direct deposit form generation, mobile check deposit, ATM locator, spending "
            "categorization, and statement download. Support contact: most apps have one-tap "
            "access to call, chat, or secure message customer service. Push notifications: "
            "enable transaction alerts — real-time notifications for every purchase provide "
            "the earliest possible fraud detection. Account management: update personal information "
            "(phone number, email, mailing address), manage beneficiaries, and change PIN without "
            "branch visit. The mobile app has replaced most branch visit needs for routine "
            "account management. Ensure app and phone OS are kept updated for security patches."
        ),
        "metadata": {"product_type": "Digital Support", "tags": ["mobile app", "card lock", "transaction alerts", "self-service", "digital banking"]},
    },
    {
        "title": "Automated Phone System (IVR)",
        "text": (
            "Interactive Voice Response (IVR) systems provide automated phone banking for routine "
            "inquiries without waiting for a live agent. Available 24/7: account balances, "
            "recent transactions (last 5–10), payment confirmations, branch hours and locations, "
            "interest rates, and routing/account number confirmation. Navigation tips: most IVRs "
            "respond to spoken keywords or keypad input; saying 'agent,' 'representative,' or "
            "pressing '0' often bypasses menus to reach a live person. When to use IVR: "
            "quick balance check, payment confirmation, or branch information when the app is "
            "unavailable. Security: authenticate with your PIN or last 4 of SSN; never provide "
            "full SSN or password to an incoming caller claiming to be your bank — legitimate "
            "IVR systems do not call you requesting login credentials."
        ),
        "metadata": {"product_type": "Support Channel", "tags": ["IVR", "automated phone", "phone banking", "account balance", "24/7 self-service"]},
    },
    {
        "title": "CFPB Complaint Process",
        "text": (
            "The Consumer Financial Protection Bureau (CFPB) provides a formal complaint process "
            "when banking issues cannot be resolved directly with the financial institution. "
            "How to file: visit consumerfinance.gov/complaint, describe the issue, select the "
            "financial product/company, and submit. The CFPB forwards complaints to the company, "
            "which must respond within 15 days and resolve within 60 days. The CFPB publishes "
            "complaint data publicly (without personal information) — companies take CFPB "
            "complaints seriously as they affect their public complaint record. Use CFPB when: "
            "the bank denies a legitimate fraud claim, refuses to honor required Regulation E "
            "dispute rights, engages in discriminatory practices, or fails to respond to "
            "direct complaints. CFPB resolution statistics: approximately 97% of complaints "
            "result in a response from the company; consumers report satisfactory resolution "
            "in approximately 50–60% of cases. Also useful: your state's banking regulator "
            "and the OCC (for nationally chartered banks)."
        ),
        "metadata": {"product_type": "Escalation Resource", "tags": ["CFPB", "complaint", "escalation", "regulatory complaint", "consumer rights"]},
    },
    {
        "title": "Personal Banker / Relationship Manager",
        "text": (
            "A personal banker (or relationship manager) is a dedicated bank employee assigned "
            "to manage the relationship with specific customers — typically those with significant "
            "assets or complex banking needs. Services provided: comprehensive financial review, "
            "priority access and reduced wait times, dedicated phone and email contact, proactive "
            "outreach for relevant product changes or opportunities, assistance with complex "
            "transactions, loan facilitation, and business banking needs. Access: typically "
            "available to customers with $100,000–$250,000+ in relationship balances at large banks; "
            "private banking relationships start at $1M+. For smaller customers: many credit "
            "unions and community banks assign all members a primary contact. How to request: "
            "ask your bank's branch manager if you qualify for a dedicated relationship. "
            "A good personal banker proactively identifies opportunities to improve your "
            "banking relationship and advocates internally when issues arise."
        ),
        "metadata": {"product_type": "Premium Service", "tags": ["personal banker", "relationship manager", "private banking", "premium service", "dedicated contact"]},
    },
    {
        "title": "Financial Wellness Tools and Education Resources",
        "text": (
            "Many banks and credit unions offer financial wellness programs to help customers "
            "improve financial literacy and outcomes. Common offerings: budgeting tools integrated "
            "with account data (spending analysis, category budgets), financial calculators "
            "(mortgage affordability, loan payoff, retirement), educational content (articles, "
            "videos, webinars on topics from budgeting to investing), credit score monitoring "
            "(free FICO or VantageScore with explanation), and certified financial counselors "
            "(some credit unions offer free financial counseling to members). HUD-approved "
            "housing counselors: free or low-cost counseling for homebuyers and those facing "
            "foreclosure. NFCC (National Foundation for Credit Counseling): non-profit network "
            "providing low-cost debt counseling. These resources are underutilized — even basic "
            "free tools (credit score monitoring, spending categorization) can significantly "
            "improve financial awareness and decision-making."
        ),
        "metadata": {"product_type": "Support Resource", "tags": ["financial wellness", "budgeting tools", "financial education", "credit score", "counseling"]},
    },
    {
        "title": "Fraud and Identity Theft Protection Services",
        "text": (
            "Banks offer various fraud protection services beyond standard transaction monitoring. "
            "Included services (at most banks, free): zero liability on unauthorized card "
            "transactions, real-time fraud alerts, ability to instantly lock/unlock cards via app, "
            "notification of new account openings or address changes. Optional/premium services: "
            "identity theft insurance (reimburses costs of recovery — legal fees, lost wages, "
            "credit monitoring — typically $1M coverage), dark web monitoring (alerts if your "
            "information appears on dark web data breaches), credit monitoring and alerts, "
            "social security number monitoring. Offered by: Lifelock (now Norton LifeLock), "
            "IdentityForce, myFICO, Experian IdentityWorks, and many banks' own programs. "
            "Note: no service can prevent identity theft — they detect and help recover. "
            "Free alternatives: credit freezes at all three bureaus, AnnualCreditReport.com "
            "annual review, and Google Alerts for your name provide meaningful protection "
            "at no cost."
        ),
        "metadata": {"product_type": "Security Service", "tags": ["fraud protection", "identity theft", "zero liability", "dark web monitoring", "credit monitoring"]},
    },
    {
        "title": "Overdraft Assistance Programs",
        "text": (
            "Many banks now offer formal overdraft assistance programs as alternatives to "
            "traditional overdraft fees. Program types: (1) Grace period programs: if account "
            "is overdrawn at day end, a 24-hour window to deposit before a fee is charged "
            "(Chase, Bank of America, TD Bank). (2) Small buffer programs: no fee for overdrafts "
            "under $5–$50 (Ally, Capital One, PNC). (3) Overdraft Grace Balance: automatically "
            "transfers from savings if balance falls below a threshold. (4) Fee-free overdraft "
            "lines of credit: credit unions often offer low-APR overdraft lines (12–18% APR) "
            "versus traditional $35 fees. (5) Financial hardship programs: for customers "
            "experiencing genuine hardship, fee waiver programs may be available. "
            "If you're hit with overdraft fees: contact customer service immediately and "
            "request a one-time courtesy waiver — this is standard practice at most banks "
            "for customers with a good history and is rarely advertised. Keep records of "
            "the conversation."
        ),
        "metadata": {"product_type": "Support Service", "tags": ["overdraft assistance", "grace period", "fee waiver", "overdraft protection", "hardship program"]},
    },
    {
        "title": "Credit Union Member Services",
        "text": (
            "Credit union member services differ from commercial bank customer service in several "
            "important ways. As a member-owner, you have a voice in the credit union's governance "
            "(annual meetings, board elections). Member services typically include: same deposit "
            "insurance (NCUA = FDIC equivalent for credit unions), access to shared branching "
            "network (5,600+ locations nationwide), CO-OP ATM network (30,000 fee-free ATMs), "
            "financial counseling from member services staff, hardship programs for members "
            "experiencing financial difficulty, and reduced fees across most products. "
            "Complaint resolution: file with the credit union's member services first; "
            "if unresolved, escalate to the NCUA (National Credit Union Administration — "
            "ncua.gov/consumers/complaint). Credit unions are generally known for more "
            "personalized service than large commercial banks. If you're underserved by "
            "your current bank, exploring local credit union membership is strongly recommended."
        ),
        "metadata": {"product_type": "Support Channel", "tags": ["credit union", "member services", "shared branching", "NCUA", "co-op ATM"]},
    },
    {
        "title": "Estate Banking Assistance",
        "text": (
            "Estate banking assistance helps families manage the financial accounts of a deceased "
            "account holder. Services include: notifying the bank of a death, accessing funds "
            "needed immediately for funeral expenses (most banks have a small immediate disbursement "
            "policy), inventory of accounts and safe deposit box contents, transferring or closing "
            "accounts according to the estate, and releasing funds to beneficiaries or estate. "
            "Required documentation: certified death certificate (multiple copies recommended), "
            "letters testamentary (court-issued if estate is going through probate), or letters "
            "of administration (if no will). Beneficiary designations (POD accounts): bypass "
            "probate — beneficiary can claim with death certificate + photo ID. Joint accounts: "
            "surviving joint owner retains access and ownership. Bank time limits: estates should "
            "act within 1 year for most bank claims. Some states have 'small estate affidavit' "
            "procedures that bypass probate for small estates — check your state's rules. "
            "Bank estate specialists are trained to help grieving families navigate this sensitively."
        ),
        "metadata": {"product_type": "Specialty Service", "tags": ["estate banking", "deceased account holder", "beneficiary", "probate", "death certificate"]},
    },
    {
        "title": "Disability and Accessibility Services",
        "text": (
            "Banks are required by the Americans with Disabilities Act (ADA) and other laws to "
            "provide equal access to banking services. Accessibility services: TTY/TDD phone "
            "service for hearing-impaired customers (dedicated phone numbers), screen-reader "
            "compatible websites and mobile apps (WCAG accessibility standards), large-print "
            "and Braille account statements on request, accessible branches (wheelchair access, "
            "accessible ATMs), and video relay interpreting services for in-branch sign language "
            "needs. Additional accommodations: banks can make reasonable accommodations for "
            "customers with cognitive disabilities, including simplified account structures, "
            "trusted contact persons, and guardian/conservator account management. "
            "If you need accommodations not being provided: ask to speak with the accessibility "
            "services coordinator or ADA compliance officer. Filing an ADA complaint: "
            "U.S. Department of Justice civil rights division handles ADA complaints against "
            "financial institutions."
        ),
        "metadata": {"product_type": "Accessibility", "tags": ["ADA", "accessibility", "disability services", "TTY", "screen reader"]},
    },
    {
        "title": "Financial Hardship Program",
        "text": (
            "Banks and credit unions offer financial hardship programs for customers experiencing "
            "job loss, medical emergency, natural disaster, or other financial crises. Programs "
            "vary by institution and product: mortgage forbearance (temporary payment pause or "
            "reduction), student loan deferment (servicer programs), credit card hardship "
            "programs (reduced interest rate, waived fees, temporary payment reduction), "
            "overdraft fee waivers, short-term personal loans at reduced rates, and extended "
            "payment plans for existing debt. How to access: call your bank or lender and "
            "ask specifically for hardship programs — these are rarely advertised. Explain "
            "your situation; you may need to provide documentation. Important: proactively "
            "contact your lender BEFORE missing a payment. A proactive call to discuss "
            "hardship before a missed payment gives you far more options and protects your "
            "credit. FDIC and NCUA both encourage lenders to work with customers facing "
            "genuine hardship."
        ),
        "metadata": {"product_type": "Support Program", "tags": ["hardship program", "financial difficulty", "forbearance", "deferment", "job loss"]},
    },
]

FAQS = [
    {
        "title": "How do I report a lost or stolen debit or credit card?",
        "text": (
            "Report a lost or stolen card immediately: (1) Use your bank's mobile app to instantly "
            "lock or freeze the card while you search for it — if found, unlock it; if not, "
            "proceed to cancellation. (2) Call the fraud hotline on the back of the card "
            "(have the account number handy if possible, or the bank's main number). Most "
            "banks have 24/7 fraud hotlines. (3) Online banking: many banks allow card "
            "cancellation and replacement requests online. Replacement timeline: standard "
            "replacement is 5–7 business days; expedited shipping (1–2 days) is usually "
            "available, sometimes free for fraud cases. Liability: Regulation E (debit) and "
            "the Fair Credit Billing Act (credit) both limit your liability to $0–$50 if "
            "reported promptly. Most banks have $0 liability policies for fraud. While waiting "
            "for a replacement: use digital wallets (Apple Pay, Google Pay) if your card is "
            "already registered — the virtual token still works even after the physical card "
            "is cancelled."
        ),
        "metadata": {"category": "Card Issues", "tags": ["lost card", "stolen card", "card freeze", "fraud report", "replacement card"]},
    },
    {
        "title": "How do I reset my online banking password?",
        "text": (
            "If you've forgotten your online banking password: (1) Click 'Forgot Password' on the "
            "login page. (2) You'll be asked to verify your identity — typically via email or "
            "SMS to your registered contact (one-time code), security questions, or last 4 "
            "digits of SSN plus account information. (3) Create a new password: minimum 8–12 "
            "characters (varies by bank), including uppercase, lowercase, number, and symbol. "
            "If you're locked out after multiple failed attempts: most banks automatically "
            "unlock after 15–30 minutes, or you can call customer service for immediate "
            "assistance. If your account was locked due to suspicious activity: you'll need "
            "to call and verify your identity with an agent. Password security best practices: "
            "use a unique password (not shared with any other site), consider a password manager "
            "(Bitwarden — free, 1Password — paid), enable two-factor authentication (2FA) once "
            "you're back in. Never share your banking password with anyone, including bank employees."
        ),
        "metadata": {"category": "Account Access", "tags": ["password reset", "locked account", "2FA", "login", "online banking security"]},
    },
    {
        "title": "What should I do if I don't recognize a transaction on my account?",
        "text": (
            "If you see an unrecognized transaction: (1) Check the full merchant name — transactions "
            "often appear with a parent company name, not the merchant name you know (e.g., "
            "'AMZN MKTP' for Amazon, 'WHOLEFDS' for Whole Foods, 'TST*' for Toast-powered "
            "restaurants). Use Google to search the transaction description. (2) Check if a "
            "family member or authorized user made the purchase. (3) Review if you have any "
            "free trials that started billing. (4) If still unrecognized after checking, "
            "report it as potentially fraudulent through your bank's app, online banking "
            "dispute center, or by calling. Don't wait — Regulation E requires reporting "
            "within 60 days for maximum protection. (5) If fraud is confirmed: your bank "
            "will cancel the card, issue a new one, and initiate a chargeback with the merchant. "
            "You should receive provisional credit within 1–5 business days while the "
            "investigation proceeds."
        ),
        "metadata": {"category": "Dispute Resolution", "tags": ["unrecognized transaction", "dispute", "fraud", "chargeback", "Regulation E"]},
    },
    {
        "title": "How do I update my phone number or email address with my bank?",
        "text": (
            "Keeping contact information current is critical for security alerts, OTP verification, "
            "and statement delivery. Methods to update: (1) Online banking: log in, navigate to "
            "Profile or Settings, update phone number and/or email, confirm the change with a "
            "verification code sent to the OLD contact method (or by answering security questions). "
            "(2) Mobile app: same process through settings. (3) Branch: in-person with government ID. "
            "(4) Phone: call customer service; verification required. Why keeping contacts current "
            "matters: two-factor authentication sends codes to your registered phone/email; fraud "
            "alerts require a working number; if you can't receive verification codes, you may be "
            "locked out. After changing your phone number: update with every financial institution "
            "(banks, investment accounts, credit cards, loans). Also update: the IRS via tax return "
            "or Form 8822. A disconnected old phone number can become a security vulnerability "
            "if reassigned to someone else who then receives your OTP codes."
        ),
        "metadata": {"category": "Account Management", "tags": ["update contact", "phone number", "email update", "2FA", "account security"]},
    },
    {
        "title": "Why was my card declined even though I have enough money?",
        "text": (
            "A card decline doesn't always mean insufficient funds. Common reasons: (1) Insufficient "
            "available balance: there may be a hold on a recent deposit reducing your available "
            "balance below the transaction amount. (2) Daily spending limit exceeded: most debit "
            "cards have daily purchase limits ($2,000–$5,000) separate from the account balance. "
            "(3) Transaction fraud alert: the bank's system flagged the purchase as potentially "
            "fraudulent (unusual merchant, unusual amount, out-of-area purchase). (4) Expired card: "
            "the physical card has an expiration date — renew when the new card arrives. "
            "(5) Merchant-specific issues: some merchants (gas stations, hotels) place temporary "
            "authorization holds. (6) International use: card not enabled for international "
            "purchases by default (call bank before traveling). (7) Card damaged: chip or magnetic "
            "stripe failure. Solutions: call the number on the back of your card, check available "
            "balance vs. actual balance, or enable international use before travel."
        ),
        "metadata": {"category": "Card Issues", "tags": ["card declined", "spending limit", "fraud hold", "available balance", "international use"]},
    },
    {
        "title": "How long does a dispute investigation take?",
        "text": (
            "Dispute investigation timelines are regulated: Under Regulation E (debit card): "
            "the bank has 10 business days to investigate (5 days for new accounts). During "
            "this time, if the bank needs more time, they may extend to 45 business days "
            "but MUST provisionally credit your account within 10 days while investigating. "
            "Under the Fair Credit Billing Act (credit card): disputed billing errors must "
            "be acknowledged within 30 days, resolved within 2 billing cycles (maximum 90 days). "
            "You're not required to pay the disputed amount while under investigation for "
            "credit cards. During the investigation: provide any documentation requested "
            "(screenshots, receipts, communications with merchant); respond promptly to any "
            "bank requests for information. If resolved against you: provisional credit may be "
            "reversed; you'll receive written explanation and have the right to request "
            "documentation the bank relied on and to submit rebuttal evidence."
        ),
        "metadata": {"category": "Dispute Resolution", "tags": ["dispute timeline", "investigation", "provisional credit", "Reg E", "FCBA"]},
    },
    {
        "title": "How do I set up or change my PIN?",
        "text": (
            "A PIN (Personal Identification Number) is a 4-digit code for ATM transactions and "
            "credit card chip-and-PIN purchases. Methods to set or change: (1) ATM: most banks "
            "allow PIN change at their ATMs — select 'PIN services' or 'change PIN' from the menu. "
            "(2) Online banking or mobile app: some banks allow PIN management in the card "
            "management section. (3) Phone: call customer service; they'll guide you through "
            "a secure PIN-change process or send a PIN mailer. (4) Branch: in-person with ID. "
            "PIN security rules: don't use easily guessed numbers (1234, 0000, birth year, "
            "address numbers). Never write your PIN on or near the card. Never share your PIN "
            "with anyone — not bank employees, family members, or service providers. ATM "
            "skimmers: shield the keypad when entering your PIN. If you suspect your PIN "
            "was compromised, change it immediately and review recent transactions for "
            "unauthorized ATM withdrawals."
        ),
        "metadata": {"category": "Account Security", "tags": ["PIN", "PIN change", "ATM PIN", "card security", "PIN skimmer"]},
    },
    {
        "title": "What is the difference between a complaint and a dispute?",
        "text": (
            "A dispute is a formal challenge to a specific transaction — requesting that an "
            "unauthorized or incorrect charge be reversed. Disputes are governed by federal law "
            "(Regulation E for debit, FCBA for credit) with specific timelines and resolution "
            "processes. A complaint is a broader expression of dissatisfaction with a bank's "
            "policies, products, procedures, or service quality. Complaints can be filed: "
            "with the bank's customer service (first step), with the bank's formal complaint "
            "process (usually through the website), with the CFPB (consumerfinance.gov), "
            "with your state's banking regulator, or with the OCC's Customer Assistance Group "
            "(for nationally chartered banks). When to file a complaint vs. a dispute: "
            "if a merchant charged you incorrectly — dispute. If the bank denied a legitimate "
            "Regulation E dispute — both dispute (escalate internally) and CFPB complaint. "
            "If the bank charged fees you didn't agree to — complaint. CFPB complaints "
            "often prompt more thorough review than standard customer service."
        ),
        "metadata": {"category": "Issue Resolution", "tags": ["complaint", "dispute", "CFPB", "Reg E", "FCBA"]},
    },
    {
        "title": "How do I find my account and routing numbers?",
        "text": (
            "Your account number and routing number are needed for direct deposit setup, external "
            "account linking, electronic payments, and wire transfers. Where to find them: "
            "(1) Checkbook: on the bottom of a check, left-to-right: routing number (9 digits), "
            "account number, check number. (2) Online banking: log in, select the account, "
            "look for 'Account Details' or 'Account Information.' (3) Mobile app: tap on the "
            "account, usually shows routing and account numbers with tap-to-copy. (4) Statement: "
            "printed on your monthly account statement. (5) Bank website: some banks list their "
            "routing numbers publicly (search '[bank name] routing number'). Note: the routing "
            "number for ACH transactions may differ from the routing number for wire transfers "
            "at some banks — confirm which is needed for your purpose. Never email or text "
            "your account number to unknown parties. Providing account number and routing "
            "number enables electronic payment initiation — share only with trusted parties "
            "or to receive legitimate payments."
        ),
        "metadata": {"category": "Account Information", "tags": ["routing number", "account number", "direct deposit", "check", "online banking"]},
    },
    {
        "title": "How do I close an account I no longer use?",
        "text": (
            "Closing a dormant or unwanted account requires a few steps to do correctly: "
            "(1) Update all direct deposits to route to your new account. (2) Redirect all "
            "automatic payments (bills, subscriptions) to a new account — make a complete list "
            "first. (3) Allow all outstanding checks and pending transactions to clear. "
            "(4) Spend down or transfer the remaining balance. (5) Contact the bank by phone, "
            "online, or in-branch to formally request account closure. Provide ID. "
            "(6) Confirm in writing (email to the bank) and request written confirmation of "
            "the closure date. Why formal closure matters: leaving an account open but unused "
            "can result in dormancy fees (after 12–24 months of inactivity); the account "
            "may eventually escheat (be turned over to the state as unclaimed property). "
            "If the account has a negative balance: it must be resolved (paid) before closure. "
            "Request the final account statement for your records."
        ),
        "metadata": {"category": "Account Management", "tags": ["close account", "account closure", "dormant account", "direct deposit update", "autopay"]},
    },
    {
        "title": "What can I do if the ATM gave me the wrong amount?",
        "text": (
            "If an ATM dispenses the wrong amount: (1) Contact your bank immediately — call "
            "the fraud/customer service line. Report: the ATM location, date/time, transaction "
            "amount shown on receipt, actual amount received. Do not leave without noting the "
            "ATM's ID number (usually displayed on the machine). (2) ATM errors are typically "
            "resolved in your favor after the bank 'balances' the ATM — a process where they "
            "count the cash in the machine against expected amounts. If the ATM is found to "
            "have had a short dispense, your account is credited. (3) Keep your receipt: it's "
            "your primary evidence. If the ATM didn't give a receipt, note the exact time "
            "on your phone. Resolution timeline: 5–10 business days is typical for ATM "
            "error resolution; if the ATM is owned by a third party (not your bank), "
            "resolution may take longer as your bank must coordinate with the ATM owner. "
            "Regulation E covers these disputes with the same timelines as other debit disputes."
        ),
        "metadata": {"category": "ATM Issues", "tags": ["ATM error", "wrong amount", "ATM dispute", "Regulation E", "ATM receipt"]},
    },
    {
        "title": "How do I dispute a credit card charge from a merchant?",
        "text": (
            "Credit card disputes have two phases: first, attempt to resolve directly with the "
            "merchant; if unsuccessful, dispute with the card issuer. Step 1 — contact the "
            "merchant: call customer service, explain the issue, and request resolution. "
            "Keep notes (date, representative name, outcome). Many issues resolve faster "
            "this way. Step 2 — dispute with your bank/card issuer if the merchant doesn't "
            "resolve within a reasonable time: file online, via app, or by phone. The Fair "
            "Credit Billing Act (FCBA) requires disputes to be filed within 60 days of the "
            "statement containing the charge. Valid dispute reasons: merchandise not received, "
            "item not as described, duplicate charge, wrong amount, unauthorized transaction. "
            "The issuer contacts the merchant (who has 30 days to respond with evidence). "
            "If the merchant doesn't respond or can't substantiate the charge, you win. "
            "If the merchant provides valid evidence, the charge stands. For high-value "
            "disputes: document everything carefully — screenshots, emails, original order "
            "confirmation."
        ),
        "metadata": {"category": "Dispute Resolution", "tags": ["credit card dispute", "chargeback", "FCBA", "merchant dispute", "60-day rule"]},
    },
    {
        "title": "How do I activate a new debit or credit card?",
        "text": (
            "Activate a new card through one of these methods: (1) Phone: call the activation "
            "number on the sticker on the front of the new card. You'll need to verify "
            "identity (card number, SSN last 4, date of birth, billing address). (2) Online "
            "banking: log in, navigate to card management, select 'Activate New Card.' "
            "(3) Mobile app: most banking apps have a card activation option in card settings. "
            "(4) ATM: use the new card to make a transaction or PIN change — this activates "
            "it simultaneously. (5) First purchase: some issuers auto-activate on first use "
            "(check the card's sticker for the activation method). "
            "After activation: set your PIN (if debit); register for digital wallets (Apple Pay, "
            "Google Pay); update your card number with any stored payment profiles (Amazon, "
            "Netflix, utilities). Destroy the old card: cut through the chip and magnetic strip; "
            "some banks accept old cards returned in-branch for secure destruction."
        ),
        "metadata": {"category": "Card Management", "tags": ["card activation", "new card", "PIN setup", "digital wallet", "card replacement"]},
    },
    {
        "title": "What do I do if I think my identity has been stolen?",
        "text": (
            "Identity theft requires immediate, systematic response. Priority actions: "
            "(1) Place fraud alerts or credit freezes at all three bureaus — Equifax, Experian, "
            "TransUnion (free, do this within 24 hours). A freeze is more powerful. "
            "(2) Report to the FTC at IdentityTheft.gov — creates an official recovery plan. "
            "(3) File a police report — required for some dispute resolution and insurance claims. "
            "(4) Review all financial accounts for unauthorized activity: bank accounts, "
            "credit cards, retirement accounts, brokerage accounts. (5) Contact each bank "
            "with suspected fraud — freeze accounts, dispute unauthorized transactions. "
            "(6) Check for new accounts opened in your name: request free credit reports "
            "at AnnualCreditReport.com; review all accounts for unfamiliar ones. "
            "(7) Change passwords on all financial accounts; enable 2FA. (8) If tax fraud "
            "suspected (fraudulent return filed in your name): contact IRS at 1-800-908-4490. "
            "Recovery is a process — document everything."
        ),
        "metadata": {"category": "Identity Theft", "tags": ["identity theft", "credit freeze", "fraud alert", "IdentityTheft.gov", "FTC"]},
    },
    {
        "title": "Why is my bank asking for more information about a transaction?",
        "text": (
            "Banks are required by law to monitor for suspicious activity under the Bank Secrecy "
            "Act (BSA) and Anti-Money Laundering (AML) regulations. They may ask for information "
            "about transactions that are: (1) Unusually large relative to account history. "
            "(2) International, particularly to or from high-risk jurisdictions. (3) Involving "
            "a new payee with an unusual amount. (4) Involving business accounts with unusual "
            "transaction patterns. Common questions asked: source of funds (where did the money "
            "come from?), purpose of the transfer, relationship to recipient, supporting "
            "documentation (contracts, invoices, sales agreements). You must answer honestly — "
            "refusing to answer may result in the transaction being declined. False information "
            "is a federal offense. Banks are prohibited from telling you if they've filed a "
            "Suspicious Activity Report (SAR). These are routine compliance inquiries — "
            "legitimate transactions are approved. The process protects both you and the "
            "broader financial system from fraud and financial crime."
        ),
        "metadata": {"category": "Compliance", "tags": ["BSA", "AML", "suspicious activity", "KYC", "source of funds"]},
    },
    {
        "title": "How do I set up account alerts and notifications?",
        "text": (
            "Account alerts are one of the most effective fraud prevention and account management "
            "tools available. Types of alerts: balance threshold (alert when balance drops below "
            "a set amount), large transaction (every transaction over $X), login alert (every "
            "account login), unusual activity (bank-identified fraud alerts), direct deposit "
            "received, payment processed, and statement available. How to set up: log in to "
            "online banking or open the mobile app; navigate to 'Alerts,' 'Notifications,' or "
            "'Account Settings'; select the alert types and thresholds; choose delivery method "
            "(email, SMS, push notification). Recommended setup: enable ALL transaction alerts "
            "via push notification — real-time visibility into every card transaction is the "
            "earliest possible fraud detection. Low balance alert at $200 prevents overdrafts. "
            "Login alert adds a second layer of account takeover detection. Most alerts are "
            "free; some banks charge for SMS alerts — check your account terms. Enable "
            "alerts immediately after opening any new account."
        ),
        "metadata": {"category": "Account Security", "tags": ["account alerts", "transaction notifications", "fraud detection", "push notification", "SMS alerts"]},
    },
    {
        "title": "How do I get a bank reference letter or verification letter?",
        "text": (
            "A bank reference letter or account verification letter confirms that you have an "
            "account in good standing at the institution. Common uses: rental applications "
            "(landlords verifying financial stability), visa applications, mortgage pre-qualification "
            "with another lender, business credit applications, and professional licensing. "
            "How to request: (1) Visit a branch and request the letter from a banker — typically "
            "ready same-day or within 24 hours. (2) Call customer service and request a written "
            "verification letter mailed to you. (3) Some banks allow requests through secure "
            "message in online banking. What the letter typically includes: account holder name, "
            "account type, account opening date, and a statement that the account is in good "
            "standing. Fees: typically $10–$25 for a formal reference letter; some accounts "
            "include this service free. For international use: request letterhead, original "
            "signature, and bank seal — many foreign institutions require these formalities."
        ),
        "metadata": {"category": "Account Services", "tags": ["bank reference letter", "verification letter", "account in good standing", "rental application", "visa application"]},
    },
    {
        "title": "What options do I have if I'm unhappy with my bank's service?",
        "text": (
            "If you're dissatisfied with your bank: (1) First, escalate internally. Ask to speak "
            "with a supervisor; write a formal complaint to the bank's official complaint address. "
            "Many issues resolve at this level. (2) File with the CFPB: for issues involving "
            "consumer protection violations (improper fees, unauthorized transactions, "
            "servicing errors). Companies respond to CFPB complaints within 15 days. "
            "(3) File with your state banking regulator: state-chartered banks are regulated "
            "by state banking departments — file at your state's banking department website. "
            "(4) File with the OCC (if nationally chartered bank): occ.gov customer assistance. "
            "(5) Consider switching: if service is consistently poor, explore credit unions "
            "(member-owned, typically better service), community banks (relationship-focused), "
            "or online banks (competitive rates, lower fees). Switching is easier than ever — "
            "most banks help you transfer direct deposit and automatic payments. Competition "
            "is your most powerful tool — banks compete for deposits and accounts."
        ),
        "metadata": {"category": "Complaint Resolution", "tags": ["bank complaint", "CFPB", "OCC", "state regulator", "switch banks"]},
    },
    {
        "title": "How do I request a copy of a check I wrote?",
        "text": (
            "Copies of canceled checks can be needed for: proof of payment to a landlord or "
            "contractor, tax documentation, dispute resolution, or legal proceedings. "
            "How to obtain: (1) Online banking: many banks maintain 7 years of check images "
            "accessible through your account history. Search by date or check number; "
            "download as PDF. (2) Mobile app: same check images typically accessible. "
            "(3) Monthly statements: some banks include check images in PDF statements. "
            "(4) Request from bank: call or visit a branch and request a specific check copy. "
            "Fee: $5–$15 per copy; often free in online banking self-service. Processing time: "
            "images are typically available immediately online; mailed copies take 7–10 days. "
            "For very old checks (beyond 7 years): banks are not required to retain records "
            "beyond their retention policy — some maintain longer records, some don't. "
            "Keep important check receipts (contracts, security deposits) as backup documentation."
        ),
        "metadata": {"category": "Account Services", "tags": ["check copy", "canceled check", "proof of payment", "check image", "tax documentation"]},
    },
    {
        "title": "What is a bank hold and how do I get it released?",
        "text": (
            "A bank hold restricts access to deposited funds while the bank verifies the deposit "
            "will clear. Hold lengths are governed by federal Regulation CC. Common reasons for "
            "extended holds: new account (open less than 30 days), large check (over $5,525), "
            "account with overdraft history, check from a bank in another country, or fraud "
            "suspicion. To request hold release: speak with a branch manager or call customer "
            "service. Explain why you need the funds urgently. Provide information that may "
            "reduce concern: the source and nature of the check, relationship to the payer, "
            "purpose of the funds. Bring the payer's contact information if possible. "
            "Branch managers have discretion to reduce hold periods. Documentation helps: "
            "if the check is from a business, bring the invoice or contract it relates to. "
            "If you regularly receive large checks: establish a longer banking history at the "
            "institution to reduce future holds. Wire transfers for large time-sensitive "
            "amounts avoid hold issues entirely."
        ),
        "metadata": {"category": "Deposits", "tags": ["hold release", "check hold", "Regulation CC", "branch manager", "deposit hold"]},
    },
    {
        "title": "How do I handle a banking issue while traveling internationally?",
        "text": (
            "International travel requires advance banking preparation: Before travel: "
            "(1) Notify your bank of travel dates and destinations — prevents security "
            "block on your card for 'unusual' international transactions. Many banks allow "
            "this through the app (card settings → travel notice). (2) Enable international "
            "use if required by your bank. (3) Verify PIN is active (some international "
            "transactions require chip-and-PIN). (4) Identify fee-free international ATM "
            "access: Schwab Bank reimburses all ATM fees worldwide. While traveling: "
            "(1) Use ATMs rather than currency exchange booths — better rates. (2) Choose "
            "'charge in local currency' (not USD) at point of sale — dynamic currency "
            "conversion is expensive. (3) If card is blocked: call the number on the back "
            "of the card (reverse charge international number is usually available); "
            "use the bank's app to unlock. Emergency: most banks can wire emergency funds "
            "or provide a temporary card number for digital purchases within 24 hours."
        ),
        "metadata": {"category": "Travel Banking", "tags": ["international travel", "travel notice", "foreign ATM", "card block", "dynamic currency conversion"]},
    },
    {
        "title": "How do I report suspected elder financial abuse at my bank?",
        "text": (
            "Elder financial abuse is one of the fastest-growing financial crimes — over $3 billion "
            "is stolen from seniors annually. Banks have specific protocols and legal obligations. "
            "If you suspect a customer is being exploited: (1) Bank employees are mandatory reporters "
            "in most states — they must report suspected exploitation to Adult Protective Services (APS) "
            "and/or state regulators. (2) Contact the bank directly: ask to speak with a fraud "
            "specialist or branch manager; describe the concerning activity. (3) Bank can: place "
            "a temporary hold on suspicious transactions (some state laws authorize this), contact "
            "the account's Trusted Contact Person, flag the account for enhanced monitoring. "
            "External reporting: (1) Adult Protective Services: your county APS handles adult "
            "exploitation cases. (2) Local law enforcement for theft or fraud. (3) Consumer "
            "Financial Protection Bureau (for bank-specific issues). Signs of elder financial "
            "abuse: sudden large withdrawals, new persons accompanying the elder, changes to "
            "beneficiary designations, confusion about finances."
        ),
        "metadata": {"category": "Elder Protection", "tags": ["elder financial abuse", "APS", "mandatory reporting", "trusted contact", "financial exploitation"]},
    },
    {
        "title": "How do I set up a trust account at a bank?",
        "text": (
            "A bank trust account holds assets managed by a trustee for beneficiaries. Types of "
            "trust accounts: (1) Revocable living trust account: grantor maintains control during "
            "lifetime; avoids probate at death. (2) Irrevocable trust account: assets permanently "
            "transferred; protects from creditors, reduces estate taxes. (3) Testamentary trust: "
            "created by a will; established at death. (4) Special needs trust: holds assets for "
            "a disabled beneficiary without disqualifying them from government benefits. "
            "To open a trust account at a bank: bring the complete trust document (or a "
            "certification of trust — a shorter document the trustee can certify), trustee's "
            "government ID, EIN if the trust requires one (irrevocable trusts) or SSN for "
            "revocable trusts. The account is titled '[Trustee Name] as Trustee of [Trust Name].' "
            "FDIC coverage: $250,000 per beneficiary (up to 5 beneficiaries) = up to $1.25M "
            "coverage at one bank. See an estate attorney to create the trust document before "
            "opening the account."
        ),
        "metadata": {"category": "Specialty Accounts", "tags": ["trust account", "revocable trust", "trustee", "estate planning", "FDIC"]},
    },
    {
        "title": "How can I speak to a real person at my bank quickly?",
        "text": (
            "Navigating IVR menus to reach a live agent faster: (1) Most systems respond to "
            "saying 'agent,' 'representative,' 'human,' or 'operator.' (2) Pressing '0' or "
            "'0#' repeatedly often bypasses menus or reaches an operator. (3) After each "
            "menu option, pressing '0' may route to an agent. (4) The GetHuman website "
            "(gethuman.com) maintains bank-specific shortcuts for reaching live agents at major "
            "banks. Alternative channels: live chat through the bank's app or website often "
            "has shorter wait times than phone. Timing: early morning (8–9 AM local), "
            "mid-afternoon (2–3 PM), and late evening have lower wait times; avoid "
            "Monday mornings and post-holiday days. Specific services require specific numbers: "
            "card fraud line (always answered faster), home loan servicing, and business "
            "banking each have dedicated numbers — check the website for the right number. "
            "If wait is too long: request a callback (most banks offer this) so you don't "
            "lose your place in line."
        ),
        "metadata": {"category": "Customer Service", "tags": ["reach live agent", "customer service", "IVR bypass", "callback", "wait time"]},
    },
    {
        "title": "What are my rights if a bank denies my account application?",
        "text": (
            "If a bank denies your account application, you have rights under several federal laws. "
            "Adverse action notice: if denied based on a ChexSystems or credit report, the bank "
            "must provide a written adverse action notice identifying the consumer reporting "
            "agency used. You then have the right to request a free copy of that report "
            "from the agency within 60 days. Fair Credit Reporting Act (FCRA): dispute any "
            "inaccurate information in the ChexSystems or credit report used in the decision. "
            "Equal Credit Opportunity Act (ECOA) and Fair Housing Act: prohibit denial based "
            "on race, color, religion, national origin, sex, marital status, age, or receipt "
            "of public assistance. If you believe you were denied discriminatorily, file with "
            "the CFPB and/or your state AG. Alternatives to denial: ask about second-chance "
            "accounts, credit union membership, or Bank On certified accounts. "
            "The bank is not required to explain specifically why beyond the adverse action notice."
        ),
        "metadata": {"category": "Account Access", "tags": ["account denial", "adverse action notice", "ChexSystems", "FCRA", "ECOA"]},
    },
    {
        "title": "What is a bank's hold harmless letter?",
        "text": (
            "A hold harmless letter (also called an indemnification letter) is a bank document "
            "where the bank releases itself from liability for following a customer's specific "
            "instructions. Situations where banks may request one: when a customer requests an "
            "unusual transaction against the bank's advice, when releasing escrow funds under "
            "dispute, when honoring a check the bank has concerns about, or when a customer "
            "waives their right to fraud investigation. As a customer: carefully consider "
            "before signing any hold harmless letter — you're agreeing that if something "
            "goes wrong, you won't hold the bank responsible. If a bank employee asks you "
            "to sign one related to a wire or large transfer that seems unusual: pause and "
            "consider whether the transaction is something you fully understand and intend. "
            "Do not sign under pressure or urgency. Consult an attorney for significant "
            "transactions. Legitimate banks rarely use hold harmless letters for routine "
            "customer transactions."
        ),
        "metadata": {"category": "Banking Documents", "tags": ["hold harmless letter", "indemnification", "liability waiver", "bank documents", "fraud risk"]},
    },
    {
        "title": "How do I request an official bank statement for a loan application?",
        "text": (
            "Lenders typically require 2–3 months of bank statements for loan applications "
            "(mortgages, personal loans, auto loans, business loans). Statement requirements: "
            "must show account holder name, account number, all deposits and transactions, "
            "beginning and ending balances. Formats accepted: (1) Online PDF download: most "
            "lenders accept digitally downloaded PDFs from your online banking portal — these "
            "are considered official as they come directly from the bank's system. Download "
            "from the statements section of online banking. (2) Printed bank statement: "
            "brought from the branch, typically requires teller date stamp for mortgage "
            "applications. (3) Official bank letter with stamps: some international lenders "
            "require this. Mortgage-specific: underwriters look for: large unusual deposits "
            "(must explain source of funds), consistent direct deposit (employment verification), "
            "overdraft history, and minimum balance requirements. Large cash deposits "
            "within 60 days of application require documentation of source."
        ),
        "metadata": {"category": "Account Services", "tags": ["bank statement", "loan application", "mortgage", "PDF statement", "official statement"]},
    },
    {
        "title": "What do I do if the bank made an error on my account?",
        "text": (
            "Bank errors — while rare — do occur. Common errors: incorrect fee charges, "
            "duplicate transactions, missed deposits, or payment processing errors. "
            "Steps to resolve: (1) Document the error: take a screenshot or note the exact "
            "amounts, dates, and transaction descriptions involved. (2) Contact the bank "
            "immediately: phone customer service or visit a branch. Explain calmly and "
            "specifically what the error is. (3) Request a supervisor if the front-line "
            "agent cannot resolve it immediately. (4) If the error involves a fee: ask "
            "for immediate reversal — most fee errors are corrected on the spot. (5) If "
            "involving a transaction: open a formal dispute. (6) Follow up in writing: "
            "send a secure message confirming your report of the error and the resolution "
            "agreed upon. Banks have a duty of care and must correct errors. If the bank "
            "refuses to correct a clear error: file with the CFPB. Keep all documentation. "
            "Legal remedies: the Electronic Fund Transfer Act allows recovery of consequential "
            "damages from bank errors that cause additional financial harm."
        ),
        "metadata": {"category": "Error Resolution", "tags": ["bank error", "incorrect fee", "duplicate transaction", "dispute", "CFPB"]},
    },
]

MARKET_COMMENTARY = [
    {
        "title": "The Transformation of Bank Customer Service: AI and Human Balance",
        "text": (
            "Banking customer service is undergoing a fundamental transformation driven by AI, "
            "with banks investing heavily in chatbots and virtual assistants while maintaining "
            "human agents for complex needs. Current state: AI chatbots handle 40–60% of all "
            "customer service interactions at large banks (balance inquiries, payment status, "
            "branch hours, basic troubleshooting). Human agents focus on complex issues, "
            "emotional situations (fraud trauma, bereavement banking), and sales. "
            "AI quality improvements: first-generation chatbots frustrated customers with "
            "inability to handle nuance. Second-generation large language model based chatbots "
            "(GPT-4 class) can handle much more complex conversations with higher satisfaction "
            "rates. Customer sentiment: most customers are comfortable with AI for simple "
            "tasks but strongly prefer human agents for financial advice, disputes, and "
            "sensitive issues. The optimal design: AI handles speed and volume; human agents "
            "handle complexity and empathy."
        ),
        "metadata": {"period": "2024-2025", "topic": "Customer Service Technology", "tags": ["AI customer service", "chatbot", "human agents", "digital banking", "customer experience"]},
    },
    {
        "title": "Rising Bank Fraud: How Institutions Are Fighting Back",
        "text": (
            "Bank fraud losses are rising despite improved detection capabilities — consumer "
            "fraud losses to the top 20 U.S. banks exceeded $10 billion in 2023. The fastest "
            "growing fraud types: authorized push payment (APP) fraud where customers are "
            "socially engineered into sending money; account takeover fraud (credential theft); "
            "synthetic identity fraud (combining real and fake identity information); and "
            "check fraud (resurging due to mail theft). Bank countermeasures: real-time "
            "AI transaction scoring (every transaction evaluated in milliseconds), "
            "behavioral biometrics (typing patterns, device fingerprints), network-level "
            "fraud intelligence sharing, customer education campaigns, and friction "
            "introduction for unusual high-value transactions (mandatory call-backs). "
            "Regulatory pressure: CFPB pushing banks to expand reimbursement for APP fraud. "
            "UK's Faster Payments Service mandates reimbursement for most APP fraud — "
            "U.S. regulators are watching the UK model closely."
        ),
        "metadata": {"period": "2024-2025", "topic": "Bank Fraud Prevention", "tags": ["bank fraud", "APP fraud", "account takeover", "check fraud", "fraud prevention"]},
    },
    {
        "title": "The State of Banking Accessibility for Underserved Populations",
        "text": (
            "Despite progress, approximately 5 million U.S. households remain unbanked (no bank "
            "account), and 18 million are underbanked (have an account but rely on alternative "
            "financial services). Underbanked populations disproportionately include lower-income "
            "households, Black and Hispanic households, younger adults, and individuals with "
            "disabilities. Progress being made: the Bank On program (Cities for Financial "
            "Empowerment Fund) has certified 200+ bank and credit union account products as "
            "meeting low-fee, minimum feature standards — providing banking access without "
            "barriers. The FDIC's Mission-Driven Bank Fund supports Minority Depository "
            "Institutions (MDIs) and Community Development Financial Institutions (CDFIs). "
            "Challenges: ChexSystems records, lack of required documents (ID, address "
            "verification), and distrust of financial institutions. Community outreach, "
            "multilingual banking, and financial literacy programs are critical for closing "
            "the access gap."
        ),
        "metadata": {"period": "2024-2025", "topic": "Financial Inclusion", "tags": ["unbanked", "underbanked", "Bank On", "CDFI", "financial inclusion"]},
    },
    {
        "title": "Social Engineering: The Human Element of Banking Fraud",
        "text": (
            "Social engineering has replaced technical hacking as the primary method for banking "
            "fraud. Criminals exploit human psychology rather than technical vulnerabilities: "
            "urgency and fear ('your account is compromised, act NOW'), authority ('I'm from "
            "the FBI/IRS/bank fraud department'), scarcity ('this is your last chance'), and "
            "trust ('I'm calling because I noticed suspicious activity'). Common scripts: "
            "bank impersonation (call appearing to come from your bank asking you to verify "
            "or transfer funds), government impersonation (IRS, Social Security, Medicare), "
            "grandparent scam (pretending to be a grandchild in trouble), romance scam, "
            "tech support scam. Consumer defenses: hang up and call back on a known number; "
            "legitimate organizations NEVER request wire transfer, gift cards, or Zelle "
            "payment over the phone; be especially skeptical of urgency and secrecy requests. "
            "Banks are training employees to recognize and interrupt social engineering "
            "scripts at the teller and phone level."
        ),
        "metadata": {"period": "2024-2025", "topic": "Fraud Awareness", "tags": ["social engineering", "fraud awareness", "bank impersonation", "scam prevention", "consumer education"]},
    },
    {
        "title": "Customer Experience Benchmarks: Who's Winning in Banking Satisfaction",
        "text": (
            "J.D. Power's annual U.S. Retail Banking Satisfaction Study provides annual rankings "
            "of bank customer satisfaction. 2024 highlights: regional and community banks "
            "consistently outperform large national banks on satisfaction scores; USAA (military "
            "and family members) leads all banks for the 18th consecutive year; credit unions "
            "score higher than commercial banks overall. Key satisfaction drivers: digital "
            "banking experience (app functionality and reliability), problem resolution speed, "
            "proactive communication about accounts and relevant offers, and branch/human "
            "accessibility when needed. Large bank performance: Capital One and Chase lead "
            "large bank category; Wells Fargo has improved significantly after its account "
            "scandal recovery. The trend: satisfaction correlates strongly with digital "
            "experience quality for younger customers and with branch availability for older "
            "customers. One-size-fits-all approaches fail both segments."
        ),
        "metadata": {"period": "2024-2025", "topic": "Customer Satisfaction", "tags": ["banking satisfaction", "JD Power", "USAA", "credit union", "customer experience"]},
    },
    {
        "title": "Regulatory Changes Affecting Bank Customer Protections in 2025",
        "text": (
            "2024–2025 has seen significant regulatory activity impacting consumer banking: "
            "(1) CFPB credit card late fee rule: proposed cap of $8 on credit card late fees "
            "(versus current average $32) was struck down by a federal court in 2024 — the "
            "status is under appeals. (2) Open banking rule (1033): finalized, requiring banks "
            "to provide consumer-authorized data access to third parties by 2026–2030 (phased). "
            "(3) CFPB overdraft rule: proposed limits on overdraft fees at large banks "
            "($3–$14 versus current $35). (4) Zelle/APP fraud: CFPB signaling more prescriptive "
            "guidance on Authorized Push Payment fraud reimbursement. (5) AI in lending: "
            "increased scrutiny of AI-based underwriting for fair lending compliance. "
            "These regulatory changes reflect a consistent consumer protection trend. "
            "Banks are adapting proactively — many have already reduced overdraft fees ahead "
            "of mandated changes to preempt regulatory action."
        ),
        "metadata": {"period": "2024-2025", "topic": "Banking Regulation", "tags": ["CFPB", "regulatory changes", "overdraft rule", "credit card fees", "open banking"]},
    },
    {
        "title": "Mental Health and Financial Stress: How Banks Are Responding",
        "text": (
            "Financial stress is one of the leading causes of anxiety, depression, and relationship "
            "problems. 60%+ of Americans report financial stress as a top concern. Banks are "
            "increasingly acknowledging the emotional dimension of financial services. Progressive "
            "banks are: training customer service agents in empathetic communication for customers "
            "in financial distress; partnering with financial wellness organizations; providing "
            "connections to financial counseling through EAP (Employee Assistance Program) "
            "networks; offering hardship programs proactively rather than waiting for customers "
            "to ask. Some banks have implemented 'financial wellbeing scores' that proactively "
            "identify customers who may be heading toward financial stress (increasing credit "
            "card utilization, declining savings, increasing overdrafts) and reach out with "
            "support resources before crisis hits. NFCC-member credit counselors and HUD-approved "
            "housing counselors provide free or low-cost professional support for customers "
            "in financial difficulty."
        ),
        "metadata": {"period": "2024-2025", "topic": "Financial Wellbeing", "tags": ["financial stress", "mental health", "financial counseling", "hardship support", "bank wellness programs"]},
    },
    {
        "title": "Check Fraud Renaissance: Why Paper Check Crime Is Surging",
        "text": (
            "Despite the general decline of paper check usage, check fraud has surged dramatically — "
            "increasing over 150% since 2021 according to FinCEN data. The catalyst: organized "
            "crime groups discovered that USPS mail theft combined with check washing "
            "(chemically erasing and rewriting a stolen check's details) creates an efficient "
            "fraud pipeline. Key fraud types: check washing (stolen personal or business checks "
            "altered), counterfeit checks (exact reproductions of real checks), and official "
            "check fraud. Industries most affected: small businesses, landlords, law firms. "
            "Prevention measures: use gel-ink pens (much harder to wash than ballpoint). "
            "Use ACH, Zelle, or wire for high-value payments instead of mailing checks. "
            "Use USPS Informed Delivery to track incoming mail. Consider a USPS PO Box for "
            "business checks. Report stolen mail to USPS Postal Inspection Service. "
            "The OCC and FinCEN have issued advisories urging banks to apply positive pay "
            "and enhanced verification for check deposits."
        ),
        "metadata": {"period": "2024-2025", "topic": "Check Fraud", "tags": ["check fraud", "check washing", "mail theft", "USPS", "positive pay"]},
    },
    {
        "title": "Digital Banking for the Underbanked: Progress and Challenges",
        "text": (
            "Fintech companies and neobanks have made the most progress in serving underbanked "
            "populations. Chime's SpotMe (fee-free overdraft up to $200), Early Pay (2 days "
            "early direct deposit), and Credit Builder (secured card with automatic on-time "
            "reporting) have been particularly impactful for lower-income users who were "
            "underserved by traditional banks. CashApp's banking services provide broad access "
            "with minimal requirements. Challenges: (1) Neobanks are not banks — most hold "
            "deposits at partner banks with FDIC pass-through insurance; the pass-through "
            "arrangement broke down in several high-profile cases (Synapse Financial "
            "Technologies bankruptcy, 2024) where customers lost access to funds. "
            "(2) Customer service for neobanks is often inferior to traditional banks for "
            "complex issues. (3) Credit-building products require consistent usage habits "
            "to be effective. The lesson: neobanks serve important access functions but "
            "consumers should understand the underlying deposit structure and customer "
            "service limitations."
        ),
        "metadata": {"period": "2024-2025", "topic": "Financial Inclusion", "tags": ["neobank", "underbanked", "Chime", "CashApp", "Synapse bankruptcy"]},
    },
    {
        "title": "Scam Trends: What Banking Customers Need to Know in 2025",
        "text": (
            "Banking scams are becoming more sophisticated and harder to detect. Top scam "
            "categories affecting bank customers: (1) AI voice cloning — fraudsters clone "
            "the voice of a family member or bank representative using AI, creating highly "
            "convincing audio to request urgent transfers. (2) QR code phishing — malicious "
            "QR codes redirect to fake bank login pages. (3) Fake check scams — sophisticated "
            "counterfeit checks deposited, then requesting return of 'overpayment' before "
            "the check bounces. (4) Pig butchering investment scams — long-term romance/trust "
            "building leading to large crypto transfers. (5) Lottery/prize scams requiring "
            "fees before 'releasing winnings.' Defense framework: establish a family 'safe word' "
            "for voice calls; never scan unknown QR codes for banking; wait 10+ business days "
            "before acting on deposited check proceeds; never send money to strangers; "
            "be extraordinarily skeptical of investment 'opportunities' found online. "
            "Scam sophistication is growing faster than most consumers' awareness."
        ),
        "metadata": {"period": "2025", "topic": "Scam Prevention", "tags": ["scam trends", "AI voice cloning", "QR phishing", "pig butchering", "fake check"]},
    },
]

CLIENT_SCENARIOS = [
    {
        "title": "Case Study: Resolving an Unauthorized $1,200 Credit Card Charge",
        "text": (
            "Profile: Jennifer, 42, noticed a $1,200 charge from an unfamiliar electronics "
            "retailer on her credit card statement. She had not made this purchase.\n\n"
            "Resolution timeline: Day 1: Jennifer called her credit card company's fraud line "
            "— 10 minutes wait. Agent confirmed she did not authorize the charge, cancelled her "
            "card immediately, and issued a provisional credit of $1,200 to her account within "
            "1 business day. New card expedited (2-day delivery). Day 3: Investigation team "
            "contacted the merchant, who confirmed the purchase was made from a different IP "
            "address and shipping address than Jennifer's account history. Day 12: Merchant "
            "confirmed the chargeback; $1,200 credit made permanent. Jennifer changed all "
            "passwords where the card was stored (Amazon, Netflix, etc.) and enrolled in "
            "credit monitoring. Lesson: credit cards provide superior fraud protection — "
            "provisional credit, strong FCBA rights, and zero liability policies make "
            "them preferable to debit cards for online purchases."
        ),
        "metadata": {"scenario_type": "Fraud Resolution", "tags": ["credit card fraud", "unauthorized charge", "chargeback", "provisional credit", "FCBA"]},
    },
    {
        "title": "Case Study: Elderly Customer Targeted by IRS Impersonation Scam",
        "text": (
            "Profile: George, 78, received a phone call from someone claiming to be an IRS "
            "agent saying he owed $4,500 in back taxes and would be arrested unless he "
            "paid immediately via wire transfer.\n\n"
            "What happened at the bank: George went to his branch to wire $4,500. A trained "
            "teller noticed several red flags: urgency, an unusual request for George (no "
            "prior wires), and a story involving government debt payment via wire. The teller "
            "excused herself, spoke with the branch manager, and returned to explain to George "
            "that the IRS does NOT demand wire transfers and this had the characteristics of "
            "a common scam. George was reluctant at first but agreed to call the IRS directly "
            "using the number from irs.gov (not the number the caller had given). The IRS "
            "confirmed no balance was owed. George was deeply grateful. The bank filed a "
            "suspicious activity report. Lesson: bank staff are often the last line of defense "
            "against elder fraud. Enabling a trusted contact on George's account provides "
            "an additional layer of protection going forward."
        ),
        "metadata": {"scenario_type": "Scam Prevention", "tags": ["IRS scam", "elder fraud", "branch intervention", "wire fraud prevention", "trusted contact"]},
    },
    {
        "title": "Case Study: Technical Issue — Duplicate ACH Charges from Utility Company",
        "text": (
            "Profile: Sarah, 35, set up autopay with her electric utility. The utility company "
            "accidentally ran the ACH debit twice ($187.43 each), overdrafting her account and "
            "triggering an overdraft fee ($35).\n\n"
            "Resolution steps: (1) Contacted the utility company first — confirmed the error "
            "within 10 minutes and initiated a reversal ACH for the duplicate charge. "
            "Appeared in her account in 2 business days. (2) Called her bank to dispute the "
            "overdraft fee caused by the duplicate charge: 'I was overdrafted due to a "
            "vendor ACH error, not my own spending.' Bank waived the $35 fee immediately "
            "as a one-time courtesy. (3) Sarah set up a low-balance alert ($200 minimum) "
            "so she'll be notified before any transaction risks overdrafting. (4) She also "
            "set up a linked savings account as overdraft backup. Total out-of-pocket cost: $0. "
            "Timeline: resolved within 3 business days. Key takeaway: proactive, polite "
            "escalation to both the vendor and the bank resolved this efficiently. "
            "Keeping records of autopay amounts helps identify discrepancies quickly."
        ),
        "metadata": {"scenario_type": "Technical Issue", "tags": ["duplicate ACH", "utility autopay", "overdraft fee waiver", "ACH reversal", "account alerts"]},
    },
    {
        "title": "Case Study: Rebuilding After Account Compromise",
        "text": (
            "Profile: Michael, 29, discovered his online banking credentials had been stolen "
            "and used to transfer $3,500 to an external account he didn't recognize.\n\n"
            "Response and recovery: (1) Called bank immediately — account frozen within 2 hours "
            "of the fraudulent transfer. Bank initiated wire recall. (2) Changed passwords for "
            "online banking and all accounts using the same password (password manager installed). "
            "Enabled 2FA via authenticator app on all financial accounts. (3) Placed fraud "
            "alerts at all three credit bureaus (free). (4) Filed Regulation E dispute — bank "
            "provisionally credited $3,500 within 2 business days while investigating. "
            "(5) Wire recall was partially successful: $1,800 of the $3,500 was recovered "
            "before withdrawal. The remaining $1,700 was covered by the bank under their "
            "zero-liability fraud policy after investigation confirmed Michael did not "
            "authorize the transfer. (6) Michael enrolled in the bank's credit monitoring "
            "service and scheduled a comprehensive account security review. Total loss: $0. "
            "Time to resolve: 3 weeks for full investigation completion."
        ),
        "metadata": {"scenario_type": "Account Recovery", "tags": ["account compromise", "account takeover", "Reg E", "zero liability", "credential theft"]},
    },
    {
        "title": "Case Study: Navigating an ATM Dispute",
        "text": (
            "Profile: Carlos, 44, used an ATM at a convenience store to withdraw $300. "
            "The machine displayed 'Transaction Complete' but dispensed no cash.\n\n"
            "Dispute process: (1) Carlos immediately called his bank's 24/7 line — reported "
            "the failed ATM dispense, provided the ATM location and approximate time. "
            "(2) Bank opened an ATM dispute investigation under Regulation E. Provisional "
            "credit of $300 issued within 5 business days. (3) The bank contacted the ATM "
            "operator (a third-party ATM company, not his bank). ATM operator sent their "
            "technician to 'balance' the machine — counting cash against expected amounts. "
            "(4) The ATM was found to be 'long' by $300 (it had $300 more than expected — "
            "consistent with a failed dispense). (5) Investigation confirmed in Carlos's "
            "favor: provisional credit made permanent. Total timeline: 18 business days "
            "for final resolution. Lessons: always note the ATM's location, ID number, "
            "and exact time; your phone's timestamp can serve as evidence; ATM disputes "
            "take longer when a third-party ATM is involved versus a bank-owned ATM."
        ),
        "metadata": {"scenario_type": "ATM Dispute", "tags": ["ATM dispute", "failed dispense", "Regulation E", "ATM operator", "provisional credit"]},
    },
    {
        "title": "Case Study: First-Time Homebuyer Needing Bank Statement Documentation",
        "text": (
            "Profile: Ana, 31, applying for an FHA mortgage. Loan officer requested 3 months "
            "of bank statements. Ana is concerned about two large deposits that weren't from "
            "her payroll.\n\n"
            "Documentation strategy: The two large deposits: $5,000 from selling her car "
            "and $3,000 gifted by her mother toward the down payment. Mortgage underwriters "
            "must document the source of all large deposits (over 50% of monthly income). "
            "Documentation provided: (1) For car sale: bill of sale for the vehicle showing "
            "the $5,000 sale price, matching the deposit date. (2) For gift: a gift letter "
            "signed by Ana's mother stating the $3,000 is a gift (not a loan), the donor's "
            "name, address, relationship, and that no repayment is required. FHA-specific: "
            "gifts must be from acceptable donors (family, employer, nonprofit). "
            "The loan officer confirmed these were fully acceptable — no issues. "
            "Ana learned: having documentation ready when applying accelerates the mortgage "
            "process. Large cash deposits without documentation cause underwriting delays "
            "or denial."
        ),
        "metadata": {"scenario_type": "Mortgage Documentation", "tags": ["bank statements", "mortgage", "gift letter", "large deposit", "FHA documentation"]},
    },
    {
        "title": "Case Study: Handling Banking During a Divorce",
        "text": (
            "Profile: Rachel, 44, going through a divorce. She and her husband have joint "
            "checking and savings accounts at their bank. She needs to separate finances "
            "while protecting her interests.\n\n"
            "Account transition strategy: (1) Open individual accounts immediately — Rachel "
            "opened a new individual checking account (same bank for easy transfer) and "
            "redirected her direct deposit. (2) Consult an attorney before closing joint "
            "accounts — freezing is possible, but unilateral closure could create legal "
            "complications depending on divorce decree. In many states, marital funds cannot "
            "be unilaterally removed during divorce proceedings. (3) Attorney advised Rachel "
            "to document joint account balances on a specific date for divorce proceedings. "
            "(4) Update all beneficiary designations on accounts, life insurance, and "
            "retirement accounts immediately — remove soon-to-be-ex-spouse. "
            "(5) Update authorized users on any credit cards. (6) Alert her bank's security "
            "team about the situation — they can flag any unusual activity. (7) Set up "
            "separate accounts for children's expenses if co-parenting. Lesson: move "
            "quickly on beneficiary updates — this is often more important than the accounts."
        ),
        "metadata": {"scenario_type": "Life Transition", "tags": ["divorce banking", "joint account separation", "beneficiary update", "financial separation", "divorce"]},
    },
    {
        "title": "Case Study: Managing Banking for an Elderly Parent with Dementia",
        "text": (
            "Profile: David, 52, his mother Carol, 80, has been diagnosed with early-stage "
            "dementia. David needs to help manage her finances while Carol still has legal "
            "capacity to grant authority.\n\n"
            "Transition plan executed while Carol had capacity: (1) Estate attorney prepared "
            "a Durable Power of Attorney (DPOA) with Carol's full understanding and consent. "
            "(2) David took the DPOA to Carol's bank — presented certified DPOA copy; bank "
            "reviewed and accepted; David added as authorized signer on checking account. "
            "(3) Trusted Contact: David added as trusted contact on all accounts. "
            "(4) Transaction limits: bank reduced Carol's ATM daily limit to $200; "
            "added a callback requirement for any wire transfers. (5) Alerts: all transaction "
            "alerts set to notify David's email/phone. (6) Investment accounts: financial "
            "advisor met with both Carol and David; David was added as authorized agent on "
            "investment accounts with the DPOA. Three months later, Carol's dementia "
            "progressed significantly. Because the legal groundwork was in place, David "
            "could seamlessly manage all of Carol's finances without court intervention."
        ),
        "metadata": {"scenario_type": "Elder Account Management", "tags": ["dementia", "power of attorney", "elder banking", "account management", "cognitive decline"]},
    },
    {
        "title": "Case Study: New Immigrant Successfully Opening a Bank Account",
        "text": (
            "Profile: Fatima, 27, recently arrived from Somalia on a refugee visa. She has no "
            "U.S. credit history, an ITIN (not yet a SSN), and limited English. She was "
            "turned away from two large banks.\n\n"
            "Successful path: (1) A social worker referred Fatima to a local credit union "
            "with a community development mission that specifically serves immigrant populations. "
            "(2) The credit union accepted: ITIN, refugee documentation (I-94), secondary ID "
            "(Somali national ID), and proof of address (letter from refugee resettlement "
            "agency). (3) With a Somali-speaking staff member's assistance, Fatima opened "
            "a basic savings account and a 'second chance' checking account with no overdraft. "
            "(4) After 6 months of consistent positive use, she qualified for a secured credit "
            "card through the credit union — beginning her U.S. credit history. (5) 12 months "
            "later: 680 credit score, unsecured credit card, eligible for a standard checking "
            "account. The credit union's mission-driven approach made banking access possible "
            "where commercial banks refused. ITIN plus secondary ID is sufficient documentation "
            "at many institutions."
        ),
        "metadata": {"scenario_type": "Banking Access", "tags": ["immigrant banking", "ITIN", "refugee", "credit union", "credit building"]},
    },
    {
        "title": "Case Study: Tech Support Scam Targeting Online Banking",
        "text": (
            "Profile: Robert, 68, was browsing the web when a popup appeared warning his "
            "computer was infected and providing a 1-800 number to call for 'Microsoft support.' "
            "He called and was asked to install remote access software.\n\n"
            "What the scammers did: After gaining remote access, the scammers navigated to "
            "Robert's open banking session and initiated a $5,000 wire transfer. They then "
            "called Robert's bank impersonating the bank, claiming to have blocked the wire "
            "and asking Robert to 'confirm' it by providing his one-time code (2FA code sent "
            "by the bank). Robert provided the code, which verified the wire.\n\n"
            "Response and outcome: Robert realized something was wrong when his bank balance "
            "changed. He called the bank immediately. The wire had cleared; a recall was "
            "initiated. The receiving bank was contacted through IC3; $3,200 was recovered. "
            "Robert's bank reimbursed the remaining $1,800 under their fraud policy given the "
            "circumstances. Robert's devices were wiped and restored. Lessons: never provide "
            "a 2FA code to anyone who calls YOU; tech companies never call you with unsolicited "
            "warnings; never allow remote access to your computer for unsolicited requests."
        ),
        "metadata": {"scenario_type": "Scam Recovery", "tags": ["tech support scam", "remote access", "wire fraud", "2FA bypass", "Microsoft scam"]},
    },
    {
        "title": "Case Study: CFPB Complaint Resolving an Unjust Bank Denial",
        "text": (
            "Profile: Marcus, 41, a Black business owner, applied for a small business line "
            "of credit at a national bank. Despite strong financials ($280,000 annual revenue, "
            "good credit score), he received a denial with vague reasons. His white business "
            "partner with similar financials was approved at the same bank.\n\n"
            "Action taken: (1) Marcus requested the specific adverse action reasons in writing "
            "— bank provided generic risk criteria. (2) Marcus filed a CFPB complaint "
            "detailing the circumstances and requesting a fair lending review. (3) Marcus "
            "also filed a complaint with the OCC (the bank was nationally chartered). "
            "(4) The OCC opened a fair lending investigation. (5) Within 60 days, the bank "
            "contacted Marcus and offered to reconsider his application with a senior credit "
            "officer. (6) Upon reconsideration, the line of credit was approved. The bank "
            "also conducted an internal review of similar cases. Lesson: the CFPB and OCC "
            "complaints created documented accountability. Fair lending is the law — ECOA "
            "and the Fair Housing Act prohibit discrimination in credit on protected "
            "characteristics. Use regulatory channels when other remedies fail."
        ),
        "metadata": {"scenario_type": "Discrimination Complaint", "tags": ["CFPB complaint", "fair lending", "ECOA", "racial discrimination", "OCC complaint"]},
    },
    {
        "title": "Case Study: Student Managing Banking for Study Abroad",
        "text": (
            "Profile: Emma, 21, spending a semester in Germany. She has a Chase checking "
            "account and is worried about banking fees while abroad.\n\n"
            "Preparation and execution: (1) Reviewed Chase's international fee structure: "
            "3% foreign transaction fee on debit purchases; $5 ATM fee + 3% conversion. "
            "These fees would significantly add up over 4 months. (2) Opened a Charles "
            "Schwab High Yield Investor Checking account — no foreign transaction fees, "
            "all ATM fees reimbursed worldwide. Funded with $3,000 from her Chase account "
            "before departure. (3) Notified both Chase and Schwab of her travel to Germany "
            "(dates and locations) to prevent security blocks. (4) In Germany: used Schwab "
            "debit card for ATM withdrawals (always chose local currency, not USD to avoid "
            "dynamic currency conversion). Avoided using Chase debit entirely while abroad. "
            "(5) Emergency: set up international calling on her phone plan to contact "
            "banks if needed. Estimated savings vs. using Chase abroad: $150–$300 over "
            "4 months. Schwab checking is widely recommended for international students "
            "and travelers for exactly this reason."
        ),
        "metadata": {"scenario_type": "International Banking", "tags": ["study abroad", "Schwab checking", "ATM fee reimbursement", "foreign transaction fee", "international banking"]},
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
