from .rules import has_permission

class ABACPolicy:
    def __init__(self):
        self.policies = []

    def add_policy(self, policy):
        self.policies.append(policy)

    def evaluate(self, user, resource):
        # Quy tắc đặc biệt: Nếu người dùng là admin, luôn cấp quyền truy cập
        if user.role == 'admin':
            return True
        for policy in self.policies:
            if has_permission(user, resource, policy):
                return True
        return False
