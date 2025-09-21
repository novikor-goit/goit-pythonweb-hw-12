# src.conf package

## Submodules

## src.conf.config module

###
*class* src.conf.config.Settings(\_case_sensitive: bool | None = None, \_nested_model_default_partial_update: bool | None = None, \_env_prefix: str | None = None, \_env_file: DotenvType | None = PosixPath('.'), \_env_file_encoding: str | None = None, \_env_ignore_empty: bool | None = None, \_env_nested_delimiter: str | None = None, \_env_nested_max_split: int | None = None, \_env_parse_none_str: str | None = None, \_env_parse_enums: bool | None = None, \_cli_prog_name: str | None = None, \_cli_parse_args: bool | list[str] | tuple[str, ...] | None = None, \_cli_settings_source: CliSettingsSource[Any] | None = None, \_cli_parse_none_str: str | None = None, \_cli_hide_none_type: bool | None = None, \_cli_avoid_json: bool | None = None, \_cli_enforce_required: bool | None = None, \_cli_use_class_docs_for_groups: bool | None = None, \_cli_exit_on_error: bool | None = None, \_cli_prefix: str | None = None, \_cli_flag_prefix_char: str | None = None, \_cli_implicit_flags: bool | None = None, \_cli_ignore_unknown_args: bool | None = None, \_cli_kebab_case: bool | None = None, \_cli_shortcuts: Mapping[str, str | list[str]] | None = None, \_secrets_dir: PathType | None = None, , DB_USER: str, DB_PASSWORD: SecretStr, DB_HOST: str, DB_PORT: int, DB_NAME: str, DB_URL: str, JWT_SECRET: str, JWT_ALGORITHM: str, ACCESS_TOKEN_LIFETIME_MINUTES: int, REFRESH_TOKEN_LIFETIME_DAYS: int = 7, CRYPT_ALGORITHM: str = 'bcrypt', MAIL_USERNAME: str = '', MAIL_PASSWORD: SecretStr = SecretStr(''), MAIL_FROM: str, MAIL_PORT: int, MAIL_SERVER: str, MAIL_FROM_NAME: str = 'Test App', MAIL_STARTTLS: bool = False, MAIL_SSL_TLS: bool = False, MAIL_USE_CREDENTIALS: bool = False, MAIL_VALIDATE_CERTS: bool = False, CLOUDINARY_CLOUD_NAME: str, CLOUDINARY_API_KEY: str, CLOUDINARY_API_SECRET: SecretStr, REDIS_HOST: str = 'redis', REDIS_PORT: int = 6379)

Bases: `BaseSettings`

#### ACCESS_TOKEN_LIFETIME_MINUTES *: int*

#### CLOUDINARY_API_KEY *: str*

#### CLOUDINARY_API_SECRET *: SecretStr*

#### CLOUDINARY_CLOUD_NAME *: str*

#### CRYPT_ALGORITHM *: str*

#### DB_HOST *: str*

#### DB_NAME *: str*

#### DB_PASSWORD *: SecretStr*

#### DB_PORT *: int*

#### DB_URL *: str*

#### DB_USER *: str*

#### JWT_ALGORITHM *: str*

#### JWT_SECRET *: str*

#### MAIL_FROM *: str*

#### MAIL_FROM_NAME *: str*

#### MAIL_PASSWORD *: SecretStr*

#### MAIL_PORT *: int*

#### MAIL_SERVER *: str*

#### MAIL_SSL_TLS *: bool*

#### MAIL_STARTTLS *: bool*

#### MAIL_USERNAME *: str*

#### MAIL_USE_CREDENTIALS *: bool*

#### MAIL_VALIDATE_CERTS *: bool*

#### REDIS_HOST *: str*

#### REDIS_PORT *: int*

#### REFRESH_TOKEN_LIFETIME_DAYS *: int*

#### model_config *: ClassVar[SettingsConfigDict]* *= {'arbitrary_types_allowed': True, 'case_sensitive': False, '
cli_avoid_json': False, 'cli_enforce_required': False, 'cli_exit_on_error': True, 'cli_flag_prefix_char': '-', '
cli_hide_none_type': False, 'cli_ignore_unknown_args': False, 'cli_implicit_flags': False, 'cli_kebab_case': False, '
cli_parse_args': None, 'cli_parse_none_str': None, 'cli_prefix': '', 'cli_prog_name': None, 'cli_shortcuts': None, '
cli_use_class_docs_for_groups': False, 'enable_decoding': True, 'env_file': '.env', 'env_file_encoding': None, '
env_ignore_empty': False, 'env_nested_delimiter': None, 'env_nested_max_split': None, 'env_parse_enums': None, '
env_parse_none_str': None, 'env_prefix': '', 'extra': 'forbid', 'json_file': None, 'json_file_encoding': None, '
nested_model_default_partial_update': False, 'protected_namespaces': ('model_validate', 'model_dump', '
settings_customise_sources'), 'secrets_dir': None, 'toml_file': None, 'validate_default': True, 'yaml_config_section':
None, 'yaml_file': None, 'yaml_file_encoding': None}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

## Module contents
