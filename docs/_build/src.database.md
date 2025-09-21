# src.database package

## Submodules

## src.database.models module

### *class* src.database.models.Base(\*\*kwargs: Any)

Bases: `DeclarativeBase`

#### metadata *: ClassVar[MetaData]* *= MetaData()*

Refers to the `_schema.MetaData` collection that will be used
for new `_schema.Table` objects.

#### SEE ALSO

orm_declarative_metadata

#### registry *: ClassVar[\_RegistryType]* *= <sqlalchemy.orm.decl_api.registry object>*

Refers to the `_orm.registry` in use where new
`_orm.Mapper` objects will be associated.

### *class* src.database.models.Contact(\*\*kwargs)

Bases: [`Base`](#src.database.models.Base)

#### birthday *: Mapped[date]*

#### created_at *: Mapped[datetime]*

#### email *: Mapped[str]*

#### first_name *: Mapped[str]*

#### id *: Mapped[int]*

#### last_name *: Mapped[str]*

#### phone *: Mapped[str]*

#### to_dict() → dict

#### updated_at *: Mapped[datetime]*

#### user *: Mapped[[User](#src.database.models.User)]*

#### user_id *: Mapped[int]*

### *class* src.database.models.User(\*\*kwargs)

Bases: [`Base`](#src.database.models.Base)

#### avatar *: Mapped[str]*

#### contacts *: Mapped[list[[Contact](#src.database.models.Contact)]]*

#### created_at *: Mapped[datetime]*

#### email *: Mapped[str]*

#### id *: Mapped[int]*

#### is_confirmed *: Mapped[bool]*

#### password *: Mapped[str]*

#### role *: Mapped[str]*

#### to_dict() → dict

#### updated_at *: Mapped[datetime]*

#### username *: Mapped[str]*

## src.database.role module

### *class* src.database.role.Role(\*values)

Bases: `str`, `Enum`

#### ADMIN *= 'admin'*

#### USER *= 'user'*

## src.database.session_manager module

### *class* src.database.session_manager.DatabaseSessionManager(url: str)

Bases: `object`

#### session()

### *async* src.database.session_manager.get_db() → AsyncGenerator[AsyncSession, None]

### src.database.session_manager.get_session_manager() → [DatabaseSessionManager](#src.database.session_manager.DatabaseSessionManager)

## Module contents
