class User:
    def __init__(self, name, role, location):
        self.name = name
        self.role = role
        self.location = location


class Resource:
    def __init__(self, name, location):
        self.name = name
        self.location = location

class ABACPolicy:
    def __init__(self):
        self.rules = []

    def add_rule(self, condition):
        self.rules.append(condition)

    def check_access(self, user, resource):
        for rule in self.rules:
            if not rule(user, resource):
                return False
        return True

# Định nghĩa các điều kiện
def is_admin(user, resource):
    return user.role == 'admin'

def is_same_location(user, resource):
    return user.location == resource.location

def main():
    # Tạo người dùng và tài nguyên
    user1 = User(name='Alice', role='admin', location='office')
    user2 = User(name='Bob', role='user', location='home')
    resource1 = Resource(name='Document', location='office')
    resource2 = Resource(name='Server', location='datacenter')

    # Tạo chính sách ABAC
    policy = ABACPolicy()

    # Thêm các quy tắc vào chính sách
    policy.add_rule(is_admin)
    policy.add_rule(is_same_location)

    # Kiểm tra quyền truy cập
    print(user1.name, " access Document:", policy.check_access(user1, resource1))  # True
    print(user1.name, " access Server:", policy.check_access(user1, resource2))    # False
    print(user2.name, " access Document:", policy.check_access(user2, resource1))  # False
    print(user2.name, " access Server:", policy.check_access(user2, resource2))    # False

if __name__ == "__main__":
    main()
