from config import config
import secrets
import getpass

config["JWT_SECRET"] = secrets.token_hex(40)

if __name__ == "__main__":

    if not config["MONGO"].get("USER"):
        config["MONGO"]["USER"] = input("MongoDB Username: ")

    if not config["MONGO"].get("PASSWORD"):
        config["MONGO"]["PASSWORD"] = getpass.getpass("MongoDB Password: ")

    import api
    api.app.run()