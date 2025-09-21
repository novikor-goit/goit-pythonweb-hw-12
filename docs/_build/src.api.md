# src.api package

## Subpackages

* [src.api.routes package](src.api.routes.md)
    * [Submodules](src.api.routes.md#submodules)
    * [src.api.routes.auth module](src.api.routes.md#module-src.api.routes.auth)
        * [`confirm_email()`](src.api.routes.md#src.api.routes.auth.confirm_email)
        * [`login()`](src.api.routes.md#src.api.routes.auth.login)
        * [`password_reset()`](src.api.routes.md#src.api.routes.auth.password_reset)
        * [`refresh_token()`](src.api.routes.md#src.api.routes.auth.refresh_token)
        * [`register_user()`](src.api.routes.md#src.api.routes.auth.register_user)
        * [`request_password_reset()`](src.api.routes.md#src.api.routes.auth.request_password_reset)
    * [src.api.routes.contacts module](src.api.routes.md#module-src.api.routes.contacts)
        * [`create_contact()`](src.api.routes.md#src.api.routes.contacts.create_contact)
        * [`delete_contact()`](src.api.routes.md#src.api.routes.contacts.delete_contact)
        * [`get_contacts_list()`](src.api.routes.md#src.api.routes.contacts.get_contacts_list)
        * [`get_single_contact()`](src.api.routes.md#src.api.routes.contacts.get_single_contact)
        * [`get_upcoming_birthdays()`](src.api.routes.md#src.api.routes.contacts.get_upcoming_birthdays)
        * [`update_contact()`](src.api.routes.md#src.api.routes.contacts.update_contact)
    * [src.api.routes.users module](src.api.routes.md#module-src.api.routes.users)
        * [`me()`](src.api.routes.md#src.api.routes.users.me)
        * [`update_avatar()`](src.api.routes.md#src.api.routes.users.update_avatar)
    * [Module contents](src.api.routes.md#module-src.api.routes)

## Submodules

## src.api.exceptions module

### *exception* src.api.exceptions.NoSuchEntityException(field: str, value: int | str)

Bases: `Exception`

## src.api.schemas module

###
*class* src.api.schemas.AccessTokenResponse(, access_token: str, refresh_token: str, token_type: str = 'Bearer', expires_in: int)

Bases: `BaseModel`

#### access_token *: str*

#### expires_in *: int*

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### refresh_token *: str*

#### token_type *: str*

###
*class* src.api.schemas.ContactCreate(, first_name: Annotated[str, MaxLen(max_length=50)], last_name: Annotated[str, MaxLen(max_length=50)], email: EmailStr, phone: Annotated[str, MaxLen(max_length=20)], birthday: PastDate | None = None)

Bases: [`ContactUpdate`](#src.api.schemas.ContactUpdate)

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

###
*class* src.api.schemas.ContactModel(, id: int, first_name: Annotated[str, MaxLen(max_length=50)], last_name: Annotated[str, MaxLen(max_length=50)], email: EmailStr, phone: Annotated[str, MaxLen(max_length=20)], birthday: PastDate | None = None, created_at: datetime, updated_at: datetime)

Bases: [`ContactUpdate`](#src.api.schemas.ContactUpdate), [`PersistedEntity`](#src.api.schemas.PersistedEntity)

#### created_at *: datetime*

#### model_config *: ClassVar[ConfigDict]* *= {'from_attributes': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### updated_at *: datetime*

###
*class* src.api.schemas.ContactUpdate(, first_name: Annotated[str, MaxLen(max_length=50)], last_name: Annotated[str, MaxLen(max_length=50)], email: EmailStr, phone: Annotated[str, MaxLen(max_length=20)], birthday: PastDate | None = None)

Bases: `BaseModel`

#### birthday *: PastDate | None*

#### email *: EmailStr*

#### first_name *: str*

#### last_name *: str*

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### phone *: str*

### *class* src.api.schemas.HTTPError(, detail: str)

Bases: `BaseModel`

#### detail *: str*

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

### *class* src.api.schemas.PasswordReset(, token: str, new_password: str)

Bases: `BaseModel`

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### new_password *: str*

#### token *: str*

### *class* src.api.schemas.PasswordResetRequest(, email: EmailStr)

Bases: `BaseModel`

#### email *: EmailStr*

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

### *class* src.api.schemas.PersistedEntity(, id: int)

Bases: `BaseModel`

#### id *: int*

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

###
*class* src.api.schemas.UserCreate(, username: Annotated[str, MaxLen(max_length=50)], email: Annotated[EmailStr, MaxLen(max_length=255)], password: str)

Bases: `BaseModel`

#### email *: EmailStr*

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### password *: str*

#### username *: str*

###
*class* src.api.schemas.UserResponse(, id: int, username: str, email: EmailStr, created_at: datetime, updated_at: datetime, is_confirmed: bool, avatar: HttpUrl | None)

Bases: `BaseModel`

#### avatar *: HttpUrl | None*

#### created_at *: datetime*

#### email *: EmailStr*

#### id *: int*

#### is_confirmed *: bool*

#### model_config *: ClassVar[ConfigDict]* *= {'from_attributes': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### updated_at *: datetime*

#### username *: str*

## Module contents
