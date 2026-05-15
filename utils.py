def save_credentials(username, password):

    with open(".env", "r") as file:
        lines = file.readlines()

    with open(".env", "w") as file:

        for line in lines:

            if line.startswith("PORTAL_USER="):
                file.write(f"PORTAL_USER={username}\n")

            elif line.startswith("PORTAL_PASS="):
                file.write(f"PORTAL_PASS={password}\n")

            else:
                file.write(line)