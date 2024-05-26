def has_permission(user, resource, policy):
    for attribute, value in policy.items():
        if getattr(user, attribute) != value:
            return False
    return True
