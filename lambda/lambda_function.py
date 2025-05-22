import json
import os
import pymysql
import logging
import boto3
import base64
from werkzeug.security import generate_password_hash
from datetime import datetime

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get database connection parameters from environment variables
DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
DB_PORT = int(os.environ.get('DB_PORT', 3306))

# Initialize SSM client for retrieving secrets
ssm = boto3.client('ssm')

def get_secret(secret_name):
    """Retrieve secret from AWS Parameter Store"""
    try:
        response = ssm.get_parameter(
            Name=secret_name,
            WithDecryption=True
        )
        return response['Parameter']['Value']
    except Exception as e:
        logger.error(f"Error retrieving secret {secret_name}: {str(e)}")
        raise e

def get_db_connection():
    """Create a connection to the MySQL database"""
    try:
        # If using Parameter Store for secrets, retrieve them
        if not DB_PASSWORD:
            db_password = get_secret('/mindcare/db/password')
        else:
            db_password = DB_PASSWORD
            
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=db_password,
            db=DB_NAME,
            port=DB_PORT,
            connect_timeout=5
        )
        return conn
    except pymysql.MySQLError as e:
        logger.error(f"Error connecting to MySQL database: {str(e)}")
        raise e

def validate_signup_data(data):
    """Validate the signup data"""
    errors = []
    
    # Check required fields
    if not data.get('usn'):
        errors.append("Username is required")
    if not data.get('pas'):
        errors.append("Password is required")
    
    # Validate email format if provided
    email = data.get('email')
    if email and '@' not in email:
        errors.append("Invalid email format")
    
    return errors

def lambda_handler(event, context):
    """Lambda function handler for user signup"""
    logger.info("Received event: " + json.dumps(event))
    
    try:
        # Parse request body
        if 'body' in event:
            try:
                if isinstance(event['body'], str):
                    body = json.loads(event['body'])
                else:
                    body = event['body']
            except json.JSONDecodeError:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'message': 'Invalid JSON in request body'})
                }
        else:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'message': 'Missing request body'})
            }
        
        # Validate signup data
        validation_errors = validate_signup_data(body)
        if validation_errors:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'message': 'Validation failed', 'errors': validation_errors})
            }
        
        # Extract user data
        usn = body.get('usn')
        pas = body.get('pas')
        email = body.get('email')
        
        # Hash the password
        encpassword = generate_password_hash(pas)
        
        # Connect to the database
        conn = get_db_connection()
        
        with conn.cursor() as cursor:
            # Check if username already exists
            cursor.execute("SELECT id FROM user WHERE usn = %s", (usn,))
            if cursor.fetchone():
                return {
                    'statusCode': 409,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'message': 'Username is already taken'})
                }
            
            # Check if email already exists (if provided)
            if email:
                cursor.execute("SELECT id FROM user WHERE email = %s", (email,))
                if cursor.fetchone():
                    return {
                        'statusCode': 409,
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*'
                        },
                        'body': json.dumps({'message': 'Email is already registered'})
                    }
            
            # Insert new user
            current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            if email:
                cursor.execute(
                    "INSERT INTO user (usn, pas, email, date_registered) VALUES (%s, %s, %s, %s)",
                    (usn, encpassword, email, current_time)
                )
            else:
                cursor.execute(
                    "INSERT INTO user (usn, pas, date_registered) VALUES (%s, %s, %s)",
                    (usn, encpassword, current_time)
                )
            
            conn.commit()
        
        conn.close()
        
        return {
            'statusCode': 201,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'User registered successfully'})
        }
        
    except pymysql.MySQLError as e:
        logger.error(f"Database error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Database error occurred'})
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'An error occurred during signup'})
        }