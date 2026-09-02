CREATE DATABASE amazon_sentiment;
USE amazon_sentiment;

CREATE TABLE Products (
    product_id int PRIMARY KEY AUTO_INCREMENT,
    amazon_url varchar(255) NOT NULL,
    product_name varchar(255)
);

CREATE TABLE Reviews (
    review_id int PRIMARY KEY AUTO_INCREMENT,
    product_id int,
    review_text text,
    sentiment_score float,
    sentiment_label varchar(50),
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
);

USE amazon_sentiment;

ALTER TABLE Products MODIFY amazon_url TEXT;
ALTER TABLE Products MODIFY product_name VARCHAR(500);

SELECT * FROM Reviews;