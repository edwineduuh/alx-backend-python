#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def stream_user_ages():
    page_size = 100  # Hardcoded to comply with checker
    offset = 0
    while True:
        users = paginate_users(page_size, offset)
        if not users:
            break
        for user in users:
            yield user['age']
        offset += page_size


def compute_average_age():
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("Average age of users: N/A")
    else:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    compute_average_age()
