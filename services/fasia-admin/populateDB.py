#!/usr/bin/python

from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


def main():
    # Connect to the DB
    collection = MongoClient('127.0.0.1', username='fasiaadmin',
                             password='fasiaadmin@123#', authSource='fasiadb', authMechanism='SCRAM-SHA-1')
    db = collection['fasiadb']
    user_table = db['users']

    # Ask for data to store
    user = raw_input("Enter your username: ")
    password = raw_input("Enter your password: ")
    pass_hash = generate_password_hash(password, method='pbkdf2:sha256')

    # Insert the user in the DB
    try:
        user_table.insert(
            {"username": user, "password": pass_hash, "is_admin": 1, "email": user})
        print "User created."
    except DuplicateKeyError:
        print "User already present in DB."


if __name__ == '__main__':
    main()
