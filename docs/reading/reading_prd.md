# Reading Management System - Product Requirements Document

**Document Version:** 1.0  
**Last Updated:** May 20, 2026  
**Status:** Implementation Complete (Based on Current Service)

---

## 1. Executive Summary

The Reading Management System is a comprehensive feature that allows users to track their reading activities across multiple items (books, articles, etc.) in their personal library. It enables users to create reading sessions, track reading progress with granular metrics, manage reading goals and queues, and maintain detailed statistics about their reading habits.

---

## 2. Product Vision & Goals

### Vision
Empower users to develop meaningful reading habits through intelligent tracking, goal-setting, and progress visualization.

### Key Goals
1. **Track Reading Sessions**: Record when users start and finish reading items
2. **Monitor Progress**: Track pages read or percentage completion with detailed progress entries
3. **Goal Management**: Set and achieve annual reading goals
4. **Reading Queue**: Maintain a reading queue with items to be read
5. **Statistics & Insights**: Provide detailed reading statistics and historical data
6. **Status Management**: Support multiple reading statuses (reading, completed, dropped)

---

## 3. Core Features

### 3.1 Reading Session Management
Create and manage reading sessions for library items with multiple readings per item support.

**Key Capabilities:**
- Create new reading sessions for items
- Support multiple readings for the same item (track reading history)
- Automatic session numbering (first read, second read, etc.)
- Track both active and completed readings
- Prevent overlapping reading sessions
- Validate date constraints (new reading can't start before previous finishes)

### 3.2 Reading Progress Tracking
Record detailed progress entries for ongoing readings.

**Key Capabilities:**
- Multiple progress entry types: page-based or percentage-based
- Automatic calculation between pages and percentages
- One entry per day limit (updates existing entry if already recorded today)
- Validate progress doesn't exceed item's total pages
- Track reading rate/rating per progress entry
- Capture comments/notes with each entry
- Automatic reading completion when 100% or final page reached
- Progress date tracking

### 3.3 Reading Queue & Goals
Manage a reading queue with annual goal tracking.

**Key Capabilities:**
- Add items to reading queue for specific years
- Automatic active status management
- Mark goals as achieved with achievement date
- Deactivate items from queue
- Prevent removal of items with active readings
- Year-based goal organization
- Per-item goal status tracking

### 3.4 Reading Status Management
Granular status tracking for reading sessions.

**Status Types:**
- **reading**: Currently reading (active=true)
- **read/completed**: Finished reading (active=false, finish_date set)
- **dropped**: Abandoned reading (active=false, finish_date set)

### 3.5 Reading Statistics
Comprehensive reading analytics and history.

**Available Metrics:**
- Total readings count per item
- Last reading date and history
- Current reading status and progress
- Current page and percentage completion
- Reading streak/frequency data
- Goal achievement statistics

---

## 4. Data Models & Entities

### 4.1 Reading Model

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | UUID | Unique identifier | Primary Key, Auto-generated |
| owner_id | UUID | User who owns the reading | Foreign Key to User, Required |
| item_id | int | Item being read | Foreign Key to Item, Required |
| start_date | date | Reading start date | Required, Non-null |
| finish_date | date | Reading completion date | Optional, Nullable |
| number | int | Reading sequence number | Default=1, Read-only |
| status_id | str | Current reading status | Foreign Key to Status (reading, read, dropped) |
| active | bool | Whether reading is in progress | Default=true for new readings |
| progress | List[ReadingProgress] | Progress entries | 1-to-many relationship |
| item | Item | Related item object | Eager loaded |
| status | Status | Related status object | Eager loaded |

### 4.2 Reading Progress Model

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | UUID | Unique identifier | Primary Key, Auto-generated |
| reading_id | UUID | Associated reading | Foreign Key to Reading, Required |
| item_id | int | Associated item | Foreign Key to Item, Required |
| progress_date | date | Progress entry date | Required, One per day per reading |
| page | int | Current page number | Optional, Nullable |
| percentage | float | Completion percentage | Optional, Nullable, 0-100 |
| rate | int | User rating/score | Optional, Nullable |
| comment | str | User notes | Optional, Nullable |
| reading | Reading | Associated reading | Back-reference |
| item | Item | Associated item | Back-reference |

### 4.3 Reading Queue Model

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | UUID | Unique identifier | Primary Key, Auto-generated |
| owner_id | UUID | User who owns the goal | Foreign Key to User, Required |
| item_id | int | Item in queue | Foreign Key to Item, Required |
| year | int | Goal year | Required |
| achieved | bool | Goal completion status | Default=false |
| date_achieved | datetime | Goal achievement date | Optional, Nullable |
| active | bool | Queue status | Implicit, Soft-delete indicator |
| item | Item | Related item object | Eager loaded |

---

## 5. API Specification

### 5.1 GraphQL Queries

#### Query: getReading
Retrieve a specific reading session by ID.

```graphql
query {
  getReading(readingId: "uuid") {
    id
    itemId
    item { ... }
    itemTitle
    startDate
    finishDate
    number
    active
    statusId
    statusName
    progress { ... }
  }
}
```

**Parameters:**
- `readingId` (UUID, required): The reading session ID

**Returns:** ReadingSchema object

**Error Cases:**
- 404 NOT FOUND: Reading not found

---

#### Query: getReadings
Retrieve multiple readings with optional filtering and progress inclusion.

```graphql
query {
  getReadings(params: {
    itemId: 123
    readingId: "uuid"
    getProgress: true
  }) {
    quantity
    readings { ... }
  }
}
```

**Parameters:**
- `params.itemId` (int, optional): Filter by item
- `params.readingId` (UUID, optional): Filter by specific reading
- `params.getProgress` (bool, default=false): Include progress entries

**Returns:** 
```typescript
{
  quantity: int,
  readings: ReadingSchema[]
}
```

**Validation:**
- Cannot specify both `itemId` and `readingId`

---

#### Query: getActiveReadings
Retrieve all currently active readings for the user.

```graphql
query {
  getActiveReadings {
    quantity
    readings { ... }
  }
}
```

**Returns:**
```typescript
{
  quantity: int,
  readings: ReadingSchema[]
}
```

---

#### Query: getReadingProgress
Get all progress entries for a specific reading.

```graphql
query {
  getReadingProgress(params: {
    readingId: "uuid"
  }) {
    quantity
    itemTitle
    pagesRead
    progress { ... }
  }
}
```

**Parameters:**
- `params.readingId` (UUID, required): Reading session ID

**Returns:**
```typescript
{
  quantity: int,
  itemTitle: string,
  pagesRead: string,      // Format: "125/300 - 41.67%"
  progress: ProgressSchema[]
}
```

---

#### Query: getReadingStats
Get comprehensive reading statistics for an item.

```graphql
query {
  getReadingStats(params: { itemId: 123 }) {
    stats {
      readingsCount
      lastReadingDate
      isCurrentlyReading
      currentReadingId
      currentPage
      currentPercentage
      lastReadings { ... }
    }
  }
}
```

**Parameters:**
- `params.itemId` (int, required): Item ID

**Returns:**
```typescript
{
  stats: {
    readingsCount: int,
    lastReadingDate: date | null,
    isCurrentlyReading: boolean,
    currentReadingId: UUID | null,
    currentPage: int | null,
    currentPercentage: float | null,
    lastReadings: ReadingSchema[]
  }
}
```

**Validation:**
- If `isCurrentlyReading=true`, `currentReadingId` must be provided

---

#### Query: getReadingQueue
Get reading queue/goals for a specific year.

```graphql
query {
  getReadingQueue(params: { year: 2026 }) {
    goals {
      id
      itemId
      item { ... }
      achieved
      dateAchieved
      year
    }
  }
}
```

**Parameters:**
- `params.year` (int, optional): Filter by year (defaults to all active goals)

**Returns:**
```typescript
{
  goals: Array<{
    id: UUID,
    itemId: int,
    item: ItemSchema,
    achieved: boolean,
    dateAchieved: datetime | null,
    year: int
  }>
}
```

---

### 5.2 GraphQL Mutations

#### Mutation: createReading
Create a new reading session for an item.

```graphql
mutation {
  createReading(reading: {
    itemId: 123
    startDate: "2026-05-20"
    finishDate: null
    isDropped: false
  }) {
    created
    readingId
    itemTitle
  }
}
```

**Parameters:**
- `reading.itemId` (int, required): Item to read
- `reading.startDate` (date, default=today): Reading start date
- `reading.finishDate` (date, optional): If provided, marks reading as completed
- `reading.isDropped` (bool, default=false): Dropped status

**Returns:**
```typescript
{
  created: boolean,
  readingId: UUID,
  itemTitle: string
}
```

**Business Logic:**
- Checks for existing active reading on same item (prevents duplicates)
- Validates new reading doesn't start before previous reading ended
- Sets status based on finish_date (reading vs read)
- Auto-increments reading number based on history
- Sets owner_id to authenticated user
- Auto-adds item to reading queue if not already present

**Error Cases:**
- 412 PRECONDITION_FAILED: Active reading already exists for item
- 412 PRECONDITION_FAILED: New reading starts before previous finishes

---

#### Mutation: createReadingProgress
Record progress entry for an ongoing reading.

```graphql
mutation {
  createReadingProgress(progress: {
    readingId: "uuid"
    progressType: "page"        # or "percentage"
    value: 125
    progressDate: "2026-05-20"
    rate: 5
    comment: "Great chapter!"
  }) {
    created
    itemTitle
    readingProgressId
  }
}
```

**Parameters:**
- `progress.readingId` (UUID, required): Reading session
- `progress.progressType` (enum: "page" | "percentage", required)
- `progress.value` (int, required): Page number or percentage (1-100)
- `progress.progressDate` (date, required): Entry date
- `progress.rate` (int, optional): Rating/score
- `progress.comment` (str, optional): User notes

**Returns:**
```typescript
{
  created: boolean,
  itemTitle: string,
  readingProgressId: UUID
}
```

**Business Logic:**
- Validates progress_date is not before last entry date
- Validates new value > last entry value (monotonic increase)
- Validates page doesn't exceed item's total pages
- One entry per day limit (updates existing if same day)
- Auto-converts between pages/percentage using item's page count
- Auto-completes reading when page==totalPages or percentage==100
- Updates rate and comment on same-day updates

**Error Cases:**
- 404 NOT FOUND: Reading not found
- 428 PRECONDITION_REQUIRED: Progress date older than last entry
- 428 PRECONDITION_REQUIRED: Progress value less than last entry
- 428 PRECONDITION_REQUIRED: Page exceeds item total pages
- Validation: percentage must be 1-100
- Validation: page must be positive integer

---

#### Mutation: updateReadingQueue
Add item to reading queue or toggle queue status.

```graphql
mutation {
  updateReadingQueue(params: {
    itemId: 123
    year: 2026
  }) {
    created
    readingGoalId
    currentStatus
    isCurrentlyInQueue
    itemId
    itemTitle
  }
}
```

**Parameters:**
- `params.itemId` (int, required): Item to add to queue
- `params.year` (int, optional): Goal year (defaults to current year)

**Returns:**
```typescript
{
  created: boolean,
  readingGoalId: UUID,
  currentStatus: "active" | "inactive",
  isCurrentlyInQueue: boolean,
  itemId: int,
  itemTitle: string
}
```

**Business Logic:**
- If item already in queue:
  - If achieved: raise error (can't re-add achieved goal)
  - If has active reading: raise error (can't remove while reading)
  - If inactive: toggle to inactive (soft-delete)
  - Returns current status
- If item not in queue:
  - Validates item exists
  - Creates new queue entry with active=true
  - Sets owner_id to authenticated user
  - Returns created=true

**Error Cases:**
- 412 PRECONDITION_FAILED: Item has achieved goal this year
- 412 PRECONDITION_FAILED: Item has active reading (can't remove)
- 404 NOT FOUND: Item not found

---

#### Mutation: updateReadingStatus
Change reading status (reading → completed/dropped, etc.).

```graphql
mutation {
  updateReadingStatus(params: {
    readingId: "uuid"        # or itemId
    itemId: 123
    newStatus: "completed"   # "reading" | "completed" | "dropped"
  }) {
    updatedStatus
    itemTitle
  }
}
```

**Parameters:**
- `params.readingId` (UUID, optional): Reading session ID
- `params.itemId` (int, optional): Item ID (uses active reading)
- `params.newStatus` (enum, required): Target status

**Returns:**
```typescript
{
  updatedStatus: string,
  itemTitle: string
}
```

**Business Logic:**
- Supports updating by reading_id or active reading for item_id
- If `newStatus="completed"` (reading → finished):
  - Sets finish_date = today
  - Sets active = false
  - Sets status_id = "read"
  - Marks queue goal as achieved if exists
- If `newStatus="reading"`:
  - Sets finish_date = null
  - Sets active = true
  - Sets status_id = "reading"
- If `newStatus="dropped"`:
  - Sets finish_date = today
  - Sets active = false
  - Sets status_id = "dropped"

**Error Cases:**
- 404 NOT FOUND: Reading not found

---

### 5.3 REST Endpoints

#### GET /reading/active
Get active readings for authenticated user.

**URL:** `GET /api/reading/active`

**Authentication:** Required (Bearer token)

**Returns:**
```typescript
{
  quantity: int,
  readings: ReadingSchema[]
}
```

**Description:** REST endpoint for fetching all currently active readings. GraphQL equivalent: `getActiveReadings` query.

---

## 6. Business Logic & Rules

### 6.1 Reading Session Rules

| Rule | Description | Implementation |
|------|-------------|-----------------|
| **Unique Active Reading** | Only one active reading per item at a time | Checked on create_reading |
| **Sequential Dates** | New reading start_date > previous reading finish_date | Checked on create_reading |
| **Auto-numbering** | Reading sessions numbered sequentially (1, 2, 3...) | Set in create_reading |
| **Auto Status** | Status determined by finish_date at creation | set in create_reading |
| **Auto Queue Addition** | Item auto-added to queue if not present | In create_reading |
| **Owner Isolation** | Users only see their own readings | Query filtered by user_id |

### 6.2 Progress Tracking Rules

| Rule | Description | Implementation |
|------|-------------|-----------------|
| **Monotonic Increase** | Page/percentage can only increase | Validated in create_progress_v2 |
| **One per Day** | Max one entry per day per reading | Checked, updated if duplicate |
| **Page Limit** | Pages can't exceed item's total pages | Validated in create_progress_v2 |
| **Auto-conversion** | Auto-calculate percentage from pages (and vice versa) | _set_values method |
| **Auto-completion** | Mark reading complete at 100% or final page | In create_progress_v2 |
| **Date Ordering** | Progress date must be >= previous entry date | Validated in create_progress_v2 |

### 6.3 Reading Queue Rules

| Rule | Description | Implementation |
|------|-------------|-----------------|
| **Year-based Goals** | Goals tracked per year | In ReadingQueueModel |
| **Active Flag** | Soft-delete via active flag | Query filter on active=true |
| **Prevent Removal** | Can't remove item from queue if actively reading | Checked in update_reading_queue |
| **Achievement Tracking** | Track when goals are achieved | date_achieved set on completion |
| **Current Year Focus** | get_item_in_active_queue filters current year | In ReadingManager |

---

## 7. User Workflows

### 7.1 Start Reading an Item

**Flow:**
1. User selects item from library
2. User creates reading session via `createReading` mutation
3. System validates:
   - No active reading exists for item
   - Start date is valid
4. System creates ReadingModel:
   - Sets number based on reading history
   - Sets status based on finish_date
   - Sets owner_id to user
5. System auto-adds item to reading queue if needed
6. Returns confirmation with reading_id

**Error Scenarios:**
- Active reading already exists → 412 PRECONDITION_FAILED
- Start date before previous finish → 412 PRECONDITION_FAILED

---

### 7.2 Track Reading Progress

**Flow:**
1. User records progress via `createReadingProgress` mutation
2. System validates:
   - Reading exists and belongs to user
   - Progress date valid (not before last entry)
   - Value valid (page/percentage within bounds)
   - Value > last entry value (monotonic)
3. System checks if duplicate day:
   - If YES: Updates existing entry (page, percentage, rate, comment)
   - If NO: Creates new ReadingProgressModel
4. System auto-calculates missing metric:
   - If page given: Calculate percentage = (page/totalPages)*100
   - If percentage given: Calculate page = (percentage/100)*totalPages
5. System checks completion:
   - If percentage==100 or page==totalPages: Auto-completes reading
6. Returns confirmation with progress_id

**Error Scenarios:**
- Reading not found → 404
- Progress date before last → 428 PRECONDITION_REQUIRED
- Value less than last → 428 PRECONDITION_REQUIRED  
- Page exceeds total → 428 PRECONDITION_REQUIRED
- Invalid percentage range → Validation error
- Invalid page (negative) → Validation error

---

### 7.3 Manage Reading Queue/Goals

**Flow:**
1. User adds item to reading queue via `updateReadingQueue` mutation
2. System checks current queue status:
   - **Not in queue**: Creates new ReadingQueueModel, returns created=true
   - **Already active**: 
     - If achieved: Raise 412 error
     - If has active reading: Raise 412 error
     - Otherwise: Deactivate (active=false), returns created=false
3. System auto-sets year to current year if not provided
4. Returns queue status and item details

---

### 7.4 Complete or Drop a Reading

**Flow:**
1. User calls `updateReadingStatus` mutation with new_status
2. System identifies reading (via reading_id or item_id)
3. System updates based on new_status:
   - **reading**: Sets active=true, finish_date=null, status_id="reading"
   - **completed**: Sets active=false, finish_date=today, status_id="read"
   - **dropped**: Sets active=false, finish_date=today, status_id="dropped"
4. If status→completed:
   - System finds reading queue goal for item
   - If goal exists: Sets achieved=true, date_achieved=now
5. Returns confirmation with new status

---

### 7.5 View Reading Statistics

**Flow:**
1. User requests statistics via `getReadingStats` query with item_id
2. System queries:
   - All readings for item (ordered by start_date desc)
   - Active reading for item (if exists)
   - Latest progress for active reading (if exists)
3. System compiles stats object:
   - readings_count: Total readings
   - last_reading_date: Newest reading start_date
   - is_currently_reading: active reading exists?
   - current_reading_id: Active reading UUID
   - current_page/percentage: From latest progress
   - last_readings: List of all readings
4. Returns comprehensive stats object

---

## 8. Error Handling

### HTTP Status Codes

| Code | Scenario | Message Example |
|------|----------|-----------------|
| 400 | Invalid request/validation | "percentage must be between 1 and 100" |
| 404 | Resource not found | "Reading not found", "Item not found" |
| 412 | Precondition failed | "Active reading already exists", "Item has active reading" |
| 428 | Precondition required | "Progress date cannot be older than last entry" |

### Validation Rules

**CreateReadingRequest:**
- item_id: Required, positive integer
- start_date: Optional (defaults to today)
- finish_date: Optional, if provided must be >= start_date
- is_dropped: Optional boolean

**CreateProgressRequestV2:**
- reading_id: Required UUID
- progress_type: Required (page or percentage)
- value: Required
  - If "percentage": 1 ≤ value ≤ 100
  - If "page": value ≥ 0
- progress_date: Required
- rate: Optional (1-5 typically)
- comment: Optional string

**UpdateReadingStatusRequest:**
- Either reading_id OR item_id (not both)
- new_status: Required (reading, completed, dropped)

---

## 9. Technical Architecture

### 9.1 Layer Architecture

```
┌─────────────────────────────────────┐
│   GraphQL / REST Endpoints          │
│   (Resolvers & Routers)             │
├─────────────────────────────────────┤
│   Service Layer                     │
│   (ReadingService)                  │
│   - Business Logic                  │
│   - Validation                      │
│   - Orchestration                   │
├─────────────────────────────────────┤
│   Manager Layer                     │
│   (ReadingManager)                  │
│   - Database CRUD                   │
│   - Query building                  │
├─────────────────────────────────────┤
│   Model/Schema Layer                │
│   - SQLAlchemy Models               │
│   - Pydantic Schemas                │
├─────────────────────────────────────┤
│   Data Layer                        │
│   - SQLAlchemy AsyncSession         │
│   - PostgreSQL Database             │
└─────────────────────────────────────┘
```

### 9.2 Key Classes

**ReadingService** (`services/reading.py`)
- `create_reading()` - Create new reading session
- `get_readings()` - Query readings with filters
- `get_reading_by_id()` - Single reading lookup
- `get_active_readings()` - Active readings for user
- `create_progress_v2()` - Create progress entry
- `get_progress()` - Progress list for reading
- `update_reading_status()` - Change reading status
- `update_reading_queue()` - Manage queue goals
- `get_reading_queue()` - Query queue/goals
- `get_reading_stats()` - Statistics for item
- `_finish_reading()` - Internal completion logic
- `_set_values()` - Progress value conversion

**ReadingManager** (`managers/reading.py`)
- `create_reading()` - Save reading
- `update_reading()` - Update reading fields
- `get_reading_by_id()` - Fetch reading
- `get_readings()` - Batch query with joins
- `get_item_last_readings()` - History for item
- `get_all_active_readings()` - User's active readings
- `get_item_active_reading()` - Current reading for item
- `create_progress()` - Save progress
- `update_progress()` - Update progress
- `get_progress()` - Fetch progress list
- `get_latest_progress()` - Most recent entry
- `add_reading_queue()` - Create queue entry
- `get_reading_queue()` - Query queue with filters
- `get_item_in_active_queue()` - Current goal for item
- `update_item_status_in_queue()` - Update goal status

**Resolvers** (`resolvers/reading.py`)
- GraphQL query/mutation bindings
- Input validation via decorators
- Service delegation

### 9.3 Database Schema

**reading table**
```sql
CREATE TABLE reading (
  id UUID PRIMARY KEY,
  owner_id UUID NOT NULL,
  item_id INT NOT NULL FOREIGN KEY,
  start_date DATE NOT NULL,
  finish_date DATE,
  number INT DEFAULT 1,
  status_id VARCHAR FOREIGN KEY,
  active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

**reading_progress table**
```sql
CREATE TABLE reading_progress (
  id UUID PRIMARY KEY,
  reading_id UUID NOT NULL FOREIGN KEY,
  item_id INT NOT NULL FOREIGN KEY,
  progress_date DATE NOT NULL,
  page INT,
  percentage FLOAT,
  rate INT,
  comment TEXT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  UNIQUE(reading_id, progress_date)
)
```

**reading_queue table**
```sql
CREATE TABLE reading_queue (
  id UUID PRIMARY KEY,
  owner_id UUID NOT NULL,
  item_id INT NOT NULL FOREIGN KEY,
  achieved BOOLEAN DEFAULT FALSE,
  date_achieved DATETIME,
  year INT NOT NULL,
  active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

---

## 10. API Response Examples

### Example: Create Reading
**Request:**
```json
{
  "itemId": 1,
  "startDate": "2026-05-20",
  "finishDate": null,
  "isDropped": false
}
```

**Response (200):**
```json
{
  "created": true,
  "readingId": "550e8400-e29b-41d4-a716-446655440000",
  "itemTitle": "The Great Gatsby"
}
```

---

### Example: Create Progress Entry
**Request:**
```json
{
  "readingId": "550e8400-e29b-41d4-a716-446655440000",
  "progressType": "page",
  "value": 145,
  "progressDate": "2026-05-20",
  "rate": 4,
  "comment": "Excellent pacing so far"
}
```

**Response (200):**
```json
{
  "created": true,
  "itemTitle": "The Great Gatsby",
  "readingProgressId": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

---

### Example: Get Reading Stats
**Request:**
```json
{
  "itemId": 1
}
```

**Response (200):**
```json
{
  "stats": {
    "readingsCount": 2,
    "lastReadingDate": "2026-05-20",
    "isCurrentlyReading": true,
    "currentReadingId": "550e8400-e29b-41d4-a716-446655440000",
    "currentPage": 145,
    "currentPercentage": 48.5,
    "lastReadings": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "itemId": 1,
        "startDate": "2026-05-15",
        "finishDate": null,
        "number": 1,
        "active": true,
        "statusId": "reading",
        "statusName": "Reading"
      },
      {
        "id": "650e8400-e29b-41d4-a716-446655440001",
        "itemId": 1,
        "startDate": "2025-03-10",
        "finishDate": "2025-04-05",
        "number": 0,
        "active": false,
        "statusId": "read",
        "statusName": "Read"
      }
    ]
  }
}
```

---

## 11. Future Enhancements

Potential features for future iterations:

1. **Social Features**
   - Share reading progress with friends
   - See friends' reading activities
   - Collaborative reading clubs

2. **Advanced Analytics**
   - Reading speed calculation (pages/day)
   - Monthly/yearly reading summaries
   - Genre-based statistics
   - Longest active reading streak

3. **Recommendations**
   - Suggest next book based on history
   - Similar book recommendations
   - Reading difficulty progression

4. **Reading Modes**
   - Audiobook progress tracking
   - E-reader integration
   - Physical vs digital tracking

5. **Notifications**
   - Reading reminders
   - Goal completion notifications
   - Friend activity alerts

6. **Advanced Goals**
   - Pages read per month targets
   - Genre diversity goals
   - Author exploration challenges

---

## 12. Appendix: API Summary Table

| Operation | Endpoint | Method | Purpose |
|-----------|----------|--------|---------|
| getReading | GraphQL | Query | Get single reading by ID |
| getReadings | GraphQL | Query | Get filtered readings |
| getActiveReadings | GraphQL | Query | Get user's active readings |
| getReadingProgress | GraphQL | Query | Get progress entries |
| getReadingStats | GraphQL | Query | Get reading statistics |
| getReadingQueue | GraphQL | Query | Get reading goals/queue |
| createReading | GraphQL | Mutation | Start new reading |
| createReadingProgress | GraphQL | Mutation | Record progress |
| updateReadingQueue | GraphQL | Mutation | Add/remove from queue |
| updateReadingStatus | GraphQL | Mutation | Change reading status |
| GET /reading/active | REST | GET | Get active readings |

---

**Document End**
