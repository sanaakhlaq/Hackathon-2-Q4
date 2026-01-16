# Database Agent Specification

## Agent Classification
**Level 4 Expert** - As defined in `.specify/memory/constitution.md` Agent Skills Registry

## Overview
The Database Agent specializes in Neon PostgreSQL schema design, SQLAlchemy model definitions, and database management. This agent ensures optimized database operations, proper indexing, and ACID compliance for the application.

## Responsibilities
- Design and maintain Neon PostgreSQL schema with proper indexing
- Create and manage SQLAlchemy models with relationships
- Handle connection pooling and session management
- Implement schema migrations and evolution strategies
- Ensure ACID compliance and transaction management

## Technical Specifications

### Database Configuration
- **Database**: Neon Serverless PostgreSQL
- **Connection Pooling**: QueuePool with optimized settings
- **Pool Size**: 5 connections minimum
- **Max Overflow**: 10 additional connections
- **Recycle Time**: 300 seconds (5 minutes)
- **Pre-ping**: Enabled for connection verification

### Model Definitions
#### User Model
- **Table Name**: `users`
- **Primary Key**: `id` (Integer, auto-increment)
- **Fields**:
  - `name`: String(100), not null, indexed
  - `email`: String(100), unique, not null, indexed
  - `hashed_password`: String(255), not null
  - `created_at`: DateTime, default UTC timestamp, indexed
  - `updated_at`: DateTime, default UTC timestamp, on-update, indexed
- **Relationships**: One-to-many with todos (cascade delete)

#### Todo Model
- **Table Name**: `todos`
- **Primary Key**: `id` (Integer, auto-increment)
- **Fields**:
  - `title`: String(200), not null, indexed
  - `description`: Text, nullable
  - `completed`: Boolean, default false, indexed
  - `user_id`: Integer, foreign key to users.id, not null, indexed
  - `created_at`: DateTime, default UTC timestamp, indexed
  - `updated_at`: DateTime, default UTC timestamp, on-update, indexed
- **Relationships**: Many-to-one with user

### Indexing Strategy
- `idx_users_email`: Index on email (for authentication)
- `idx_users_created_at`: Index on creation timestamp
- `idx_todos_user_id`: Index on user_id (for queries)
- `idx_todos_completed`: Index on completion status
- `idx_todos_created_at`: Index on creation timestamp

### Connection Management
- Engine initialization with Neon-optimized settings
- Session management with proper lifecycle (create, commit, close)
- Error handling for connection failures
- Automatic connection recycling

## Implementation Requirements
- Use SQLAlchemy ORM with declarative base
- Implement proper error handling for database operations
- Optimize for Neon Serverless with connection pooling
- Include proper validation and constraints
- Follow ACID principles for all transactions

## Security Considerations
- Parameterized queries to prevent SQL injection
- Proper isolation levels for concurrent operations
- Secure connection handling with environment variables
- Password hashing handled at application level (not database)

## Performance Optimization
- Proper indexing strategy for query optimization
- Connection pooling to minimize connection overhead
- Efficient query patterns for common operations
- Batch operations where appropriate