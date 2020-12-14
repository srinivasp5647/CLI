
create database shopgarrage;

use shopgarrage;

Create database shopgarrage;

Create table Customers(customerID int AUTO_INCREMENT PRIMARY KEY, name VARCHAR(20) not null, email VARCHAR(200) not null, address VARCHAR(200));

Create table Admin(id int AUTO_INCREMENT PRIMARY KEY, email VARCHAR(200) not null, password VARCHAR(200) not null);

Create table Category(categoryID int AUTO_INCREMENT PRIMARY KEY, title VARCHAR(20)not null);

Create table Products(productID int AUTO_INCREMENT PRIMARY KEY, name VARCHAR(20), price FLOAT(20, 2), description VARCHAR(200), categoryID int, FOREIGN KEY(categoryID) REFERENCES Category(categoryID) );

Create table Cart(cartID int AUTO_INCREMENT PRIMARY KEY, customerID int, paid BOOLEAN, FOREIGN KEY(customerID) REFERENCES Customers(customerID) );

Create table Cart_Products(cpID int AUTO_INCREMENT PRIMARY KEY, cartID int, productID int, quantity int, total FLOAT(20, 2), FOREIGN KEY(cartID) REFERENCES Cart(cartID), FOREIGN KEY(productID) REFERENCES Products(productID));

Create table Payments(paymentID int AUTO_INCREMENT PRIMARY KEY, cartID int, amount FLOAT(20, 2), discount int(20), total FLOAT(20, 2), Paid BOOLEAN, FOREIGN KEY(cartID) REFERENCES Cart(cartID) );


