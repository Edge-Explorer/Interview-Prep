# Company Intelligence Database

**Data Curated & Authored by: Karan Shelar**

This folder contains the curated company interview intelligence database.

## 📁 Files

- **`company_profiles.json`** - The main database (currently 383 companies)
- **`company_template.json`** - Template for adding new companies

## 🆕 How to Add a New Company

### Method 1: Using the Helper Script (Recommended)

1. Open `backend/add_company.py`
2. Edit the `NEW_COMPANY` dictionary at the top
3. Run: `python add_company.py`
4. Test: `python test_company_intel.py`

### Method 2: Manual Edit

1. Open `company_profiles.json`
2. Copy the template from `company_template.json`
3. Paste it inside the `"companies"` section
4. Fill in all the details
5. Update `"total_companies"` count in `"meta"` section
6. Save the file

## 📋 Company Structure

Each company should have:

```json
{
    "CompanyName": {
        "name": "Full Company Name",
        "industry": "Industry/Sector",
        "size": "Small/Medium/Large",
        "interview_style": "Style description",
        "difficulty_level": "Medium/High/Very High",
        "cultural_values": ["Value1", "Value2", ...],
        "interview_rounds": {
            "Technical": { ... },
            "Behavioral": { ... },
            "System Design": { ... }
        },
        "red_flags": ["Flag1", "Flag2", ...],
        "average_process_duration": "X-Y weeks",
        "interview_count": "X-Y rounds"
    }
}
```

## 🏢 Current Companies by Domain (383 Total)

### Engineering & Tech (134 Companies)
- Google, Amazon, Microsoft, Nvidia, Meta, Apple, Netflix, Salesforce, Tesla, OpenAI, Anthropic, DeepMind, Snowflake, Databricks, Vercel, Stripe.

### Healthcare & Medical (22 Companies)
- Pfizer, Mayo Clinic, Johnson & Johnson, UnitedHealth Group, Novartis, Roche, Merck, Sanofi, AstraZeneca, GSK, Eli Lilly.

### Finance & Accounting (22 Companies)
- Goldman Sachs, JPMorgan, Morgan Stanley, BlackRock, Visa, Mastercard, AMEX, PayPal, Square, Robinhood, Coinbase.

### Legal (22 Companies)
- Kirkland & Ellis, DLA Piper, Baker McKenzie, Skadden, Latham & Watkins, Clifford Chance, Freshfields, Allen & Overy, Linklaters.

### Construction & Trades (23 Companies)
- AECOM, Caterpillar, John Deere, Bechtel, Turner Construction, Larsen & Toubro, Tata Projects, Jacobs Solutions, Vinci, Skanska.

### Creative & Design (21 Companies)
- Pixar, DreamWorks, Industrial Light & Magic (ILM), Electronic Arts, Ubisoft, Nintendo, Adobe, Figma, Canva, Spotify, SoundCloud.

### Education & Training (21 Companies)
- Coursera, Udacity, Khan Academy, Duolingo, Chegg, MasterClass, Codecademy, Harvard University, Stanford, MIT (Tech roles).

### Science & Research (22 Companies)
- NASA, CERN, SpaceX, Blue Origin, DeepMind, ISRO, Argonne National Lab, Oak Ridge Lab, Max Planck Society, RIKEN, CSIRO.

### Social Services & Non-Profits (23 Companies)
- UNICEF, Bill & Melinda Gates Foundation, American Red Cross, Amnesty International, Doctors Without Borders, World Bank, WHO.

### Hospitality & Tourism (21 Companies)
- Airbnb, Marriott International, Hilton, Hilton, Expedia Group, Booking.com, TripAdvisor, Disney Parks, Emirates, Delta Airlines.

### Business & Management (23 Companies)
- McKinsey & Company, BCG, Bain & Company, Deloitte, PwC, EY, KPMG, Accenture, Gartner, Forrester Research, Robert Half.

### Sales & Marketing (20 Companies)
- Ogilvy, McCann Worldgroup, Leo Burnett, Dentsu, Publicis Sapient, Nielsen, Ipsos, Kantar, AppLovin, Experian Marketing.

## 🎯 Tips for Adding Companies

1. **Research thoroughly** - Use Glassdoor, Blind, Reddit, company career pages
2. **Be specific** - Generic info doesn't help candidates
3. **Include real examples** - Actual interview questions are valuable
4. **Cultural values matter** - These heavily influence behavioral rounds
5. **Red flags are important** - Help candidates avoid common mistakes

## 🔄 After Adding Companies

1. **Test the system**: `python test_company_intel.py`
2. **Update READMEs**: Update company count in main README.md and backend/README.md
3. **Commit changes**: `git add . && git commit -m "feat: add [CompanyName] to database"`

## 📊 Data Sources

Good sources for company interview intelligence:
- Glassdoor Interview Reviews
- Blind (teamblind.com)
- Reddit (r/cscareerquestions, r/ExperiencedDevs)
- Company career pages
- LeetCode company tags
- GeeksforGeeks interview experiences

## ⚠️ Important Notes

- **Keep it legal** - Only use publicly available information
- **Be accurate** - Wrong info hurts candidates
- **Stay updated** - Interview processes change, update periodically
- **Backup first** - Always backup before major edits
