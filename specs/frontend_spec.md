# Frontend Agent Specification

## Agent Classification
**Level 4 Expert** - As defined in `.specify/memory/constitution.md` Agent Skills Registry

## Overview
The Frontend Agent specializes in Next.js development with App Router, Tailwind CSS styling, and API integration. This agent creates responsive, user-friendly interfaces that connect to backend services using secure authentication patterns.

## Responsibilities
- Implement Next.js App Router architecture with proper page structure
- Create responsive UI components using Tailwind CSS
- Integrate with backend APIs using secure authentication
- Manage client-side state and authentication tokens
- Implement form validation and user experience patterns
- Handle responsive design for multiple device sizes

## Technical Specifications

### Next.js App Router Structure
#### Directory Structure
- **app/**: Next.js 13+ App Router
  - **layout.tsx**: Root layout with global styles
  - **page.tsx**: Home page with authentication redirect
  - **login/page.tsx**: Login form component
  - **signup/page.tsx**: Signup form component
  - **dashboard/page.tsx**: Todo dashboard with CRUD operations

#### Page Components
- **Home Page**:
  - Redirects authenticated users to dashboard
  - Provides login/signup links for unauthenticated users
  - Responsive design with gradient background

- **Login Page**:
  - Email and password form fields
  - Client-side validation
  - Error handling and display
  - Navigation to signup page

- **Signup Page**:
  - Name, email, and password fields
  - Client-side validation for password strength
  - Auto-login after successful signup
  - Navigation to login page

- **Dashboard Page**:
  - Todo list display with completion status
  - Add new todo form
  - Edit and delete functionality
  - User logout capability

### Tailwind CSS Styling
#### Responsive Design
- Mobile-first approach with responsive breakpoints
- Flexbox and Grid layouts for complex components
- Responsive spacing and typography
- Touch-friendly interface elements

#### Component Styling
- **Forms**: Consistent styling with validation states
- **Buttons**: Primary and secondary action buttons
- **Cards**: Content containers with shadows and rounded corners
- **Navigation**: Header with logout functionality
- **Lists**: Todo items with checkbox and action buttons

#### Color Palette
- Primary: Indigo (buttons, links, highlights)
- Background: Gradient from blue-50 to indigo-100
- Text: Gray with appropriate contrast ratios
- Status: Red for errors, green for success

### API Integration
#### Authentication Management
- **Token Storage**: JWT tokens in localStorage
- **Authentication Check**: Client-side verification
- **Token Validation**: Decode JWT payload for user info
- **Logout Functionality**: Remove token and redirect

#### API Endpoints
- **Authentication**:
  - POST `/login` - User authentication
  - POST `/signup` - User registration
  - GET `/me` - Current user info

- **Todo Operations**:
  - POST `/todos` - Create new todo
  - GET `/todos` - Retrieve user todos
  - PUT `/todos/{id}` - Update todo status
  - DELETE `/todos/{id}` - Delete todo

#### Fetch Implementation
- **Axios/Fetch**: HTTP client for API calls
- **Error Handling**: Comprehensive error responses
- **Loading States**: Visual feedback during requests
- **Authentication Headers**: Bearer token for protected routes

### State Management
#### Client-Side State
- **Todo State**: Manage todo list in component state
- **Form State**: Track form inputs and validation
- **Authentication State**: Track login status and user info
- **Error State**: Display error messages to users

#### User Experience Patterns
- **Form Validation**: Real-time validation feedback
- **Loading Indicators**: Visual feedback during API calls
- **Success/Error Messages**: Clear feedback for user actions
- **Navigation**: Intuitive routing between pages

## Implementation Requirements
- Use Next.js App Router with TypeScript
- Implement responsive design with Tailwind CSS
- Include proper error handling and user feedback
- Follow accessibility best practices
- Optimize for performance and SEO

## Security Considerations
- Secure token storage in localStorage
- Proper authentication headers for API calls
- Input sanitization and validation
- Prevention of XSS through proper escaping
- Secure transmission over HTTPS

## Performance Optimization
- Code splitting and lazy loading
- Image optimization and responsive loading
- Efficient state management to minimize re-renders
- Proper HTTP caching strategies
- Bundle size optimization with tree-shaking