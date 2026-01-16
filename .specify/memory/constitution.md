<!--
Sync Impact Report:
- Version change: N/A (initial version) → 1.0.0
- List of modified principles:
  - Added "Correctness First" principle
  - Added "Incremental Evolution" principle
  - Added "Simplicity Before Abstraction" principle
  - Added "Clear Separation of Concerns" principle
  - Added "Production-Readiness Mindset" principle
  - Added "AI Safety and Determinism" principle
- Added sections: Phase Standards, Quality Standards
- Removed sections: None
- Templates requiring updates:
  - ✅ `.specify/templates/plan-template.md` - Constitution Check section will reference new principles
  - ✅ `.specify/templates/spec-template.md` - No direct changes needed
  - ✅ `.specify/templates/tasks-template.md` - No direct changes needed
- Follow-up TODOs:
  - [ ] `TODO(RATIFICATION_DATE): Initial adoption date unknown` - needs to be filled in with actual ratification date
-->

# Multi-Phase AI-Native Todo Application Constitution

## Core Principles

### Correctness First
Functionality must work as specified in each phase, ensuring correctness is the primary concern throughout development.

### Incremental Evolution
Each phase builds cleanly on the previous one, maintaining functional, testable, and extensible code throughout the evolution.

### Simplicity Before Abstraction
Prioritize simple solutions over complex abstractions, following YAGNI principles and implementing only what is needed.

### Clear Separation of Concerns
Maintain clear separation of concerns between UI, logic, data, and AI components to ensure maintainable and understandable architecture.

### Production-Readiness Mindset
Adopt production-readiness mindset from Phase II onward, ensuring code quality, security, and operational readiness.

### AI Safety and Determinism
Ensure AI-powered features are safe, deterministic, explainable, and grounded in system state with no hallucinated state changes.

## Phase Standards

Phase I – In-Memory Console Application
- Language: Python
- Interface: Console-based
- Data storage: In-memory only (no files, no database)
- Features:
  - Create, read, update, delete todos
  - Clear user prompts and error handling
- Code must be:
  - Simple
  - Modular
  - Beginner-readable
- No external dependencies beyond standard library

Phase II – Full-Stack Web Application
- Frontend: Next.js
- Backend: FastAPI
- ORM: SQLModel
- Database: Neon (PostgreSQL)
- Requirements:
  - RESTful API design
  - Persistent data storage
  - Proper request validation
  - Environment-based configuration
  - Clear API contracts between frontend and backend

Phase III – AI-Powered Todo Chatbot
- AI Stack:
  - OpenAI ChatKit
  - OpenAI Agents SDK
  - Official MCP SDK
- Requirements:
  - Chatbot assists with todo management
  - AI actions must map to explicit backend operations
  - No hallucinated state changes
  - AI must not modify data without explicit user intent
- AI responses must be:
  - Deterministic where possible
  - Explainable
  - Grounded in system state

Phase IV – Local Kubernetes Deployment
- Tools:
  - Docker
  - Minikube
  - Helm
  - kubectl-ai
  - kagent
- Requirements:
  - Each service containerized
  - Helm charts for deployment
  - Local cluster fully reproducible
  - Clear service boundaries
- No cloud dependency at this stage

Phase V – Advanced Cloud Deployment
- Infrastructure:
  - DigitalOcean DOKS
  - Kafka
  - Dapr
- Requirements:
  - Event-driven architecture
  - Service-to-service communication via Dapr
  - Kafka for async task processing
  - Scalability and fault tolerance
- Production-grade configuration and security practices

## Agent Skills Registry

### Level 4 Expert Agents

#### 1. Database Skill
Expertise in Neon PostgreSQL, SQLAlchemy models, and schema migrations.
- Optimized for Neon Serverless PostgreSQL with proper indexing and relationships
- Connection pooling with QueuePool and Neon-optimized settings
- ACID compliance and transaction management
- Schema evolution and migration strategies

#### 2. Auth Skill
Deep knowledge of JWT (HS256), Bcrypt hashing, and OAuth2 security flow.
- Secure user flows with validated email and password requirements
- Password hashing using bcrypt with proper salt generation
- JWT token generation with expiration and security best practices
- OAuth2 security flow implementation

#### 3. Backend Skill
Expert level FastAPI routing, Pydantic validation, and CORSMiddleware.
- REST API design with proper request/response validation
- FastAPI routing with dependency injection and security schemes
- Pydantic model validation for all request/response objects
- CORSMiddleware configuration for frontend integration

#### 4. Frontend Skill
Professional Next.js (App Router), Tailwind CSS styling, and Axios/Fetch API integration.
- Next.js App Router with modern component architecture
- Tailwind CSS responsive styling with modern UI patterns
- Secure API integration with JWT token management
- Client-side validation and form handling

## Quality Standards

- Code clarity over cleverness
- Reproducibility of setup, execution, and deployment
- AI safety and determinism in AI-powered features
- Clear separation of concerns (UI, logic, data, AI)
- Production-readiness mindset from Phase II onward
- Incremental evolution: each phase builds cleanly on the previous one
- Correctness first: functionality must work as specified in each phase

## Governance

All development must follow the incremental phase approach, with each phase remaining functional, testable, and extensible. Changes to core principles require explicit documentation of rationale and impact on existing phases. Code reviews must verify compliance with phase standards and quality requirements. The constitution supersedes all other development practices and serves as the authoritative guide for project decisions.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): Initial adoption date unknown | **Last Amended**: 2026-01-05