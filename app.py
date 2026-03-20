"""
Signia Home Care - Flask Web Application
-----------------------------------------
Company:  Signia Home Care
Address:  3030 Holmes Ave S, Minneapolis, MN 55408
Licenses: Comprehensive Home Care program | Basic 245D program

Run:  python app.py  (dev)
Prod: gunicorn -w 4 -b 0.0.0.0:8000 app:app
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# TODO: Replace with a strong secret key in production (store in .env)
app.secret_key = os.environ.get("SECRET_KEY", "change-me-in-production")

# ---------------------------------------------------------------------------
# Business Information (edit here to update across the whole site)
# ---------------------------------------------------------------------------
BUSINESS = {
    "name":         "Signia Home Care",
    "tagline":      "Compassionate Care. Trusted Support. Minnesota Home Care.",
    "address":      "3030 Holmes Ave S, Minneapolis, MN 55408",
    "city":         "Minneapolis",
    "state":        "Minnesota",
    "zip":          "55408",
    "phone":        "(763) 308-3282",
    "fax":          "(612) 395-5381",
    "email":        "hi@signiasolutions.com",
    "hours":        "Monday – Friday: 8:00 AM – 4:30 PM",
    "hours_on_call": "After Hours: (763) 308-3282",
    "licenses":     ["Comprehensive Home Care", "Basic 245D Certified"],
    "service_area": "Minneapolis, St. Paul, Plymouth, Edina, Bloomington, Eden Prairie, Minnetonka, Richfield, St. Louis Park, and the greater Twin Cities metro area",
}

# ---------------------------------------------------------------------------
# Comprehensive Home Care Services
# ---------------------------------------------------------------------------
COMPREHENSIVE_SERVICES = [
    {
        "slug":       "advanced-practice-nurse-services",
        "name":       "Advanced Practice Nurse Services",
        "short":      "APRN-level clinical oversight and care planning in the home.",
        "icon":       "🩺",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Advanced Practice Nurse Services | Signia Home Care Minneapolis MN",
        "meta_desc":  "Signia Home Care provides Advanced Practice Nurse services in Minneapolis and the Twin Cities. Expert clinical support delivered with compassion in your home.",
        "hero_headline":    "Advanced Practice Nurse Services",
        "hero_sub":         "Expert Clinical Support — Right in Your Home",
        "intro":            "When a loved one needs highly skilled clinical oversight, an Advanced Practice Registered Nurse (APRN) can make an enormous difference. APRNs bring graduate-level training and specialized expertise directly to the people they serve — no hospital trip required.",
        "description":      "Advanced Practice Nurses at Signia Home Care may conduct thorough health assessments, collaborate on care plans, order or review diagnostic tests, manage medications, and provide clinical guidance to individuals and families. Their work helps ensure that complex health needs are met safely and thoughtfully, supporting your loved one's dignity, comfort, and independence at home.",
        "who_benefits":     [
            "Individuals managing complex or multiple chronic health conditions",
            "Clients transitioning from a hospital or rehabilitation facility back home",
            "Families seeking a higher level of clinical oversight for a loved one",
            "People who require ongoing medication management or clinical monitoring",
        ],
        "how_it_helps":     [
            "Reduces unnecessary hospitalizations through proactive home-based clinical care",
            "Supports coordinated, person-centered care planning",
            "Empowers families with expert clinical guidance and education",
            "Promotes safety, dignity, and quality of life in familiar surroundings",
        ],
        "what_to_expect":   "Following an initial assessment, an APRN works closely with you, your family, and your care team to develop a personalized plan of care. Visits are scheduled based on clinical need and program fit. Services are individualized and may vary based on assessment findings, physician collaboration, and program eligibility.",
        "why_signia":       "Our commitment to compassionate, high-quality care means you'll always work with skilled professionals who treat your family like their own. Signia Home Care is approved and certified by the State of Minnesota and dedicated to meeting the highest standards of home care excellence.",
    },
    {
        "slug":       "registered-nurse-services",
        "name":       "Registered Nurse Services",
        "short":      "Skilled nursing assessments, monitoring, wound care, and health education.",
        "icon":       "💉",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Registered Nurse Services | Signia Home Care Minneapolis MN",
        "meta_desc":  "Skilled registered nurse home visits in Minneapolis and Twin Cities. Wound care, assessments, medication oversight, and compassionate nursing support.",
        "hero_headline":    "Registered Nurse Services",
        "hero_sub":         "Skilled Nursing Care Delivered with Compassion",
        "intro":            "Having a Registered Nurse (RN) visit your home can provide peace of mind for both clients and families. Our RNs bring clinical skill and genuine warmth to every visit, helping individuals manage health conditions, recover from illness, and stay safely at home.",
        "description":      "Registered Nurses with Signia Home Care may perform health assessments, monitor vital signs, manage wound care, oversee medication regimens, educate clients and caregivers on health conditions, and coordinate with physicians and other members of the care team. Whether you need short-term support after a hospitalization or ongoing skilled nursing services, our team is here to help.",
        "who_benefits":     [
            "Individuals recovering from surgery, illness, or hospitalization",
            "Clients with chronic conditions requiring skilled nursing monitoring",
            "People who need wound care, IV therapy oversight, or medication management",
            "Families who want expert clinical guidance in the comfort of home",
        ],
        "how_it_helps":     [
            "Monitors health status to detect and respond to changes early",
            "Reduces readmission risk through skilled home-based follow-up care",
            "Educates clients and family members to support confidence and safety",
            "Bridges the gap between clinical care and everyday home life",
        ],
        "what_to_expect":   "An RN will conduct an initial in-home assessment to understand your needs and goals. From there, a personalized care plan is developed and visits are scheduled accordingly. Communication with your physician or care team is an important part of this process. Services are individualized based on assessment and program fit.",
        "why_signia":       "Signia Home Care's registered nurses are more than clinicians — they are advocates for your well-being. We hold a state-approved Comprehensive Home Care program and are committed to safe, high-quality, person-centered nursing care.",
    },
    {
        "slug":       "licensed-practical-nurse-services",
        "name":       "Licensed Practical Nurse Services",
        "short":      "Hands-on skilled nursing support under RN and physician direction.",
        "icon":       "🏥",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Licensed Practical Nurse Services | Signia Home Care Minneapolis MN",
        "meta_desc":  "LPN home care services in Minneapolis and Twin Cities. Skilled nursing tasks, wound care support, and compassionate hands-on help at home.",
        "hero_headline":    "Licensed Practical Nurse Services",
        "hero_sub":         "Skilled, Hands-On Nursing Support in Your Home",
        "intro":            "Licensed Practical Nurses (LPNs) are an essential part of a skilled home care team. Working under the direction of a Registered Nurse or physician, our LPNs deliver reliable, hands-on clinical support that helps individuals manage their health and stay comfortable at home.",
        "description":      "LPNs at Signia Home Care may assist with wound care, monitor vital signs, administer medications as directed, support activities of daily living that require skilled oversight, and provide education to clients and family members. They work as part of a coordinated care team, ensuring consistent, quality care between visits.",
        "who_benefits":     [
            "Clients who need regular skilled nursing tasks such as wound care or vital sign monitoring",
            "Individuals managing chronic illness who need consistent clinical support",
            "People who benefit from hands-on assistance delivered by a skilled nurse",
            "Families seeking dependable, professional nursing visits",
        ],
        "how_it_helps":     [
            "Delivers consistent skilled nursing support between physician and RN visits",
            "Helps individuals manage health conditions confidently at home",
            "Supports caregiver education and family confidence",
            "Provides a trusted, familiar face with clinical training",
        ],
        "what_to_expect":   "LPN visits are scheduled as part of your overall plan of care, developed with an RN and your healthcare team. Each visit is documented and communicated to ensure continuity of care. Services are individualized and subject to assessment and program eligibility.",
        "why_signia":       "At Signia Home Care, our LPNs are selected for their clinical skill and their genuine care for the people they serve. We are proud to provide compassionate, high-quality nursing support to Minnesota families.",
    },
    {
        "slug":       "physical-therapy-services",
        "name":       "Physical Therapy Services",
        "short":      "Restore strength, mobility, and independence with in-home physical therapy.",
        "icon":       "🦵",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Physical Therapy Services | Signia Home Care Minneapolis MN",
        "meta_desc":  "In-home physical therapy services in Minneapolis and the Twin Cities. Regain strength, balance, and independence with expert PT support at home.",
        "hero_headline":    "Physical Therapy Services",
        "hero_sub":         "Move Better, Live Better — in the Comfort of Home",
        "intro":            "Recovering from an injury, surgery, or managing a condition that affects your movement doesn't have to mean long trips to a clinic. Our physical therapists bring expert care directly to your home, where healing happens best.",
        "description":      "Physical therapists at Signia Home Care evaluate your strength, balance, mobility, and functional abilities, then design a personalized therapy plan to help you reach your goals. Services may include therapeutic exercises, gait training, fall prevention education, pain management techniques, and guidance for safe participation in daily activities.",
        "who_benefits":     [
            "Individuals recovering from hip or knee replacement surgery",
            "Clients rebuilding strength and mobility after a stroke",
            "People managing conditions like Parkinson's disease, MS, or arthritis",
            "Anyone at risk of falling who wants to build balance and confidence",
        ],
        "how_it_helps":     [
            "Reduces fall risk through targeted balance and strength training",
            "Supports faster recovery in the familiar environment of home",
            "Builds functional independence for daily tasks like walking and climbing stairs",
            "Empowers clients and families with home exercise programs",
        ],
        "what_to_expect":   "Your physical therapist will perform an initial evaluation to assess your current abilities and set meaningful goals with you. A customized therapy plan is created and updated as you progress. Services require a physician referral and are individualized based on assessment and program fit.",
        "why_signia":       "Our physical therapists understand that every person's journey is different. At Signia Home Care, we celebrate every step forward and are committed to helping you reach your highest level of function and independence.",
    },
    {
        "slug":       "occupational-therapy-services",
        "name":       "Occupational Therapy Services",
        "short":      "Regain independence in daily activities with skilled occupational therapy.",
        "icon":       "🖐️",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Occupational Therapy Services | Signia Home Care Minneapolis MN",
        "meta_desc":  "Home-based occupational therapy in Minneapolis and Twin Cities. Regain independence in bathing, dressing, and daily tasks with our skilled OT team.",
        "hero_headline":    "Occupational Therapy Services",
        "hero_sub":         "Helping You Live Independently — One Daily Task at a Time",
        "intro":            "Occupational therapy is all about helping people do the everyday things that matter most — getting dressed, preparing a meal, bathing safely, or returning to a beloved hobby. Our occupational therapists bring this vital expertise directly to your home.",
        "description":      "Occupational therapists with Signia Home Care assess your environment, abilities, and daily routines, then create a personalized plan to help you function as independently as possible. They may recommend adaptive equipment, modify your home for safety, teach new techniques for daily tasks, and provide caregiver training to support your success.",
        "who_benefits":     [
            "Individuals recovering from a stroke or brain injury",
            "People adapting to a new physical limitation or disability",
            "Clients who want to remain safely independent at home",
            "Anyone who needs help relearning or adapting daily living skills",
        ],
        "how_it_helps":     [
            "Restores independence in meaningful daily activities",
            "Improves home safety through environmental assessment and modification guidance",
            "Supports family and caregiver training for consistent home routines",
            "Enhances quality of life and confidence in daily function",
        ],
        "what_to_expect":   "Your OT will conduct a thorough home and functional assessment, identify barriers to independence, and develop a treatment plan tailored to your specific goals. Services require a physician referral and are based on assessment findings and program eligibility.",
        "why_signia":       "We believe that living independently — in whatever way that looks for each person — is a fundamental part of quality of life. Our occupational therapists are passionate about helping people thrive at home.",
    },
    {
        "slug":       "speech-language-pathologist-services",
        "name":       "Speech-Language Pathologist Services",
        "short":      "Communication, swallowing, and cognitive support from a licensed SLP.",
        "icon":       "🗣️",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Speech-Language Pathology Services | Signia Home Care Minneapolis MN",
        "meta_desc":  "In-home speech therapy in Minneapolis and Twin Cities. Communication, swallowing disorders, and cognitive support from our licensed speech-language pathologists.",
        "hero_headline":    "Speech-Language Pathologist Services",
        "hero_sub":         "Restoring Communication, Confidence, and Safe Swallowing",
        "intro":            "Being able to communicate clearly and eat safely are fundamental to quality of life. Our speech-language pathologists provide expert, compassionate support for individuals experiencing challenges with communication, swallowing, voice, or cognition — all in the comfort of home.",
        "description":      "Speech-Language Pathologists (SLPs) at Signia Home Care evaluate and treat a wide range of conditions including aphasia, dysarthria, dysphagia (swallowing difficulties), cognitive-communication disorders, and voice concerns. They work with clients to improve functional communication skills and ensure safe eating and swallowing practices.",
        "who_benefits":     [
            "Individuals recovering from a stroke who have difficulty speaking or swallowing",
            "Clients with Parkinson's disease, MS, or other neurological conditions",
            "People who have experienced a traumatic brain injury",
            "Anyone with difficulties eating, speaking, or expressing themselves clearly",
        ],
        "how_it_helps":     [
            "Restores or improves speech and language abilities for meaningful communication",
            "Reduces aspiration risk through swallowing evaluation and therapy",
            "Supports cognitive communication strategies for daily life",
            "Trains family members and caregivers in communication support techniques",
        ],
        "what_to_expect":   "Your SLP will begin with a comprehensive evaluation of your communication and/or swallowing abilities. A treatment plan is created and therapy sessions are conducted in your home. Services require a physician referral and are individualized based on assessment and program fit.",
        "why_signia":       "We know how isolating it can feel when communication becomes difficult. Our speech-language pathologists bring patience, expertise, and genuine encouragement to every session, helping clients rediscover their voice.",
    },
    {
        "slug":       "respiratory-therapy-services",
        "name":       "Respiratory Therapy Services",
        "short":      "Expert respiratory support for individuals with breathing or pulmonary conditions.",
        "icon":       "🫁",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Respiratory Therapy Services | Signia Home Care Minneapolis MN",
        "meta_desc":  "Home respiratory therapy in Minneapolis and Twin Cities. Skilled support for COPD, oxygen therapy, ventilators, and breathing conditions.",
        "hero_headline":    "Respiratory Therapy Services",
        "hero_sub":         "Skilled Breathing Support in the Comfort of Your Home",
        "intro":            "For individuals living with COPD, asthma, or other respiratory conditions, expert support at home can make a significant difference in comfort, safety, and quality of life. Our respiratory therapists bring specialized expertise directly to you.",
        "description":      "Respiratory therapists at Signia Home Care may assess pulmonary function, assist with oxygen therapy management, provide ventilator support, teach breathing techniques, and educate clients and families on managing respiratory conditions. They collaborate closely with your physician and care team to ensure your breathing needs are met safely and effectively.",
        "who_benefits":     [
            "Individuals with COPD, asthma, or chronic lung disease",
            "Clients requiring home oxygen therapy or ventilator support",
            "People recovering from pneumonia or respiratory illness",
            "Anyone who needs education and monitoring for a breathing condition",
        ],
        "how_it_helps":     [
            "Improves respiratory function and symptom management at home",
            "Reduces emergency room visits through proactive monitoring and education",
            "Supports safe use of oxygen equipment and respiratory devices",
            "Empowers clients with breathing techniques for daily life",
        ],
        "what_to_expect":   "Your respiratory therapist will assess your breathing, review your equipment, and develop a plan to support your respiratory health. All care is coordinated with your physician. Services are individualized based on assessment and program fit.",
        "why_signia":       "Breathing easier starts with the right support. Signia Home Care is committed to providing expert, compassionate respiratory therapy that helps you or your loved one live more comfortably at home.",
    },
    {
        "slug":       "social-worker-services",
        "name":       "Social Worker Services",
        "short":      "Emotional support, care coordination, and community resource connection.",
        "icon":       "🤝",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Social Worker Services | Signia Home Care Minneapolis MN",
        "meta_desc":  "Home care social work services in Minneapolis and Twin Cities. Emotional support, care coordination, and community resource navigation for individuals and families.",
        "hero_headline":    "Social Worker Services",
        "hero_sub":         "Support Beyond the Medical — Caring for the Whole Person",
        "intro":            "Navigating health challenges affects more than just the body. Social workers play a vital role in supporting the emotional, social, and practical needs of individuals and their families — helping everyone involved feel less alone in the journey.",
        "description":      "Our social workers assist with care coordination, emotional support, crisis intervention, advance care planning conversations, connecting families to community resources, and helping individuals understand their rights and options. They serve as a bridge between your family and the broader healthcare and social services system in Minnesota.",
        "who_benefits":     [
            "Individuals and families facing the challenges of a new diagnosis",
            "Caregivers who are feeling overwhelmed or burned out",
            "People navigating complex health, housing, or financial situations",
            "Anyone who needs help understanding care options and community resources",
        ],
        "how_it_helps":     [
            "Reduces caregiver stress through practical support and resource connection",
            "Helps families make informed decisions about care and future planning",
            "Provides emotional support and counseling during difficult transitions",
            "Connects clients to Minnesota community programs and benefits",
        ],
        "what_to_expect":   "A social worker will conduct a comprehensive psychosocial assessment and work with you and your family to identify needs, goals, and available resources. They remain available as a continued point of contact throughout your care. Services are individualized based on assessment and program fit.",
        "why_signia":       "We believe that caring for the whole person — mind, body, and spirit — is the foundation of excellent home care. Our social workers are compassionate advocates who walk alongside you every step of the way.",
    },
    {
        "slug":       "dietician-nutritionist-services",
        "name":       "Dietician and Nutritionist Services",
        "short":      "Personalized nutrition support to promote health and healing at home.",
        "icon":       "🥗",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Dietician & Nutritionist Services | Signia Home Care Minneapolis MN",
        "meta_desc":  "In-home dietician and nutritionist services in Minneapolis and Twin Cities. Personalized nutrition planning to support health, healing, and independence.",
        "hero_headline":    "Dietician and Nutritionist Services",
        "hero_sub":         "Nourishing Health and Healing — One Meal at a Time",
        "intro":            "Good nutrition is one of the most powerful tools for healing, managing chronic conditions, and maintaining quality of life. Our registered dieticians and nutritionists bring personalized nutrition expertise directly to your home.",
        "description":      "Our dieticians assess nutritional status, identify deficiencies or concerns, and develop personalized eating plans that support your health goals. They work with individuals managing diabetes, kidney disease, heart conditions, weight challenges, swallowing difficulties, and many other conditions. Caregiver and family education is also an important part of the service.",
        "who_benefits":     [
            "Individuals managing diabetes, kidney disease, or heart conditions",
            "People at risk for malnutrition or unintentional weight loss",
            "Clients with swallowing difficulties who need texture-modified diets",
            "Anyone who wants expert guidance on eating well for their health condition",
        ],
        "how_it_helps":     [
            "Supports chronic disease management through targeted nutrition strategies",
            "Reduces complications associated with poor nutrition",
            "Empowers clients and families with practical, achievable eating guidance",
            "Complements medical care with an evidence-based nutritional approach",
        ],
        "what_to_expect":   "Your dietician will complete a nutritional assessment and review your health history, current diet, and goals. A personalized nutrition plan is developed and followed up to track progress. Services require a physician referral and are individualized based on assessment and program fit.",
        "why_signia":       "We know that food is more than fuel — it's comfort, culture, and connection. Our nutrition professionals create practical plans that respect your preferences, your culture, and your health.",
    },
    {
        "slug":       "medication-management",
        "name":       "Medication Management",
        "short":      "Safe, accurate medication support to protect health and prevent errors.",
        "icon":       "💊",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Medication Management Services | Signia Home Care Minneapolis MN",
        "meta_desc":  "Home medication management in Minneapolis and Twin Cities. Skilled nursing oversight to help clients take the right medication safely, at the right time.",
        "hero_headline":    "Medication Management Services",
        "hero_sub":         "The Right Medication, at the Right Time, Every Time",
        "intro":            "Managing multiple medications can be confusing and even dangerous without proper support. Our skilled nursing team provides expert medication management to help individuals take their medications correctly, avoid harmful interactions, and stay safe at home.",
        "description":      "Medication management services may include medication reviews, reconciliation, setup of medication systems, oversight of self-administration, teaching clients and caregivers about medications, and coordination with prescribing physicians. This service is performed or supervised by a nurse on our team and is an important part of safe home care for individuals managing complex medication regimens.",
        "who_benefits":     [
            "Individuals taking multiple medications for chronic conditions",
            "People who have recently been discharged from a hospital or rehab facility",
            "Clients or families concerned about medication errors or confusion",
            "Individuals who need assistance organizing and tracking their medications",
        ],
        "how_it_helps":     [
            "Reduces the risk of medication errors, missed doses, or dangerous interactions",
            "Supports safe transitions from hospital to home",
            "Educates clients and family caregivers on medication purpose and side effects",
            "Coordinates with physicians to ensure prescriptions align with current health status",
        ],
        "what_to_expect":   "A nurse on our team will review all current medications, identify any concerns, and develop a medication management plan. Ongoing monitoring ensures that any changes in health status or prescriptions are addressed promptly. Services are individualized based on assessment and clinical need.",
        "why_signia":       "Medication safety is a top priority at Signia Home Care. Our clinical team brings the focus and expertise needed to protect your loved one's health every single day.",
    },
    {
        "slug":       "delegated-tasks",
        "name":       "Delegated Tasks to Unlicensed Personnel",
        "short":      "Nurse-delegated care tasks performed by trained home care aides.",
        "icon":       "📋",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Delegated Care Tasks | Signia Home Care Minneapolis MN",
        "meta_desc":  "Nurse-delegated home care tasks in Minneapolis and Twin Cities. Trained home care aides perform specific care tasks under the supervision of a nurse on our team.",
        "hero_headline":    "Delegated Care Tasks",
        "hero_sub":         "Skilled Care Extended Through a Trusted Team",
        "intro":            "In Minnesota, licensed nurses may delegate specific care tasks to trained home care aides, expanding the reach of skilled clinical care. This allows more individuals to receive the support they need, consistently and safely, right in their homes.",
        "description":      "Under the Minnesota Home Care Act, a nurse on our team may assess a client's needs and delegate specific tasks — such as certain personal care or health maintenance activities — to a trained home care aide. The nurse maintains oversight and the aide performs the task as directed. This model of care supports efficiency and continuity while maintaining clinical safety standards.",
        "who_benefits":     [
            "Clients who need consistent, skilled-level support between nurse visits",
            "Individuals whose care needs require specific trained assistance daily",
            "Families who want clinical oversight built into everyday home care routines",
        ],
        "how_it_helps":     [
            "Extends the reach of clinical care into daily routines",
            "Ensures tasks are performed correctly and consistently",
            "Supports continuity of care through a coordinated team approach",
            "Maintains clinical safety standards through nurse oversight",
        ],
        "what_to_expect":   "A nurse on our team will assess your care needs and determine which tasks, if any, are appropriate for delegation. The nurse will train and supervise the home care aide and maintain clinical oversight throughout the service period. All delegated tasks are documented and monitored.",
        "why_signia":       "Our team approach to care means you receive expert oversight at every level. At Signia Home Care, no detail is too small when it comes to your safety and well-being.",
    },
    {
        "slug":       "transfers-and-mobility-assistance",
        "name":       "Transfers and Mobility Assistance",
        "short":      "Safe, hands-on help moving, walking, and positioning for comfort and safety.",
        "icon":       "🚶",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Transfers & Mobility Assistance | Signia Home Care Minneapolis MN",
        "meta_desc":  "Safe transfer and mobility assistance in Minneapolis and Twin Cities. Our trained caregivers help individuals move safely, reducing fall risk and supporting independence.",
        "hero_headline":    "Transfers and Mobility Assistance",
        "hero_sub":         "Safe Movement, Greater Independence, Less Risk",
        "intro":            "Moving safely from bed to chair, walking to the bathroom, or navigating your home should never feel uncertain or frightening. Our trained caregivers provide expert, hands-on assistance with transfers and mobility — protecting your safety and your dignity every step of the way.",
        "description":      "Hands-on transfer and mobility assistance includes helping clients move between positions or surfaces (such as bed to wheelchair or chair to standing), supporting walking, and assisting with positioning for comfort and safety. Caregivers are trained in proper body mechanics and safe transfer techniques to minimize risk for both the client and the caregiver.",
        "who_benefits":     [
            "Individuals with limited strength, balance, or mobility",
            "People recovering from surgery, illness, or injury",
            "Clients using mobility equipment such as wheelchairs or walkers",
            "Individuals at risk of falls who need steady, reliable support",
        ],
        "how_it_helps":     [
            "Significantly reduces the risk of falls and related injuries",
            "Supports greater participation in daily activities and routines",
            "Provides peace of mind for both clients and family members",
            "Maintains dignity by providing respectful, skilled physical support",
        ],
        "what_to_expect":   "An assessment will identify your specific mobility needs and any equipment that may help. Caregivers are matched to clients based on care needs and trained in your specific transfer techniques. Services are individualized based on assessment and program fit.",
        "why_signia":       "Safety and dignity go hand in hand. Our team is trained to support movement in ways that feel respectful, comfortable, and empowering — because how care is given matters just as much as what is given.",
    },
    {
        "slug":       "treatments-and-therapies",
        "name":       "Treatments and Therapies",
        "short":      "Skilled treatment delivery and therapeutic support in the home setting.",
        "icon":       "⚕️",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Home Treatments & Therapies | Signia Home Care Minneapolis MN",
        "meta_desc":  "In-home treatments and therapies in Minneapolis and Twin Cities. Skilled clinical support for wound care, IV therapy, injections, and more.",
        "hero_headline":    "Treatments and Therapies at Home",
        "hero_sub":         "Expert Clinical Treatments — Delivered Where You Live",
        "intro":            "Many medical treatments and therapies that once required a clinic or hospital stay can now be safely performed at home by skilled care professionals. Signia Home Care brings these capabilities to you, supporting healing and health in the place you feel most comfortable.",
        "description":      "Skilled treatments and therapies may include wound care and dressing changes, administration of injections, IV therapy oversight, ostomy care, catheter care, and other physician-ordered clinical treatments. All treatments are performed or supervised by our trained care team and documented carefully for continuity of care.",
        "who_benefits":     [
            "Individuals with wounds, surgical incisions, or chronic skin conditions",
            "Clients who require IV antibiotics, fluids, or other infusion therapy at home",
            "People managing ostomies, catheters, or other medical devices",
            "Anyone with physician-ordered treatments that can be safely performed at home",
        ],
        "how_it_helps":     [
            "Delivers necessary medical treatments without the burden of clinic travel",
            "Reduces infection risk and promotes healing in a controlled home environment",
            "Maintains continuity with physician-directed treatment plans",
            "Supports faster recovery through timely, skilled intervention",
        ],
        "what_to_expect":   "Treatments are always performed according to a physician's orders and individualized plan of care. A care team member will review the treatment plan, gather necessary supplies, and perform each service with care and precision. Services are individualized based on clinical need and program eligibility.",
        "why_signia":       "When skilled treatments are needed, trust matters. Signia Home Care's skilled care team provides precise, compassionate care that gives you confidence your health is in excellent hands.",
    },
    {
        "slug":       "eating-assistance",
        "name":       "Eating Assistance for Complex Needs",
        "short":      "Skilled eating support for clients with complicating swallowing or feeding challenges.",
        "icon":       "🍽️",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Eating Assistance Services | Signia Home Care Minneapolis MN",
        "meta_desc":  "Skilled eating assistance in Minneapolis and Twin Cities for clients with swallowing difficulties, feeding challenges, or complex nutritional needs at home.",
        "hero_headline":    "Eating Assistance for Complex Needs",
        "hero_sub":         "Safe, Dignified Mealtime Support for Every Individual",
        "intro":            "For individuals with swallowing difficulties, neurological conditions, or other complicating factors, mealtime can be a challenging and even risky time. Our skilled team provides careful, dignified eating assistance to help clients receive proper nutrition safely and comfortably.",
        "description":      "This service addresses complex eating challenges that require skilled observation and intervention, such as dysphagia (difficulty swallowing), aspiration risk, specialized positioning needs, or the need for texture-modified foods as ordered by a healthcare professional. Caregivers trained in these needs provide hands-on assistance while monitoring for safety.",
        "who_benefits":     [
            "Individuals with dysphagia or swallowing difficulties",
            "Clients at risk of aspiration during meals",
            "People with neurological conditions affecting eating ability",
            "Individuals who need specialized positioning or modified textures at mealtimes",
        ],
        "how_it_helps":     [
            "Reduces the risk of aspiration and related complications",
            "Ensures clients receive adequate nutrition and hydration safely",
            "Supports mealtime dignity and enjoyment",
            "Complements the work of speech-language pathologists and dieticians",
        ],
        "what_to_expect":   "Eating assistance is coordinated with your clinical team, including any recommendations from a speech-language pathologist or dietician. Caregivers follow individualized protocols to support safe and pleasant mealtimes. Services are based on clinical assessment and program fit.",
        "why_signia":       "Mealtimes should be moments of nourishment and pleasure, not stress. Our team approaches every mealtime with patience, skill, and the respect every person deserves.",
    },
    {
        "slug":       "complex-specialty-healthcare",
        "name":       "Complex and Specialty Healthcare Services",
        "short":      "Advanced home-based care for individuals with complex or high-acuity health needs.",
        "icon":       "🏨",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Complex & Specialty Healthcare | Signia Home Care Minneapolis MN",
        "meta_desc":  "Complex and specialty home healthcare in Minneapolis and Twin Cities. Expert clinical support for individuals with high-acuity or multi-system health needs.",
        "hero_headline":    "Complex and Specialty Healthcare Services",
        "hero_sub":         "Advanced Clinical Care — Wherever You Call Home",
        "intro":            "Some individuals have medical needs that are more complex, requiring a higher level of clinical expertise and coordination. Signia Home Care is equipped to support individuals with complex or specialty healthcare needs through our Comprehensive Home Care license.",
        "description":      "Complex and specialty healthcare services may include care for individuals with multi-system medical conditions, those requiring advanced wound management, clients with high-acuity nursing needs, or individuals transitioning from intensive care settings. Our clinical team works closely with physicians, specialists, and family members to ensure comprehensive, coordinated care at home.",
        "who_benefits":     [
            "Individuals with multiple, complex chronic conditions",
            "Clients transitioning from ICU or acute care to home",
            "People requiring advanced wound or specialty care management",
            "Individuals with high-acuity needs who prefer or require home-based care",
        ],
        "how_it_helps":     [
            "Provides hospital-level clinical expertise in the home setting",
            "Reduces repeated hospitalizations through proactive, skilled management",
            "Coordinates across specialties to ensure comprehensive care",
            "Supports quality of life and dignity for individuals with complex needs",
        ],
        "what_to_expect":   "A comprehensive clinical assessment will be conducted to understand your specific needs. A care plan is developed in collaboration with your physician and care team. Ongoing monitoring and communication ensure that changes are addressed promptly. Services are individualized and subject to assessment and program eligibility.",
        "why_signia":       "Complex needs require experienced hands and compassionate hearts. Signia Home Care is committed to meeting even the most challenging clinical needs with excellence, sensitivity, and respect.",
    },
    {
        "slug":       "personal-care-assistance",
        "name":       "Personal Care Assistance",
        "short":      "Respectful help with dressing, bathing, grooming, hygiene, and daily routines.",
        "icon":       "🛁",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Personal Care Assistance | Signia Home Care Minneapolis MN",
        "meta_desc":  "Personal care assistance in Minneapolis and Twin Cities. Dignified help with bathing, dressing, grooming, oral hygiene, and daily personal routines.",
        "hero_headline":    "Personal Care Assistance",
        "hero_sub":         "Dignified, Respectful Help with Your Daily Routines",
        "intro":            "Getting dressed, bathing, and maintaining personal hygiene are fundamental parts of how we feel about ourselves each day. When these tasks become difficult, the right support can restore both comfort and confidence. Our caregivers provide respectful, dignified personal care that honors your individuality.",
        "description":      "Personal care assistance includes hands-on help with dressing, self-feeding support, oral hygiene, hair care, grooming, toileting, and bathing. Our caregivers approach every task with sensitivity and respect for privacy and personal preferences. Services are individualized to your routine, culture, and comfort.",
        "who_benefits":     [
            "Individuals with physical limitations that affect daily self-care",
            "Older adults who need assistance maintaining their hygiene and routines",
            "People recovering from illness, surgery, or injury",
            "Individuals living with disabilities who need consistent personal care support",
        ],
        "how_it_helps":     [
            "Supports daily comfort, cleanliness, and personal dignity",
            "Reduces caregiver burden on family members",
            "Builds a consistent, trusting relationship between caregiver and client",
            "Promotes emotional well-being through maintained personal routines",
        ],
        "what_to_expect":   "Your care plan will include your personal preferences, cultural considerations, and schedule. Caregivers follow your routine and work at your pace. Services are individualized based on assessment and program fit.",
        "why_signia":       "We understand that personal care is deeply personal. Every Signia Home Care caregiver is selected for their kindness, professionalism, and ability to provide care that truly respects the individual.",
    },
    {
        "slug":       "standby-assistance",
        "name":       "Standby Assistance",
        "short":      "A caregiver within arm's reach for safety while you perform daily activities.",
        "icon":       "🛡️",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Standby Assistance Services | Signia Home Care Minneapolis MN",
        "meta_desc":  "Standby assistance in Minneapolis and Twin Cities. A trained caregiver stays within arm's reach to ensure safety while you perform daily activities independently.",
        "hero_headline":    "Standby Assistance",
        "hero_sub":         "Your Safety Net — Close By, Ready to Help",
        "intro":            "Sometimes the best support is simply knowing someone is nearby. Standby assistance allows individuals to perform daily activities themselves — building confidence and independence — while a trained caregiver remains within arm's reach for safety.",
        "description":      "Standby assistance means a caregiver is physically present and ready to intervene if needed, without actually performing the task for the client. This approach is used during activities like bathing, showering, walking, or exercising, where there is a safety risk but the individual can perform the task with supervision. It is an important tool for balancing independence with safety.",
        "who_benefits":     [
            "Individuals at risk of falling during daily activities",
            "People rebuilding confidence after an injury or illness",
            "Those who can perform tasks independently but need a safety presence",
            "Clients and families who want peace of mind during higher-risk activities",
        ],
        "how_it_helps":     [
            "Prevents falls and accidents during higher-risk daily activities",
            "Preserves and promotes client independence and autonomy",
            "Reduces family anxiety about a loved one's safety at home",
            "Supports confidence-building as part of recovery or ongoing care",
        ],
        "what_to_expect":   "Your care plan will identify which activities require standby assistance. Caregivers are trained to be present and attentive without being intrusive, respecting your independence while ensuring your safety. Services are individualized based on assessment.",
        "why_signia":       "Independence matters deeply to us. We provide standby assistance that empowers individuals to do what they can for themselves, with a trusted safety net always close by.",
    },
    {
        "slug":       "medication-reminders",
        "name":       "Medication Reminders",
        "short":      "Verbal or visual reminders to help clients take their scheduled medications.",
        "icon":       "⏰",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Medication Reminder Services | Signia Home Care Minneapolis MN",
        "meta_desc":  "Medication reminder services in Minneapolis and Twin Cities. Verbal and visual prompts to help individuals remember to take their scheduled medications on time.",
        "hero_headline":    "Medication Reminders",
        "hero_sub":         "Gentle Reminders to Keep Your Health on Track",
        "intro":            "Forgetting to take a medication — or taking it at the wrong time — can have real health consequences. Our caregivers provide gentle verbal or visual reminders to help individuals stay consistent with their medication schedules, supporting better health outcomes at home.",
        "description":      "Medication reminder services involve a caregiver providing a verbal or visual prompt at the scheduled time for a client to take their own medications. This is different from medication administration — the individual takes their medication themselves. It is a helpful support for those who are independent in their medication-taking but benefit from a reminder to stay on schedule.",
        "who_benefits":     [
            "Individuals who independently take their own medications but sometimes forget",
            "People with mild cognitive changes who benefit from consistent prompting",
            "Clients managing busy or complex daily schedules",
            "Families who want assurance that a loved one is staying on schedule",
        ],
        "how_it_helps":     [
            "Improves medication adherence and related health outcomes",
            "Provides peace of mind for clients and family members",
            "Supports independence by prompting rather than doing",
            "Reduces the risk of missed or doubled doses",
        ],
        "what_to_expect":   "Reminders are built into your care plan and delivered at the times your medications are scheduled. Caregivers do not handle or administer medications — they simply remind you it is time. If medication management concerns arise, a nurse on our team can assess further needs.",
        "why_signia":       "Small reminders make a big difference. Our caregivers approach every prompt with warmth and respect, helping you feel supported rather than managed.",
    },
    {
        "slug":       "treatment-exercise-reminders",
        "name":       "Treatment and Exercise Reminders",
        "short":      "Verbal or visual prompts for scheduled treatments, exercises, and health routines.",
        "icon":       "🏋️",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Treatment & Exercise Reminders | Signia Home Care Minneapolis MN",
        "meta_desc":  "Treatment and exercise reminders in Minneapolis and Twin Cities. Verbal and visual prompts to help individuals follow through on prescribed routines and exercises.",
        "hero_headline":    "Treatment and Exercise Reminders",
        "hero_sub":         "Keeping Your Health Routines on Track, Every Day",
        "intro":            "Prescribed exercises, wound care routines, and other health treatments are most effective when done consistently. Our caregivers provide friendly verbal or visual reminders to help individuals follow their prescribed routines without prompting from family members.",
        "description":      "Treatment and exercise reminder services include prompting individuals to perform their scheduled home exercises (as prescribed by physical or occupational therapy), complete wound care routines, use prescribed medical devices, or follow other health-related routines ordered by your doctor or health provider. The individual performs the activity themselves — the caregiver provides the reminder.",
        "who_benefits":     [
            "Individuals completing a home exercise program from physical or occupational therapy",
            "People with prescribed wound care or other home treatment routines",
            "Clients who benefit from gentle structure and reminders during the day",
            "Those recovering from surgery or illness and following a prescribed home protocol",
        ],
        "how_it_helps":     [
            "Supports compliance with prescribed therapeutic routines",
            "Promotes faster recovery and better outcomes through consistency",
            "Reduces the need for family members to manage or prompt daily routines",
            "Keeps individuals engaged and accountable in their own health",
        ],
        "what_to_expect":   "Reminders are incorporated into your daily care schedule. Caregivers are briefed on your prescribed routines and know when to prompt you. They support without taking over — preserving your independence and engagement in your own care.",
        "why_signia":       "Consistency is the key to progress. Our caregivers are cheerful reminders of what matters most — your health and your goals.",
    },
    {
        "slug":       "modified-diet-preparation",
        "name":       "Modified Diet Preparation",
        "short":      "Preparing texture-modified or therapeutic meals as ordered by a health professional.",
        "icon":       "👨‍🍳",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Modified Diet Meal Preparation | Signia Home Care Minneapolis MN",
        "meta_desc":  "Modified diet preparation in Minneapolis and Twin Cities. Caregivers prepare texture-modified and therapeutic meals based on licensed health professional orders.",
        "hero_headline":    "Modified Diet Preparation",
        "hero_sub":         "Nutritious, Safe Meals Tailored to Your Health Needs",
        "intro":            "For individuals who require a specific diet ordered by their physician or dietician — whether texture-modified, low-sodium, diabetic-friendly, or otherwise therapeutic — our trained caregivers ensure meals are prepared correctly and safely every time.",
        "description":      "Modified diet preparation involves preparing meals that follow specific dietary orders issued by your doctor or health provider, such as a physician, dietician, or speech-language pathologist. This may include chopped, minced, or pureed textures for swallowing safety, or nutritionally targeted meals for chronic disease management. Caregivers are briefed on the specific dietary needs and follow them consistently.",
        "who_benefits":     [
            "Individuals with dysphagia requiring texture-modified foods",
            "Clients with diabetes, kidney disease, or heart conditions requiring therapeutic diets",
            "People whose physician or dietician has ordered a specific dietary protocol",
            "Families who want assurance that prescribed diets are being followed correctly",
        ],
        "how_it_helps":     [
            "Ensures dietary orders are followed consistently and safely",
            "Reduces the risk of aspiration from improper food textures",
            "Supports chronic disease management through appropriate nutrition",
            "Takes the burden of specialized meal preparation off family caregivers",
        ],
        "what_to_expect":   "Your care team will receive and follow all dietary orders from your licensed health professional. Caregivers are trained on your specific requirements. Meal preferences and cultural considerations are incorporated where possible within the dietary guidelines.",
        "why_signia":       "A meal prepared with care and clinical accuracy is a gift. Our team takes modified diet preparation seriously — because your safety and nutrition are not things we ever take lightly.",
    },
    {
        "slug":       "laundry-services",
        "name":       "Laundry Services",
        "short":      "Help with washing, drying, and folding laundry to keep your home running smoothly.",
        "icon":       "🧺",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Home Care Laundry Services | Signia Home Care Minneapolis MN",
        "meta_desc":  "Laundry assistance in Minneapolis and Twin Cities. Caregivers help with washing, drying, folding, and putting away laundry as part of home care services.",
        "hero_headline":    "Laundry Services",
        "hero_sub":         "Clean Clothes, Fresh Home, One Less Worry",
        "intro":            "Laundry is one of those tasks that never stops — and for individuals with health challenges or limited mobility, it can become a real burden. Our caregivers help keep up with laundry so you or your loved one can focus on what matters most.",
        "description":      "Laundry services as part of home care may include sorting, washing, drying, folding, and putting away clothing, linens, and other household laundry. This service is provided in the context of a broader care plan and supports the overall health, hygiene, and comfort of the individuals we serve.",
        "who_benefits":     [
            "Individuals who have difficulty lifting, bending, or operating appliances",
            "Older adults who need support maintaining household routines",
            "People recovering from surgery or illness who have limited energy",
            "Caregivers who need relief from household task burden",
        ],
        "how_it_helps":     [
            "Ensures clean clothing and linens are always available",
            "Reduces physical strain for individuals with limited mobility or energy",
            "Supports overall hygiene and health through clean home textiles",
            "Frees up energy for activities and interactions that matter more",
        ],
        "what_to_expect":   "Laundry support is built into your care plan. Caregivers follow your preferences for sorting, washing, and organizing. This service is provided as part of your overall home care program.",
        "why_signia":       "It's the everyday things that make a home feel good. Our caregivers are happy to handle the laundry so you can rest, connect with family, or simply enjoy your day.",
    },
    {
        "slug":       "housekeeping-services",
        "name":       "Housekeeping and Household Chores",
        "short":      "Light housekeeping and household task support to keep your home safe and comfortable.",
        "icon":       "🧹",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Housekeeping & Home Care Chores | Signia Home Care Minneapolis MN",
        "meta_desc":  "Housekeeping and household chore support in Minneapolis and Twin Cities. Keeping your home clean, safe, and comfortable as part of our home care services.",
        "hero_headline":    "Housekeeping and Household Chores",
        "hero_sub":         "A Clean, Safe Home — for a Healthier, Happier You",
        "intro":            "A clean, organized home is more than comfortable — it's safer and healthier. When everyday housekeeping tasks become difficult, our caregivers step in to help keep your living space tidy and hazard-free.",
        "description":      "Housekeeping and household chore services may include light cleaning such as vacuuming, mopping, wiping surfaces, cleaning bathrooms and kitchens, taking out trash, and other routine household tasks. This service is included as part of a comprehensive home care plan and is designed to support the health and safety of the home environment.",
        "who_benefits":     [
            "Individuals who have difficulty with physical housekeeping tasks",
            "Older adults who want to maintain a clean, organized home",
            "People recovering from illness or surgery with limited energy",
            "Families who want assurance their loved one's home is clean and safe",
        ],
        "how_it_helps":     [
            "Reduces fall hazards from clutter and slippery surfaces",
            "Supports overall hygiene and health in the home environment",
            "Relieves stress associated with an unmaintained home",
            "Frees up time and energy for rest and meaningful activities",
        ],
        "what_to_expect":   "Housekeeping tasks are incorporated into your care plan based on your needs and preferences. Caregivers work efficiently and respectfully, following your household preferences. This service is part of your broader home care program.",
        "why_signia":       "Home should be a sanctuary. Our caregivers take pride in maintaining a clean, welcoming environment that makes coming home feel exactly as it should — comfortable and safe.",
    },
    {
        "slug":       "meal-preparation",
        "name":       "Meal Preparation",
        "short":      "Nutritious, home-cooked meals prepared by a caring caregiver.",
        "icon":       "🥘",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Meal Preparation Services | Signia Home Care Minneapolis MN",
        "meta_desc":  "Home meal preparation in Minneapolis and Twin Cities. Caregivers prepare nutritious, personalized meals to support health and independence at home.",
        "hero_headline":    "Meal Preparation Services",
        "hero_sub":         "Nourishing Meals, Made with Care",
        "intro":            "Good nutrition starts with good food — and good food starts with someone who cares enough to make it. Our caregivers prepare fresh, nutritious meals that reflect your preferences, dietary needs, and daily schedule.",
        "description":      "Meal preparation services include planning and preparing breakfast, lunch, dinner, and snacks based on the client's preferences, dietary needs, and any orders from your doctor or health provider. Caregivers can work with recipes, accommodate dietary restrictions, and ensure meals are served at an appropriate temperature and in an accessible setting.",
        "who_benefits":     [
            "Individuals who have difficulty cooking due to physical or cognitive challenges",
            "Older adults who want to maintain good nutrition at home",
            "People with dietary restrictions who need thoughtful meal planning and preparation",
            "Families who want a loved one to have regular, nourishing meals",
        ],
        "how_it_helps":     [
            "Ensures consistent access to nutritious, appealing meals",
            "Supports chronic disease management through diet adherence",
            "Reduces the risk of poor nutrition and related health complications",
            "Provides a comforting daily routine and social interaction at mealtime",
        ],
        "what_to_expect":   "Your preferences, cultural background, and dietary needs are central to how meals are planned and prepared. Caregivers are flexible, creative, and genuinely interested in making food you enjoy. Meals are prepared fresh and with care during each visit.",
        "why_signia":       "A good meal is an act of love. Our caregivers put heart into every dish they prepare, because we believe good nutrition and good food are essential parts of a good life.",
    },
    {
        "slug":       "shopping-assistance",
        "name":       "Shopping Assistance",
        "short":      "Grocery and essential shopping support to keep your home well-stocked.",
        "icon":       "🛒",
        "category":   "comprehensive",
        "category_label": "Comprehensive Home Care",
        "meta_title": "Shopping Assistance Services | Signia Home Care Minneapolis MN",
        "meta_desc":  "Grocery and shopping assistance in Minneapolis and Twin Cities. Caregivers help with grocery shopping and essential errands as part of home care services.",
        "hero_headline":    "Shopping Assistance",
        "hero_sub":         "Keeping Your Pantry Stocked and Your Needs Met",
        "intro":            "Getting to the grocery store can be a challenge for many individuals receiving home care. Our caregivers help ensure you always have what you need — from groceries to household essentials — so your home stays stocked and your needs are met.",
        "description":      "Shopping assistance services include accompanying clients on shopping trips or completing grocery and household shopping on their behalf, following a list provided by the client or care team. Caregivers may assist with carrying items, organizing purchases, and helping put groceries away at home.",
        "who_benefits":     [
            "Individuals who have difficulty driving or traveling to stores",
            "People with limited mobility or energy who cannot manage shopping independently",
            "Older adults who want help keeping their home stocked with essentials",
            "Clients who need assistance planning and completing grocery shopping",
        ],
        "how_it_helps":     [
            "Ensures consistent access to food and household essentials",
            "Reduces the burden of transportation and physical shopping challenges",
            "Supports nutrition and independence by keeping pantry needs met",
            "Provides a helpful, reliable routine that families can count on",
        ],
        "what_to_expect":   "Shopping assistance is scheduled as part of your care plan. Caregivers follow your shopping list, preferences, and budget guidance. If accompanying you, they provide physical support and assistance throughout the trip.",
        "why_signia":       "The little things matter. Whether it's making sure there's milk in the fridge or picking up a favorite snack, our caregivers are happy to handle the shopping so you can stay comfortable at home.",
    },
]

# ---------------------------------------------------------------------------
# Basic 245D Services
# ---------------------------------------------------------------------------
BASIC_245D_SERVICES = [
    {
        "slug":       "individual-community-living-supports",
        "name":       "Individual Community Living Supports (ICLS)",
        "short":      "Flexible support to help individuals live as independently as possible in their community.",
        "icon":       "🏡",
        "category":   "basic_245d",
        "category_label": "Basic 245D Support Services",
        "meta_title": "Individual Community Living Supports (ICLS) | Signia Home Care MN",
        "meta_desc":  "Individual Community Living Supports (ICLS) in Minneapolis and Twin Cities. Personalized home and community support for independence under Minnesota 245D.",
        "hero_headline":    "Individual Community Living Supports (ICLS)",
        "hero_sub":         "Personalized Support for Independent Living",
        "intro":            "Everyone deserves to live in the community of their choice, with the support they need to thrive. Individual Community Living Supports are designed to help individuals do just that — live as independently as possible, in their own home, on their own terms.",
        "description":      "Under Minnesota's 245D basic support services, Individual Community Living Supports (ICLS) provide flexible assistance with daily activities and community participation. Services may include help with personal care, household tasks, community navigation, skill-building, and other supports that promote independence and quality of life. ICLS are tailored to each person's individual goals and support plan.",
        "who_benefits":     [
            "Adults with disabilities who want to live independently in the community",
            "Individuals who receive services through Minnesota's Medicaid waiver programs",
            "People who need flexible, individualized support to participate fully in community life",
            "Those transitioning from more restrictive settings to community-based living",
        ],
        "how_it_helps":     [
            "Supports greater independence and community participation",
            "Builds daily living skills and confidence over time",
            "Provides flexible, person-centered support tailored to individual goals",
            "Reduces reliance on more restrictive care settings",
        ],
        "what_to_expect":   "Services are based on an individualized support plan developed with you and your support team. Signia Home Care works within the framework of your case management and waiver program. Services are subject to program eligibility, funding, and individual assessment.",
        "why_signia":       "We believe in the right of every person to live with dignity and independence. Signia Home Care's 245D-certified team is committed to providing person-centered support that helps you reach your goals and live well in your community.",
    },
    {
        "slug":       "24-hour-emergency-assistance",
        "name":       "24-Hour Emergency Assistance",
        "short":      "Around-the-clock support access for safety and peace of mind.",
        "icon":       "🚨",
        "category":   "basic_245d",
        "category_label": "Basic 245D Support Services",
        "meta_title": "24-Hour Emergency Assistance | Signia Home Care Minneapolis MN",
        "meta_desc":  "24-hour emergency home care assistance in Minneapolis and Twin Cities. On-call support for individuals with disabilities living independently in Minnesota.",
        "hero_headline":    "24-Hour Emergency Assistance",
        "hero_sub":         "Peace of Mind — Around the Clock",
        "intro":            "For individuals living independently, knowing that help is available at any hour provides essential peace of mind. Our 24-hour emergency assistance service ensures that support is never more than a call away, no matter when the need arises.",
        "description":      "24-hour emergency assistance is a 245D service that provides individuals with access to support at any time of day or night in the event of an emergency or an urgent need. This may involve telephone or electronic check-in, a scheduled overnight presence, or on-call availability depending on the individual's support plan. The service is designed to support safety and independence for individuals who live alone or without a constant caregiver.",
        "who_benefits":     [
            "Adults with disabilities who live independently and want safety assurance",
            "Individuals whose support plan identifies a need for emergency backup",
            "People who may need guidance or help during unexpected situations after hours",
            "Families who want peace of mind about a loved one's overnight safety",
        ],
        "how_it_helps":     [
            "Provides immediate access to support during after-hours emergencies",
            "Reduces anxiety and fear for individuals living alone",
            "Supports greater independence by providing a reliable safety net",
            "Ensures fast response to health or safety concerns at any hour",
        ],
        "what_to_expect":   "The format of emergency assistance is determined by your individual support plan. Services may include scheduled check-ins, a personal emergency response system, or on-call staff. All arrangements are made based on your specific needs and program eligibility.",
        "why_signia":       "We never stop caring — and neither does our on-call team. Signia Home Care is committed to being there for you, day or night, so you can live independently with confidence.",
    },
    {
        "slug":       "companion-services",
        "name":       "Companion Services",
        "short":      "Meaningful social connection and friendly companionship for those who need it most.",
        "icon":       "😊",
        "category":   "basic_245d",
        "category_label": "Basic 245D Support Services",
        "meta_title": "Companion Services | Signia Home Care Minneapolis MN",
        "meta_desc":  "Companion services in Minneapolis and Twin Cities. Friendly, meaningful social support and companionship for individuals receiving home care services in Minnesota.",
        "hero_headline":    "Companion Services",
        "hero_sub":         "Friendship, Connection, and Someone Who Cares",
        "intro":            "Loneliness and isolation can be as harmful to health as many physical conditions. Our companion services provide meaningful social connection, friendly conversation, and consistent human presence for individuals who benefit from regular companionship.",
        "description":      "Companion services under 245D basic support services provide supervision and social support through activities such as conversation, shared activities, accompanying clients on community outings, reading together, playing games, watching programs, and other socially meaningful interactions. Companions do not provide personal care, skilled nursing, or household tasks — they provide the gift of genuine human presence and engagement.",
        "who_benefits":     [
            "Individuals who experience social isolation or loneliness",
            "People who live alone and benefit from regular friendly interaction",
            "Older adults or individuals with disabilities who enjoy social engagement",
            "Clients whose care plan includes supervision or social support hours",
        ],
        "how_it_helps":     [
            "Reduces social isolation and the associated health impacts",
            "Provides consistent, friendly social engagement and supervision",
            "Supports emotional well-being and mental health",
            "Gives family caregivers reassurance and respite time",
        ],
        "what_to_expect":   "Companions are matched based on compatibility, interests, and personality. Visits are scheduled according to your support plan and may include activities of your choice. Companion services are a 245D basic support service and are subject to program eligibility and funding.",
        "why_signia":       "We believe that connection is care. Our companions are warm, genuine people who bring light and friendship to every visit — because everyone deserves someone who is truly glad to spend time with them.",
    },
    {
        "slug":       "homemaker-services",
        "name":       "Homemaker Services",
        "short":      "Household task support to keep your home safe, clean, and comfortable.",
        "icon":       "🏠",
        "category":   "basic_245d",
        "category_label": "Basic 245D Support Services",
        "meta_title": "Homemaker Services | Signia Home Care Minneapolis MN",
        "meta_desc":  "Homemaker services in Minneapolis and Twin Cities. Household support including cleaning, laundry, and errands for individuals receiving 245D services in Minnesota.",
        "hero_headline":    "Homemaker Services",
        "hero_sub":         "A Well-Kept Home — for a Better Quality of Life",
        "intro":            "Maintaining a clean, organized, and safe home environment is essential for health and well-being. Homemaker services provide practical household support that helps individuals focus on what truly matters — living their life.",
        "description":      "Homemaker services under Minnesota's 245D basic support services provide assistance with household tasks that the individual is unable to perform due to their disability or condition. Services may include cleaning, laundry, grocery shopping, light meal preparation, and other household activities that maintain a healthy home environment. Homemaker services do not include personal care.",
        "who_benefits":     [
            "Individuals with disabilities who have difficulty managing household tasks",
            "People who receive services under a Minnesota Medicaid waiver program",
            "Adults who need structured household support to maintain safe, independent living",
            "Those whose support plan includes homemaker assistance as a funded service",
        ],
        "how_it_helps":     [
            "Maintains a clean, safe, and organized home environment",
            "Reduces stress from overwhelming or physically demanding household tasks",
            "Supports health and hygiene through consistent home maintenance",
            "Allows individuals to focus energy on activities that bring meaning and joy",
        ],
        "what_to_expect":   "Homemaker services are based on your individual support plan and scheduled accordingly. Caregivers follow your preferences and work within the scope of your approved services. Services are subject to program eligibility and individual assessment.",
        "why_signia":       "A well-maintained home is the foundation of independent living. Our homemakers take their work seriously — providing reliable, respectful support that makes a real difference in daily life.",
    },
    {
        "slug":       "individualized-home-supports",
        "name":       "Individualized Home Supports Without Training",
        "short":      "Flexible, personalized support for daily tasks and community participation at home.",
        "icon":       "⭐",
        "category":   "basic_245d",
        "category_label": "Basic 245D Support Services",
        "meta_title": "Individualized Home Supports | Signia Home Care Minneapolis MN",
        "meta_desc":  "Individualized home supports (without training) in Minneapolis and Twin Cities. Flexible, person-centered assistance for daily living under Minnesota 245D.",
        "hero_headline":    "Individualized Home Supports Without Training",
        "hero_sub":         "Personalized, Flexible Support — Built Around You",
        "intro":            "Not everyone needs the same kind of support — and your care shouldn't be one-size-fits-all. Individualized Home Supports provide flexible, person-centered assistance that adapts to your unique needs, goals, and daily routines.",
        "description":      "Individualized Home Supports without training is a 245D basic service that provides assistance with activities of daily living and support for community participation based on a person's individual needs and goals. Services are not focused on skill-building or teaching (which would fall under 'with training') but rather on providing direct, practical support. The specific services provided are determined by the individual's support plan.",
        "who_benefits":     [
            "Adults with disabilities who need flexible, individualized daily support",
            "Individuals whose needs do not require a training or skill-building focus",
            "People enrolled in Minnesota Medicaid waiver programs with this funded service",
            "Those who want consistent, familiar support from a trusted provider",
        ],
        "how_it_helps":     [
            "Provides flexible, personalized support matched to your individual needs",
            "Supports daily living activities and community participation",
            "Offers consistency and reliability in day-to-day support",
            "Respects individual preferences and routines in service delivery",
        ],
        "what_to_expect":   "Services are defined by your individual support plan, developed with your case manager and support team. Signia Home Care works collaboratively within that plan to provide consistent, reliable support. Eligibility is determined by your waiver program.",
        "why_signia":       "Your support plan should be as unique as you are. Signia Home Care takes the time to understand who you are, what matters to you, and how we can best support your daily life.",
    },
    {
        "slug":       "night-supervision",
        "name":       "Night Supervision",
        "short":      "Overnight caregiver presence for safety, reassurance, and nighttime support.",
        "icon":       "🌙",
        "category":   "basic_245d",
        "category_label": "Basic 245D Support Services",
        "meta_title": "Night Supervision Services | Signia Home Care Minneapolis MN",
        "meta_desc":  "Night supervision home care in Minneapolis and Twin Cities. Overnight caregiver presence for safety, reassurance, and support under Minnesota 245D.",
        "hero_headline":    "Night Supervision Services",
        "hero_sub":         "Rest Easy — Knowing Someone Is There",
        "intro":            "Nighttime can be a vulnerable time for individuals who need support. Whether the concern is safety, confusion, fall risk, or simply the reassurance of knowing someone is nearby, our night supervision service provides a trained caregiver through the overnight hours.",
        "description":      "Night supervision is a 245D basic support service that provides an awake or on-call caregiver in the home overnight to monitor and respond to the needs of the individual being served. The caregiver provides supervision, safety monitoring, and assistance as needed throughout the night. This service is appropriate for individuals who cannot safely be left alone overnight.",
        "who_benefits":     [
            "Individuals who wander or experience confusion at night",
            "People who cannot safely manage nighttime needs without assistance",
            "Clients at risk of falls or injury during overnight hours",
            "Families who need overnight support coverage while getting needed rest",
        ],
        "how_it_helps":     [
            "Ensures immediate response to overnight needs or emergencies",
            "Significantly reduces nighttime fall and safety risks",
            "Gives family caregivers the rest they need to continue daytime caregiving",
            "Provides the individual with comfort and security through the night",
        ],
        "what_to_expect":   "Night supervision is scheduled according to your support plan and individual needs. Caregivers are alert and available throughout the designated hours. Services are individualized and subject to program eligibility and funding.",
        "why_signia":       "Peace of mind has no bedtime. Our overnight caregivers bring calm, attentive presence through the night — so both individuals and family caregivers can rest more easily.",
    },
    {
        "slug":       "respite-care",
        "name":       "Respite Care Services",
        "short":      "Planned relief for family caregivers — so everyone gets the rest they need.",
        "icon":       "💙",
        "category":   "basic_245d",
        "category_label": "Basic 245D Support Services",
        "meta_title": "Respite Care Services | Signia Home Care Minneapolis MN",
        "meta_desc":  "Respite care in Minneapolis and Twin Cities. Planned caregiver relief so family caregivers can rest, recharge, and continue providing loving care at home.",
        "hero_headline":    "Respite Care Services",
        "hero_sub":         "Rest for Caregivers. Continuity of Care for Loved Ones.",
        "intro":            "Caring for a loved one is one of the most meaningful things a person can do — and one of the most demanding. Respite care provides temporary, planned relief for family caregivers, giving them time to rest, recharge, and attend to their own needs.",
        "description":      "Respite care is a 245D basic support service that provides planned, temporary substitute care for a primary caregiver. A trained Signia Home Care caregiver steps in to care for your loved one while you take a break — whether for a few hours, a day, or longer as allowed by your program. Respite services support the sustainability of family caregiving and benefit both the caregiver and the person being served.",
        "who_benefits":     [
            "Family caregivers who provide the primary care for a loved one with a disability",
            "Individuals whose care plan includes respite as a funded 245D service",
            "Families experiencing caregiver fatigue or burnout",
            "Primary caregivers who need time for their own appointments, errands, or rest",
        ],
        "how_it_helps":     [
            "Prevents caregiver burnout and supports long-term caregiving sustainability",
            "Provides the person being served with consistent, trusted substitute care",
            "Gives family caregivers the rest and renewal they need",
            "Supports the health and well-being of the entire family unit",
        ],
        "what_to_expect":   "Respite care is scheduled in advance as part of your support plan. Signia Home Care caregivers are introduced and familiarized with the individual's needs and routines before providing substitute care. Services are individualized and subject to program eligibility and funding limits.",
        "why_signia":       "Caring for a caregiver is caring for the whole family. Signia Home Care is honored to provide respite services that allow families to sustain their commitment to their loved ones — for the long haul.",
    },
]

# Combined lookup for service detail pages
ALL_SERVICES = {s["slug"]: s for s in COMPREHENSIVE_SERVICES + BASIC_245D_SERVICES}

# ---------------------------------------------------------------------------
# Context helper — inject BUSINESS info into every template
# ---------------------------------------------------------------------------
@app.context_processor
def inject_globals():
    return {"business": BUSINESS}

# ---------------------------------------------------------------------------
# Main Pages
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    all_svcs = COMPREHENSIVE_SERVICES + BASIC_245D_SERVICES
    return render_template(
        "index.html",
        title="Compassionate Home Care in Minneapolis, MN | Signia Home Care",
        meta_desc="Signia Home Care provides compassionate, state-certified home care services in Minneapolis and the Twin Cities. Skilled care and daily living support. Call today.",
        services_preview=all_svcs[:8],
    )

@app.route("/about/")
def about():
    return render_template(
        "about.html",
        title="About Us | Signia Home Care – Minneapolis, MN",
        meta_desc="Learn about Signia Home Care — a trusted Minnesota home care team dedicated to compassionate, dignified care in Minneapolis and the Twin Cities.",
    )

@app.route("/services/")
def services():
    return render_template(
        "services/index.html",
        title="Our Services | Signia Home Care – Minneapolis, MN",
        meta_desc="Signia Home Care offers a wide range of home care services in Minneapolis and the Twin Cities — nursing, therapy, personal care, companionship, and more.",
        all_services=COMPREHENSIVE_SERVICES + BASIC_245D_SERVICES,
    )

@app.route("/services/comprehensive-home-care/")
def comprehensive_home_care():
    return redirect(url_for("services"), 301)

@app.route("/services/basic-245d/")
def basic_245d():
    return redirect(url_for("services"), 301)

@app.route("/services/<slug>/")
def service_detail(slug):
    service = ALL_SERVICES.get(slug)
    if service is None:
        return render_template("404.html", title="Page Not Found"), 404

    # Related services: 3 others from the full list (exclude current)
    related = [s for s in COMPREHENSIVE_SERVICES + BASIC_245D_SERVICES if s["slug"] != slug][:3]

    return render_template(
        "services/detail.html",
        title=service["meta_title"],
        meta_desc=service["meta_desc"],
        service=service,
        related=related,
    )

@app.route("/referral/", methods=["GET", "POST"])
def referral():
    if request.method == "POST":
        # TODO: Integrate with an email service or CRM (e.g., SendGrid, Mailchimp)
        # Fields collected: referrer_name, organization, phone, email,
        #                   client_name, client_phone, service_interest, notes
        referrer_name = request.form.get("referrer_name", "").strip()
        if not referrer_name:
            flash("Please enter your name.", "error")
            return redirect(url_for("referral"))
        flash(
            "Thank you for your referral! A member of our team will follow up within one business day.",
            "success",
        )
        return redirect(url_for("referral"))
    return render_template(
        "referral.html",
        title="Make a Referral | Signia Home Care Minneapolis MN",
        meta_desc="Refer a patient or client to Signia Home Care in Minneapolis. Simple referral process for hospitals, social workers, case managers, and families.",
        all_services=COMPREHENSIVE_SERVICES + BASIC_245D_SERVICES,
    )

@app.route("/careers/", methods=["GET", "POST"])
def careers():
    if request.method == "POST":
        # TODO: Save application to database or email to HR
        first_name = request.form.get("first_name", "").strip()
        if not first_name:
            flash("Please enter your first name.", "error")
            return redirect(url_for("careers") + "#apply")
        flash(
            "Thank you for applying! We've received your application and will be in touch if there is a potential fit.",
            "success",
        )
        return redirect(url_for("careers") + "#apply")
    return render_template(
        "careers.html",
        title="Careers | Join the Signia Home Care Team – Minneapolis, MN",
        meta_desc="Join the Signia Home Care team in Minneapolis, MN. We're hiring compassionate caregivers, nurses, and support staff across the Twin Cities.",
    )

@app.route("/contact/", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # TODO: Integrate with an email service or CRM
        name = request.form.get("name", "").strip()
        if not name:
            flash("Please enter your name.", "error")
            return redirect(url_for("contact"))
        flash(
            "Thank you for reaching out! We will be in touch within one business day.",
            "success",
        )
        return redirect(url_for("contact"))
    return render_template(
        "contact.html",
        title="Contact Us | Signia Home Care – Minneapolis, MN",
        meta_desc="Contact Signia Home Care in Minneapolis, MN. We'd love to answer your questions about home care services for you or a loved one.",
    )

# ---------------------------------------------------------------------------
# Error Handlers
# ---------------------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", title="Page Not Found | Signia Home Care"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html", title="Something Went Wrong | Signia Home Care"), 500

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Development only — use gunicorn in production
    app.run(debug=True, host="0.0.0.0", port=5001)
