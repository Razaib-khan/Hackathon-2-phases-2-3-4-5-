---
description: "Task list template for feature implementation"
---

# Tasks: Speckit Plus Phase II – Full-Stack Todo Application

**Input**: Design documents from `/specs/speckit-plus-phase-ii/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume web app structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 [P] Create frontend directory structure per implementation plan
- [X] T002 [P] Create backend directory structure per implementation plan
- [X] T003 [P] Initialize Next.js project with TypeScript in frontend/
- [X] T004 [P] Initialize FastAPI project with SQLModel in backend/
- [X] T005 [P] Configure linting and formatting tools for both frontend and backend

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Foundation
- [X] T006 Setup database schema and migrations framework using SQLModel and Neon
- [X] T007 [P] Create Users table with fields: id, first_name, last_name, email (unique), password_hash, favorite_teacher
- [X] T008 [P] Create Tasks table with fields: id, user_id (FK), title, description, priority, timestamp, status
- [X] T009 Define database relationships and constraints per data-model.md
- [X] T010 [P] Add indexes to database per data-model.md requirements

### Authentication Foundation
- [X] T011 [P] Implement authentication framework using Better Auth
- [X] T012 Configure JWT token generation and validation
- [X] T013 Implement user isolation enforcement in authentication layer
- [X] T014 [P] Implement password strength validation

### API Foundation
- [X] T015 Setup API routing and middleware structure in FastAPI
- [X] T016 Configure error handling and logging infrastructure
- [X] T017 Setup environment configuration management

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic Task Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to create, view, update, and delete their personal tasks

**Independent Test**: Can be fully tested by creating a task, viewing it, updating its details, and deleting it while delivering complete task management functionality

### Backend Implementation for US1
- [X] T018 [US1] Create GET /api/{user_id}/tasks endpoint for retrieving user tasks
- [X] T019 [US1] Create POST /api/{user_id}/tasks endpoint for creating tasks
- [X] T020 [US1] Create GET /api/{user_id}/tasks/{id} endpoint for retrieving specific task
- [X] T021 [US1] Create PUT /api/{user_id}/tasks/{id} endpoint for updating tasks
- [X] T022 [US1] Create DELETE /api/{user_id}/tasks/{id} endpoint for deleting tasks
- [X] T023 [US1] Implement user isolation validation for all task endpoints

### Frontend Implementation for US1
- [X] T024 [US1] Create responsive task list component in frontend/src/components/TaskList/
- [X] T025 [US1] Create task item component in frontend/src/components/TaskItem/
- [X] T026 [US1] Create task creation form component in frontend/src/components/TaskForm/
- [X] T027 [US1] Create task update form component in frontend/src/components/TaskForm/
- [X] T028 [US1] Integrate frontend API service with task endpoints

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Completion and Prioritization (Priority: P1)

**Goal**: Enable users to mark tasks as complete/incomplete and assign priority levels

**Independent Test**: Can be fully tested by toggling task completion status and changing priority levels while delivering task organization functionality

### Backend Implementation for US2
- [X] T029 [US2] Create PATCH /api/{user_id}/tasks/{id}/complete endpoint for toggling completion
- [X] T030 [US2] Add priority validation to task creation/update endpoints (Critical, High, Medium, Low)
- [X] T031 [US2] Implement priority filtering in GET /api/{user_id}/tasks endpoint

### Frontend Implementation for US2
- [X] T032 [US2] Add completion checkbox to task item component
- [X] T033 [US2] Add priority selection dropdown to task forms
- [X] T034 [US2] Implement visual priority indicators in task list (color coding)
- [X] T035 [US2] Connect completion toggle to PATCH /api/{user_id}/tasks/{id}/complete endpoint

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Search and Filtering (Priority: P2)

**Goal**: Enable users to search tasks by keywords and filter by priority, status, and timestamp

**Independent Test**: Can be fully tested by searching and filtering tasks while delivering enhanced navigation capabilities

### Backend Implementation for US3
- [X] T036 [US3] Add search functionality to GET /api/{user_id}/tasks endpoint (title and description)
- [X] T037 [US3] Add status filtering to GET /api/{user_id}/tasks endpoint
- [X] T038 [US3] Add timestamp range filtering to GET /api/{user_id}/tasks endpoint
- [X] T039 [US3] Implement combined filter logic for multiple parameters

### Frontend Implementation for US3
- [X] T040 [US3] Create search bar component in frontend/src/components/SearchFilter/
- [X] T041 [US3] Create filter controls component for priority, status, and timestamp
- [X] T042 [US3] Integrate search and filter with task list component
- [X] T043 [US3] Implement real-time search and filtering with API calls

---

## Phase 6: User Story 4 - Theme Preference (Priority: P2)

**Goal**: Enable users to toggle between dark and light mode themes

**Independent Test**: Can be fully tested by toggling theme preference while delivering enhanced visual experience

### Frontend Implementation for US4
- [X] T044 [US4] Implement theme context in frontend/src/utils/theme.js
- [X] T045 [US4] Create theme toggle component in frontend/src/components/ThemeToggle/
- [X] T046 [US4] Implement dark/light CSS themes in frontend/src/styles/themes/
- [X] T047 [US4] Persist theme preference in localStorage or cookies

---

## Phase 7: User Story 5 - User Account Management (Priority: P1)

**Goal**: Enable users to create accounts, sign in, sign out, change passwords, recover passwords, and delete accounts

**Independent Test**: Can be fully tested by completing account lifecycle operations while delivering secure user access

### Backend Implementation for US5
- [X] T048 [US5] Create POST /api/auth/signup endpoint for user registration
- [X] T049 [US5] Create POST /api/auth/signin endpoint for user login
- [X] T050 [US5] Create POST /api/auth/signout endpoint for user logout
- [X] T051 [US5] Create PUT /api/auth/password endpoint for password change
- [X] T052 [US5] Create POST /api/auth/forgot-password endpoint for password recovery
- [X] T053 [US5] Create DELETE /api/auth/account endpoint for account deletion
- [X] T054 [US5] Implement favorite teacher security question validation
- [X] T055 [US5] Add password change validation (requires old password)

### Frontend Implementation for US5
- [X] T056 [US5] Create signup page component in frontend/src/pages/Auth/
- [X] T057 [US5] Create signin page component in frontend/src/pages/Auth/
- [X] T058 [US5] Create account management page in frontend/src/pages/Account/
- [X] T059 [US5] Create password change form in frontend/src/components/Auth/
- [X] T060 [US5] Create password recovery form in frontend/src/components/Auth/
- [X] T061 [US5] Implement authentication service in frontend/src/services/auth.js

---

## Phase 8: Feature Integration and Validation

**Purpose**: Ensure all components work together seamlessly

### Integration Tasks
- [X] T062 Integrate all frontend components with backend API
- [X] T063 Implement comprehensive error handling across all features
- [X] T064 Add loading states and user feedback for all operations
- [X] T065 Ensure responsive design works across all device sizes
- [X] T066 Implement proper authentication flow across all pages

### Validation Tasks
- [X] T067 Validate all API endpoints against OpenAPI contract in contracts/api-contract.yaml
- [X] T068 Verify user isolation - each user only accesses their own tasks
- [X] T069 Test all CRUD operations for correctness
- [X] T070 Test search and filter functionality with various inputs
- [X] T071 Test authentication flows (signup, signin, password change, recovery)
- [X] T072 Test theme persistence across sessions
- [X] T073 Validate data integrity and constraints at database level

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T074 Documentation updates in docs/
- [X] T075 Code cleanup and refactoring
- [X] T076 Performance optimization across all stories
- [X] T077 [P] Add unit tests (if requested) in frontend/tests/ and backend/tests/
- [X] T078 Security hardening
- [X] T079 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Integration (Phase 8)**: Depends on all user stories being complete
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Depends on User Story 1 (completion of basic CRUD)
- **User Story 3 (P2)**: Depends on User Story 1 (uses task list component)
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Independent of other stories
- **User Story 5 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, User Stories 1, 4, and 5 can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members