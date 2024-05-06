from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Проверяет, совпадает ли указанный пароль с хэшированным паролем.

        :param plain_password: Нехэшированный пароль, введенный пользователем.
        :param hashed_password: Хэшированный пароль, сохраненный в базе данных.
        :return: True, если пароль верный, иначе False.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Получает хэш для указанного пароля.

        :param password: Пароль, который нужно захэшировать.
        :return: Хэшированный пароль.
        """
        return pwd_context.hash(password)
