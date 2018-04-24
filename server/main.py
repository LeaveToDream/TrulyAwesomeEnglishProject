from config import config
import secrets
import getpass

config["JWT_SECRET"] = secrets.token_hex(40)

def main():

    if not config["MONGO"].get("USER"):
        config["MONGO"]["USER"] = input("MongoDB Username: ")

    if not config["MONGO"].get("PASSWORD"):
        config["MONGO"]["PASSWORD"] = getpass.getpass("MongoDB Password: ")

    import api
    return api.app


if __name__ == "__main__":

    main().run()

