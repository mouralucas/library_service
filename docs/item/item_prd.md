# Item Management System - Product Requirements Document

**Document Version:** 1.0  
**Last Updated:** May 20, 2026  
**Status:** Implementation Complete (Based on Current Service)

---

## 1. Executive Summary

The Item Management System is a comprehensive feature for managing library items (books, articles, etc.) with rich metadata, relationships to authors, publishers, collections, and series. It provides detailed item cataloging, status tracking, location management, and integration with reading activities. Users can create, search, filter, and organize items in their personal library with support for tracking reading history and goals through linked reading sessions.

---

## 2. Product Vision & Goals

### Vision
Enable users to build and maintain a comprehensive, well-organized digital library with detailed metadata, meaningful relationships, and seamless integration with reading tracking and goal management.

### Key Goals
1. **Rich Item Cataloging**: Store detailed information about books, articles, and other written materials
2. **Metadata Management**: Track ISBN, publication dates, pages, pricing, and other key attributes
3. **Relationship Management**: Link items to authors, publishers, collections, and series
4. **Status Tracking**: Monitor item acquisition and reading status over time
5. **Location Management**: Track physical storage locations of items
6. **Integrated Reading Tracking**: Connect items with reading sessions and goals
7. **Search & Discovery**: Enable flexible filtering, sorting, and searching across the library

---

## 3. Core Features

### 3.1 Item Creation & Management
Create and manage library items with comprehensive metadata.

**Key Capabilities:**
- Create new library items with detailed metadata
- Update item information (partial updates supported)
- Track item ownership (multi-user support)
- Auto-generate or import item metadata
- Support multiple item formats (physical books, e-books, audiobooks, articles)
- Store cover images and summaries
- Track pricing information (cover price vs. actual paid price)

### 3.2 Author & Relationship Management
Manage author relationships with items.

**Key Capabilities:**
- Define main author for each item
- Add multiple co-authors to items
- Track author roles (author, translator)
- Link items to publishers
- Link items to book series
- Link items to collections
- Automatic author/publisher relationship creation

### 3.3 Status Tracking
Track and manage item status history.

**Key Capabilities:**
- Current item status (e.g., unread, reading, read, dropped)
- Status history with dates for each state change
- Last status and change date tracking
- Automatic status history entries on status changes
- Status-based item filtering

### 3.4 Location Management
Track physical storage locations of items.

**Key Capabilities:**
- Define item storage locations
- Store physical location details
- Organize items by location
- Query items by single or multiple locations
- Add location descriptions and notes

### 3.5 Item Discovery & Search
Comprehensive search and filtering capabilities.

**Key Capabilities:**
- Filter by title, author, status, type, collection, series
- Advanced summary view with reading goal/progress integration
- Detailed item view with all metadata
- Sorting by various fields (ascending/descending)
- Batch operations on item lists

### 3.6 Reading Integration
Seamless integration with reading tracking system.

**Key Capabilities:**
- Track if item has active reading goal
- Display current/last reading information
- Show latest reading progress (page/percentage)
- Include reading queue status in item view
- Auto-add items to queue on reading creation

---

## 4. Data Models & Entities

### 4.1 Item Model

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | int | Unique identifier | Primary Key, Auto-increment |
| owner_id | UUID | Item owner/user | Required, User isolation |
| title | str | Item title | Required, Indexed |
| subtitle | str | Item subtitle | Optional, Nullable |
| isbn | str | ISBN number | Optional, Nullable, Unique per owner |
| pages | int | Total pages | Default=0 |
| publication_date | date | Publication date | Optional, Nullable |
| original_publication_date | date | Original publication date | Optional, Nullable |
| edition | int | Edition number | Default=1 |
| volume | int | Volume number | Default=1 |
| serie_id | int | Associated series | Foreign Key to Serie, Nullable |
| language_id | str | Item language | Foreign Key to Language, Nullable |
| publisher_id | int | Publisher | Foreign Key to Publisher, Nullable |
| main_author_id | int | Primary author | Foreign Key to Author, Required |
| collection_id | int | Associated collection | Foreign Key to Collection, Required |
| format_id | str | Format (hardcover, paperback, ebook, etc) | Optional, Nullable |
| item_type_id | str | Type (book, article, etc) | Optional, Nullable |
| last_status_id | str | Current status | Foreign Key to Status, Required |
| last_status_date | date | Status change date | Optional, Nullable |
| cover_price | float | Original price | Default=0 |
| paid_price | float | Actual purchase price | Default=0 |
| summary | str | Item description/summary | Optional, Nullable, Long text |
| observation | str | Additional notes | Optional, Nullable, Long text |
| origin | str | Data source | Default="SYSTEM" |
| cover | str | Cover image URL | Optional, Nullable |
| location_id | UUID | Physical storage location | Foreign Key to ItemLocation, Nullable |
| created_at | datetime | Creation timestamp | Auto-set |
| updated_at | datetime | Last update timestamp | Auto-set |

**Relationships:**
- main_author: One-to-One with Author (eager loaded)
- serie: One-to-One with Serie (lazy loaded)
- language: One-to-One with Language (lazy loaded)
- publisher: One-to-One with Publisher (lazy loaded)
- collection: One-to-One with Collection (eager loaded)
- last_status: One-to-One with Status (eager loaded)
- authors: Many-to-Many with Author via ItemAuthor (lazy loaded)
- status: Many-to-Many with Status via ItemStatus (lazy loaded)

---

### 4.2 ItemAuthor Model (Many-to-Many Junction)

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | UUID | Unique identifier | Primary Key, Auto-generated |
| item_id | int | Associated item | Foreign Key to Item, Required |
| author_id | int | Associated author | Foreign Key to Author, Required |
| is_main | bool | Main author flag | Default=true |
| is_translator | bool | Translator flag | Default=false |

**Relationships:**
- item: Many-to-One with Item (eager loaded)
- author: Many-to-One with Author (eager loaded)

---

### 4.3 ItemStatus Model (Status History)

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | UUID | Unique identifier | Primary Key, Auto-generated |
| item_id | int | Associated item | Foreign Key to Item, Required |
| status_id | str | Status at this point | Foreign Key to Status, Required |
| date | date | Status change date | Required |

**Relationships:**
- item: Many-to-One with Item (eager loaded)
- status: Many-to-One with Status (eager loaded)

---

### 4.4 ItemLocation Model

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | int | Unique identifier | Primary Key, Auto-increment |
| name | str | Location name | Required (e.g., "Living Room", "Office Shelf") |
| physical_location | str | Physical address/description | Required (e.g., "Apartment 4B, Bookshelf 1") |
| description | str | Additional details | Optional, Nullable |

---

## 5. API Specification

### 5.1 GraphQL Queries

#### Query: getDetailedItems
Retrieve detailed information about items with comprehensive filtering.

```graphql
query {
  getDetailedItems(params: {
    itemId: 1
    title: "Great Gatsby"
    mainAuthorId: 5
    itemTypeId: "BOOK"
    statusId: "unread"
    orderBy: [{field: "title", direction: "ASC"}]
  }) {
    quantity
    items { ... }
  }
}
```

**Parameters:**
- `params.itemId` (int, optional): Filter by specific item
- `params.title` (str, optional): Filter by title
- `params.mainAuthorId` (int, optional): Filter by main author
- `params.itemTypeId` (str, optional): Filter by item type
- `params.statusId` (str, optional): Filter by current status
- `params.orderBy` (List[OrderBy], optional): Sorting criteria

**Returns:**
```typescript
{
  quantity: int,
  items: ItemSchema[]
}
```

**Fields in ItemSchema:**
- id, owner_id, title, subtitle, isbn, pages
- publication_date, original_publication_date
- serie_id, serie_name, language_id, volume
- publisher_id, publisher_name, main_author_id, main_author_name
- collection_id, collection_name, format_id, item_type_id
- last_status_id, last_status_name, last_status_date
- cover_price, paid_price, cover, summary, observation
- authors_ids, authors_names
- is_in_reading_queue (boolean)

---

#### Query: getItemSummary
Get a summary view of items with integrated reading goal/progress data.

```graphql
query {
  getItemSummary(params: {
    id: 1
    itemTypeId: "BOOK"
    activeGoal: true
    activeReading: false
    orderBy: [{field: "title", direction: "ASC"}]
  }) {
    quantity
    summary { ... }
  }
}
```

**Parameters:**
- `params.id` (int, optional): Filter by item ID
- `params.itemTypeId` (str, optional): Filter by item type
- `params.activeGoal` (bool, default=false): Only items with active reading goals
- `params.activeReading` (bool, default=false): Only items with active readings
- `params.orderBy` (List[OrderBy], optional): Sorting criteria

**Returns:**
```typescript
{
  quantity: int,
  summary: Array<{
    id: int,
    title: string,
    cover: string,
    mainAuthorId: int,
    mainAuthorName: string,
    readingGoalId: UUID | null,
    readingGoalYear: int | null,
    readingGoalAchieved: bool | null,
    readingId: UUID | null,
    readingStartDate: date | null,
    lastPage: int | null,
    lastPercentage: float | null
  }>
}
```

**Use Case:** Dashboard view showing items with reading context at a glance.

---

#### Query: getItem
Retrieve a single item by ID.

```graphql
query {
  getItem(id: 1) {
    item { ... }
  }
}
```

**Parameters:**
- `id` (int, required): Item ID

**Returns:**
```typescript
{
  item: ItemSchema
}
```

**Error Cases:**
- 404 NOT FOUND: Item not found

---

#### Query: getItemLocations
Get all available item storage locations.

```graphql
query {
  getItemLocations {
    quantity
    locations { ... }
  }
}
```

**Returns:**
```typescript
{
  quantity: int,
  locations: ItemLocationSchema[]
}
```

**Fields:**
- id, name, physical_location, description

---

#### Query: getItemsByLocation
Get items organized by storage location.

```graphql
query {
  getItemsByLocation(params: {
    locationIds: [1, 2, 3]
  }) {
    # Returns grouped results
  }
}
```

**Parameters:**
- `params.locationIds` (List[int], optional): Filter by location IDs

**Returns:**
```typescript
Array<{
  locationId: int,
  locationName: string,
  items: ItemSchema[]
}>
```

---

### 5.2 GraphQL Mutations

#### Mutation: createItem
Create a new library item.

```graphql
mutation {
  createItem(item: {
    title: "The Great Gatsby"
    subtitle: "A Novel of the Jazz Age"
    mainAuthorId: 5
    authorsIds: [6, 7]
    publisherId: 3
    collectionId: 1
    serieId: null
    itemTypeId: "BOOK"
    isbn: "978-0-7432-7356-5"
    pages: 180
    volume: 1
    publicationDate: "1925-04-10"
    originalPublicationDate: "1925-04-10"
    languageId: "en"
    formatId: "HARDCOVER"
    coverPrice: 29.99
    paidPrice: 15.50
    summary: "..."
    observation: "First edition"
    lastStatusId: "unread"
    lastStatusDate: "2026-05-20"
    cover: "https://..."
    locationId: 1
  }) {
    created
    id
    title
  }
}
```

**Parameters:**
- `item.title` (str, required): Item title
- `item.mainAuthorId` (int, required): Primary author
- `item.authorsIds` (List[int], optional): Co-authors
- `item.collectionId` (int, required): Collection
- `item.lastStatusId` (str, required): Initial status
- `item.lastStatusDate` (date, required): Status date
- `item.locationId` (int, required): Storage location
- Other metadata fields: subtitle, isbn, pages, publication_date, etc.

**Returns:**
```typescript
{
  created: boolean,
  id: int,
  title: string
}
```

**Business Logic:**
- Sets owner_id to authenticated user
- Creates ItemAuthorModel entries for main and co-authors
- Creates initial ItemStatusModel entry
- Auto-adds to default collection if needed
- Validates required fields

**Error Cases:**
- 400 BAD REQUEST: Missing required fields
- 404 NOT FOUND: Referenced author/publisher/collection not found

---

#### Mutation: updateItem
Update an existing library item.

```graphql
mutation {
  updateItem(item: {
    id: 1
    title: "Updated Title"
    pages: 185
    lastStatusId: "reading"
    lastStatusDate: "2026-05-20"
    locationId: 2
  }) {
    created
    id
    title
  }
}
```

**Parameters:**
- `item.id` (int, required): Item to update
- All other fields optional (partial update)
- `item.authorsIds` (List[int], optional): Update co-authors (TODO: not yet implemented)

**Returns:**
```typescript
{
  created: boolean,
  id: int,
  title: string
}
```

**Business Logic:**
- Only updates specified fields (exclude_unset=True)
- If last_status_id changes: Creates new ItemStatusModel entry
- If status_id updated but no date provided: Uses current date
- Maintains author relationships (update not yet fully implemented)
- User-isolated: Only users can update their own items

**Error Cases:**
- 404 NOT FOUND: Item not found
- 400 BAD REQUEST: Invalid field values

---

### 5.3 REST Endpoints

#### PATCH /item
Update a single item via REST.

**URL:** `PATCH /api/item`

**Authentication:** Required (Bearer token)

**Request Body:**
```json
{
  "id": 1,
  "title": "Updated Title",
  "pages": 185,
  "lastStatusId": "reading"
}
```

**Returns:** CreateItemResponse

**Description:** REST wrapper for updateItem mutation. Useful for client applications preferring REST over GraphQL.

---

## 6. Business Logic & Rules

### 6.1 Item Creation Rules

| Rule | Description | Implementation |
|------|-------------|-----------------|
| **User Ownership** | All items belong to authenticated user | Set in create_item |
| **Required Metadata** | Title, author, collection, status required | Enforced in schema |
| **Auto Author Linking** | Main + co-authors linked via ItemAuthor | In __add_author |
| **Status History Init** | Initial status creates history entry | In __update_status |
| **Default Values** | Pages=0, Edition=1, Volume=1, Origin="SYSTEM" | In model |
| **Cover Image** | Default cover if not provided | Default in schema |

### 6.2 Item Update Rules

| Rule | Description | Implementation |
|------|-------------|-----------------|
| **Partial Updates** | Only specified fields updated | exclude_unset=True |
| **Status Change Tracking** | Status change creates history entry | In __update_status |
| **Date Auto-set** | Status date defaults to today if not provided | Can be added in service |
| **Validation** | All updates validate data types/ranges | Pydantic validation |
| **User Isolation** | Users only update their own items | Query filter by owner_id |

### 6.3 Item Retrieval Rules

| Rule | Description | Implementation |
|------|-------------|-----------------|
| **Detailed View** | Includes all relationships + derived fields | get_detailed_items |
| **Summary View** | Lightweight with reading context | get_item_summary |
| **Reading Integration** | Auto-includes reading queue status | Subquery in get_detailed_items |
| **Author Aggregation** | Collects all authors with names | array_agg in query |
| **Eager Loading** | Key relationships loaded immediately | joinedload options |

---

## 7. User Workflows

### 7.1 Add Item to Library

**Flow:**
1. User provides item metadata via `createItem` mutation
2. System validates:
   - Required fields present (title, author, collection, status)
   - Author exists in database
   - Collection exists
   - Status is valid
3. System creates ItemModel:
   - Sets owner_id to user
   - Sets provided metadata
   - Sets initial timestamps
4. System creates ItemAuthorModel entries:
   - Main author (is_main=true)
   - Co-authors (is_main=false)
5. System creates initial ItemStatusModel:
   - Links initial status_id
   - Sets date to today or provided date
6. System auto-adds to reading queue if specified
7. Returns confirmation with item_id

**Error Scenarios:**
- Author not found → 404
- Collection not found → 404
- Invalid status → 400
- Duplicate ISBN (for same user) → 400

---

### 7.2 Update Item Metadata

**Flow:**
1. User provides item ID and fields to update via `updateItem` mutation
2. System fetches current item
3. System validates update:
   - Item exists and belongs to user
   - Updated fields valid
   - New relationships exist (if updating author/publisher)
4. System performs partial update:
   - Only specified fields updated
   - Timestamps auto-updated
5. System checks if status changed:
   - If YES: Creates ItemStatusModel entry with new status
   - If NO: No status history entry
6. Returns confirmation with updated item

**Error Scenarios:**
- Item not found → 404
- Invalid field values → 400
- Referenced author/publisher not found → 404

---

### 7.3 Search & Filter Items

**Flow:**
1. User queries items via `getDetailedItems` with filters
2. System builds query with filters:
   - Filters by owner_id (user isolation)
   - Applies title/author/status/type filters if provided
   - Joins author/publisher/collection/status tables
   - Includes derived fields (is_in_reading_queue, etc.)
3. System applies sorting if requested
4. System returns results with all details

**Common Scenarios:**
- Get unread books: `statusId: "unread"`
- Filter by author: `mainAuthorId: 5`
- Get items by collection: `collectionId: 1`
- Search by title: `title: "Great Gatsby"`
- Get items ready to read: `statusId: "unread", activeGoal: true`

---

### 7.4 Get Item Summary with Reading Context

**Flow:**
1. User queries items via `getItemSummary` with optional filters
2. System builds complex query with subqueries:
   - Gets current year reading goals per item
   - Gets latest reading for each item
   - Gets latest progress for latest reading
3. System applies filters (activeGoal, activeReading, etc.)
4. System returns lightweight summary with reading context:
   - Item basic info (title, cover, author)
   - Current reading goal status
   - Latest reading date and progress

**Use Case:** Dashboard displaying what to read next with progress overview

---

### 7.5 Organize Items by Location

**Flow:**
1. User queries locations via `getItemLocations`
2. User optionally queries items by location(s) via `getItemsByLocation`
3. System returns items grouped by location:
   - Location details (name, physical location, description)
   - All items in that location
4. User can use this to organize/find physical books

---

## 8. Item Status System

### Status Types (Defined in Status Model)

Common status values for items:

| Status | Meaning | Used For |
|--------|---------|----------|
| unread | Never read | New acquisitions |
| reading | Currently reading | Active reads |
| read | Completed reading | Finished reads |
| dropped | Abandoned | Items given up on |
| wanttoread | On reading list | Future reads |
| favorite | Highly rated | Special items |
| owned | Collected but not reading | Collection items |

**Status Tracking:**
- last_status_id: Current status
- last_status_date: When status changed
- ItemStatusModel history: Full audit trail of all status changes

---

## 9. Error Handling

### HTTP Status Codes

| Code | Scenario | Message Example |
|------|----------|-----------------|
| 400 | Invalid request/validation | "title is required", "invalid status_id" |
| 404 | Resource not found | "Item not found", "Author not found" |
| 403 | Permission denied | "Cannot access other user's items" |

### Validation Rules

**CreateItemRequest:**
- title: Required, string
- mainAuthorId: Required, positive integer
- collectionId: Required, positive integer
- lastStatusId: Required, valid status
- lastStatusDate: Required, date
- locationId: Required, positive integer
- authorsIds: Optional, list of integers
- isbn: Optional, string (unique per user)
- pages: Optional (default=0), positive integer
- volume: Optional (default=1), positive integer
- All date fields: Optional or required as specified

**UpdateItemRequest:**
- id: Required, positive integer
- All other fields: Optional
- When provided, fields validated with same rules as CreateItemRequest

---

## 10. Technical Architecture

### 10.1 Layer Architecture

```
┌─────────────────────────────────────┐
│   GraphQL / REST Endpoints          │
│   (Resolvers & Routers)             │
├─────────────────────────────────────┤
│   Service Layer                     │
│   (ItemService)                     │
│   - Business Logic                  │
│   - Orchestration                   │
│   - Status History Management       │
├─────────────────────────────────────┤
│   Manager Layer                     │
│   (ItemManager)                     │
│   - Database CRUD                   │
│   - Complex Query Building          │
│   - Relationship Management         │
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

### 10.2 Key Classes

**ItemService** (`services/item.py`)
- `create_item()` - Create new item with authors/status
- `update_item()` - Update item metadata
- `get_item_summary()` - Lightweight summary with reading context
- `get_detailed_items()` - Full item details with filters
- `get_item_by_id()` - Single item lookup
- `get_item_locations()` - List all locations
- `get_items_by_location()` - Items grouped by location
- `__update_status()` - Create status history entry
- `__add_author()` - Link authors to item

**ItemManager** (`managers/item.py`)
- `create_item()` - Save item
- `update_item()` - Update item fields
- `get_item_by_id()` - Fetch item
- `get_detailed_items()` - Complex query with joins
- `get_item_summary()` - Summary view with subqueries
- `get_item_status_history()` - Status audit trail
- `get_item_locations()` - Fetch locations
- `get_items_by_location()` - Query by location
- `get_items_indexed()` - Map items by ID

**Resolvers** (`resolvers/item.py`)
- GraphQL query/mutation bindings
- Input validation via decorators
- Service delegation

### 10.3 Database Schema

**item table**
```sql
CREATE TABLE item (
  id INT PRIMARY KEY AUTO_INCREMENT,
  owner_id UUID NOT NULL,
  title VARCHAR(255) NOT NULL INDEX,
  subtitle VARCHAR(255),
  isbn VARCHAR(20),
  pages INT DEFAULT 0,
  publication_date DATE,
  original_publication_date DATE,
  edition INT DEFAULT 1,
  serie_id INT FOREIGN KEY,
  language_id VARCHAR FOREIGN KEY,
  volume INT DEFAULT 1,
  publisher_id INT FOREIGN KEY,
  main_author_id INT NOT NULL FOREIGN KEY,
  collection_id INT NOT NULL FOREIGN KEY,
  format_id VARCHAR,
  type VARCHAR,
  last_status_id VARCHAR NOT NULL FOREIGN KEY,
  last_status_date DATE,
  cover_price FLOAT DEFAULT 0,
  paid_price FLOAT DEFAULT 0,
  summary TEXT,
  observation TEXT,
  origin VARCHAR DEFAULT 'SYSTEM',
  cover VARCHAR,
  location_id UUID FOREIGN KEY,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

**item_author table**
```sql
CREATE TABLE item_author (
  id UUID PRIMARY KEY,
  item_id INT NOT NULL FOREIGN KEY,
  author_id INT NOT NULL FOREIGN KEY,
  is_main BOOLEAN DEFAULT TRUE,
  is_translator BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP,
  UNIQUE(item_id, author_id)
)
```

**item_status table**
```sql
CREATE TABLE item_status (
  id UUID PRIMARY KEY,
  item_id INT NOT NULL FOREIGN KEY,
  status_id VARCHAR NOT NULL FOREIGN KEY,
  date DATE NOT NULL,
  created_at TIMESTAMP
)
```

**item_location table**
```sql
CREATE TABLE item_location (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  physical_location VARCHAR(255) NOT NULL,
  description TEXT,
  created_at TIMESTAMP
)
```

---

## 11. API Response Examples

### Example: Create Item
**Request:**
```json
{
  "title": "The Great Gatsby",
  "subtitle": "A Novel of the Jazz Age",
  "mainAuthorId": 5,
  "authorsIds": [],
  "collectionId": 1,
  "publisherId": 3,
  "itemTypeId": "BOOK",
  "isbn": "978-0-7432-7356-5",
  "pages": 180,
  "publicationDate": "1925-04-10",
  "languageId": "en",
  "formatId": "HARDCOVER",
  "coverPrice": 29.99,
  "paidPrice": 15.50,
  "lastStatusId": "unread",
  "lastStatusDate": "2026-05-20",
  "locationId": 1
}
```

**Response (200):**
```json
{
  "created": true,
  "id": 42,
  "title": "The Great Gatsby"
}
```

---

### Example: Get Detailed Items
**Request:**
```json
{
  "itemId": null,
  "title": "Great",
  "mainAuthorId": null,
  "itemTypeId": "BOOK",
  "statusId": "unread",
  "orderBy": [{"field": "title", "direction": "ASC"}]
}
```

**Response (200):**
```json
{
  "quantity": 2,
  "items": [
    {
      "id": 42,
      "ownerId": "550e8400-e29b-41d4-a716-446655440000",
      "title": "The Great Gatsby",
      "subtitle": "A Novel of the Jazz Age",
      "mainAuthorId": 5,
      "mainAuthorName": "F. Scott Fitzgerald",
      "isbn": "978-0-7432-7356-5",
      "pages": 180,
      "publicationDate": "1925-04-10",
      "serieId": null,
      "serieName": null,
      "collectionId": 1,
      "collectionName": "Classic Literature",
      "publisherId": 3,
      "publisherName": "Scribner",
      "formatId": "HARDCOVER",
      "itemTypeId": "BOOK",
      "lastStatusId": "unread",
      "lastStatusName": "Unread",
      "lastStatusDate": "2026-05-20",
      "coverPrice": 29.99,
      "paidPrice": 15.50,
      "cover": "https://...",
      "summary": "A classic American novel...",
      "authorsIds": [],
      "authorsNames": [],
      "isInReadingQueue": false
    }
  ]
}
```

---

### Example: Get Item Summary
**Request:**
```json
{
  "activeGoal": true,
  "activeReading": false
}
```

**Response (200):**
```json
{
  "quantity": 1,
  "summary": [
    {
      "id": 42,
      "title": "The Great Gatsby",
      "cover": "https://...",
      "mainAuthorId": 5,
      "mainAuthorName": "F. Scott Fitzgerald",
      "readingGoalId": "550e8400-e29b-41d4-a716-446655440001",
      "readingGoalYear": 2026,
      "readingGoalAchieved": false,
      "readingId": null,
      "readingStartDate": null,
      "lastPage": null,
      "lastPercentage": null
    }
  ]
}
```

---

### Example: Update Item
**Request:**
```json
{
  "id": 42,
  "lastStatusId": "reading",
  "lastStatusDate": "2026-05-21"
}
```

**Response (200):**
```json
{
  "created": true,
  "id": 42,
  "title": "The Great Gatsby"
}
```

---

## 12. Future Enhancements

Potential features for future iterations:

1. **Advanced Metadata**
   - ISBN validation and auto-import from APIs
   - Genre/category tagging
   - Ratings and reviews per user
   - Reading difficulty/age rating
   - Content warnings

2. **Social Features**
   - Share reading lists
   - See friends' libraries
   - Book recommendations based on reading history
   - Community ratings and discussions

3. **Inventory Management**
   - Multiple copies per item tracking
   - Lending/borrowing features
   - Item condition tracking
   - Donation/sale tracking

4. **Advanced Search**
   - Full-text search on title/summary
   - Genre/tag-based search
   - Similar item recommendations
   - Advanced filter combinations saved as views

5. **Import/Export**
   - Import from Goodreads
   - CSV/JSON import/export
   - ISBN barcode scanning
   - Batch item import

6. **Analytics**
   - Library statistics (total items, value, etc.)
   - Reading patterns and trends
   - Genre distribution
   - Cost analysis

7. **Item Relationships**
   - "Part of" relationships
   - "Sequel to" tracking
   - Related items suggestions
   - Series/collection auto-ordering

---

## 13. Appendix: API Summary Table

| Operation | Endpoint | Method | Purpose |
|-----------|----------|--------|---------|
| getDetailedItems | GraphQL | Query | Get items with full details and filters |
| getItemSummary | GraphQL | Query | Get summary view with reading context |
| getItem | GraphQL | Query | Get single item by ID |
| getItemLocations | GraphQL | Query | Get all storage locations |
| getItemsByLocation | GraphQL | Query | Get items grouped by location |
| createItem | GraphQL | Mutation | Create new item |
| updateItem | GraphQL | Mutation | Update item metadata |
| PATCH /item | REST | PATCH | Update item (REST) |

---

**Document End**
