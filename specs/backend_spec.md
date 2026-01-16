# Backend Agent Specification

## Agent Classification
**Level 4 Expert** - As defined in `.specify/memory/constitution.md` Agent Skills Registry

## Overview
The Backend Agent specializes in FastAPI development, including route definition, request/response validation with Pydantic models, and middleware configuration. This agent creates robust REST APIs that integrate with authentication and database layers.

## Responsibilities
- Design and implement FastAPI routes for all application endpoints
- Create Pydantic models for request/response validation
- Configure CORSMiddleware for frontend integration
- Handle dependency injection for authentication
- Implement proper error handling and HTTP status codes
- Connect to Auth and Database agents for business logic

## Technical Specifications

### FastAPI Configuration
#### Application Setup
- Title: "Todo API"
- Description: FastAPI backend for Todo application with authentication
- Version: 1.0.0
- OpenAPI documentation enabled by default

#### Middleware Configuration
- **CORSMiddleware**:
  - Allow origins: ["*"] (production: specific origins only)
  - Allow credentials: true
  - Allow methods: ["*"]
  - Allow headers: ["*"]

### Pydantic Model Definitions
#### Request Models
- **UserSignupRequest**:
  - name: String with min/max length validation
  - email: String with format validation
  - password: String with minimum length validation

- **UserLoginRequest**:
  - email: String with format validation
  - password: String with minimum length validation

- **TodoCreateRequest**:
  - title: String with required validation
  - description: Optional string with max length

- **TodoUpdateRequest**:
  - title: Optional string with validation
  - description: Optional string with validation
  - completed: Optional boolean

#### Response Models
- **UserResponse**:
  - id: Integer
  - name: String
  - email: String
  - created_at: Optional DateTime

- **TodoResponse**:
  - id: Integer
  - title: String
  - description: Optional String
  - completed: Boolean
  - user_id: Integer
  - created_at: DateTime
  - updated_at: DateTime

- **TokenResponse**:
  - access_token: String
  - token_type: String (default: "bearer")

- **ErrorResponse**:
  - detail: String

### Route Specifications
#### Authentication Routes
- **POST /signup**:
  - Request: UserSignupRequest
  - Response: UserResponse (201)
  - Errors: 400 (validation), 409 (duplicate), 500 (server error)

- **POST /login**:
  - Request: UserLoginRequest
  - Response: TokenResponse (200)
  - Errors: 401 (invalid credentials), 400 (validation), 500 (server error)

- **GET /me**:
  - Authentication: Bearer token required
  - Response: UserResponse (200)
  - Errors: 401 (unauthorized), 404 (user not found)

#### Todo Routes
- **POST /todos**:
  - Authentication: Bearer token required
  - Request: TodoCreateRequest
  - Response: TodoResponse (201)
  - Errors: 401 (unauthorized), 400 (validation), 500 (server error)

- **GET /todos**:
  - Authentication: Bearer token required
  - Response: List[TodoResponse] (200)
  - Errors: 401 (unauthorized), 500 (server error)

- **GET /todos/{id}**:
  - Authentication: Bearer token required
  - Response: TodoResponse (200)
  - Errors: 401 (unauthorized), 404 (not found), 500 (server error)

- **PUT /todos/{id}**:
  - Authentication: Bearer token required
  - Request: TodoUpdateRequest
  - Response: TodoResponse (200)
  - Errors: 401 (unauthorized), 400 (validation), 404 (not found), 500 (server error)

- **DELETE /todos/{id}**:
  - Authentication: Bearer token required
  - Response: Success message (200)
  - Errors: 401 (unauthorized), 404 (not found), 500 (server error)

### Authentication Dependencies
#### JWT Token Verification
- HTTPBearer security scheme
- Custom get_current_user dependency
- Token decoding and validation
- User information retrieval from database

#### Database Session Management
- get_db dependency for session injection
- Proper session lifecycle (create, commit, close)
- Error handling for database operations
- Connection pooling integration

## Implementation Requirements
- Use FastAPI's dependency injection system
- Implement proper request/response validation
- Include comprehensive error handling
- Follow REST API best practices
- Document all endpoints with OpenAPI

## Security Considerations
- JWT token validation for protected routes
- Input validation through Pydantic models
- SQL injection prevention through ORM
- Proper authentication for all protected endpoints
- Secure transmission of sensitive data

## Performance Optimization
- Efficient database queries with proper filtering
- Connection pooling for database operations
- Minimal data transfer in responses
- Caching considerations for frequently accessed data
- Proper indexing on database queries