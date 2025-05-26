# Business Requirements Document: SSO PoC (SAML & OIDC with RBAC)

**Version:** 1.1
**Date:** May 25, 2025
**Author:** David Santander
**Project Sponsor:** Educational Initiative

**1. Introduction & Purpose**
This document outlines the business requirements for a Proof of Concept (PoC) project. The primary goal of this PoC is to build, demonstrate, and explain Single Sign-On (SSO) functionality using SAML 2.0 and OpenID Connect (OIDC), including basic Role-Based Access Control (RBAC). The project will leverage Python (Flask) for backend services, Vue.js for frontend UIs, Keycloak as an open-source identity solution, and Docker for Windows. The objective is to create an accessible, comprehensive, and hands-on educational environment for a diverse audience (architects, junior developers, non-technical stakeholders) to understand these SSO mechanisms, their differences, and their practical application.

**2. Business Objectives & Goals**

* **BO1: Comprehensive SSO Understanding:** Provide a practical, hands-on learning environment for understanding core SSO concepts, protocol flows, and configuration for a varied audience.
* **BO2: Demonstrate SAML Integration with RBAC:** Illustrate a typical SAML-based SSO flow, including the passing and interpretation of user roles for basic authorization.
* **BO3: Demonstrate OIDC Integration with RBAC:** Illustrate a typical OIDC-based SSO flow (Authorization Code Flow), including the passing and interpretation of user roles from ID/Access tokens for basic authorization.
* **BO4: Highlight Protocol Differences Clearly:** Explain and demonstrate the key differences in architecture, implementation, message flows, token types, security considerations, and typical use cases between SAML and OIDC.
* **BO5: Leverage Modern Tooling:** Utilize Docker for Windows, Python (Flask), Vue.js, and Keycloak to ensure the PoC is reproducible, modern, and accessible.
* **BO6: Create Multi-faceted Educational Material:** Produce clear documentation, diagrams, code comments, and a summary presentation explaining the setup, configuration, architecture, workflows, and observed behaviors.

**3. Scope**

**3.1. In Scope:**

* **Identity Provider (IdP/OP) - Keycloak Setup:**
  * Deployment of Keycloak using Docker.
  * Configuration of a Keycloak realm.
  * Creation of test user accounts with assigned roles (e.g., "viewer," "editor").
  * Configuration of a SAML client (for the SAML SP) in Keycloak, including attribute/role mapping.
  * Configuration of an OIDC client (for the OIDC RP) in Keycloak, including scope/claim/role mapping.
* **SAML Service Provider (SP) Application ("App1-SAML"):**
  * Backend: Development of a simple Python Flask web application acting as a SAML SP.
  * Frontend: A simple Vue.js frontend interacting with the Flask backend.
  * Integration of the Flask backend with Keycloak using a Python SAML library.
  * Demonstration of IdP-initiated and SP-initiated SSO.
  * Display of authenticated username and assigned roles received from the SAML assertion.
  * Protection of a specific resource/route, accessible based on authentication and potentially a specific role.
* **OpenID Connect Relying Party (RP) Application ("App2-OIDC"):**
  * Backend: Development of a simple Python Flask web application acting as an OIDC RP.
  * Frontend: A simple Vue.js frontend interacting with the Flask backend.
  * Integration of the Flask backend with Keycloak (as OP) using a Python OIDC library (Authorization Code Flow).
  * Display of authenticated username and assigned roles (from ID Token claims and/or UserInfo endpoint).
  * Protection of a specific resource/route, accessible based on authentication and potentially a specific role.
* **SSO Flows:**
  * Demonstration of login to SP/RP via IdP.
  * Demonstration of single logout (SLO) for both SAML and OIDC.
* **Dockerization:**
  * Containerization of Keycloak, and the SP/RP applications (Flask backends + serving static Vue frontends) using Docker Compose for easy setup on Docker for Windows.
* **Documentation & Explanation (Comprehensive):**
  * Detailed READMEs: setup, configuration steps for Keycloak, SP, and RP (backend & frontend considerations).
  * Architecture Diagrams: High-level component diagram showing IdP, SP, RP, and User Agent.
  * Sequence Diagrams: Detailed diagrams for SAML SP-initiated flow, OIDC Authorization Code flow, and logout flows.
  * Workflow Explanations: Step-by-step textual descriptions accompanying the diagrams.
  * In-App Explanations: (If feasible) Minor text within the mock apps indicating current state or last action.
  * Code Comments: Explaining specific SAML/OIDC integration points and RBAC handling in Python code.
  * A comparative summary document/presentation: SAML vs. OIDC, covering architecture, message formats, complexity, security aspects, typical use cases, and RBAC implementation.

**3.2. Out of Scope:**

* Production-grade security hardening beyond standard PoC best practices.
* Advanced IdP features (e.g., multi-factor authentication, complex authorization policies beyond role mapping, identity brokering).
* Complex UI/UX for the mock applications; functionality and clarity over aesthetics.
* Performance testing or scalability assessments.
* Automated testing suites.
* Advanced Vue.js state management or complex frontend routing unless essential for demonstration.
* Direct OIDC SPA flows from Vue.js without backend involvement (backend will handle OIDC redirects).

**4. Stakeholders**

* **Primary Audience:** Architects, Junior Developers, Business/Non-Technical Stakeholders.
* **Project Lead/Developer:** [Person building the PoC]
* **(Optional) Mentor/Reviewer:** [Person guiding/reviewing the PoC]

**5. Requirements**

**5.1. Functional Requirements:**

* **FR1: IdP Installation & Configuration:** The user must be able to easily install and run Keycloak using Docker. Documentation must cover creating a realm, users, roles, and configuring SAML & OIDC clients including role mapping.
* **FR2: Test User Management:** Keycloak must allow creation of test users with distinct roles (e.g., `user_role_A`, `user_role_B`).
* **FR3: SAML SP Application ("App1-SAML"):**
  * FR3.1: The application will consist of a Python Flask backend and a Vue.js frontend.
  * FR3.2: The Flask backend must integrate with Keycloak as a SAML SP.
  * FR3.3: Unauthenticated users accessing protected frontend views/backend API routes should be redirected via the Flask backend to Keycloak for SAML authentication.
  * FR3.4: Upon successful authentication, the user is redirected back to the Flask SP, establishing a session.
  * FR3.5: The Vue.js frontend should display the authenticated username and user's roles (received via the Flask backend from the SAML assertion).
  * FR3.6: The application must have at least one protected resource/API endpoint accessible only to authenticated users. Access to a sub-part of this resource (or another resource) should be conditional on possessing a specific role.
  * FR3.7: A logout function should invalidate the local Flask session and trigger SAML SLO via Keycloak.
* **FR4: OIDC RP Application ("App2-OIDC"):**
  * FR4.1: The application will consist of a Python Flask backend and a Vue.js frontend.
  * FR4.2: The Flask backend must integrate with Keycloak as an OIDC RP using Authorization Code Flow.
  * FR4.3: Unauthenticated users accessing protected frontend views/backend API routes should be redirected via the Flask backend to Keycloak for OIDC authentication.
  * FR4.4: Upon successful authentication and consent, the user is redirected back to the Flask RP, which obtains tokens.
  * FR4.5: The Flask backend should obtain, validate, and store (in session) ID Token and Access Token.
  * FR4.6: The Vue.js frontend should display the authenticated username and user's roles (from claims in the ID Token or UserInfo endpoint, retrieved by the Flask backend).
  * FR4.7: The application must have at least one protected resource/API endpoint accessible only to authenticated users. Access to a sub-part of this resource (or another resource) should be conditional on possessing a specific role claim.
  * FR4.8: A logout function should invalidate the local Flask session, (ideally) revoke tokens, and redirect to Keycloak's `end_session_endpoint`.
* **FR5: SSO Experience:** A user authenticated via Keycloak for one application (e.g., SAML SP) should be able to access the other application (e.g., OIDC RP) without re-entering credentials, given an active Keycloak session.
* **FR6: Educational Content & Presentation:**
  * FR6.1: Clear, step-by-step instructions for setting up the PoC environment (Docker, Keycloak, Apps).
  * FR6.2: Detailed explanations of configurations (Keycloak clients, role mappings, SP/RP app settings).
  * FR6.3: Visual diagrams: Architecture, Component, and Sequence diagrams for major flows.
  * FR6.4: A comparative summary (document and/or presentation slides) outlining SAML vs. OIDC based on the PoC, covering:
    * Protocol flow differences.
    * Message/token formats and structure.
    * Security mechanisms (signatures, encryption points).
    * Ease of implementation (backend perspective).
    * RBAC handling.
    * Typical use-cases and when to choose one over the other.
    * Frontend vs. Backend responsibilities in the PoC.

**5.2. Non-Functional Requirements:**

* **NFR1: Ease of Setup:** Deployable with minimal commands using Docker Compose on Windows.
* **NFR2: Understandability:** Code (Python, Vue.js) should be simple, well-commented. Documentation should cater to varying technical depths.
* **NFR3: Reproducibility:** Reliably reproducible by others following the documentation.
* **NFR4: Open Source:** All core components are open-source.

**5.3. Technical Requirements:**

* **TR1: Operating System:** Docker for Windows.
* **TR2: Programming Languages:** Python 3.x (backend), JavaScript (ES6+ for Vue.js frontend).
* **TR3: Frameworks:** Flask (Python backend), Vue.js (frontend).
* **TR4: Identity Provider:** Keycloak (latest stable version) running in Docker.
* **TR5: SAML Library (Python):** e.g., `python3-saml` or similar.
* **TR6: OIDC Library (Python):** e.g., `Authlib` or similar.
* **TR7: Containerization:** Docker, Docker Compose.

**6. Assumptions**

* A working Docker for Windows environment with internet access is available.
* Basic familiarity with Python, Flask, JavaScript, Vue.js, web concepts, and command-line usage is assumed for those deeply studying the code. High-level explanations will be provided for other stakeholders.
* Flask applications will serve their respective static Vue.js build artifacts.
* The focus is on clear demonstration of SSO and RBAC, not UI/UX perfection or complex application logic.

**7. Constraints**

* The project is a PoC for educational purposes, not for production.
* Timeline for development is limited (to be defined).
* Complexity of RBAC will be limited to basic role checking (e.g., "user has role X").

**8. Success Criteria**

* **SC1:** All components (Keycloak, App1-SAML, App2-OIDC) deploy and run via Docker Compose.
* **SC2:** SSO login, SLO, and RBAC (role display and protected resource access based on role) are functional for both SAML SP and OIDC RP applications.
* **SC3:** SSO session sharing between App1 and App2 via Keycloak is demonstrated.
* **SC4:** User attributes (username, roles) are passed and displayed in both applications.
* **SC5:** Comprehensive documentation (READMEs, diagrams, summary presentation) is complete, clear, and accurate for the target audiences.
* **SC6:** The PoC effectively highlights key differences between SAML and OIDC.
* **SC7:** The PoC successfully serves its educational purpose for architects, junior developers, and non-technical stakeholders.

**9. Deliverables**

* **D1:** `docker-compose.yml` file and associated Dockerfiles.
* **D2:** Source code for the SAML SP (Flask backend & Vue.js frontend assets).
* **D3:** Source code for the OIDC RP (Flask backend & Vue.js frontend assets).
* **D4:** Keycloak realm export file or detailed configuration steps/scripts.
* **D5:** Comprehensive `README.md` (or set of linked markdown files) covering:
  * PoC overview, objectives, architecture.
  * Prerequisites.
  * Step-by-step setup, deployment, and configuration instructions.
  * Explanation of SAML and OIDC flows with reference to the PoC and diagrams.
  * Explanation of RBAC implementation.
  * Troubleshooting tips.
* **D6:** Sequence diagrams (e.g., PlantUML or draw.io) for login and logout flows.
* **D7:** Architecture and Component diagrams.
* **D8:** A presentation (e.g., PowerPoint, Google Slides, or Markdown-based slides) summarizing the PoC, findings, and the SAML vs. OIDC comparison.

**10. Glossary**

* **SSO:** Single Sign-On
* **IdP:** Identity Provider
* **OP:** OpenID Provider
* **SP:** Service Provider (SAML)
* **RP:** Relying Party (OIDC)
* **SAML:** Security Assertion Markup Language
* **OIDC:** OpenID Connect
* **RBAC:** Role-Based Access Control
* **Assertion:** (SAML) A package of security information including identity and attributes.
* **ID Token:** (OIDC) A JWT containing identity information.
* **Access Token:** (OIDC/OAuth2) A token granting access to resources.
* **JWT:** JSON Web Token
* **Flask:** Python micro web framework.
* **Vue.js:** Progressive JavaScript framework for UIs.
* **Keycloak:** Open-source Identity and Access Management solution.
* **Docker:** Containerization platform.
* **Docker Compose:** Tool for multi-container Docker applications.

---

This revised BRD should provide a solid foundation for your educational PoC project. Let me know if you have any more questions or adjustments!
