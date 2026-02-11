# Company Intelligence Database

This folder contains the curated company interview intelligence database.

## 📁 Files

- **`company_profiles.json`** - The main database (currently 30 companies)
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

## 🏢 Current Companies (30)

### FAANG & Tech Giants (12)
- Google, Amazon, Microsoft, Meta, Apple, Netflix
- Uber, Salesforce, Adobe, Atlassian, Shopify, Twilio

### Indian Tech (9)
- **E-commerce/Food**: Flipkart, Zomato, Swiggy
- **Fintech**: Razorpay, CRED, Paytm
- **IT Services**: TCS, Infosys, Wipro

### Finance (2)
- Goldman Sachs, JPMorgan Chase

### Consulting (3)
- McKinsey & Company, BCG, Deloitte

### High-Growth Tech (4)
- Stripe, Airbnb, Snowflake, Databricks

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
