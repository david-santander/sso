Okay, here is a comprehensive documentation of the content displayed in the PDF and Word documents shown in the video.

---

**Document 1: Netegrity SiteMinder® Federation Security Services Guide v6.0 (PDF)**
*Displayed from approximately 0:27 to 1:29 in the video.*

**Cover Page:**

* **Title:** Netegrity SiteMinder® Federation Security Services Guide
* **Version:** v6.0
* **Logo:** Netegrity (with slogan: "Securely let business in. Keep risk out.")
* **Company Information:**
  * Netegrity, Inc.
  * 201 Jones Road, 4th Floor
  * Waltham, MA 02451
  * Phone: (781) 690-1700
  * Fax: (781) 467-0513
  * URL: <http://www.netegrity.com>
* **Copyright:** Copyright © 1997-2004 Netegrity, Inc. All rights reserved.
* **Legal Notices:**
  * Netegrity products and associated documentation are protected by copyright and distributed under a licensing agreement.
  * Document prepared for use by Netegrity, Inc. employees, licensees, and customers.
  * No part of the document may be reproduced or transmitted without prior written permission.
  * Netegrity, Inc. reserves the right to, without notice, modify or revise any part of this document or change product features or specifications.
  * This product contains encryption technology. Exporting these encryption algorithms to certain countries may be prohibited or restricted by the laws of the United States.
  * Netegrity®, SiteMinder®, TransactionMinder®, and IdentityMinder™ and other Netegrity products or services referenced herein are trademarks or registered trademarks of Netegrity, Inc.
  * SiteMinder and Netegrity logos are trademarks of Netegrity, Inc. and may be reproduced only with permission of Netegrity.
  * All other trademarks or registered trademarks mentioned in this document are the property of their respective owners.
  * Netegrity, Inc. SHALL NOT BE LIABLE FOR TECHNICAL OR EDITORIAL ERRORS OR OMISSIONS CONTAINED HEREIN; NOR FOR INCIDENTAL OR CONSEQUENTIAL DAMAGES RESULTING FROM THE PERFORMANCE OR USE OF THIS MATERIAL.
* **Date of Publication:** January 2004

---

**Table of Contents (Pages 3-4):**

* **Preface (Page 5)**
  * Documents Related to this Product (Page 5)
  * Netegrity Documentation Conventions (Page 5)
  * Customer Support (Page 6)
* **Chapter 1. Federation Security Services (Page 7)**
  * Introduction (Page 7)
  * Use Cases (Page 8)
    * Use Case 1: Single Sign-on based on Account Linking (Page 8)
    * Use Case 2: Single Sign-on based on User Attributes (Page 9)
    * Use Case 3: Single Sign-on with no Local User Account (Page 10)
    * Use Case 4: Extended Networks (Page 11)
  * Federation Security Services Concepts (Page 12)
    * Security Assertion Markup Language (SAML) (Page 12)
    * Producers and Consumers (Page 13)
    * User Mapping (Page 13)
  * Benefits of SiteMinder Federation Security Services (Page 14)
  * SiteMinder Components for Federation Security Services (Page 15)
    * Finding Information About Federation Security Services (Page 16)
    * SAML Assertion Generator (Page 16)
    * SAML Artifact Authentication Scheme (Page 17)
    * Federation Web Services (Page 17)
    * SAML Affiliate Agent (Page 18)
    * Debugging Features (Page 18)
  * Examples of Federation Security Services Solutions (Page 19)
    * Example 1: Solution for Single Sign-on based on Account Linking (Page 19)
    * Example 2: Solution for Single Sign-on based on User Attributes (Page 21)
    * Example 3: Solution for Single Sign-on with no Local User Account (Page 22)
    * Example 4: Solution for Extended Networks (Page 24)
  * Detailed Flow of Federation Security Services Process (Page 25)
    * Terminology (Page 26)
    * Detailed Flow Diagram (Page 27)
* **Index (Page 29)**

---

**Preface (Pages 5-6):**

* **Documents Related to this Product (Page 5):**
  * Netegrity Policy Server Release Notes
  * Netegrity SiteMinder Web Agent Release Notes
  * Netegrity SiteMinder Web Agent Installation Guide
  * Netegrity SiteMinder SAML Affiliate Agent Guide
  * Netegrity Policy Server Installation Guide
  * Netegrity Policy Server Management
  * Netegrity SiteMinder Policy Design
  * Netegrity SiteMinder Agent Guide
  * Netegrity SiteMinder Option Pack Release Notes
  * Netegrity Glossary
* **Netegrity Documentation Conventions (Page 5):** Table with columns: Object, Represented by, Example.
  * Buttons, menus, menu items, field names, Web page titles, and check boxes: arial bold, e.g., "Click OK to continue."
  * Text that you enter: consolas new bold, e.g., "Enter YES or NO."
  * Text that the system displays: courier new, e.g., "The system displays the following message: Process complete."
  * File and path names, Program names: courier new, e.g., "Navigate to c:\site-minder\bin. Execute smxttprogram."
  * Variables: italic, e.g., "Enter c:\install_root\bin, where c:\install_root is the location of SiteMinder."
  * Menu trail: selection > selection > selection, e.g., "Start > Settings > Control Panel"
* **Customer Support (Page 6):**
  * Contacting Netegrity Customer Support:
    * Telephone:
      * Toll-free (U.S. and Canada only): (877) 748-3646 (877-SITEMINDER)
      * Asia-Pacific: +603-2055 3333
      * International: (781) 890-1700
    * Online: <https://support.netegrity.com>
  * Information to have ready:
    * Netegrity product name(s) and version number(s)
    * Installed components of the Netegrity product(s)
    * Type of computer platforms used and version numbers of operating systems
    * A description of your problem

---

**Chapter 1. Federation Security Services (Pages 7-28):**

* **Introduction (Page 7):**
  * Growth of e-business networks provides opportunities for businesses to form partnerships.
  * New business opportunities present challenges:
    * Exchanging information about users between partners securely.
    * Flexibility to establish a link between a user identity at a partner and a user identity in your company.
    * Enabling single sign-on across partner Web sites in multiple domains.
    * Handling different user session models between partner sites (single-site logout across all partner Web sites or separate sessions for each partner Web site).
    * Controlling access to resource based on user information received from a partner.
    * Interoperability across heterogeneous environments (Windows, UNIX, various Web servers like IIS, SunONE, Apache).
  * SiteMinder Federation Security Services provides a solution to these challenges.
  * **Note:** SiteMinder Federation Security Services is a separately licensed SiteMinder option.
* **Use Cases (Pages 8-11):**
  * **Use Case 1: Single Sign-on based on Account Linking (Page 8):**
    * Diagram: Employee -> (Internet) -> <www.smcompany.com> (employee portal, links to Health Benefits, User Store with Joe 1213, Jane 1410, Jared 9003) -> <www.ahealthco.com> (Your health plans MEDICAL/DENTAL, User Store with Joe 1213, Jane 1410, Jared 9003).
    * Description: An employee of smcompany.com authenticates at an employee portal and clicks a link to view health benefits at <www.ahealthco.com>. The employee is taken to ahealthco.com's Web site and presented with health benefit information without having to sign on to ahealthco.com's Web site. ahealthco.com maintains user identities for every employee of smcompany.com.
  * **Use Case 2: Single Sign-on based on User Attributes (Page 9):**
    * Diagram: Employee -> (Internet) -> <www.smcompany.com> (employee portal, links to Parts Supplier, User Store with Joe Eng 1213, Jane Sales 1410, Jared Purch 9003) -> <www.partsco.com> (Welcome Joe Smith, Documentation/Troubleshooting links; Welcome Jane Smith, Order Portion link; User Store mapping groups to access rights).
    * Description: smcompany.com buys parts from partsco.com. An engineer at smcompany.com clicks a link to access information at <www.partsco.com> and is taken to the technical/troubleshooting portion. A buyer is taken to the order portion. partsco.com's Web site is personalized. partsco.com does not maintain user identities for all employees at smcompany.com, but controls access based on attributes from smcompany.com.
  * **Use Case 3: Single Sign-on with no Local User Account (Page 10):**
    * Diagram: Employee -> (Internet) -> <www.smcompany.com> (employee portal, links to Discounts, User Store with Joe 1213, Jane 1410, Jared 9003) -> <www.discounts.com> (Welcome Jane Smith, Discounts for employees of smcompany.com: New Deals, Overstock).
    * Description: smcompany.com offers employee discounts by partnering with discounts.com. An employee authenticates at smcompany.com, clicks a link, and is presented with discounts at discounts.com without re-authenticating. discounts.com does not maintain any identities for employees of smcompany.com.
  * **Use Case 4: Extended Networks (Page 11):**
    * Diagram: User1 -> (Internet) -> <www.smcompany.com> (employee portal, links to Health Benefits/Parts Supplier/Discounts, User Store with Jane 1213, Jared 1410, Jared 9003) -> <www.ahealthco.com> (Your health plans, links to discounts.smcompany.com, User Store with Jane 1213, Jared 1633) -> <www.discounts.com> (Welcome Jane Smith, Discounts for employees of ahealthco.com, User Store linking Jane 1213, Jared 1633). User2 path also shown.
    * Description: smcompany.com, ahealthco.com, and discounts.com all participate in an extended federated network. Not all of ahealthco.com's customers work at smcompany.com, so ahealthco.com provides discounts to its customers by establishing a new network between ahealthco.com and discounts.com. Different users access sites differently.
* **Federation Security Services Concepts (Pages 12-13):**
  * **Security Assertion Markup Language (SAML) (Page 12):**
    * Standard developed by OASIS.
    * XML framework for exchanging authentication and authorization information.
    * SAML defines: SAML assertion, SAML protocol, SAML bindings.
    * Two profiles: Browser/Artifact, Browser/POST.
    * Link for more information: <http://www.oasis-open.org/committees/security/docs> and select document `oasis-bindings-01.pdf`.
  * **Producers and Consumers (Page 13):**
    * Producer: Site that generates SAML assertions. Assertions contain information about a user.
    * Consumer: Site that uses SAML assertion to authenticate a user.
    * A site can be both.
  * **User Mapping (Page 13):**
    * Establishes a relationship between a user identity at one business and a user identity at another business.
    * Two types:
      * One-to-one mapping: Maps a unique remote user directory entry to a unique user entry at the consumer.
      * N-to-one mapping (account linking): Maps multiple remote user directory entries to a single local profile, or maps a group of remote user directory entries to a single local profile.
    * Diagrams illustrating One-to-one (Producer User Store: Jane 1213 -> Consumer User Store: Jane 1213) and N-to-one (Producer User Store: Joe 1410, Jane 1213, Sales 1003 -> Consumer User Store: Division1 Eng, Division2 Sales).
* **Benefits of SiteMinder Federation Security Services (Page 14):**
  * Secure profile sharing
  * Flexible user-attribute mapping
  * Flexible user mapping
  * Cross-domain single sign-on
  * Policy-based access control
  * Rich session models (SAML Affiliate Agent only)
* **SiteMinder Components for Federation Security Services (Pages 15-18):**
  * **Finding Information About Federation Security Services (Page 16):** Components and general concepts. Links to other guides for detailed info (Policy Server Option Pack, Policy configuration, SAML artifact authentication scheme, Web Agent installation, Federation Web Services application, Setting up the application).
  * **SAML Assertion Generator (Page 16):** Policy Server component. Creates SAML assertion for a user who has a session at a producer site. Installed by Policy Server User Interface.
  * **SAML Artifact Authentication Scheme (Page 17):** Enables a SiteMinder site to act as a SAML consumer. Maps remote user information to local users. Part of the Policy Server Option Pack.
  * **Federation Web Services (Page 17):** A Web server (like Apache or IIS) that runs the Web Agent. Application includes components: Assertion Retrieval, Session Synchronization, Notification Alerts, SAML Credential Collector.
  * **SAML Affiliate Agent (Page 18):** Stand-alone component for sites that do not use Netegrity Policy Server and Web Agent. Provides single sign-on and session management capabilities.
  * **Debugging Features (Page 18):**
    * Web Agent Log: Information about any request to generate a SAML assertion at a producer site.
    * Assertion Retrieval Service Log: Information about requests to retrieve SAML assertions.
    * Policy Server Log: Log the results of calls from the SAML assertion generator and SAML artifact authentication scheme.
    * SAML Affiliate Agent Log: Information about activities at a consumer site protected by the SAML Affiliate Agent.
* **Examples of Federation Security Services Solutions (Pages 19-24):**
  * These examples show how components work together.
  * **Example 1: Solution for Single Sign-on based on Account Linking (Page 19-20):**
    * Diagram: Employee -> Initial authentication -> Producer <www.smcompany.com> (Web Agent, Federation Web Services, Assertion Generator, Assertion Retrieval Service, Policy Server with Option Pack) -> Single sign-on via SAML artifact -> Consumer <www.ahealthco.com> (Federation Web Services, SAML credential collector, Web Agent with Option Pack, Policy Server with Option Pack).
    * Flow described: Initial authentication, Web Agent requests SAML artifact, redirect to consumer, SAML credential collector handles artifact, assertion retrieved, access to resources. Administrator uses Policy Server User Interface to configure an affiliate.
  * **Example 2: Solution for Single Sign-on based on User Attributes (Page 21):**
    * Diagram similar to Example 1, with Producer <www.smcompany.com> and Consumer <www.partsco.com>.
    * Configuration similar to Example 1, except the administrator defines an attribute specifying the user’s department.
  * **Example 3: Solution for Single Sign-on with no Local User Account (Page 22-23):**
    * Diagram similar to Example 1, with Producer <www.smcompany.com> and Consumer <www.discounts.com> (using SAML Affiliate Agent instead of Policy Server).
    * Flow described for this configuration.
  * **Example 4: Solution for Extended Networks (Page 24-25):**
    * Diagram: User1/User2 -> Producer A (<www.smcompany.com>) -> Consumer and Producer B (<www.ahealthco.com>) -> Consumer C (<www.discounts.com>). Each with relevant SiteMinder components.
    * Describes how smcompany.com, ahealthco.com, and discounts.com are configured with multiple affiliates.
* **Detailed Flow of Federation Security Services Process (Pages 25-28):**
  * **Terminology (Page 26):**
    * Assertion Consumer URL: URL where SAML credential collector is located.
    * Intersite Transfer URL: URL that transfers a user from producer to consumer.
    * No Access URL: URL where SAML credential collector at consumer redirects if user has no rights.
    * Producer Configuration Information: Data required by the service to call a SAML producer site and obtain an assertion.
    * SAML Artifact: 42-byte, hex-encoded ID referencing an assertion stored with the assertion server at producer.
    * Target: The URL or resource a user is ultimately trying to access.
  * **Detailed Flow Diagram (Page 27-28):**
    * Sequence Diagram: User's Browser, Producer Site (User Agent, Web Server, Assertion Retrieval Service, Assertion Generator), Consumer Site (Web Agent, SAML Cred. Collector, SAML Artf. Auth. Scheme).
    * Steps 1-17 shown in diagram and listed in text:
            1. Initial request
            2. 401 challenge
            3. Credentials
            4. SMSession
            5. Intersite Transfer URL
            6. Generate assertion
            7. SAML artifact
            8. 302 redirect
            9. AssertionConsumer URL with SAML Artifact and target
            10. (SP)Protected, Producer Config. Info
            11. SAML request with SAML artifact
            12. SAML response with SAML assertion
            13. Login
            14. Success
            15. SMSession for consumer and 302 redirect to Target
            16. Request for Target
            17. (Target content)
    * Detailed textual description of each step.

---

**Index (Pages 29-30):**

* Standard alphabetical index. Examples:
  * A: assertion consumer URL, assertion generator, assertion retrieval service
  * B: benefits, Federation Security Services
  * S: SAML, single sign-on (SSO), SiteMinder components
  * U: use case (extended network, SSO with account linking, SSO with no local user account, SSO with user attributes)
  * User mapping

---
---
