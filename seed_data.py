from database import init_db, save_attempt

sample_attempts = [
    ("192.168.1.10", "admin", "12345", "Chrome", "India", "Vijayawada", 20),
    ("192.168.1.10", "admin", "admin123", "Chrome", "India", "Vijayawada", 45),
    ("192.168.1.10", "root", "toor", "Chrome", "India", "Vijayawada", 60),
    ("10.0.0.5", "root", "password", "Firefox", "USA", "New York", 70),
    ("10.0.0.5", "root", "123456", "Firefox", "USA", "New York", 85),
    ("172.16.1.8", "test", "test123", "Edge", "UK", "London", 10),
    ("172.16.1.8", "guest", "guest", "Edge", "UK", "London", 15),
    ("203.45.67.8", "admin", "letmein", "Safari", "India", "Chennai", 55),
    ("203.45.67.8", "admin", "admin", "Safari", "India", "Chennai", 65),
    ("203.45.67.8", "admin", "password1", "Safari", "India", "Chennai", 75),
    ("145.23.11.9", "user1", "hello123", "Chrome", "Germany", "Berlin", 25),
    ("145.23.11.9", "user2", "welcome", "Chrome", "Germany", "Berlin", 30),
    ("192.168.2.14", "student", "vit123", "Firefox", "India", "Vellore", 12),
    ("192.168.2.14", "student", "1234", "Firefox", "India", "Vellore", 22),
    ("100.64.1.20", "admin", "root123", "Chrome", "India", "Hyderabad", 50),
    ("100.64.1.20", "admin", "pass@123", "Chrome", "India", "Hyderabad", 58),
    ("88.45.22.11", "root", "qwerty", "Edge", "Canada", "Toronto", 40),
    ("88.45.22.11", "root", "abc123", "Edge", "Canada", "Toronto", 48),
    ("76.54.33.19", "tester", "test", "Safari", "Australia", "Sydney", 18),
    ("76.54.33.19", "tester", "testtest", "Safari", "Australia", "Sydney", 28),
    ("55.66.77.88", "admin", "0000", "Chrome", "India", "Mumbai", 35),
    ("55.66.77.88", "admin", "1111", "Chrome", "India", "Mumbai", 42),
    ("55.66.77.88", "admin", "2222", "Chrome", "India", "Mumbai", 68),
    ("11.22.33.44", "guest", "guest123", "Firefox", "Singapore", "Singapore", 14),
    ("11.22.33.44", "guest", "guest@123", "Firefox", "Singapore", "Singapore", 19),
    ("200.100.50.25", "root", "superuser", "Edge", "UAE", "Dubai", 72),
    ("200.100.50.25", "root", "rootroot", "Edge", "UAE", "Dubai", 80),
    ("150.80.60.40", "demo", "demo123", "Chrome", "India", "Bangalore", 16),
    ("150.80.60.40", "demo", "demodemo", "Chrome", "India", "Bangalore", 21),
    ("91.81.71.61", "admin", "finaltry", "Safari", "India", "Delhi", 95)
]


def seed_db():
    init_db()
    for attempt in sample_attempts:
        save_attempt(*attempt)
    print("Sample data inserted successfully!")


if __name__ == "__main__":
    seed_db()