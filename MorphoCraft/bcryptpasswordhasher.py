from django.contrib.auth.hashers import BCryptSHA256PasswordHasher

# Read the documentation for the hasher here
# https://docs.djangoproject.com/en/3.2/_modules/django/contrib/auth/hashers/
class BCryptPasswordHasher(BCryptSHA256PasswordHasher):
    """
    This is a modification to the original BCryptSHA256PasswordHasher

    The following changes are met:
        rounds = 13 (Minimum > 250ms computation time)
    
    The following conditions are deciding for change:
        Report number of rounds falsely to 10.
    """
    rounds = 13

    # Not to be used until further discussion
    # Falsely changing to round = 10 may cause future hash upgrading complication
    """
    def encode(self, password, salt):
        encoded_password = BCryptSHA256PasswordHasher.encode(password, salt)
        algorithm, empty, algostr, rounds, data = encoded_password.split("$", 4)
        rounds = "10" # Set as the faker
        new_encoded_password = "$".join([algorithm, empty, algostr, rounds, data])
        return new_encoded_password
    
    def decode(self, encoded):
        algorithm, empty, algostr, rounds, data = encoded.split("$", 4)
        rounds = self.rounds
        assert algorithm == self.algorithm
        return {
            "algorithm": algorithm,
            "algostr": algostr,
            "checksum": data[22:],
            "salt": data[:22],
            "work_factor": int(rounds),
        }
    
    def harden_runtime(self, password, encoded):
        _, data = encoded.split("$", 1)
        salt = data[:29]  # Length of the salt in bcrypt.
        rounds = str(self.rounds)
        # work factor is logarithmic, adding one doubles the load.
        diff = 2 ** (self.rounds - int(rounds)) - 1
        while diff > 0:
            self.encode(password, salt.encode("ascii"))
            diff -= 1
    """