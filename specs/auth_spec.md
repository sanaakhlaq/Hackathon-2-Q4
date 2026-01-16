# Auth Agent Specification

## Agent Classification
**Level 4 Expert** - As defined in `.specify/memory/constitution.md` Agent Skills Registry

## Overview
The Auth Agent specializes in authentication and security mechanisms, including JWT token management, bcrypt password hashing, and OAuth2 security flows. This agent ensures secure user flows and proper credential validation.

## Responsibilities
- Manage secure user registration and login flows
- Implement bcrypt password hashing with proper salt generation
- Handle JWT token creation with HS256 algorithm
- Validate user credentials and authentication
- Implement OAuth2 security flow patterns
- Provide password reset functionality

## Technical Specifications

### Authentication Methods
#### User Registration (Signup)
- Validate email format using regex
- Validate password strength (minimum 8 characters)
- Hash passwords using bcrypt with salt generation
- Check for duplicate email addresses
- Create new user records in database
- Return user information without sensitive data

#### User Login
- Validate email format using regex
- Verify credentials against hashed password
- Generate JWT access token with expiration
- Handle invalid credentials appropriately
- Return access token for subsequent requests

### Password Security
#### Bcrypt Hashing
- Use bcrypt.gensalt() for salt generation
- Apply bcrypt.hashpw() for password hashing
- Implement bcrypt.checkpw() for password verification
- Hash length: 60 characters (standard bcrypt output)
- Salt rounds: Default bcrypt recommendation

### JWT Token Management
#### Token Generation
- Algorithm: HS256 (HMAC SHA-256)
- Secret key: Stored in BETTER_AUTH_SECRET environment variable
- Expiration: 30 minutes by default
- Claims:
  - `sub`: User email (subject)
  - `scopes`: User permissions (default: ["user"])
  - `exp`: Expiration timestamp

#### Token Verification
- Decode tokens using jwt.decode()
- Validate expiration using jwt.ExpiredSignatureError
- Handle malformed tokens with jwt.JWTError
- Return appropriate error messages for each failure type

### Security Measures
#### Input Validation
- Email validation using regex pattern: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- Password minimum length: 8 characters
- Prevent SQL injection through parameterized queries
- Sanitize user inputs where appropriate

#### Error Handling
- Custom AuthException for authentication errors
- Distinct error messages for different failure types
- Prevent user enumeration through timing attacks
- Log security-relevant events appropriately

### OAuth2 Flow Implementation
#### Authorization
- Support for bearer token authentication
- Token validation middleware
- Scopes-based access control
- Refresh token considerations

#### Session Management
- JWT-based stateless sessions
- Proper token storage recommendations
- Secure token transmission
- Session termination procedures

## Implementation Requirements
- Use python-jose for JWT operations
- Implement proper exception handling
- Validate all user inputs
- Follow security best practices
- Include comprehensive error messages

## Security Considerations
- Secure storage of secret keys in environment variables
- Proper password hashing without plaintext storage
- Secure token transmission over HTTPS
- Prevention of common authentication vulnerabilities
- Rate limiting considerations for brute force protection

## Performance Optimization
- Efficient password verification algorithms
- Cached token validation where appropriate
- Minimal database queries for authentication
- Proper session management to reduce overhead