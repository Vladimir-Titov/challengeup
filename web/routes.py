from starlette.routing import Route

from web.api import challenges, user_challenges, user_contacts, users

routes = [
    # Challenges routes
    Route('/challenges', challenges.GetChallenges, methods=['GET']),
    Route('/challenges', challenges.CreateChallenge, methods=['POST']),
    Route('/challenges/{id}', challenges.GetChallengeByID, methods=['GET']),
    Route('/challenges/{id}', challenges.UpdateChallengeByID, methods=['PATCH']),
    Route('/challenges/{id}', challenges.DeleteChallengeByID, methods=['DELETE']),
    # Users routes
    Route('/users', users.GetUsers, methods=['GET']),
    Route('/users', users.CreateUser, methods=['POST']),
    Route('/users/{id}', users.GetUserByID, methods=['GET']),
    Route('/users/{id}', users.UpdateUserByID, methods=['PATCH']),
    Route('/users/{id}', users.DeleteUserByID, methods=['DELETE']),
    # User contacts routes
    Route('/user-contacts', user_contacts.GetUserContacts, methods=['GET']),
    Route('/user-contacts', user_contacts.CreateUserContact, methods=['POST']),
    Route('/user-contacts/{id}', user_contacts.GetUserContactByID, methods=['GET']),
    Route('/user-contacts/{id}', user_contacts.UpdateUserContactByID, methods=['PATCH']),
    Route('/user-contacts/{id}', user_contacts.DeleteUserContactByID, methods=['DELETE']),
    Route('/users/{user_id}/contacts', user_contacts.GetContactsByUserID, methods=['GET']),
    # User challenges routes
    Route('/user-challenges', user_challenges.GetUserChallenges, methods=['GET']),
    Route('/user-challenges', user_challenges.CreateUserChallenge, methods=['POST']),
    Route('/user-challenges/{id}', user_challenges.GetUserChallengeByID, methods=['GET']),
    Route('/user-challenges/{id}', user_challenges.UpdateUserChallengeByID, methods=['PATCH']),
    Route('/user-challenges/{id}', user_challenges.DeleteUserChallengeByID, methods=['DELETE']),
]
