# Video Content Documentation: SiteMinder CitiSSO Knowledge Center

**Video Start Time:** 0:00

**Initial View (0:02 - 0:22): SiteMinder KC Home**

* **Page Title:** SiteMinder CitiSSO Knowledge Center
* **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/SiteMinder%20KC%20Home.aspx`
* **Left Navigation "I want to..." links visible:**
  * Know more about SiteMinder's functionality
  * Install SiteMinder
  * Configure SiteMinder
  * Create Course-Grained Entitlements and Access Control
  * Enable Safeword (OTP) authentication
  * Federate with external vendors
  * Use CitiSSO Services
  * Understand CitiSSO Password Policies
  * Get more information
  * Obtain documents
  * Get support
* **Main Content Sections:**
  * **Introductory Paragraph:** "SiteMinder Technology combines product functionality, services, and best practices..."
  * **Developer's Corner:**
    * **Processes and Procedures:**
      * SiteMinder Product Downloads
      * Password Change Templates
      * CitiSSO High IS De-Isolation Solution
      * Requesting LDAP Groups and LAD IDs
      * Safeword/OTP Authentication
      * SM Register
      * UAT Performance Analysis
    * **Branding:**
      * Citi Internet Branding Standards
    * **Best Practices:**
      * CitiSSO Session Timeout Considerations
      * CitiSSO Cross Site Scripting Deviations Process
      * SiteMinder VTM Best Practices and VA Remediation Guidance
    * **Reference Materials:** (Visible after scrolling at 0:08)
      * Application Server Agent Documentation
      * CA SiteMinder Vendor Overview
      * CitiSSO Infrastructure Architecture Design
      * Custom Agent/API Installation Document
      * Documentation Index
      * SiteMinder 6.0 Vendor Documentation
  * **SiteMinder R12.52 Documentation:**
    * R12.52 Policy Server
    * Policy Server Docs
    * SecureSSO Docs
    * SecureSSO F.A.Q.
  * **SiteMinder R12.8 Documentation:**
    * R12.8 Docs
  * **SiteMinder Web Agents (SMWA):**
    * SMWA Docs
    * New Branding SiteMinder WebAgent Templates for Windows and RHEL
    * sminfoagent.zip
  * **SiteMinder R12 Documentation:** (Visible after scrolling at 0:08)
    * R12 Policy Server
  * **Most popular pages and documents...** (Visible after scrolling at 0:08)
    * CitiSSO Infrastructure Architecture Design
    * SiteMinder Product Downloads
    * CA eTrust® SiteMinder Web Agent Installation Guide 6.x QMR 5
    * CA eTrust® SiteMinder Web Agent Guide 6.x QMR 5
    * CA eTrust® SiteMinder Policy Server Policy Design R6.0 SP 5
    * FAQ
    * Procedure for Requesting LDAP Groups and LAD IDs
    * SiteMinder Functionality
    * Submitting Requests to SM Register
  * **Right Sidebar:**
    * Feedback section
    * "<Click here> for a Full Listing of Releases"
    * RFP/RFT links for various SiteMinder WebAgent versions
    * SiteMinder Certified Standard Documentation (SiteMinder 6.0 OMRS CR35 Certified...)
    * Related Technical Standards (Authentify, Citi Federation, Citi2EE, etc.)
    * Links (Citi Glossary, CitiSAML Knowledge Center, etc.)

---

**Page 2 (0:22 - 0:31): SiteMinder Functionality**

* **Accessed via:** Left navigation "Know more about SiteMinder's functionality"
* **Page Title (in content area):** SiteMinder - overview
* **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/SiteMinder%20Functionality.aspx`
* **Main Content:**
  * "SiteMinder Technology combines product functionality, services, and best practices..." (similar to home)
  * Mentions Single Sign-On (SSO), Policy Server, Web Agent, Policy/Key store, user store.
  * Diagram: High-level organization of SiteMinder (Web Servers, Policy Server, User Store, Key Store).
  * "Some of the rich functionality of SiteMinder includes:"
    * Customized Pages
    * Session Time Out
    * Logout
    * SSL Communication
    * User Population (Client Entry Tool CET)
  * Links to: SiteMinder Certified Standard Build, CitiSSO Design Specifications, CitiSSO Infrastructure Architecture Design, and Vendor documents.

---

**Page 3 (0:31 - 0:38): Installing and Configuring SiteMinder**

* **Accessed via:** Left navigation "Install SiteMinder"
* **Page Title (in content area):** Installing and Configuring SiteMinder
* **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/Install%20SiteMinder.aspx`
* **Main Content:**
  * Step 1: Request through the SM Register tool. Link to SM Register User Guide.
  * Step 2: SSO Operations setup. Details provided: Trusted Host Admin ID, Password, Policy Server Host Names, Agent Config Object Name (ACO), Host Config Object Name (HCO).
  * Step 3: Download, install, configure web agent. Link to SiteMinder 6.X Product Downloads page.
  * Note: Information on agent types (client-server, thick clients, non-web based) and Webank Applications.

---

**Page 4 (0:38 - 0:59): Post-Installation Configurations**

* **Accessed via:** Left navigation "Configure SiteMinder"
* **Page Title (in content area):** Post-Installation Configurations
* **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/Configure%20SiteMinder.aspx`
* **Main Content (List of configurations, some with details):**
  * User Login ID (is HTTP_SM_USER)
  * Log File Settings
  * Failed Login Redirect (to /siteminderagent/forms/failedlogin.html)
  * Password Change Templates
  * Customization of the Login and Password Change Pages
  * Authorizations (Download sminfoagent.tar/zip, customize templates)
  * Password Resets (Link to OneReset (<https://onereset.citigroup.net>))
  * FCC Password Services (smpsservices.fcc)
    * Implementations for Single Sign-On requirement and other applications.
  * Best Practices (Session Timeouts, Cross Site Scripting, Vulnerability Threat Management/VTM)
  * Bad CSS Characters logoff
  * Cookie Providers for Cross-Domain SSO
  * LDAP Groups
    * Creating LDAP groups
    * Client Entry Tool (URLs for Dev, Stg, Prd: centryd.nj.ssmb.com, centrys.nj.ssmb.com, centry.nj.ssmb.com)
  * Configure unauth (redirect to /sminfoagent/forms/unauth.html)
  * Configuring SiteMinder for External Users
  * High & Risk Applications
  * Ethical Hacks
  * Performance Tuning

---

**Page 5 (0:59 - 1:16): Creating Course-Grained Entitlements and Access Control**

* **Accessed via:** Left navigation "Create Course-Grained Entitlements and Access Control"
* **Page Title (in content area):** Creating Course-Grained Entitlements and Access Control
* **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/Create%20Course-Grained%20Entitlements%20and%20Access%20Control.aspx`
* **Main Content:**
  * Creating an LDAP Group (Request in Citi Marketplace: Dev/UAT, Production)
  * Using Client Entry Tool (CET) to Manage Membership (links to Dev, Stg, Prd: centryd.nj.ssmb.com, centrys.nj.ssmb.com, centry.nj.ssmb.com)
  * Configuring SiteMinder for External Users
  * Configuring Unauthorized Users to Access a SiteMinder-protected Resource ('configure unauth' in SM Register)
  * Application Inclusion (Legacy apps, standard inclusion process, SSO BAU team review)
    * TEST Environment
    * STAGING Environment
    * PRODUCTION Environment

---

**Page 6 (1:16 - 1:20): Strengthening Authentication**

* **Accessed via:** Left navigation "Enable Safeword (OTP) authentication"
* **Page Title (in content area):** Strengthening Authentication
* **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/Enable%20Safeword%20(OTP)%20authentication.aspx`
* **Main Content:**
  * Enabling Safeword Card Authentication (OTP). Links to "Safeword Authentication Request Process" document and "Safeword Technical Standards" page.

---

**Page 7 (1:20 - 1:23): Federation**

* **Accessed via:** Left navigation "Federate with external vendors"
* **Page Title (in content area):** Federation
* **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/Federate%20with%20external%20vendors.aspx`
* **Main Content:**
  * PKI-based solution. Link to "PKI-Based Affiliate Solution" document.
  * CitiSAML. Link to "General and Detailed SiteMinder Federation Security Services Guide v6.0" documents.

---

**Page 8 (1:23 - 1:27): CitiSSO Services**

* **Accessed via:** Left navigation "Use CitiSSO Services"
* **Page Title (in content area):** CitiSSO Services
* **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/Use%20CitiSSO%20Services.aspx`
* **Main Content:**
  * Information on using SiteMinder LAD for LDAP group membership.
  * Recommendation for applications to maintain their own authentication data.
  * Link to "CitiSSO Services Technical Standards" page for CET, LAD, GIVA, and Webtool.

---

**Page 9 (1:27 - 1:33): Password Policies on SiteMinder Products**

* **Accessed via:** Left navigation "Understand CitiSSO Password Policies"
* **Page Title (in content area):** Password Policies on SiteMinder Products (as of CISS 9.2)
* **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/Understand%20CitiSSO%20Password%20Policies.aspx`
* **Main Content:**
  * **Expiration:**
    * Internal Users: Locked after 90 days inactivity, expires if not changed after 90 days.
    * External Users: Expires from inactivity after 180 days, expires if not changed after 180 days.
  * **Locking:** Disabled after 6 successive incorrect passwords. Internal users can use OneReset.
  * **Composition:** Min length 8, max length 15, max repeating char 2, content min 1 letter & 1 digit, case sensitive.
  * **Restrictions:** Min days before reuse 90, min passwords before reuse 6.

---

**Page 10 (1:33 - 1:37): Additional Information**

* **Accessed via:** Left navigation "Get more information"
* **Page Title (in content area):** Additional Information
* **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/Get%20more%20information.aspx`
* **Main Content:**
  * Password Policies and Account Lockouts.
  * Auditing: SiteMinder tracks successful authentications for one (1) day and failed authentications for (15) days.
  * EERS: Membership of LDAP groups is automatically fed to EERS.

---

**Page 11 (1:37 - 1:40): Obtain documents (Page Not Found)**

* **Accessed via:** Left navigation "Obtain documents"
* **Page Title (in content area):** Page not found
* **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/Obtain%20documents.aspx`
* **Main Content:** "Page not found" error. The left navigation changes to show "Lists," "Recent," "storageAudits..." items, and "Site contents."

---

**Page 12 (1:40 - 1:44): Support**

* **Accessed via:** Left navigation "Get support"
* **Page Title (in content area):** Support
* **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/Get%20support.aspx`
* **Main Content:**
  * For SiteMinder Service issues, open a Virtual Ticket (VT) and assign to 'SSO'.
  * Questions can be emailed to 'SSO BAU'. Link to "SiteMinder Product Certification Process".
  * If application hosted by Webbank, contact Customer Relationship Manager (CRM).
  * Link to "CitiSSO OPERATIONS site".

---

**Page 13 (1:44 - 2:17): SiteMinder 12.0 & 12.52 Product Downloads**

* **Accessed via:** User navigates back to the home page (not explicitly shown, but implied by the content) and clicks a link, likely "SiteMinder Product Downloads" from the "Most popular pages and documents..." section.
* **Page Title (in content area):** SiteMinder 12.0 & 12.52 Product Downloads
* **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/SiteMinder%2012.0%20Product%20Downloads.aspx`
* **Main Content:**
  * SiteMinder Product Support Matrix (PSM)
  * Information on Web Agents, Application Agents, SDKs.
  * Notes about SDK limitations, CTI Engineering Certified Package, cell numbering for support, PDF/Chef/GDS links, and Vendor Binaries.
  * Links:
    * `# SiteMinder xAuthRadius 5.1.1 unified.zip > R12_SM_xAuthRad_5.1.1_unified.zip #`
    * `New branding SiteMinder WebAgent Templates update on Windows and RHEL Documentation`
    * `# CitiFederation DSSO Templates (PFDSSO Files) will be wrapped in all new CTI&E Certified #`
    * Link to `DSSO Templates`
  * **Siteminder Platform Support - Distributed (Table):**
    * Legend: 1: CTI&E Certified Citi Package, 2: CA Binaries / Package - Vendor support for non-CATE certified web-servers.
    * Columns: Web Agents, Operating Systems (Windows 2016, Windows 2019, AIX 7.1, Red Hat 7, Red Hat 8).
    * Rows for Web Agents: Microsoft IIS, Oracle HTTP Server (OHS), IBM HTTP Server (IHS), Apache HTTP Server (AHS) with specific versions.
    * Cells contain package numbers (1 or 2), version details (e.g., R12.52 SP01 cr11), Build numbers, PFDSSO template info, CTC IDs, and "Install/Config Doc" links.
  * **SDK (64-Bit) Certified for JAVA Only (Bishop Fox N/A) (Table):**
    * Columns: Operating Systems (Windows 2016, Red Hat 7, Red Hat 8).
    * Row: V 12.8 Agent APIs.
    * Cells contain package numbers (2) and "SDK Guide" links.
  * **Siteminder 6.0 Platform Support/Citi Version (Mainframe) (Table):**
    * Legend: 1: Citi Custom Package -version CR35, 2: CA Package -version CR35, 3: CA Package -version CR10.
    * Warning about limited support for Mainframe.
    * Columns: Web Agents (31-Bit / 32-Bit / 64-Bit), Operating Systems (Suse Linux 9 for System Z, Suse Linux 10 for System Z, Red Hat 5 for System z (64-bit), z/OS 1.10 - 1.13, z/OS 2.1).
    * Rows for Web Agents: IBM HTTP Server (versions like 2.0.47.1, 5.3, 6.0.xx, etc.), SDK (31 / 32-Bit) V 6.0 Agent APIs.
  * **SiteMinder Application Server Platform Support (Table):**
    * Legend: 1: WebSphere custom CITI package SM Agent version 12SP2, 2: WebLogic 12.x vendor binaries and document R12SP2CR01. *VB = Vendor Binaries.
    * Columns: Application Server Version, AIX 7, RED HAT AS/ES 4, RED HAT 6, RED HAT 7.
    * Rows: WebSphere ND (8.5.5, 9.0.x), WebLogic (10.3.6 (11g), 12.1.3, 12.2.1).

---

**Folder View 1 (2:17 - 2:21): CitiSSO Services**

* **Accessed via:** Left navigation, under "More stuff..." > "Site contents" (implied), then clicking "CitiSSO Services" folder.
* **Page Title (in content area):** CitiSSO Services (Folder in a document library named "CitiSSO Engineering")
* **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/CitiSSO%20Services/Forms/AllItems.aspx`
* **Main Content (List of files/folders):**
  * For Review 5-1-8 (Modified May 2, 2008)
  * IDMgr (Modified April 24, 2008)
  * onereset (Modified December 4, 2008)
  * SM Register (Modified April 28, 2008)
  * stg_onerset_proced.aspx (Modified December 4, 2008)

---

**Folder View 2 (2:21 - 2:24): Design Documents**

* **Accessed via:** Left navigation, under "More stuff..." > "Site contents" (implied), then clicking "Design Documents" folder.
* **Page Title (in content area):** Design Documents (Folder in a document library named "CitiSSO Engineering")
* **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/Design%20Documents/Forms/AllItems.aspx`
* **Main Content (List of files/folders):**
  * Design Specifications (Modified May 2, 2008)
  * Infrastructure Design (Modified May 2, 2008)

---

**Folder View 3 (2:24 - 2:29): presentations**

* **Accessed via:** Left navigation, under "More stuff..." > "Site contents" (implied), then clicking "presentations" folder.
* **Page Title (in content area):** presentations (Folder in a document library named "CitiSSO Engineering")
* **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/Presentations/Forms/AllItems.aspx`
* **Main Content (List of files/folders):**
  * CitiSSO Roadmap 2011 (Modified November 1, 2010)
  * CitiSSO_Roadmap09 (Modified September 9, 2008)
  * vendor (Modified September 9, 2008)

---

**Return to Home Page (2:29 - 2:31)**

* User navigates back to the "SiteMinder KC Home" page.
* **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/SiteMinder%20KC%20Home.aspx`

---

**End of Relevant Content (2:31 onwards):**

* The video transitions to an image of a person on a swing over water. This is not part of the SharePoint site content.

**Video End Time:** 2:33

This covers the browsable content shown in the video.This video displays a user navigating an internal SharePoint site named **"SiteMinder CitiSSO Knowledge Center."** The documentation below outlines the content of each page visited, with the SharePoint URL serving as the original source reference. The base URL of the SharePoint site (e.g., `yourcompany.sharepoint.com`) is represented as `[sharepoint_base_url]`.

---

### SiteMinder CitiSSO Knowledge Center - Content Documentation

1. **SiteMinder KC Home** (0:02 - 0:22)
    * **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/SiteMinder%20KC%20Home.aspx`
    * **Key Sections:**
        * **Introduction:** Overview of SiteMinder Technology for authentication and authorization.
        * **Developer's Corner:**
            * **Processes and Procedures:** Links to SiteMinder Product Downloads, Password Change Templates, CitiSSO High IS De-Isolation Solution, Requesting LDAP Groups and LAD IDs, Safeword/OTP Authentication, SM Register, UAT Performance Analysis.
            * **Branding:** Citi Internet Branding Standards.
            * **Best Practices:** CitiSSO Session Timeout Considerations, CitiSSO Cross Site Scripting Deviations Process, SiteMinder VTM Best Practices and VA Remediation Guidance.
            * **Reference Materials** (visible after scroll 0:08): Application Server Agent Documentation, CA SiteMinder Vendor Overview, CitiSSO Infrastructure Architecture Design, Custom Agent/API Installation Document, Documentation Index, SiteMinder 6.0 Vendor Documentation.
        * **SiteMinder R12.52 Documentation:** R12.52 Policy Server, Policy Server Docs, SecureSSO Docs, SecureSSO F.A.Q.
        * **SiteMinder R12.8 Documentation:** R12.8 Docs.
        * **SiteMinder Web Agents (SMWA):** SMWA Docs, New Branding SiteMinder WebAgent Templates for Windows and RHEL, sminfoagent.zip.
        * **SiteMinder R12 Documentation** (visible after scroll 0:08): R12 Policy Server.
        * **Most popular pages and documents...** (visible after scroll 0:08): Links to various guides, FAQs, and procedures.
    * **Right Sidebar:** Feedback, Full Listing of Releases, SiteMinder Certified Standard Documentation, Related Technical Standards, and other useful links.
    * **Left Navigation "I want to..." options:** Know more about SiteMinder's functionality, Install SiteMinder, Configure SiteMinder, etc.

2. **SiteMinder Functionality** (0:22 - 0:31)
    * **Accessed via:** Left navigation "Know more about SiteMinder's functionality."
    * **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/SiteMinder%20Functionality.aspx`
    * **Content:** "SiteMinder - overview," describes SiteMinder technology (SSO, Policy Server, Web Agent), includes a high-level architecture diagram, and lists rich functionalities like Customized Pages, Session Time Out, Logout, SSL Communication, User Population (Client Entry Tool CET).

3. **Installing and Configuring SiteMinder** (0:31 - 0:38)
    * **Accessed via:** Left navigation "Install SiteMinder."
    * **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/Install%20SiteMinder.aspx`
    * **Content:** Steps for installation: Request via SM Register tool, SSO Operations setup (Trusted Host Admin ID, Password, etc.), download/install/configure web agent (link to SiteMinder 6.X Product Downloads). Notes on agent types.

4. **Post-Installation Configurations** (0:38 - 0:59)
    * **Accessed via:** Left navigation "Configure SiteMinder."
    * **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/Configure%20SiteMinder.aspx`
    * **Content:** A list of post-installation configurations and detailed explanations for: User Login ID, Log File Settings, Failed Login Redirect, Password Change Templates, Customization of Login/Password Change Pages, Authorizations, Password Resets (link to OneReset), FCC Password Services, Best Practices, Bad CSS Characters, Cookie Providers for Cross-Domain SSO, LDAP Groups (Client Entry Tool URLs for Dev/Stg/Prd), Configure unauth, Configuring SiteMinder for External Users, High & Risk Applications, Ethical Hacks, Performance Tuning.

5. **Creating Course-Grained Entitlements and Access Control** (0:59 - 1:16)
    * **Accessed via:** Left navigation "Create Course-Grained Entitlements and Access Control."
    * **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/Create%20Course-Grained%20Entitlements%20and%20Access%20Control.aspx`
    * **Content:** Procedures for creating LDAP groups (via Citi Marketplace), using Client Entry Tool (CET) for membership management (links to Dev/Stg/Prd), configuring SiteMinder for external users, configuring unauthorized user access ('configure unauth'), and Application Inclusion process (legacy/new apps, SSO BAU team review, Test/Staging/Production environment considerations).

6. **Strengthening Authentication** (1:16 - 1:20)
    * **Accessed via:** Left navigation "Enable Safeword (OTP) authentication."
    * **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/Enable%20Safeword%20(OTP)%20authentication.aspx`
    * **Content:** Information on Enabling Safeword Card Authentication (OTP) with links to "Safeword Authentication Request Process" document and "Safeword Technical Standards" page.

7. **Federation** (1:20 - 1:23)
    * **Accessed via:** Left navigation "Federate with external vendors."
    * **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/Federate%20with%20external%20vendors.aspx`
    * **Content:** Details on PKI-based solution (link to "PKI-Based Affiliate Solution" document) and CitiSAML (link to "General and Detailed SiteMinder Federation Security Services Guide v6.0").

8. **CitiSSO Services** (1:23 - 1:27)
    * **Accessed via:** Left navigation "Use CitiSSO Services."
    * **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/Use%20CitiSSO%20Services.aspx`
    * **Content:** Information on SiteMinder LAD for LDAP group membership and a link to "CitiSSO Services Technical Standards" page for CET, LAD, GIVA, and Webtool.

9. **Password Policies on SiteMinder Products (as of CISS 9.2)** (1:27 - 1:33)
    * **Accessed via:** Left navigation "Understand CitiSSO Password Policies."
    * **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/Understand%20CitiSSO%20Password%20Policies.aspx`
    * **Content:** Details on Expiration (Internal/External Users), Locking (OneReset for internal users), Composition (length, repeating characters, content, case sensitivity), and Restrictions (days/passwords before reuse).

10. **Additional Information** (1:33 - 1:37)
    * **Accessed via:** Left navigation "Get more information."
    * **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/Get%20more%20information.aspx`
    * **Content:** Information on Password Policies and Account Lockouts, Auditing (SiteMinder tracking of successful/failed authentications), and EERS (LDAP group membership fed to EERS).

11. **Obtain documents (Page Not Found)** (1:37 - 1:40)
    * **Accessed via:** Left navigation "Obtain documents."
    * **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/Obtain%20documents.aspx`
    * **Content:** "Page not found" error.

12. **Support** (1:40 - 1:44)
    * **Accessed via:** Left navigation "Get support."
    * **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/Get%20support.aspx`
    * **Content:** Instructions for opening Virtual Tickets (VT), emailing 'SSO BAU' (link to SiteMinder Product Certification Process), contacting CRM for Webbank-hosted applications, and a link to the "CitiSSO OPERATIONS site."

13. **SiteMinder 12.0 & 12.52 Product Downloads** (1:44 - 2:17)
    * **Accessed via:** Navigation from Home page (likely "SiteMinder Product Downloads" link).
    * **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/SiteMinder%2012.0%20Product%20Downloads.aspx`
    * **Content:** "SiteMinder Product Support Matrix (PSM)"
        * Notes on SDKs, CTI Engineering Certified Packages, support cell numbering, broken links, and Vendor Binaries.
        * Links to xAuthRadius, WebAgent Templates, and CitiFederation DSSO Templates.
        * **Tables:**
            * **Siteminder Platform Support - Distributed:** Matrix for Web Agents (IIS, OHS, IHS, AHS) across Operating Systems (Windows, AIX, Red Hat) with version details, build numbers, CTC IDs, and Install/Config Docs.
            * **SDK (64-Bit) Certified for JAVA Only:** Matrix for V 12.8 Agent APIs across Operating Systems.
            * **Siteminder 6.0 Platform Support/Citi Version (Mainframe):** Matrix for IBM HTTP Server and SDK across Mainframe Operating Systems (Suse Linux for System Z, Red Hat for System z, z/OS).
            * **SiteMinder Application Server Platform Support:** Matrix for Application Servers (WebSphere ND, WebLogic) across Operating Systems (AIX, Red Hat).

14. **Folder View: CitiSSO Services** (2:17 - 2:21)
    * **Accessed via:** Left navigation (under "More stuff..." > "Site contents," then "CitiSSO Services" folder).
    * **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/CitiSSO%20Services/Forms/AllItems.aspx`
    * **Content (List of files/folders within "CitiSSO Engineering" library):** For Review 5-1-8, IDMgr, onereset, SM Register, stg_onerset_proced.aspx (with modification dates from 2008).

15. **Folder View: Design Documents** (2:21 - 2:24)
    * **Accessed via:** Left navigation (similar to above, then "Design Documents" folder).
    * **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/Design%20Documents/Forms/AllItems.aspx`
    * **Content (List of files/folders within "CitiSSO Engineering" library):** Design Specifications, Infrastructure Design (both modified May 2, 2008).

16. **Folder View: presentations** (2:24 - 2:29)
    * **Accessed via:** Left navigation (similar to above, then "presentations" folder).
    * **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/Presentations/Forms/AllItems.aspx`
    * **Content (List of files/folders within "CitiSSO Engineering" library):** CitiSSO Roadmap 2011 (modified 2010), CitiSSO_Roadmap09 (modified 2008), vendor (modified 2008).

17. **Return to SiteMinder KC Home** (2:29 - 2:31)
    * **Original Source Reference:** `[sharepoint_base_url]/sites/CATECollaboration.Home/SitePages/SiteMinder%20KC%20Home.aspx`

---
The video concludes at 2:33 with an image unrelated to the SharePoint site content.
