# src.repository package

## Submodules

## src.repository.contacts module

### *class* src.repository.contacts.ContactRepository(session: AsyncSession)

Bases: `object`

Repository for managing contacts.

####
*async* create(payload: [ContactCreate](src.api.md#src.api.schemas.ContactCreate), user_id: int) → [Contact](src.database.md#src.database.models.Contact)

Creates a new contact.

* **Parameters:**
    * **payload** ([*ContactCreate*](src.api.md#src.api.schemas.ContactCreate)) – The contact data.
    * **user_id** (*int*) – The user ID.
* **Returns:**
  The created contact.
* **Return type:**
  [Contact](src.database.md#src.database.models.Contact)

#### *async* delete(contact_id: int) → None

Deletes a contact.

* **Parameters:**
  **contact_id** (*int*) – The contact ID.

#### *async* get(contact_id: int) → [Contact](src.database.md#src.database.models.Contact)

Gets a contact by ID.

* **Parameters:**
  **contact_id** (*int*) – The contact ID.
* **Returns:**
  The contact.
* **Return type:**
  [Contact](src.database.md#src.database.models.Contact)

####
*async* get_list(user_id: int, skip: int | None = None, limit: int = 100, first_name: str | None = None, last_name: str | None = None, email: str | None = None) → Sequence[[Contact](src.database.md#src.database.models.Contact)]

Gets a list of contacts for a user.

* **Parameters:**
    * **user_id** (*int*) – The user ID.
    * **skip** (*int* *|* *None* *,* *optional*) – The number of contacts to skip. Defaults to None.
    * **limit** (*int* *,* *optional*) – The maximum number of contacts to return. Defaults to 100.
    * **first_name** (*str* *|* *None* *,* *optional*) – The first name to filter by. Defaults to None.
    * **last_name** (*str* *|* *None* *,* *optional*) – The last name to filter by. Defaults to None.
    * **email** (*str* *|* *None* *,* *optional*) – The email to filter by. Defaults to None.
* **Returns:**
  The list of contacts.
* **Return type:**
  Sequence[[Contact](src.database.md#src.database.models.Contact)]

####
*async* replace(contact_id: int, payload: [ContactUpdate](src.api.md#src.api.schemas.ContactUpdate)) → [Contact](src.database.md#src.database.models.Contact)

Replaces a contact.

* **Parameters:**
    * **contact_id** (*int*) – The contact ID.
    * **payload** ([*ContactUpdate*](src.api.md#src.api.schemas.ContactUpdate)) – The new contact data.
* **Returns:**
  The replaced contact.
* **Return type:**
  [Contact](src.database.md#src.database.models.Contact)

## src.repository.users module

### *class* src.repository.users.UserRepository(db: AsyncSession)

Bases: `object`

Repository for managing users.

####
*async* create(payload: [UserCreate](src.api.md#src.api.schemas.UserCreate)) → [User](src.database.md#src.database.models.User)

Creates a new user.

* **Parameters:**
  **payload** ([*UserCreate*](src.api.md#src.api.schemas.UserCreate)) – The user data.
* **Returns:**
  The created user.
* **Return type:**
  [User](src.database.md#src.database.models.User)

#### *async* get_by_email(email: str) → [User](src.database.md#src.database.models.User)

Gets a user by email.

* **Parameters:**
  **email** (*str*) – The email.
* **Returns:**
  The user.
* **Return type:**
  [User](src.database.md#src.database.models.User)

#### *async* get_by_id(user_id: int) → [User](src.database.md#src.database.models.User)

Gets a user by ID.

* **Parameters:**
  **user_id** (*int*) – The user ID.
* **Returns:**
  The user.
* **Return type:**
  [User](src.database.md#src.database.models.User)

#### *async* get_by_username(username: str) → [User](src.database.md#src.database.models.User)

Gets a user by username.

* **Parameters:**
  **username** (*str*) – The username.
* **Returns:**
  The user.
* **Return type:**
  [User](src.database.md#src.database.models.User)

####
*async* save(user: [User](src.database.md#src.database.models.User)) → [User](src.database.md#src.database.models.User)

Saves a user.

* **Parameters:**
  **user** ([*User*](src.database.md#src.database.models.User)) – The user to save.
* **Returns:**
  The saved user.
* **Return type:**
  [User](src.database.md#src.database.models.User)

## Module contents
