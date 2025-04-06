import mysql.connector
from mysql.connector import Error

def connect():
    return mysql.connector.connect(
        host='localhost',
        user='root',                 # ✅ Replace if your user is different
        password='root',   # ✅ Replace with your MySQL password
        database='blog_app'         # ✅ This is your database name
    )

def create_post(title, content, tag_string):
    try:
        conn = connect()
        cursor = conn.cursor()

        # Step 1: Insert the post
        cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
        post_id = cursor.lastrowid

        # Step 2: Prepare tags from the comma-separated string
        tags = [tag.strip().lower() for tag in tag_string.split(',')]

        for tag in tags:
            # Step 3: Check if tag already exists
            cursor.execute("SELECT id FROM tags WHERE name = %s", (tag,))
            result = cursor.fetchone()

            if result:
                tag_id = result[0]
            else:
                # If not, insert new tag
                cursor.execute("INSERT INTO tags (name) VALUES (%s)", (tag,))
                tag_id = cursor.lastrowid

            # Step 4: Insert into post_tags linking table
            cursor.execute("INSERT INTO post_tags (post_id, tag_id) VALUES (%s, %s)", (post_id, tag_id))

        conn.commit()
        print("✅ Post created successfully with tags!")

    except mysql.connector.Error as err:
        print("❌ Error:", err)

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def view_all_posts():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT title FROM posts")
    posts = cursor.fetchall()

    if posts:
        print("\n--- All Post Titles ---")
        for i, post in enumerate(posts, start=1):
            print(f"{i}. {post[0]}")
    else:
        print("No posts found.")

    cursor.close()
    conn.close()

def view_post_by_title():
    title = input("Enter the post title to view: ")
    conn = connect()
    cursor = conn.cursor()

    # Get the post
    cursor.execute("SELECT id, content FROM posts WHERE title = %s", (title,))
    post = cursor.fetchone()

    if post:
        post_id, content = post
        print(f"\n--- {title} ---")
        print(f"Content: {content}")

        # Get associated tags
        cursor.execute("""
            SELECT tags.name FROM tags
            JOIN post_tags ON tags.id = post_tags.tag_id
            WHERE post_tags.post_id = %s
        """, (post_id,))
        tags = cursor.fetchall()

        if tags:
            tag_names = [tag[0] for tag in tags]
            print("Tags:", ", ".join(tag_names))
        else:
            print("Tags: None")
    else:
        print("Post not found.")

    cursor.close()
    conn.close()

def search_posts_by_tag():
    tag_name = input("Enter tag to search: ")
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT posts.title FROM posts
        JOIN post_tags ON posts.id = post_tags.post_id
        JOIN tags ON post_tags.tag_id = tags.id
        WHERE tags.name = %s
    """, (tag_name,))
    posts = cursor.fetchall()

    if posts:
        print(f"\n--- Posts with tag '{tag_name}' ---")
        for i, post in enumerate(posts, start=1):
            print(f"{i}. {post[0]}")
    else:
        print(f"No posts found with tag '{tag_name}'.")

    cursor.close()
    conn.close()

def menu():
    while True:
        print("\n--- Blog Post Management ---")
        print("1. Create a new post")
        print("2. View all post titles")
        print("3. View post by title")
        print("4. Search posts by tag")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter post title: ")
            content = input("Enter post content: ")
            tags = input("Enter comma-separated tags: ")
            create_post(title, content, tags)
        elif choice == '2':
            view_all_posts()
        elif choice == '3':
            view_post_by_title()
        elif choice == '4':
            search_posts_by_tag()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
