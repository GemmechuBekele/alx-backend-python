# ALX_prodev Seeder

This script automated the setup of a MySQL database, including a `user_data` table populated from a CSV file hosted on a URL. Data is streamed one record at a time using a generator.

---

## 📦 Features

- Establishes connection with MySQL Server 

- Creates database `ALX_prodev` if it did not previously exist

- Creates `user_data` table with:

  - `user_id` (UUID, Primary Key, Indexed)

  - `username` (VARCHAR, NOT NULL)

  - `email_address` (VARCHAR, NOT NULL)

  - `age` (DECIMAL, NOT NULL)

- Downloads and reads CSV data from a remote URL 

- Adds new users based on email if they do not match existing users

- Streams all user data rows with a python generator

---

## 🛠 Requirements

- Python 3.x

- MySQL Server

- Python packages:

  - `mysql-connector-python`
  
  - `requests`

Use the following to install dependencies: 

```bash

pip install mysql-connector-python requests