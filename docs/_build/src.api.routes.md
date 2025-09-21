# src.api.routes package

## Submodules

## src.api.routes.auth module

### *async* src.api.routes.auth.confirm_email(token: str, db: AsyncSession = Depends(get_db))

###
*async* src.api.routes.auth.login(form_data: OAuth2PasswordRequestForm = Depends(NoneType), db: AsyncSession = Depends(get_db)) → [AccessTokenResponse](src.api.md#src.api.schemas.AccessTokenResponse)

###
*async* src.api.routes.auth.password_reset(data: [PasswordReset](src.api.md#src.api.schemas.PasswordReset), db: AsyncSession = Depends(get_db))

###
*async* src.api.routes.auth.refresh_token(token: str = Depends(OAuth2PasswordBearer), db: AsyncSession = Depends(get_db))

###
*async* src.api.routes.auth.register_user(data: [UserCreate](src.api.md#src.api.schemas.UserCreate), request: Request, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db))

###
*async* src.api.routes.auth.request_password_reset(data: [PasswordResetRequest](src.api.md#src.api.schemas.PasswordResetRequest), request: Request, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db))

## src.api.routes.contacts module

###
*async* src.api.routes.contacts.create_contact(payload: [ContactCreate](src.api.md#src.api.schemas.ContactCreate), db: AsyncSession = Depends(get_db), user: [User](src.database.md#src.database.models.User) = Depends(get_current_user))

###
*async* src.api.routes.contacts.delete_contact(contact_id: int, db: AsyncSession = Depends(get_db), user: [User](src.database.md#src.database.models.User) = Depends(get_current_user))

###
*async* src.api.routes.contacts.get_contacts_list(user: [User](src.database.md#src.database.models.User) = Depends(get_current_user), skip: int = 0, limit: int = 100, first_name: str | None = None, last_name: str | None = None, email: str | None = None, db: AsyncSession = Depends(get_db))

###
*async* src.api.routes.contacts.get_single_contact(contact_id: int, db: AsyncSession = Depends(get_db), user: [User](src.database.md#src.database.models.User) = Depends(get_current_user))

###
*async* src.api.routes.contacts.get_upcoming_birthdays(user: [User](src.database.md#src.database.models.User) = Depends(get_current_user), db: AsyncSession = Depends(get_db))

###
*async* src.api.routes.contacts.update_contact(body: [ContactUpdate](src.api.md#src.api.schemas.ContactUpdate), contact_id: int, db: AsyncSession = Depends(get_db), user: [User](src.database.md#src.database.models.User) = Depends(get_current_user))

## src.api.routes.users module

###
*async* src.api.routes.users.me(request: Request, user: [User](src.database.md#src.database.models.User) = Depends(get_current_user))

###
*async* src.api.routes.users.update_avatar(file: UploadFile = File(PydanticUndefined), user: [User](src.database.md#src.database.models.User) = Depends(get_current_user), db: AsyncSession = Depends(get_db))

## Module contents
