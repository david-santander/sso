
**Document 2: SAML Guidelines & CitiSAML Interoperability Profile (Word Document)**

*Displayed from approximately 1:31 to 2:19 in the video.*

**Cover Page (Page 1 of 13):**

* **Logo:** citi
* **Title:** SAML Guidelines & CitiSAML Interoperability Profile
* **Version:** 1.01
* **Date:** December 13, 2007
* **Originator:** 6.2.3 Application Security Domain Team
* **Confidentiality Notice:** Citigroup INTERNAL

---

**Document Revision History (Page i):**

* Table: Version, Date, Author, Comment / Changes from Prior Version
  * 0.1: 8-Aug-07, Steve Perry, Initial Draft
  * 0.2: 8-Aug-07, Steve Perry, Revised, various comments from IVJ.
  * 0.3: 8-Sep-07, Steve Perry, Revised, various comments from DS.
  * 1.0: 10-Nov-07, Steve Perry, Various Comments from IVT.
  * 1.01: 13-Dec-07, Steve Perry, Comments from IVT, Added IDP initiated SSO.
* **Lead & Author:**
  * Steve Perry (email: <steve.perry@citi.com>, phone: (972) 654-2205)
  * Dana Solo (email: <dana.solo@citi.com>, phone: (972) 659-2599)
* **Contributors & Reviewers:** (List of approximately 20 names, e.g., Firoz Abidi, Mahesh Kumar, Asge Anao, Wayne Browning, etc.)

---

**Table of Contents (Page ii):**

* 1 INTRODUCTION (Page 3)
  * 1.1 Location (Page 3)
  * 1.2 Purpose (Page 3)
  * 1.3 Audience (Page 3)
  * 1.4 SAML Overview (Page 3)
  * 1.4.1 SAML Assertions (Page 4)
* 2 USES OF SAML IN CITI (Page 5)
* 3 RECOMMENDATIONS & CITISAML INTEROPERABILITY PROFILES (Page 6)
  * 3.1 Recommendation Summary (Page 6)
    * 3.1.1 Creation of Assertions (Page 6)
    * 3.1.2 Validation/Consumption of Assertions (Page 7)
    * 3.1.3 Authentication Statements (Page 8)
    * 3.1.4 Condition Statements (Page 8)
  * 3.2 Use Cases (Page 9)
    * 3.2.1 Web-browser SSO/SP Initiated with Post Profile (Page 10)
    * 3.2.2 Web-Browser SSO/Artifact Profile (Page 11)
    * 3.2.3 Web-Browser SSO/IdP initiated with POST... (Page 12) (title cut off)

---

**1 Introduction (Page 3):**

* The core SAML specification provides significant flexibility. This document details the CitiSAML profiles.
* **1.1 Location:** The current version of this document is on <http://engineering.citigroup.net/appsec/eng> (link).
* **1.2 Purpose:**
  * Define the rules for the usage of SAML within Citi, including SAML creation, profile, and transport recommendation.
  * Establish a SAML profile and core SAML specification to ensure interoperability between disparate systems at Citi.
* **1.3 Audience:**
  * Primary audiences: those that architect, design or develop business applications that have a need to possess federation capabilities.
  * Secondary audiences: Engineering Leads (ELs) of middleware components (e.g., Citigroup SOA, Security Gateway (SSG), CA/SSO, Enterprise Service Bus (ESB)) to understand the SAML profile implemented by Citi.
* **1.4 SAML Overview:**
  * SAML (Security Assertion Markup Language) defines an XML-based framework for communicating security and identity (authentication, entitlements, and attribute) information between computing entities.
  * SAML facilitates interoperation between disparate security systems.

---

**1.4.1 SAML Assertions (Page 4):**

* A SAML assertion is a package of information that supplies one or more statements made by a SAML authority/identity provider.
* Types of assertions relevant to Citi:
  * **Authentication:** The specified subject was authenticated by a particular means at a particular time.
  * **Attribute:** The specified subject is associated with the supplied attributes.
  * **Authorization Decision:** A request to allow the specified subject to access the specified resource has been granted or denied.
* This document provides guidelines and recommendations around SAML Assertions, and specifically assertions around Authentication and Attribute assertions.
* **Diagram: "Operational Modes, Bindings, Protocols and Assertions"**
  * Operational Modes: Web Browser SSO & Artifact, Web Browser SSO & POST, ECP (Enhanced Client or Proxy), SP Lite, IdP Lite, Attribute Requester, Attribute Authority, SOAP Client
  * Bindings (highlighted in yellow): HTTP Redirect, HTTP POST, HTTP Artifact, SOAP
  * Protocols (highlighted in yellow): Assertion Query and Request, Authn Request, Artifact Resolve Protocol, Name Identifier Mapping Protocol, SAML Protocol, XACML
  * Assertions: Authn Statement, Attr Statement, Authz Decision Statement

---

**2 Uses of SAML in Citi (Page 5):**

* The use cases of SAML within Citi where the use of the profile and governance recommendations contained in this document should be followed, include:
  * Consumer SSO (Single Sign-On) functionality between Citi and third-party applications and is a potential evolution/replacement of AHS.
  * Internal application to third-party application federation.
  * Integration of various authentication mechanisms.
  * Security Token Services (STS) provided by CASSO (e.g. Siteminder/TFIM).

---

**3 Recommendations & CitiSAML Interoperability Profile (Pages 6-8):**

* This section details recommendations around the use of SAML in Citi, including recommendations around how SAML assertions should be created, consumed or validated.
* SAML should be addressed: Versions of SAML, SAML Creation, SAML Consumption/Validation, Composition of the CitiSAML Profile (Authentication Statements, Condition Statements, Attribute Statements).
* **3.1 Recommendation Summary:**
  * **3.1.1 Creation of Assertions (Page 6):** Table:
    * **SAML Version:** Recommendation: 2.0, 1.1. Additional Information: SAML 2.0 is the preferred standard for internal/external federation needs. 1.1 is an interim solution. For external federation it is recommended that only SAML 1.1 be refuted if the third party does not support SAML 2.0. Externally, SAML 2.0 is preferred although earlier versions may be needed to support partners with legacy systems.
    * **Assertion Lifetime:** Recommendation: 60 seconds to 5 minutes. Additional Information: Until such time as Citi can use Client Network Time Protocol (NTP), the recommendation of 60s is preferred. For external federation, the recommendation is to choose the most appropriate assertion lifetime, which could be 60 seconds or 5 minutes. Long running processes when the consumption of the assertion is close to the creation time, the lifetime for internal federation given time synchronization across the enterprise can be 5 minutes. For external federation given time.
    * **Time Composed:** Recommendation: UTC. Additional Information: All assertions created for internal resources should be UTC format. For external federation the recommendation is to use the format mutually agreed with the third-party.
    * **Identity:** Recommendation: Trusted. Additional Information: Recommendation: T.C. should be used unless there is another mechanism to validate. The issuer of the assertion must directly or indirectly validate the identity of the principal/end-user.
    * **Signature:** Recommendation: All assertions must be signed. Additional Information: Internal: Trusted CA. All assertions must be signed. Internal: Trusted CA (Cijinn Code Signing CA). External: Mutually agreed and consumably CA. External: Mutually agreed and consumable by third parties.
    * **Encryption:** Recommendation: SAML 2.0 Encryption is recommended for consumption by third parties. Additional Information: SAML 2.0 Encryption is recommended. Citi is not mandating the use of encryption, given the lack of SAML Encryption 1.1 in production. All assertion tokens should be passed over a secure channel like SSL/TLS / Cert.
  * **3.1.2 Validation/Consumption of Assertions (Page 7):** Table:
    * **Signature Verification:** Recommendation: Only consume signed Assertions. Additional Information: The signature should be validated for integrity. Must validate signature from trusted sources. From a Cijinn Code Signing CA. Validation of signature from a CA (i.e. a certificate) is permitted by Sign certificate. Is within expiration 24 hours?
    * **Assertion Lifetime:** Recommendation: Validate. Additional Information: Expired assertions should be rejected. Assertion Lifetime should be validated. Assertions that are expired should be rejected.
    * Footnotes:
      * [1] When Citi, acting as IdP, is issuing Assertions, the business should perform a risk assessment to ensure the risk is acceptable...
      * [2] For internal transactions, the Cijinn (External) CA should be the issuer CA. For path transactions, ideally a single trusted CA should be used. For external third party transactions, the CA should be mutually agreed with the third-party. All assertions created by internal resources should be UTC format. For external federation, the recommendation is to use the format mutually agreed with the third-party. All external transactions will use Cijinn signed assertion. All SAML Identify binding protocols should be used using guidelines in CertificateCA_Identity_Binding_Protocols_for_SAML.doc.
  * **3.1.3 Authentication Statements (Page 8):**
    * Contain business data about successful authentication performed on a subject.
    * Example XML:

            ```xml
            <saml:AuthnStatement
                AuthnInstant="2007-10-29T21:44:33.0Z"
                SessionIndex="d3f1bc70-b720-4101-7151-f35b-f210877d7f6a">
                <saml:AuthnContext>
                    <saml:AuthnContextClassRef>
                        urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport
                    </saml:AuthnContextClassRef>
                </saml:AuthnContext>
            </saml:AuthnStatement>
            ```

  * **3.1.4 Condition Statements (Page 8):**
    * Contain information on when the information regarding the assertion is valid. Recommended condition statement attributes: `NotBefore` and `NotOnOrAfter`.
    * For internal to internal federation, it is recommended that the condition statement by default use the `NotBefore` and `NotOnOrAfter` attributes.
    * Link to `High-Risk SSO Application Integration Practices` document.
    * Example XML:

            ```xml
            <saml:Conditions
                NotBefore="2007-10-29T21:43:33.0Z"
                NotOnOrAfter="2007-10-29T21:48:33.0Z">
                <saml:AudienceRestriction>
                    <saml:Audience>urn:federation:MicrosoftOnline</saml:Audience>
                </saml:AudienceRestriction>
            </saml:Conditions>
            ```

---

**3.2 Use Cases (Pages 9-12):**

* For Web-browser SSO, three approaches are recommended based on specific use-case:
  * **Web-browser SSO/SP Initiated with Post Profile:** (Highlighted) Recommended to be used when a non-authenticated user is requesting SSO authentication from a separate SP. Service Provider (SP) initiates SAML authentication (i.e., SAML request and response).
  * **Web Browser SSO/Artifact Profile:** Recommended when the user is already authenticated at the IdP and is requesting SSO access to a resource on a Service Provider (SP).
  * **Web-Browser SSO/IdP initiated with POST Profile:** Similar use-case to Web-Browser SSO/Artifact Profile and requires an unsolicited SAML response and is commonly used to federate between Citi sites when a user has already authenticated to a primary site.
* **3.2.1 Web-browser SSO/SP Initiated with Post Profile (Page 10):**
  * Recommended to be used when a non-authenticated user is requesting SSO authentication from a separate SP server. The Service Provider (SP) initiated SAML authentication (i.e., SAML profile interaction (ex., a SAML request and response)).
  * **Diagram:** Service Provider <-> User Agent <-> Identity Provider. Flow:
        1. Request target resource (SP)
        2. Discover the IdP
        3. Request SSO Service (IdP)
        4. Verify the user
        5. Request Authn Consumer Service (SP)
        6. Request Authn Assertion (IdP)
        7. Request target resource again (SP)
        8. Respond with requested resource (SP)
  * Text: This is the recommended flow for internal federation; all exchanges are front-channel exchanges, with the browser/User Agent communicating with the SAML entity at each step.
* **3.2.2 Web Browser SSO/Artifact Profile (Page 11):**
  * Recommended when the user is already authenticated at the IdP and is requesting SSO access to a resource on a Service Provider (SP). The Service Provider (SP) consumes an unsolicited SAML response and is commonly used to federate between Citi sites when a user has already authenticated to the primary site.
  * **Diagram:** IdP (Assertion Check, SAML Response) <-> Browser <-> SP (Artifact, Assertion Consumer Service, Resource). Flow:
        1. Credential Challenge (IdP)
        2. User login (IdP)
        3. Request remote resource (SP via Browser)
        4. Artifact in HTML form (IdP to Browser)
        5. POST Artifact (Browser to SP)
        6. Send <ArtifactResolve> (SP to IdP)
        7. Send <ArtifactResponse> (IdP to SP)
        8. Provide resource (SP to Browser)
* **3.2.3 Web Browser SSO/IdP Initiated with POST Profile (Page 12):**
  * Similar use-case to Web Browser SSO/Artifact Profile and requires an unsolicited SAML response and is commonly used to federate between sites when a user has already authenticated to a primary site.
  * **Diagram:** IdP (Assertion Check, SAML Response) <-> Browser <-> SP (Assertion, Assertion Consumer Service, Resource). Flow:
        1. Select remote resource (IdP)
        2. User login (IdP)
        3. Request target resource (IdP via Browser)
        4. Artifact in HTML form (with signed assertion in the HTML form) (IdP to Browser)
        5. POST Artifact/Assertion (Browser to SP)
        6. Provide resource (SP to Browser)
