# src.services package

## Submodules

## src.services.auth module

###
*async* src.services.auth.get_current_user(token: str = Depends(OAuth2PasswordBearer), db: AsyncSession = Depends(get_db)) → [User](src.database.md#src.database.models.User)

Decodes the access token, retrieves the user from the database, and returns the user object.

* **Parameters:**
    * **token** (*str* *,* *optional*) – The access token. Defaults to Depends(oauth2_scheme).
    * **db** (*AsyncSession* *,* *optional*) – The database session. Defaults to Depends(get_db).
* **Raises:**
  **HTTPException** – If the token is invalid or the user is not found.
* **Returns:**
  The current user.
* **Return type:**
  [User](src.database.md#src.database.models.User)

## src.services.cache module

### *class* src.services.cache.Cache

Bases: `object`

#### *classmethod* client() → Redis

## src.services.contacts module

### *class* src.services.contacts.ContactService(db: AsyncSession)

Bases: `object`

####
*async* assert_contact_belongs_to_user(contact_id: int, user: [User](src.database.md#src.database.models.User)) → None

####
*async* create_contact(payload: [ContactCreate](src.api.md#src.api.schemas.ContactCreate), user: [User](src.database.md#src.database.models.User)) → [Contact](src.database.md#src.database.models.Contact)

#### *async* delete_contact(contact_id: int)

#### *async* get_contact(contact_id: int)

####
*async* get_contacts(user: [User](src.database.md#src.database.models.User), skip: int | None = 0, limit: int = 100, first_name: str | None = None, last_name: str | None = None, email: str | None = None) → Sequence[[Contact](src.database.md#src.database.models.Contact)]

####
*async* get_upcoming_birthdays(user: [User](src.database.md#src.database.models.User)) → Sequence[[Contact](src.database.md#src.database.models.Contact)]

#### *async* replace_contact(contact_id: int, payload: [ContactUpdate](src.api.md#src.api.schemas.ContactUpdate))

## src.services.crypt module

### *class* src.services.crypt.CryptService

Bases: `object`

#### hash(password: str) → str

#### verify(plain_password: str, hashed_password: str) → bool

### src.services.crypt.create_access_token(data: dict) → str

### src.services.crypt.create_jwt_token(data: dict, expires_delta: timedelta) → str

### src.services.crypt.create_refresh_token(data: dict) → str

### src.services.crypt.decode_jwt_token(token: str) → dict[str, Any]

## src.services.email module

###
*async* src.services.email.send_email(email: EmailStr, username: str, host: str, subject: str, template_name: str, template_body: dict)

### src.services.email.send_email_in_background(email: EmailStr, username: str, host: str, background_tasks: BackgroundTasks, subject: str, template_name: str, template_body: dict)

## src.services.media module

### *class* src.services.media.MediaStorage

Bases: `object`

#### *static* upload_file(file: UploadFile, username: str) → str

## src.services.users module

### *class* src.services.users.UserService(db: AsyncSession)

Bases: `object`

Service for managing users.

#### *async* confirm_email(email: str) → [User](src.database.md#src.database.models.User)

Confirms a user’s email address.

* **Parameters:**
  **email** (*str*) – The email to confirm.
* **Returns:**
  The confirmed user.
* **Return type:**
  [User](src.database.md#src.database.models.User)

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
*async* update_field(user: [User](src.database.md#src.database.models.User), field: str, value: str) → [User](src.database.md#src.database.models.User)

Updates a specific field for a user.

* **Parameters:**
    * **user** ([*User*](src.database.md#src.database.models.User)) – The user to update.
    * **field** (*str*) – The field to update.
    * **value** (*str*) – The new value.
* **Returns:**
  The updated user.
* **Return type:**
  [User](src.database.md#src.database.models.User)

#### *async* update_password(email: str, new_password: str) → None

Updates a user’s password.

* **Parameters:**
    * **email** (*str*) – The user’s email.
    * **new_password** (*str*) – The new password.

## Module contents
