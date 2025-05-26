# Single Sign-On Operations SharePoint Site

**Base URL:** `https://otshare.nam.citi.net/sites/SSOEXT/`

---

## 1. Home - SSO Overview

* **Source URL:** `https://otshare.nam.citi.net/sites/SSOEXT/default.aspx`
* **Time in Video:** 0:04 - 0:16
* **Content:**
  * **Page Title:** Single Sign-On Operations
  * **Department Head:** Hartley, John
  * **Overview:** The Authentication Operations team is responsible for day-to-day operations and support for global Single Sign-On applications and Ping directory infrastructure.
  * **Services Include:**
    * Support for SiteMinder, CITI Federation, and PING user Directory (CitiAc/CRISSO External) clients' onboarding and integration.
    * Extended integration support via GSRE Hosting Group for their clients.
    * Setup of LDAP (Static/Dynamic) groups and functional IDs for applications integrated with SSO products or PING directory services.
  * **Technical Support:** Report via GIAM One Stop Shop & Virtual Assistant.
  * **Reference:** SSO Incident Tickets – Guidelines and other quick links on the SharePoint site.
  * **Site Purpose:** Provide basic information on Authentication Services processes and self-service via operational reports and lookup. For technical details, refer to the CtiSSO Engineering site.
  * **Authentication Services Weekly Client Open Forums:**
    * Encouragement for clients to join weekly forums for questions on processes or requests.
    * **NAME (North America):** Every Tuesday and Thursday, 11:00 AM - 11:30 AM ET (NY). Zoom/Citi Meeting ID: 858 257 3397, Passcode: 253724. (Link to local dial-in phone numbers).
    * **ASIA:** Every Wednesday Evening, 04:00 PM - 04:30 PM SST (Singapore Standard Time). Zoom/Citi Meeting ID: 858 298 0119, Passcode: 291297.
  * **Announcements:** "There are no items to show in this view of the 'Announcements' list."
  * **Useful Links (Sidebar):**
    * Cited FAQ
    * CATE - Siteminder Engineering Site
    * CATE - LDAP Engineering Site
    * CtiSAML/JS Affiliate Solution
    * Infoman (Change Management System)
    * Siteminder FAQ's
    * Siteminder Vulnerability Assessment (VA) Finding Remediation Guidance/Best Practices
    * Tivoli Website
    * Support Team Contacts
    * Resource for Siteminder technical details and downloads.
    * LDAP Engineering
    * Infoman aka VC (Virtual Change)/RFC (Request for Change)
    * Siteminder FAQs at Engineering Site
    * SiteMinder Vulnerability Assessment (VA) Finding Remediation Guidance/Best Practices
  * **Staff Contact (Sidebar):**
    * Authentication Operations Contact Sheet.xlsx
  * **Image:** "citi SSO Single Sign-On Operations" logo with a checkmark.

---

## 2. SecureSSO Application Onboarding Process

* **Source URL:** `https://otshare.nam.citi.net/sites/SSOEXT/Pages/SecureSSO_Application_Onboarding_Process.aspx`
* **Time in Video:** 0:16 - 0:34
* **Content:**
  * **What is Secure SSO?:** An identity and access management solution for web applications within Citi, providing SSO by integrating with PingFederate (OAuth2 Authorization Server) using OpenID Connect. Its main function is to protect an application or API.
  * **Instructions:**
        1. Report all onboarding issues via tickets: `https://otshare.nam.citi.net/sites/SSOEXT/pages/vt_reqs.aspx`
        2. Refer to SecureSSO agent supported matrix on PingAccess Agent Supported Platforms (CEDT Confluence DC - nsoot.net) before raising CMP.
        3. Client DEV, UAT, and PROD applications must be on the same platforms; deviations are not supported.
        4. If LDAP group/FID protection is needed, specify this in CMP. FID/LDAP group requests must precede SecureSSO integration requests. Group/FID names must be consistent across environments.
            *Corporate LDAP SSO - Create New Group (DEV/UAT): `https://marketplace.citigroup.net/product/39841_29362_GLOBAL`
            * Corporate LDAP SSO - Create New Group (PROD): `https://marketplace.citigroup.net/product/39841_38478_GLOBAL`
            * SSO Functional ID - Create ID: `https://marketplace.citigroup.net/product/47394_99782_GLOBAL`
        5. Correctly submitted Secure SSO CMP requests are approved within SLO. Fulfilled requests trigger an automated email with agent properties for webserver configuration.
        6. Non-compliant requests are rejected with automated notification.
        7. Maximum one application per CSI per environment per domain. Multiple URLs can be added via SecureSSO - Policy Modify.
        8. For applications with MFA critical functions (MFA-FFEC), MFA committee approval is mandatory before CMP creation. Contact "IS Global MFA Assessment Group" for guidance.
        9. SLO for all requests: `https://otshare.nam.citi.net/sites/SSOEXT/pages/SLO.aspx`
  * **Process by Environment (Development, UAT, PROD):**
    * **Development:**
            1. **Initiate Request:** Raise CMP for new SecureSSO Integration (Product - SecureSSO - Policy Create). Automated notification upon submission.
            2. **Configure Web-App Servers:** Use agent properties from automated email. Refer to PingAccess Agent Supported Platforms (CEDT Confluence DC) for guidance. Installation via CAS/Starfleet/Manual.
            3. **Perform Application Testing:** Application team tests in dev. Report SSO issues via ticket: `https://otshare.nam.citi.net/sites/SSOEXT/pages/vt_reqs.aspx`
            4. **Modification to DEV Setups:** Use CMP Product - Ping Access - Policy Modify.
    * **UAT:**
            1. **Promote Development to UAT:** Raise CMP (Product - SecureSSO - Policy Promote).
            2. **Configure Web-App Servers:** (Same as Development Step 2).
            3. **Perform Application Testing:** (Same as Development Step 3).
            4. **Modification to UAT Setups:** (Same as Development Step 4).
    * **PROD:**
            1. **Promote UAT to PROD:** Raise CMP (Product - SecureSSO - Policy Promote).
            2. **PROD Request Completion:** Approved within SLO during SSO GreenZone (considering Global Change Freeze). Automated email with agent properties upon fulfillment. Certain requests require application team checkout/logoff post-change, with email approval from owner/requestor.
            3. **Configure Web-App Servers:** (Same as Development Step 2).
            4. **PROD Application Checkout:** Application team must perform checkout. Designated tester must be online. SSO team won't perform change if tester is unavailable. Application support handles middleware/SA coordination for restarts. Report production checkout issues promptly for rollback during green zone.
            5. **Modification to PROD Setups:** (Same as Development Step 4).

---

## 3. SSO CitiFederation On-Boarding Process (SAML)

* **Source URL:** `https://otshare.nam.citi.net/sites/SSOEXT/Pages/CitiFederation_application_onboarding_Process_SAML.aspx`
* **Time in Video:** 0:34 - 1:05
* **Content:**
  * **NOTE:** Application team tracks SP/encryption certificate expiry via SSL tracker (Other type certificates ONLY). Submit crm-product to add certificate if not in SSL tracker.
  * **STEPS FOR DEVELOPMENT SETUP:**
        1. **Initiate Request:** Raise CMP: `https://marketplace.citigroup.net/product/57369_10984_GLOBAL`
        2. **Create FID or LDAP group (if needed):**
            *New Functional ID: `https://marketplace.citigroup.net/product/39841_29362_GLOBAL` (this link seems to be for LDAP group, FID link might be different or missing)
            * New LDAP Group (DEV/UAT): `https://marketplace.citigroup.net/product/39841_29362_GLOBAL`
            *Separate requests for FID per environment. One LDAP group request for DEV/UAT, separate for PROD.
        3. **Public Certificates:**
            * IDP use case (Citi is IDP): Citi public cert provided to app team (download from `https://otshare.nam.citi.net/sites/SSOEXT/SitePages/PING%20Federation.aspx`). Vendor installs to verify assertion.
            *SP use case (Citi is SP): App team gets vendor's public cert, uploads in CMP. Citi business requestor manages certs, provides updates 100+ days before expiry. Assertion: min 5 min validity (300s).
            * Self-signed certs not allowed.
            *Onboard external CA certs (non-MSPI/Digicert) in SSL Tracker via CitiMarketplace (SSL Certificate Tracker - Other type certificates ONLY).
            * Submit CitiMarketplace request for cert renewal via CitiFederation - Modification.
        4. **Auth Services Completes Request:** Automated email sent. CitiFederation URL provided. LDAP groups created if requested.
        5. **Perform Application Testing:** App team tests in dev. Report issues via ServiceNow (GIAM Virtual Assistant: `https://otshare.eur.citi.net/sites/GIAMOSS/prod/index.aspx?dialog=secops#`).
        6. **Proceed to UAT Request.**
  * **STEPS FOR STAGING/UAT SETUP:**
        1. **Promote Dev to UAT:** Raise CMP (same link as Dev Step 1).
        2. **Public Certificates:** (Same as Dev Step 3).
        3. **Auth Services Completes Request:** Automated email with info. SAML URL provided. FIDs created if requested.
        4. **Perform Application Testing:** (Same as Dev Step 5).
        5. **Raise CMP for UAT Performance Analysis:** Collect logs (3 users), submit CitiFederation - UAT Performance Analysis: `https://marketplace.citigroup.net/product/38417_10524_GLOBAL`. Proceed after CMP completion.
        6. **Proceed to Production Request.**
  * **STEPS FOR PRODUCTION SETUP:**
        1. **Promote UAT to PROD:** Raise CMP (same link as Dev Step 1).
        2. **Create FID or LDAP group (if needed):**
            * New LDAP Group (PROD): `https://marketplace.citigroup.net/product/39841_38478_GLOBAL`
        3. **Public Certificates:** (Same as Dev Step 3).
        4. **Auth Services Raises ServiceNow Change:** Seeks App Manager approval (info from CSI). Change not completed without approval. Email includes checkout details. SN approval code added to Auth Services.
        5. **Auth Services Completes Request:** Automated email with info. CitiFederation URL provided. LDAP groups created.
        6. **Application Checkout:** App team performs checkout. Issues resolved same day (if green zone/resources permit). Later issues: open ServiceNow ticket. Recommended: checkout during change window. Change may be cancelled if approval/checkout details not provided.

---

## 4. MFA (Multi Factor Authentication)

* **Source URL:** `https://otshare.nam.citi.net/sites/SSOEXT/Pages/mfa.aspx`
* **Time in Video:** 1:06 - 1:09
* **Content:**
  * **Title:** MFA (Multi Factor Authentication)
  * "Please visit the MFA-SharePoint Site for MFA related information." (Link to an "MFA-SharePoint Site").

---

## 5. Host Registration Process - New

* **Source URL:** `https://otshare.nam.citi.net/sites/SSOEXT/Pages/Host_Registration_Process_New.aspx`
* **Time in Video:** 1:10 - 1:34
* **Content:**
  * **Title:** New Host Registration Process
  * For new/replacement Web Agents for SSO Apps. Requires Host Registration, valid Change Control for PROD, and a task.
  * **Product Downloads:** `https://catecollaboration.citigroup.net/domains/security/idem/accessmgmt/citiso/SiteMinder%20_6.X_Product_Downloads/pkgs.aspx`
  * **PROD Host Registrations:** Only during SSO green zones (NA/LATAM: Mon-Thu 5-9PM EST, Fri 5PM EST-Sun 5PM EST; EMEA: Mon-Thu 5-9PM GMT, Fri 5PM GMT-Sun 5PM GMT; ASPAC: Mon-Thu 5-9PM SST, Fri 5PM SST-Sun 5PM SST).
  * **Note:** No changes during scheduled weekend server reboots (Sun 12AM-12PM local time).
  * **Effective May 8, 2023:** No manual password release. Retrieve Thadmin passwords from CyberArk.
  * **Detailed Instructions:**
        1. **Request Access to CyberArk Safe:** (One-time, per user, per environment).
            *Submit in Citi Marketplace (Guide provided).
            * Object: User ID; Type: Add/Change group membership; Safe: (from chart); Role: Req.
            *CyberArk Safe Info Table: DEV (Thadmin_D_Safe), UAT (Thadmin_U_Safe), PROD (Thadmin_P_Safe).
            * Note: 2-day SLO (excluding approvals).
        2. **Schedule Host Registration:**
            *DEV/UAT: Valid Incident Ticket. PROD: Valid Change Record. Include Siteminder system name in CI Section.
            * Siteminder System Names Table: Lists system names for DEV (Any), UAT (Any), PROD (APAC, EMEA, NAM).
            *DEV/UAT INC Template: `TTMP0000253095` (link provided).
            * PROD Change Record Template: `CTTMP0000091858` (link provided).
            *PROD Change Task Template: `TTMP0000091498` (link provided).
            * ***USE TEMPLATE OR REJECTED***
        3. **Retrieve Password:**
            *Submit/approve CyberArk password requests before release. Window <= 4 hours, within designated Password Release Window. Approval from*CISO Global Cyber Security Services - SSO L3 A Team.
            *Links to submit requests for PROD (CyberArk IM RPA) and DEV/UAT (CyberArk Common Build UAT).
            * Form Guide: Reason: RCT#Scheduled Change/Release; Ticketing System: ServiceNow-INC (DEV/UAT), ServiceNow-CHG (PROD); Ticket ID: <System Name>@<INC/CHG #>.
            * Host Registration FIDs Table: Lists Pwd Release Window, CyberArk env, Region, Available FIDs (Thadmin, Thadminm1_fid, Thadminm2_fid for DEV/UAT; Thadminasia, Thadminemea, Thadmin for PROD).
        4. **CyberArk Password Retrieval Process & FAQ:** (Link to further information).

---

## 6. Quick Process Overview

* **Source URL:** `https://otshare.nam.citi.net/sites/SSOEXT/Pages/Quick_Process.aspx`
* **Time in Video:** 1:34 - 1:57
* **Content:**
  * Table with "I want to...", "Process", "SLO/SLT" columns.
  * **General Questions:** Join Weekly Client Open Forum (Tue/Thu 11-11:30 AM ET, Zoom ID: 858 257 3397, Passcode: 253724).
  * **Set up new App:** Via CMP, automated approval: `https://cmp.nj.ssmb.com/marketplace/control/product/-productid=48317_50822_GLOBAL#`
  * **Update existing App:** Via CMP: `https://cmp.nj.ssmb.com/marketplace/control/product/-productid=48317_45597_GLOBAL`. For UAT/PROD, modify DEV first, then promote: `https://marketplace.citigroup.net/marketplace/control/product/-productid=51735_10313_GLOBAL`. Note ACO params (CsChecking, etc.) need BISO approval. UAT Perf. Analysis needed for new protected URL. Add new server/hostname in SM Register.
  * **Retire/Decommission App:** CMP for all 3 envs (Dev->Stage->Prod): `https://cmp.nj.ssmb.com/marketplace/control/product/-productid=48317_24185_GLOBAL#`. If LDAP Groups, raise 3 CMPs to delete them.
  * **Raise UAT analysis request:** Via CMP: `https://cmp.nj.ssmb.com/marketplace/control/product/-productid=31622_55300_GLOBAL#`
  * **Create new LDAP Group:** Citi Marketplace. Dev/UAT: `...productid=39841_29362_GLOBAL#`. Prod: `...productid=39841_38478_GLOBAL#`. (Fails if group not in Dev/UAT).
  * **Delete LDAP Group:** Citi Marketplace: `...ctid=48242_494834_GLOBAL#`
  * **Bulk Upload to LDAP group:** Citi Marketplace for single user add/remove, then option for bulk: `...ctid=47385_60055_GLOBAL#`. If not working, open ticket: `.../vt_reqs.aspx`
  * **SSO Password reset:** Use OneReset (Real Time).
  * **Request/Modify LDAP functional ID (Direct bind / non-Siteminder):** Citi Marketplace. Create FID: `...productid=47394_41536_GLOBAL#`. Reset/Change CSI: `...productid=47394_107498_GLOBAL#`. FID Deletion: `...productid=48242_476227_GLOBAL#` (only for IDs under <serfunids>). Legacy FIDs (sitemdradmin, etc.): `...productid=31622_550711_GLOBAL#`.
  * **Request/Modify LDAP functional ID (Siteminder/monitoring):** (Same links as above).
  * **Request new/modify LAD ID creation:** Citi Marketplace. Create: `...productid=48242_32196_GLOBAL#`. Update: `...productid=48242_42022_GLOBAL#`. Deletion: `...productid=48242_49649_GLOBAL#`.
  * **Update LDAP Group Description:** Citi Market Place ('Corporate LDAP SSO - Modify LDAP Group Description').
  * **Update CSI id for LDAP Group:** Citi Marketplace: `...ctid=48242_69873_GLOBAL#`
  * **Change Group Owner of LDAP Group:** Citi Marketplace (enter exact group name, link to search for group).
  * **Request Auth Ops SME on conf call:** Raise ServiceNow Ticket (per SSO Incident Ticket Guidelines).
  * **Fix issue in policy setup:** Raise ServiceNow Ticket (per SSO Incident Ticket Guidelines).
  * **Get info on SSO VA remediation:** Refer to "SSO Vulnerability Assessment (VA) Issues" on site (N/A SLO/SLT).
  * **Obtain Siteminder docs:** Refer to "SSO Engineering site under Obtain documents" (N/A SLO/SLT).
  * Footer: "For any other queries or questions, please open a VT and assign it to SSO".

---

## 7. SSO Incident Tickets - Guidelines

* **Source URL:** `https://otshare.nam.citi.net/sites/SSOEXT/Pages/vt_reqs.aspx`
* **Time in Video:** 1:57 - 2:11
* **Content:**
  * **Title:** Steps to report an issue with Siteminder, LDAP, CitiFederation, SecureSSO
  * **Guidelines for opening tickets:**
        1. Use CHATBOT (GIAM Assistant) first.
        2. On GIAM Assistant, click 'Chat with the Virtual Assistant.'
        3. Provide keyword/description/error message.
        4. Follow BOT prompts for resolution/answers.
        5. If unresolved, submit further responses to Chatbot for incident ticket.
        6. Provide details (issue type/impacted users) for BOT to generate INC.
        7. Chatbot generates INC, trackable via ServiceNow.
        8. Work with INC assignee.
        9. Refer L3 Ops SLO: `https://otshare.nam.citi.net/sites/SSOEXT/pages/SLO.aspx`
        10. Service management portal: `https://servicemanagement.citigroup.net/` (to track INC).
  * **Review SLO/Escalation:** SLO: `.../SLO.aspx`. Escalation: `.../escalation.aspx`.
  * **Minimum Info for Incidents (Priority Order):**
        1. Single/multiple users?
        2. User ID(s) reported.
        3. Impacted Env (Dev/UAT/Prod).
        4. Time of issue + timezone.
        5. Screenshot of error + sequence of events.
        6. Reproducible?
        7. Last working time?
        8. Changes since last working?
        9. If 24*7 work possible, provide contact details (name, number, timezone).
  * **SSO/Siteminder/Desktop SSO Issues:**
    * Provide webserver/OS version, type, bit level.
    * For webagent: Siteminder webagent/trace logs (time of issue + timezone), webagent.conf, smhost.conf, webserver access/error logs, header trace (Ethereal). TAI logs (for TAI agent).
    * For API/SDK: Property file (Siteminder config), API code execution output.
  * **Federation/SAML Issues:**
    * Type of setup (IDP/SP, Websso), CMP/Archer #, IDP/SP name, App URL, Federation Logs.
  * **Direct Bind LDAP/LAD Issues:**
    * Functional ID/LAD ID/LDAP group name, LDAP servers/DNS alias, LDAP Logs (showing error).

---

## 8. SSO SLA aka SLO/SLT

* **Source URL:** `https://otshare.nam.citi.net/sites/SSOEXT/Pages/SLO.aspx`
* **Time in Video:** 2:11 - 2:23
* **Content:**
  * Incident tickets (ServiceNow, assigned to Auth Services) subject to SLO.
  * **SEV 1 & 2:** Only PROD.
    * **SEV 1 (Major outage):** Response ASAP, work until SEV 2 state/repair.
    * **SEV 2 (Service impacted):** Response at earliest (after SEV 1s), work until SEV 3 state/repair.
    * **SEV 3 (Dev/UAT, etc.):** Actioned after SEV 1/2s addressed.
  * **Order of Priority:**
        1. Prod Env Outage (Immediate).
        2. Prod App down/service impact (Immediate).
        3. App in Prod, GO LIVE affected (ASAP).
        4. UAT SSO infra down.
        5. DEV SSO infra down.
        6. Dev/UAT Issues (Up to 10 business days). Auth Services works on tickets per order in CTI GL EX SECOPS SSO A queue. Resolve within 10 biz days (delays possible).
  * Tickets via `.../vt_reqs.aspx` process are subject to SLO.
  * **Please Note:**
        1. SLO clock starts after ticket reaches Auth Services queue (Triage/Dispatch) with all info.
        2. No email responses. Creator works with assignee via SN, sets up calls.
        3. Auth Services supports 2000+ apps globally, team in shifts, no dedicated support per app/project. Work based on Auth Services SLO.
  * **Siteminder / LDAP / Citi Federation / SecureSSO (CMP Automation / Manual):**
    * Dev/UAT: 5 biz days; Prod: 6 biz days per request (1 request per env/CMP).
  * **Citi Federation UAT Analysis CMP Requests:**
    * 2 biz days for approval (if CMP has all info).
    * 6 biz days post-approval for UAT analysis & update in Resolve IT.
  * **SSO Changes:** First come, first serve.
  * Prioritization for PROD (cannot wait for SLO): Refer to Business Critical Process.
  * Freeze period not in SLO. Prod changes during freeze must follow documented Business Critical Process.
  * Do not raise same request in all envs simultaneously (will be rejected). Complete Dev before UAT, UAT before Prod.

---

## 9. SSO Client Escalation Process

* **Source URL:** `https://otshare.nam.citi.net/sites/SSOEXT/Pages/escalation.aspx`
* **Time in Video:** 2:23 - 2:43
* **Content:**
  * **Title:** Escalation Process
  * Refer to SLO/SLT for response times. Escalate if SLO/SLT not met.
  * **Authentication Services Escalation Tree (L3 Ops):** (Provide sufficient time between escalations)
        1. Open incident ticket: `.../vt_reqs.aspx`
        2. Notify *CISO Global Cyber Security Services - Triage and Dispatch* to escalate (with justification).
        3. Urgent/outages (if no quick response after step 2): Contact Incident Management to engage Auth Services.
        4. Escalate to L3 Ops Managers for unresponded/higher priority tickets.
            *ASPAC Manager: Kranthi Terala (KT08837)
            * Global Manager: Dhanasekar Ramalingam (DK62290)
        5. Final Escalations:
            *ASPAC: Alfred Jayaprakash (AJ62222)
            * Global: Dhanasekar Ramalingam (DK62290)
  * **Note:** Auth Services Team works in shifts. Refer to schedule for contact on duty.
  * **US Team Schedule (Table):** Names, Roles (Global Manager, Team Lead), Days (Mon-Fri, Tue-Sat, Sun-Thu), Times (9am-6pm EST, 12pm-9pm EST). (Specific names listed: Dhanasekar Ramalingam, Sasidhar Vemulapalli, Tulasi Kamma, Vijit Sririam, Rajiv Biswas, Raviteja Garimella, Hareesh Reddy Seelam, Santosh Priyarka Varayogi).
  * **Singapore Team Schedule (Table):** Names, Roles (ASPAC Manager, Team Lead), Days (Mon-Fri, Tue-Sat, Sun-Thu), Times (12pm-9pm SST, 9am-6pm SST). (Specific names listed: Kranthi Terala, Raghtilak Rajasekaran, Suryakant Mishra, Raju Dumpala, Yaswanth Vinukonda).

---

## 10. SSO Password Reset Instructions

* **Source URL:** `https://otshare.nam.citi.net/sites/SSOEXT/Pages/pwdreset.aspx`
* **Time in Video:** 2:43 - 3:18
* **Content:**
  * **Title:** Procedure for Resetting a CtiSSO/SiteMinder Password Using OneReset
  * OneReset IVR System for Citi Single Sign On (CtiSSO)/SiteMinder password resets (web/telephone, 24x7).
  * **Steps:**
        1. **First Time Users: Request OneReset Pin.** (If Pin exists, go to step 2).
            *If no CtiSSO/SiteMinder password, login to `https://onereset.citigroup.net/onereset/Pages/Home.aspx` and Setup PIN.
            * If no PIN & no password: Colleague logs into OneReset site, clicks "Setup your OneReset PIN" (lock icon). Left nav: "Request Pin for another user". Enter GEID of user. PIN activated after manager approval (automated workflow).
        2. **PIN RULES:** Not all same digit; not consecutive ascending/descending; same number not repeated >3 times.
        3. **Two Options for Resetting (with OneReset PIN):**
            ***Password reset via WEB:**
                * Visit `https://onereset.citigroup.net`.
                *Enter Login ID, click magnifying glass.
                * Select 'SSO' as target system.
                *Enter 4 of 8 digits of OneReset PIN as prompted (e.g., if PIN 98765432, and 1st, 3rd, 7th, 8th digits enabled, answer 9, 7, 3, 2).
                * Click Submit. Temporary password displayed, forced change on next CtiSSO/SiteMinder login.
            ***Password reset via Phone (IVR System):**
                * Dial local number (list below).
                *Follow instructions: Provide 10-digit GEID (Global Directory). Provide 4 of 8 digits of OneReset PIN as prompted.
                * Choose SiteMinder (Citi Single Sign-On) password reset option.
                * Temporary password read out, forced change on next CtiSSO/SiteMinder login.
  * **OneReset Phone Numbers (IVR):**
    * Toll-Free US: English (866) 128-9807, Spanish +1 (866) 128-9811.
    * Link for latest list of phone numbers.
    * Table: Country, Local Number (e.g., Australia (61) 2 8225 4444, Austria TBC, ... a long list).
  * **OneReset Support:**
    * Global Hotline: +91 (22) 4003 8224
    * Email: `cti.sso@citi.com`
    * VT Group: CSOA Application Support

---

## 11. SSO Business Critical Change Process

* **Source URL:** `https://otshare.nam.citi.net/sites/SSOEXT/Pages/bus_crit.aspx`
* **Time in Video:** 3:18 - 3:26
* **Content:**
  * **Title:** Business Critical Change Process
  * **Applies when:**
    * Changes needed within 3 Business days.
    * Changes needed during Change Freeze period.
  * SSO doesn't perform changes in 3rd week/month (PBWM freeze). During freeze, 'Priority 2' changes can be submitted (with questions answered, signoffs). Requires 24 hrs notice for P2 Change post-question/MD approval. App team secures approvals. Changes ONLY after full SN approval.
  * **Information for Business Critical Change Process:**
  * **EMERGENCY JUSTIFICATION QUESTIONS:**
        1. Approval from Managing Director (sign off for EMER change).
        2. Business justification/reason?
        3. Dollar cost of emergency vs. regular cycle?
        4. Alternative methods used/why not continue?
        5. If new access, why not initiated earlier?
        6. Raise Incident, assign to 'CISO GLBL EX SECOPS SSO A SUPPORT', explain need for Business Critical emergency.

---

## 12. SSO Vulnerability Assessment (VA) Issues

* **Source URL:** `https://otshare.nam.citi.net/sites/SSOEXT/Pages/sso_va_issues.aspx`
* **Time in Video:** 3:26 - 3:38
* **Content:**
  * Reference: CATE SSO Engineering Site - SiteMinder VA Finding Remediation Guidance/Best Practices.
  * **SSO VA Issues (Table):** Lists Citigroup Ref # (e.g., CVA 0088) and Vulnerability Subject (mostly "Siteminder Issue").
    * Examples: CVA 0088 (URL Redirection upon authentication), CVA 0092 (XSS), CVA 0140 (Hidden Fields Credentials encoded Base64).
  * **Issues Details (Expands on click):**
    * **Example CVA 0088 (URL Redirection upon authentication - Siteminder Issue):**
      * **Vulnerability Category:** Input Validation/URL Redirection.
      * **Explanation:** Target parameter in `https://www.anycity.com/login.fcc` not validated backend, can be modified to redirect to arbitrary sites. Attacker can use for phishing. Sample POST request shows redirection to google.com. Backend must validate redirection parameter.
      * **Recommended Solutions:** Siteminder Rec: Redirection Upon Authentication. Agent Version >= 6qmr5 cr36 / 6.0.5.16. Policy Server >= 6.0sp5CR6.
      * **Required ACO settings:** `Validtargetdomain=<names>`, `targetasrelativeuri=YES`. For cookie provider, configure with `validtargetdomains`. `BadUrlChars=// \`. Use FCC password services.
      * **VA KB Link:** `https://archer01.citigroup.net/archer/...kbid=94855`
      * **SSO Operational Recommendations:** Request policy changes via siteminder tool: `https://webiso4.nj.ssmb.com/sitemgister/`. Takes 2 weeks. Webbank-hosted: contact CRM.

---

## 13. FAQ's

* **Source URL:** `https://otshare.nam.citi.net/sites/SSOEXT/Pages/FAQPage.aspx` (also seen as `FAQ.aspx`)
* **Time in Video:** 3:38 - 4:21
* **Content:**
  * Expandable list of FAQs.
  * **Category: Unassigned (1)**
    * Q: GBM Activation: Siteminder Template: Input Validation... A: Confluence link: `.../GISIS0001/XSS+Issue+with+FCC#E+Files`
  * **Category: Operational (14)**
    * **Q: How to Request Deviation from Standard ACO Parameter Settings:** A: Engage vendor/dev to remediate. If not possible, present to BISO/GISO for RE(Risk Exception). If RE granted, provide justification/RE for deviations.
    * **Q: How to deal with policy on Direct Binds to LDAP without using Storemi...:** A: Direct binds to corp LDAP not permitted if not for Siteminder app auth/authz. Link to policy: `...DocIdRedir.aspx?ID=CPSMID02_13-8150`
    * **Q: How to Process Multiple SM Setups Under Single CSI App ID:** A: Not allowed. If multiple setups needed (Region/Country/Module/Env), work with CSI for main CSI ID, update SM Register with child CSI.
    * **Q: How to request Test ids for stress testing:** A: SSO maintains test IDs (smeng01-15000). Raise Marketplace request "SSO LDAP services": `...product/31622_550711_GLOBAL#`. Notify SSO team of test time/pattern.
    * **Q: How to handle "Tracking Failed Logins per Application" Request:** A: SSO does not provide per-app tracking. App teams track via web server/Siteminder trace logs.
    * **Q: How to open an Incident Ticket to SSO:** A: `.../SSOEXT/pages/vt_reqs.aspx`
  * **Category: Technical (25)**
    * **Q: How to check siteminder agent version:** A: Found in first line of siteminder agent log. Locate webagent.conf.
    * **Q: How to implement siteminder monitoring for applications:** A: Request functional ID (static password) via marketplace: `...product/47394_99782_GLOBAL`
    * **Q: Case sensitive LDAP search:** A: SSO upgrading LDAP (5.2 to 6x). "givenName" and "departmentNumber" attributes affected.
    * **Q: How to implement Logout:** A: Request Logoffuri in siteminder setup (native path to logout page, unprotected). Default: /siteminderagent/forms/logoff.fcc
    * **Q: How to Change the Password that is Generated from One Reset...:** A: Use One Reset: `https://onereset.citigroup.net`.
    * **Q: How to Request Opening Firewall ports to Siteminder servers in DEV...:** A: If DMZ-hosted web servers need SSO, raise CCR/STMP to Firewall team for access to 'SSO_PROD_PS' object.
    * **Q: How to obtain data in headers/cookie from siteminder:** A: Agent submits HTTP headers (e.g., HTTP_SM_USER for userid). Siteminder library sends default configured headers.
    * **Q: How to update to the latest Siteminder Templates:** A: Artifactory link: `.../sso-cto-prod/siteminder-12870/smwa/R1252/`
    * **Q: How to setup AgentWaitTime:** A: Max time WebAgent waits for startup. Default 60s. Helps with LLANP connection errors.
    * **Q: How to ensure an application does not get impacted during SSO ma...:** A: Check "Instructions for Applications that use Siteminder Agent / API / TAI".
    * **Q: How to find my ACO name?:** A: From webagent.conf or webagent log file (path in webagent.conf).
    * **Q: How to check if my setup has deviation from standard cookie provide...:** A: From webagent log. Look for "CookieProvider" parameter.
    * **Q: How to perform LDAP searches and queries:** A: Link to "Configuring LDAP Connection for Ldapsearch Tools.pdf".
    * **Q: How to address Bad characters coming in logs:** A: Mandatory compliance for BadUrlChars: `< > " %22`.

---

## 14. SSO Operations (BAU) - Greenzones

* **Source URL:** `https://otshare.nam.citi.net/sites/SSOEXT/Pages/gz.aspx`
* **Time in Video:** 4:21 - 4:27
* **Content:**
  * **Title:** SSO Operations (BAU) - Greenzones
  * **North America/ LATAM:** Mon-Thu 5PM-9PM EST (all prod systems); Fri 5PM EST - Sun 5PM EST.
  * **EMEA:** Mon-Thu 5PM-9PM GMT (all prod systems); Fri 5PM GMT - Sun 5PM GMT.
  * **ASPAC:** Mon-Thu 5PM-9PM SST (all prod systems); Fri 5PM SST - Sun 5PM SST.
  * **Changes NOT performed during scheduled SSO server reboots:** Sunday 1 AM EST to Sunday 12 PM EST (Highlighted).
