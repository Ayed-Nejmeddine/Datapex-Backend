"""Here find all user data for tests."""
import json

USER = json.dumps(
    {
        "username": "chiraz11",
        "email": "chiraz11@example.com",
        "password1": "test-1235&",
        "password2": "test-1235&",
        "firstName": "chiraz",
        "lastName": "belaalia",
        "profile": {
            "phone": "+21640083429",
            "postalCode": 2034,
            "country": "TN",
            "city": "Dubai",
            "company": "Clevertech",
            "occupation": "ttt",
            "language": "fr",
            "email_is_verified": True,
            "phone_is_verified": True,
        },
    }
)
