from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import UserCreate
from src.database.models import User
from src.repository.users import UserRepository
from src.services.crypt import crypt


class UserService:
    """Service for managing users."""

    def __init__(self, db: AsyncSession):
        """Initializes the user service.

        Args:
            db (AsyncSession): The database session.
        """
        self.repository = UserRepository(db)

    async def create(self, payload: UserCreate) -> User:
        """Creates a new user.

        Args:
            payload (UserCreate): The user data.

        Returns:
            User: The created user.
        """
        return await self.repository.create(payload)

    async def get_by_id(self, user_id: int) -> User:
        """Gets a user by ID.

        Args:
            user_id (int): The user ID.

        Returns:
            User: The user.
        """
        return await self.repository.get_by_id(user_id)

    async def get_by_username(self, username: str) -> User:
        """Gets a user by username.

        Args:
            username (str): The username.

        Returns:
            User: The user.
        """
        return await self.repository.get_by_username(username)

    async def get_by_email(self, email: str) -> User:
        """Gets a user by email.

        Args:
            email (str): The email.

        Returns:
            User: The user.
        """
        return await self.repository.get_by_email(email)

    async def confirm_email(self, email: str) -> User:
        """Confirms a user's email address.

        Args:
            email (str): The email to confirm.

        Returns:
            User: The confirmed user.
        """
        user = await self.get_by_email(email)
        if not user.is_confirmed:
            user.is_confirmed = True
            await self.repository.save(user)
        return user

    async def update_field(self, user: User, field: str, value: str) -> User:
        """Updates a specific field for a user.

        Args:
            user (User): The user to update.
            field (str): The field to update.
            value (str): The new value.

        Returns:
            User: The updated user.
        """
        setattr(user, field, value)
        user = await self.repository.save(user)
        return user

    async def update_password(self, email: str, new_password: str) -> None:
        """Updates a user's password.

        Args:
            email (str): The user's email.
            new_password (str): The new password.
        """
        user = await self.get_by_email(email)
        user.password = crypt.hash(new_password)
        await self.repository.save(user)
