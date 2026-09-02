import mysql.connector # type: ignore
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("MYSQL_PASSWORD"), # Dynamic pull
        database="amazon_sentiment"
    )

def save_analysis_results(amazon_url, sentiment_results):
    try:
        # Connect INSIDE the safety block so if the password is wrong, it doesn't crash the server
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Insert the product record
        sql_product = "INSERT INTO Products (amazon_url) VALUES (%s)"
        cursor.execute(sql_product, (amazon_url,))
        
        # Grab the auto-incremented ID of the product we just inserted
        product_id = cursor.lastrowid
        
        # 2. Loop through the NLP results and insert each review
        sql_review = """
            INSERT INTO Reviews (product_id, review_text, sentiment_score, sentiment_label) 
            VALUES (%s, %s, %s, %s)
        """
        
        for review in sentiment_results['detailed_analysis']:
            cursor.execute(
                sql_review, 
                (product_id, review['text'], review['confidence'], review['label'])
            )
            
        # Commit the transaction to disk
        conn.commit()
        return True
        
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return False
        
    finally:
        # Ensure we only try to close the connection if it was successfully created
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()