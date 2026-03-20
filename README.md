# Signia Home Care — Website

A complete, production-ready Flask website for **Signia Home Care**, a licensed
Minnesota home care provider based in Minneapolis.

---

## File Tree

```
signia_home_care/
├── app.py                          # Main Flask application + all service data
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variable template
├── README.md                       # This file
│
├── templates/
│   ├── base.html                   # Master layout (header, nav, footer)
│   ├── index.html                  # Homepage
│   ├── about.html                  # About page
│   ├── referral.html               # Referral landing page + form
│   ├── contact.html                # Contact page + form + map placeholder
│   ├── 404.html                    # 404 error page
│   ├── 500.html                    # 500 error page
│   └── services/
│       ├── index.html              # All services landing page
│       ├── comprehensive.html      # Comprehensive Home Care category page
│       ├── basic_245d.html         # Basic 245D category page
│       └── detail.html             # Individual service detail (data-driven)
│
└── static/
    ├── css/
    │   └── style.css               # Complete CSS (CSS custom properties, responsive)
    ├── js/
    │   └── main.js                 # Mobile nav, animations, form validation
    └── images/
        └── .gitkeep                # Add logo, photos, favicon here
```

---

## Setup & Run Instructions

### 1. Prerequisites

- Python 3.9 or higher
- pip

### 2. Create a virtual environment (recommended)

```bash
cd signia_home_care
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
# Edit .env and set a strong SECRET_KEY
```

### 5. Run (development)

```bash
python app.py
```

Open your browser to: **http://localhost:5000**

### 6. Run (production with Gunicorn)

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

---

## URL Structure

| URL                                      | Page                                    |
|------------------------------------------|-----------------------------------------|
| `/`                                      | Homepage                                |
| `/about/`                                | About Us                                |
| `/services/`                             | All Services                            |
| `/services/comprehensive-home-care/`     | Comprehensive Home Care category        |
| `/services/basic-245d/`                  | Basic 245D category                     |
| `/services/<slug>/`                      | Individual service detail page (x31)    |
| `/referral/`                             | Referral landing page + form            |
| `/contact/`                              | Contact page + form                     |

### All Service Page Slugs

**Comprehensive Home Care (24 pages):**
- `/services/advanced-practice-nurse-services/`
- `/services/registered-nurse-services/`
- `/services/licensed-practical-nurse-services/`
- `/services/physical-therapy-services/`
- `/services/occupational-therapy-services/`
- `/services/speech-language-pathologist-services/`
- `/services/respiratory-therapy-services/`
- `/services/social-worker-services/`
- `/services/dietician-nutritionist-services/`
- `/services/medication-management/`
- `/services/delegated-tasks/`
- `/services/transfers-and-mobility-assistance/`
- `/services/treatments-and-therapies/`
- `/services/eating-assistance/`
- `/services/complex-specialty-healthcare/`
- `/services/personal-care-assistance/`
- `/services/standby-assistance/`
- `/services/medication-reminders/`
- `/services/treatment-exercise-reminders/`
- `/services/modified-diet-preparation/`
- `/services/laundry-services/`
- `/services/housekeeping-services/`
- `/services/meal-preparation/`
- `/services/shopping-assistance/`

**Basic 245D Services (7 pages):**
- `/services/individual-community-living-supports/`
- `/services/24-hour-emergency-assistance/`
- `/services/companion-services/`
- `/services/homemaker-services/`
- `/services/individualized-home-supports/`
- `/services/night-supervision/`
- `/services/respite-care/`

---

## Customization Guide

### Business Information
Edit the `BUSINESS` dict at the top of `app.py`:
```python
BUSINESS = {
    "phone":  "(612) 000-0000",   # ← Replace with real phone
    "email":  "info@signiahomecare.com",  # ← Replace with real email
    ...
}
```

### Logo
Replace the text logo in `base.html` with:
```html
<img src="{{ url_for('static', filename='images/logo.svg') }}"
     alt="Signia Home Care" width="200" height="56">
```
Place your logo file at `static/images/logo.svg` (or .png).

### Favicon
Add `static/images/favicon.png` (32×32 or 64×64).

### Images
Replace placeholder divs with `<img>` tags. Recommended images:
- Hero: caregiver with senior client at home (warm, natural lighting)
- About: team photo or staff smiling
- Services: activity-specific shots (cooking, PT, companionship)

### Colors
All colors are CSS custom properties in `static/css/style.css`:
```css
:root {
  --color-primary:   #2563EB;  /* Main blue */
  --color-accent:    #F97316;  /* Orange CTA */
  --color-secondary: #0E7490;  /* Teal */
}
```

### Google Map
In `contact.html`, replace the `map-placeholder` div with a real embed:
```html
<iframe
  src="https://www.google.com/maps/embed?pb=YOUR_CODE"
  width="100%" height="400"
  style="border:0; border-radius: 16px;"
  allowfullscreen="" loading="lazy"
  title="Signia Home Care office location">
</iframe>
```

### Contact / Referral Form Handling
Currently, forms show a flash message on success. To send emails:
1. Add email credentials to `.env`
2. Install Flask-Mail: `pip install Flask-Mail`
3. Replace the `# TODO` comment blocks in `app.py` with email sending logic.

---

## Suggested Image Ideas

| Page / Section             | Image Idea                                                         |
|----------------------------|--------------------------------------------------------------------|
| Homepage hero              | Warm senior at home smiling, caregiver nearby                     |
| Intro / Who We Are         | Caregiver and client sitting together, natural light               |
| Compassionate Care section | Close-up of caregiver's hand holding senior's hand                 |
| About hero                 | Team photo or diverse group of caregivers                          |
| Services (nursing)         | Nurse checking vitals in a home setting                            |
| Services (PT)              | Therapist helping client walk with a walker                        |
| Services (personal care)   | Caregiver helping senior with grooming (dignified, respectful)     |
| Services (companion)       | Two people playing cards or talking at a kitchen table             |
| Services (respite)         | Family caregiver looking relaxed while backup caregiver is present |
| Contact page               | Receptionist or staff member on phone, smiling                     |

All images should feel warm, natural, and diverse — not stock-photo sterile.

---

## Suggested Future Enhancements

1. **Email integration** — Wire forms to SendGrid, Mailchimp, or SMTP.
2. **CRM / intake system** — Connect referral form to a CRM (HubSpot, Salesforce).
3. **Blog / Resources section** — SEO content on home care topics in Minnesota.
4. **Staff profiles page** — Introduce key team members with photos and bios.
5. **Testimonials section** — Add client and family testimonials (with consent).
6. **Careers page** — Job listings and caregiver recruitment content.
7. **FAQ page** — Common questions about home care, billing, eligibility.
8. **Language support** — Spanish, Somali, Hmong translations (key Twin Cities languages).
9. **WCAG 2.1 AA audit** — Full accessibility audit and remediation.
10. **Sitemap.xml + robots.txt** — Add for SEO.
11. **Analytics** — Add Google Analytics 4 or Plausible.
12. **SSL / HTTPS** — Required for production (use Let's Encrypt via Certbot).
13. **Rate limiting** — Add Flask-Limiter to protect form endpoints from spam.
14. **Image optimization** — Use WebP format + lazy loading for all photos.

---

## Compliance / Wording Cautions

- **No guaranteed services** — All content uses language like "may be available
  based on assessment, staff availability, and program fit." Do not change this
  to imply guaranteed availability.
- **No clinical guarantees** — Content does not promise specific health outcomes.
- **No false license claims** — Services listed match the scope of Comprehensive
  Home Care and Basic 245D licenses as defined by Minnesota DHS.
- **No HIPAA compliance claims** — The form includes a privacy notice but does not
  claim HIPAA compliance. If HIPAA compliance is required, consult a healthcare
  attorney and implement a BAA with your hosting/email provider.
- **Referral form** — Advise referrers to share only necessary PHI. Do not store
  PHI in plain-text logs or unencrypted databases.
- **ADA / accessibility** — The site includes semantic HTML, ARIA labels, skip
  navigation, and keyboard-accessible navigation. A professional WCAG audit is
  recommended before launch.

---

## Licenses Referenced

- **Comprehensive Home Care License** — Governed by Minnesota Statutes 144A.43–144A.4799
  and Minnesota Rules 4668. Allows skilled clinical services and personal/household care.
- **Basic 245D License** — Governed by Minnesota Statutes 245D. Allows basic support
  services for individuals with disabilities in home and community settings.

*Content was developed using publicly available information from the State of Minnesota
Department of Health (MDH) and Department of Human Services (DHS). Always verify
current licensure requirements with the applicable agency.*
