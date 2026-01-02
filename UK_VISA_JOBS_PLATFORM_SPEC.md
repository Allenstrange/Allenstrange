# UK International Student Recruitment Platform Specification

**Assumptions:**
*   Access to the UK Government's licensed sponsor register is available via public dataset or API.
*   The definition of "New Entrant" and "Skilled Worker" salary thresholds remains consistent with current immigration rules, though values are configurable.
*   University career services are willing to integrate or promote the platform to their students.
*   GDPR compliance is a strict requirement for all student data handling.
*   "Sponsorship" refers primarily to the Skilled Worker Visa (formerly Tier 2) and Scale-up Worker Visa.

---

## 1. Executive Summary

This document outlines the product specification for a dedicated recruitment platform designed to bridge the gap between UK international students and employers willing to sponsor visas. Currently, international students face significant friction in identifying which employers hold valid sponsorship licenses, often wasting time applying to ineligible roles. Simultaneously, employers struggle to reach qualified international talent already in the UK on Student or Graduate route visas.

Our solution is a compliance-first job discovery engine that ingests and verifies employer sponsorship status against official government data. By filtering opportunities through a configurable eligibility engine—accounting for salary thresholds, occupational codes, and visa switching rules—the platform ensures high-match quality. Success will be measured by the number of verified listings, the reduction in wasted applications (rejection rate due to visa status), and the volume of successful placements (conversion to hires).

## 2. Personas and Journey Maps

### Personas

1.  **The Proactive Undergraduate (Maya)**
    *   *Profile:* 2nd year Computer Science student.
    *   *Goal:* Secure a summer internship that could lead to a graduate role with sponsorship.
    *   *Pain Point:* Finds "internship" listings but unsure if they accept non-UK nationals.

2.  **The Master’s Specialist (Raj)**
    *   *Profile:* 1-year MSc in Data Science, experienced professional back home.
    *   *Goal:* Quickly find a role before the Student visa expires; willing to switch to Graduate Route first but prefers direct sponsorship.
    *   *Pain Point:* Overqualified for generic "grad schemes", under-supported by general job boards regarding visa rules.

3.  **The Graduate Route Switcher (Elena)**
    *   *Profile:* Recently graduated, currently on a 2-year Graduate Route visa working in a non-field job.
    *   *Goal:* Switch to a Skilled Worker visa to start the 5-year clock to settlement (ILR).
    *   *Pain Point:* Need to find an employer willing to sponsor *now*, as the Graduate visa time is ticking.

4.  **The Career Switcher (Li)**
    *   *Profile:* Former finance professional retraining in Nursing/Care (Shortage Occupation).
    *   *Goal:* Find roles specifically in shortage occupations where salary thresholds might be lower and sponsorship is more readily available.
    *   *Pain Point:* Navigating complex SOC code lists and salary requirements.

### Journey Maps

**Journey 1: Discovery & Eligibility (Maya)**
1.  **Trigger:** Maya searches for "software engineering internship".
2.  **Action:** Filters by "Sponsorship Available".
3.  **System Response:** Shows jobs only from verified sponsors. Tags jobs as "Likely Eligible" based on her degree end date.
4.  **Outcome:** Maya saves 3 relevant jobs.

**Journey 2: Tailored Search (Raj)**
1.  **Trigger:** Raj uploads CV to the platform.
2.  **Action:** System parses skills (Python, SQL) and degree level.
3.  **System Response:** Suggests roles matching his skills + employers who have sponsored similar roles recently.
4.  **Outcome:** Raj receives a daily digest of "High Match" sponsor jobs.

**Journey 3: Application & Verification (Elena)**
1.  **Trigger:** Elena applies to a Marketing Manager role.
2.  **Action:** Checks "Eligibility Calculator" for the specific job salary vs. "New Entrant" threshold.
3.  **System Response:** "Green Light: Salary £32k meets the £30.96k threshold for this SOC code."
4.  **Outcome:** Elena applies with confidence, attaching a generated "Visa Eligibility Summary" for the employer.

**Journey 4: Shortage Focus (Li)**
1.  **Trigger:** Li browses "Shortage Occupations".
2.  **Action:** Selects "Health Services".
3.  **System Response:** Lists NHS trusts and private clinics with active licenses.
4.  **Outcome:** Li applies to 5 pre-vetted shortage roles.

## 3. Feature List (MoSCoW)

**Must Have (MVP)**
*   **Sponsorship-Aware Job Search:** Filter by "Verified Sponsor" (cross-referenced with Gov.uk).
*   **Eligibility Checker Engine:** Basic rules-based check (Salary vs SOC code threshold).
*   **Profile & CV Builder:** Standardized inputs for education, visa status, and skills.
*   **Verified Employer Badges:** Visual indicators of sponsorship license status (Verified/Unknown).
*   **Application Tracker:** Simple Kanban board for students (Applied, Interviewing, Offer).
*   **Job Alerts:** Email/Push notifications for new verified matches.
*   **Admin Dashboard:** For managing scraped jobs and manual verification overrides.

**Should Have**
*   **Companies House Integration:** Automated verification of employer existence and active status.
*   **In-Platform Messaging:** Secure chat between students and recruiters.
*   **University SSO:** Login via Shibboleth/OpenAthens for trusted verification.
*   **Skill-Weighted Matching:** Algorithm prioritizing hard skills alongside visa eligibility.
*   **Interview Resources:** Static content/guides for visa interviews.

**Nice to Have**
*   **Recruiter Marketplace:** dedicated portal for employers to headhunt students.
*   **Premium Features:** Paid CV reviews, "Featured" profile status.
*   **AI CV Tailoring:** Generative AI to rewrite CV summaries for specific job descriptions.
*   **Events Calendar:** Virtual career fairs within the app.

## 4. Detailed MVP Scope

**Duration:** 8-12 weeks
**Goal:** Launch a functional job board that guarantees verified sponsorship data.

| Feature | Acceptance Criteria | Success Metric |
| :--- | :--- | :--- |
| **Data Ingestion** | System ingests Gov.uk csv daily. Matches >80% of job board scrapings to sponsor list. | >10,000 verified sponsor jobs at launch. |
| **Search & Filter** | Users can search by keyword, location, and filter by "Sponsor Verified". Response time <200ms. | 50% of searches use the sponsorship filter. |
| **Student Profile** | User can input Degree, University, Visa Type, Expiry Date. | 40% profile completion rate. |
| **Eligibility Widget** | On a job page, shows "Potentially Eligible" check based on user visa & job salary. | High engagement (click-through) on widget. |
| **Apply Redirect** | "Apply Now" button tracks click and redirects to employer ATS/site. | 5% Click-through Rate (CTR) to application. |
| **Sponsor Badge** | Jobs from list have a green checkmark. Tooltip explains "Verified against UK Home Office register". | Trust score (user feedback). |

## 5. Technical Architecture

**Overview:**
A microservices-based architecture to decouple the heavy data processing (ingestion/verification) from the user-facing application (search/profile).

**Diagram Description:**
1.  **Clients:** Web (React/Next.js) and Mobile (Flutter).
2.  **API Gateway:** Nginx/Kong handling rate limiting, auth routing.
3.  **Auth Service:** Node.js + Passport (handling Email, Google, University SSO).
4.  **Core API (Backend):** Python FastAPI (for high performance and easy data integration).
    *   *Endpoints:* /jobs, /users, /applications.
5.  **Search Service:** Elasticsearch (stores indexed job documents for fast query).
6.  **Ingestion Worker:** Python script running on Cron/Airflow.
    *   *Flow:* Scrape/API -> Normalize -> Match Companies House -> Match Sponsor List -> Upsert to DB & Elastic.
7.  **Data Stores:**
    *   PostgreSQL: User data, structured job data, reference data (SOC codes).
    *   Redis: Caching search results, session storage.
    *   S3: User CVs and profile images.

**Tech Stack Rationale:**
*   **Frontend: Next.js (React):** Best for SEO (vital for job board traffic) and performance.
*   **Mobile: Flutter:** Single codebase for iOS/Android to save MVP budget.
*   **Backend: Python FastAPI:** Great for data-heavy apps; easy integration with pandas/numpy for the matching algorithm.
*   **Database: PostgreSQL:** Reliable, relational integrity for user/application data.
*   **Search: Elasticsearch:** Industry standard for complex filtering and full-text search.

## 6. Data Model & Schema

**Canonical Job Posting Schema (JSON)**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "title": { "type": "string" },
    "employer_name": { "type": "string" },
    "companies_house_id": { "type": "string", "pattern": "^[0-9A-Z]{8}$" },
    "sponsor_license_id": { "type": "string" },
    "is_verified_sponsor": { "type": "boolean" },
    "sponsorship_confidence_score": { "type": "number", "minimum": 0, "maximum": 1 },
    "location": {
      "type": "object",
      "properties": {
        "city": { "type": "string" },
        "postcode": { "type": "string" },
        "lat": { "type": "number" },
        "lon": { "type": "number" }
      }
    },
    "salary": {
      "type": "object",
      "properties": {
        "min": { "type": "integer" },
        "max": { "type": "integer" },
        "currency": { "type": "string", "default": "GBP" },
        "period": { "type": "string", "enum": ["yearly", "monthly", "hourly"] }
      }
    },
    "soc_code": { "type": "string" },
    "job_description_raw": { "type": "string" },
    "required_skills": { "type": "array", "items": { "type": "string" } },
    "apply_url": { "type": "string", "format": "uri" },
    "posted_date": { "type": "string", "format": "date-time" },
    "expires_date": { "type": "string", "format": "date-time" }
  },
  "required": ["title", "employer_name", "apply_url"]
}
```

**SQL Table: `jobs`**
```sql
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    employer_name VARCHAR(255) NOT NULL,
    companies_house_id VARCHAR(20),
    sponsor_license_id VARCHAR(50),
    is_verified_sponsor BOOLEAN DEFAULT FALSE,
    sponsorship_confidence_score DECIMAL(3, 2),
    location_city VARCHAR(100),
    salary_min INTEGER,
    salary_max INTEGER,
    currency VARCHAR(3) DEFAULT 'GBP',
    soc_code VARCHAR(10),
    description TEXT,
    apply_url TEXT,
    posted_date TIMESTAMP DEFAULT NOW(),
    expires_date TIMESTAMP
);
```

**SQL Table: `users`**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    current_visa_type VARCHAR(50), -- e.g., 'Student', 'Graduate'
    visa_expiry_date DATE,
    university_id UUID,
    degree_level VARCHAR(50), -- 'Undergraduate', 'Masters', 'PhD'
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**SQL Table: `applications`**
```sql
CREATE TABLE applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    job_id UUID REFERENCES jobs(id),
    status VARCHAR(50) DEFAULT 'applied', -- 'saved', 'applied', 'interview', 'rejected', 'offer'
    notes TEXT,
    applied_at TIMESTAMP DEFAULT NOW()
);
```

## 7. API Design

**Base URL:** `https://api.visamatch.uk/v1`

| Endpoint | Method | Description | Request Example | Response Example |
| :--- | :--- | :--- | :--- | :--- |
| `/jobs/search` | GET | Search jobs with filters | `?q=engineer&sponsor=true&loc=London` | `{ "data": [{ "id": "123", "title": "Dev", ... }], "total": 45 }` |
| `/jobs/{id}/eligibility` | POST | Check eligibility for a specific job | `{ "user_visa": "Student", "grad_date": "2024-06" }` | `{ "eligible": true, "reasons": ["Salary meets threshold"] }` |
| `/employers/verify` | GET | Check if employer is a sponsor | `?name=Acme%20Corp` | `{ "verified": true, "license_tier": "Worker (A rating)" }` |
| `/users/profile` | GET | Get current user profile | Header: `Authorization: Bearer <token>` | `{ "id": "u1", "email": "a@b.com", "visa_type": "Student" }` |
| `/users/profile` | PUT | Update profile details | `{ "visa_expiry": "2025-01-01" }` | `{ "success": true }` |
| `/notifications` | POST | Register push token | `{ "token": "fcm_token_123", "platform": "ios" }` | `{ "status": "registered" }` |

## 8. Eligibility Engine Specification

The engine evaluates a `Job` against a `User` profile and a set of `ImmigrationRules`.

**Rules Format (Configurable JSON)**

```json
{
  "rules_version": "2023-10-04",
  "skilled_worker_general_threshold": 26200,
  "new_entrant_reduction_percentage": 0.70,
  "min_hourly_rate": 10.75,
  "graduate_route_validity_years": 2,
  "shortage_occupation_list_ids": ["2112", "2113", "2114"]
}
```

**Pseudo-Code Logic (Pythonic)**

```python
def check_eligibility(user, job, rules):
    results = { "passed": True, "details": [] }

    # Check 1: Employer Sponsorship Status
    if not job.is_verified_sponsor:
        results["passed"] = False
        results["details"].append("Employer does not appear on the licensed sponsor list.")
        return results # Fail fast

    # Check 2: Salary Threshold (New Entrant vs Experienced)
    threshold = rules.skilled_worker_general_threshold
    if user.is_new_entrant: # e.g. Student or recent Grad
        threshold = threshold * rules.new_entrant_reduction_percentage

    if job.salary.max < threshold:
        results["passed"] = False
        results["details"].append(f"Salary £{job.salary.max} is below the required £{threshold}.")

    # Check 3: SOC Code Eligibility
    if job.soc_code and not is_eligible_soc(job.soc_code):
         results["passed"] = False
         results["details"].append("Job role code is not eligible for sponsorship.")

    return results
```

**UI Output:**
*   **Pass:** Green Banner: "High Likelihood of Eligibility."
*   **Fail:** Red Banner: "Check Requirements" -> "Salary below Skilled Worker threshold (£26,200)."

## 9. UI/UX Wireframes

**1. Landing Page**
*   **Hero:** "Find UK Jobs that Sponsor Visas." Search Bar (Job Title) + Location.
*   **Trust Signals:** "Verified against Gov.uk Register", "University Partners logos".
*   **CTA:** "Upload CV to Check Eligibility".

**2. Search Results**
*   **Layout:** List of cards.
*   **Card:** Job Title, Company Name (with Green Verified Badge), Salary Range, Location.
*   **Tags:** "Sponsorship Available", "New Entrant Eligible".
*   **Filters:** Sidebar with "Sponsorship Certainty" (Verified vs Likely), Salary, Sector.

**3. Job Details**
*   **Header:** Title, Apply Button (Sticky).
*   **Sponsorship Widget:** Box showing "Sponsorship Confidence: 95%". "This employer is a licensed sponsor (A-Rating)".
*   **Eligibility Checker:** Dynamic text: "Based on your profile (Student), you need a salary of £20,960. This job offers £25k. ✅ Match."

**4. Profile/CV Builder**
*   **Steps:** 1. Personal Info -> 2. Education (Uni/Degree) -> 3. Visa Status (Type/Expiry) -> 4. Upload CV.
*   **Visuals:** Progress bar. "Import from LinkedIn" button.

**5. Employer Dashboard (Admin)**
*   **List:** Scraped Jobs.
*   **Actions:** Verify Match (Manual Override), Flag as Invalid, Update SOC Code.

**Sample Copy (CTA):**
*   *Before:* "Search Jobs"
*   *After:* "Search Sponsored Jobs"
*   *Alerts:* "Get notified when a verified sponsor posts a job in Marketing."

## 10. Search & Matching Algorithm

**Scoring Model (Total 100)**

$$Score = (w_1 \cdot Sponsorship) + (w_2 \cdot Skills) + (w_3 \cdot Eligibility) + (w_4 \cdot Preferences)$$

**Feature Weights:**
1.  **Sponsorship Confidence (40%):**
    *   Verified (Gov.uk list + Company House match): 1.0
    *   Likely (Text match only): 0.5
    *   Unknown: 0.0
2.  **Visa Eligibility (30%):**
    *   Salary > Threshold: 1.0
    *   Salary < Threshold: 0.0
3.  **Skill Match (20%):**
    *   Jaccard similarity between Job Description keywords and CV skills.
4.  **Preferences (10%):**
    *   Location match, Industry match.

**Sample Calculation:**
*   **Student:** Data Science grad, requires sponsorship, London.
*   **Job A:** "Junior Data Analyst", Verified Sponsor, £30k, London.
    *   Sponsor: 1.0 * 40 = 40
    *   Eligible: £30k > Threshold => 1.0 * 30 = 30
    *   Skills: High match => 0.8 * 20 = 16
    *   Pref: London => 1.0 * 10 = 10
    *   **Total:** 96 (Top Match)
*   **Job B:** "Marketing Intern", Verified, £21k, London.
    *   Eligible: Fail (Salary too low) => 0
    *   **Total:** < 50 (Filtered out or low rank)
*   **Job C:** "Senior Data Scientist", Verified, £55k, London.
    *   Sponsor: 1.0 * 40 = 40
    *   Eligible: £55k > Threshold => 1.0 * 30 = 30
    *   Skills: Medium match (Experience gap) => 0.4 * 20 = 8
    *   Pref: London => 1.0 * 10 = 10
    *   **Total:** 88 (Strong Match but Senior Role)

## 11. Security, Privacy, and Compliance

**GDPR Checklist:**
*   [ ] **Consent:** Explicit opt-in for CV processing and email alerts.
*   [ ] **Right to Erasure:** "Delete My Account" button in settings cascades to DB and S3 deletion.
*   [ ] **Data Minimization:** Only store parsed text from CVs, not full history unless necessary.
*   [ ] **Encryption:** TLS 1.3 for transit, AES-256 for DB/S3 at rest.

**Compliance:**
*   **Disclaimer:** "We are not legal advisors. Data is based on public registers."
*   **Accuracy:** Periodic re-verification of the sponsor list (weekly sync).

## 12. QA & Testing Plan

*   **Unit Testing:** Jest (Frontend), PyTest (Backend). Coverage > 80%. Focus on Eligibility Logic.
*   **Integration Testing:** Test full flow: Scrape -> Ingest -> Search -> Apply.
*   **E2E Testing:** Playwright/Cypress. Scenarios: "User filters by verified sponsor", "User updates visa status".
*   **Accessibility (a11y):** Pa11y or Lighthouse CI. Ensure contrast ratio > 4.5:1, Aria labels on all inputs.
*   **Monitoring:**
    *   *Sentry:* Error tracking.
    *   *Prometheus/Grafana:* API latency, search 404s, "Zero Results" queries.

## 13. Launch & Growth Plan

**Partnerships:**
*   **Universities:** Pitch to International Student Offices (ISO) at top 10 UK unis (UCL, Manchester, Imperial). Offer free "white-label" access for their students.
*   **Student Unions:** Sponsorship of international student welcome weeks.

**Channels:**
*   **SEO:** Content marketing on "Skilled Worker Visa Requirements 2024", "Companies sponsoring visas UK".
*   **Social:** TikTok/Instagram Reels targeting international student hashtags (#studyinuk, #graduatevisa).

**Key Message:** "Stop wasting time on applications that go nowhere. Find verified sponsors instantly."

## 14. Roadmap (12 Weeks - 2 Week Sprints)

**Phase 1: Foundation (Weeks 1-4)**
*   *Sprint 1 (Weeks 1-2):*
    *   Infrastructure setup (AWS/GCP, DB, CI/CD).
    *   Ingestion Worker: Fetch Gov.uk CSV, match Companies House, index to Elasticsearch.
    *   Core API: `/jobs` endpoints.
*   *Sprint 2 (Weeks 3-4):*
    *   Frontend Search UI (React).
    *   Basic Filter implementation (Location, Keywords).
    *   User Auth (Email, Google) & Profile DB Schema.

**Phase 2: Core Value (Weeks 5-8)**
*   *Sprint 3 (Weeks 5-6):*
    *   Eligibility Engine v1 (Salary & SOC checks).
    *   Job Detail Page with "Eligibility Widget".
    *   Mobile App Shell (Flutter) + Search.
*   *Sprint 4 (Weeks 7-8):*
    *   Profile Builder: CV Upload & Parsing.
    *   Companies House Verification API Integration.
    *   Application Tracker (Save Job / Apply Redirect).

**Phase 3: Polish & Launch (Weeks 9-12)**
*   *Sprint 5 (Weeks 9-10):*
    *   Notifications (Email Alerts for saved searches).
    *   Admin Dashboard for manual verification.
    *   Security Audit & GDPR Compliance checks.
*   *Sprint 6 (Weeks 11-12):*
    *   Beta Release to 50 users (QA).
    *   Performance Tuning (Search Latency).
    *   Public Launch & Marketing Kick-off.

**Risk Mitigation:**
*   *Risk:* Gov.uk data format changes. *Mitigation:* Adapter pattern for data ingestion.
*   *Risk:* Low job volume. *Mitigation:* Backfill with general jobs but clearly mark as "Sponsorship Unknown".

## 15. Cost Estimates & KPIs

**Estimated Costs (Monthly - MVP)**
*   **Cloud (AWS/GCP):** £150 - £300 (RDS, Elastic Service, App Runner).
*   **3rd Party APIs:**
    *   Companies House: Free (Public API).
    *   CV Parser (e.g., Affinda): £50-£100 (Tiered).
    *   Email (SendGrid): £20.
*   **Developer Effort:** ~480 hours (approx. 3 devs x 4 weeks x 40h).

**KPIs (First 6 Months):**
1.  **Verified Jobs:** > 10,000 active listings.
2.  **MAU:** 5,000 active students.
3.  **Search Success:** < 10% searches result in "0 jobs found".
4.  **CPA (Cost Per Acquisition):** < £2.00 per registered user.

## 16. Sample Mock Data

**Job Example 1 (Verified)**
```json
{
  "title": "Software Engineer",
  "employer": "TechNova Ltd",
  "verified": true,
  "confidence": 1.0,
  "salary": { "min": 35000, "max": 45000 },
  "location": "London"
}
```

**Job Example 2 (Likely)**
```json
{
  "title": "Business Analyst",
  "employer": "Global Finance Inc",
  "verified": false,
  "confidence": 0.6,
  "salary": { "min": 28000, "max": 32000 },
  "location": "Manchester"
}
```

**Job Example 3 (Unverified)**
```json
{
  "title": "Marketing Assistant",
  "employer": "StartUp Alpha",
  "verified": false,
  "confidence": 0.2,
  "salary": { "min": 22000, "max": 24000 },
  "location": "Bristol"
}
```

**Job Example 4 (High Value Sponsor)**
```json
{
  "title": "Senior Consultant",
  "employer": "Big4 Consulting",
  "verified": true,
  "confidence": 1.0,
  "salary": { "min": 60000, "max": 80000 },
  "location": "London"
}
```

**Job Example 5 (Shortage Role)**
```json
{
  "title": "Staff Nurse",
  "employer": "NHS Trust",
  "verified": true,
  "confidence": 1.0,
  "salary": { "min": 28000, "max": 34000 },
  "location": "Leeds"
}
```

**Student Profile Example 1**
```json
{
  "name": "Maria G.",
  "visa": "Student (Tier 4)",
  "expiry": "2024-09-01",
  "degree": "MSc Marketing",
  "skills": ["SEO", "Content Writing", "Analytics"]
}
```

**Student Profile Example 2**
```json
{
  "name": "Chen L.",
  "visa": "Graduate Route",
  "expiry": "2025-06-30",
  "degree": "BSc Computer Science",
  "skills": ["Java", "Python", "React"]
}
```

---

## Next Immediate Actions

1.  **Repository Setup:** Initialize Git repo with Monorepo structure (frontend, backend, scraper).
2.  **Data Access:** Write a Python script to download the current Gov.uk register and inspect the CSV structure.
3.  **Prototype:** Sketch the "Sponsorship Widget" UI component in Figma to validate the concept.
4.  **Infrastructure:** Set up a free-tier AWS/Supabase account to host the PostgreSQL DB.
5.  **Legal:** Draft the "No Legal Advice" disclaimer text.
