CREATE TABLE User (
    userId INTEGER PRIMARY KEY AUTOINCREMENT,
    fullName VARCHAR(100) NOT NULL,
    emailAddress VARCHAR(100) NOT NULL UNIQUE,
    passwd VARCHAR(30) NOT NULL,
    userType CHAR(3) NOT NULL CHECK (userType IN ("USR", "ADM", "SLR"))
);

CREATE TABLE Product (
    productId INTEGER PRIMARY KEY AUTOINCREMENT,
    productName VARCHAR(128) NOT NULL,
    productDescription VARCHAR(1024) NOT NULL
);

CREATE TABLE Wishlist (
    userId INT NOT NULL,
    productId INT NOT NULL,
    PRIMARY KEY (userId, productId),
    FOREIGN KEY (userId) REFERENCES User(userId),
    FOREIGN KEY (productId) REFERENCES Product(productId)
);

CREATE TABLE Cart (
    userId INT NOT NULL,
    productId INT NOT NULL,
    sellerId INT NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (userId, productId, sellerId),
    FOREIGN KEY (userId) REFERENCES User(userId),
    FOREIGN KEY (sellerId) REFERENCES User(userId),
    FOREIGN KEY (productId) REFERENCES Product(productId)
);

CREATE TABLE UserAddress (
    userId INT NOT NULL,
    addressId INTEGER NOT NULL,
    addressName VARCHAR(300) NOT NULL,
    PRIMARY KEY (userId, addressId),
    FOREIGN KEY (userId) REFERENCES User(userId)
);

CREATE TABLE SellerProduct (
    productId INT NOT NULL,
    sellerId INT NOT NULL,
    price INT NOT NULL,
    discount DECIMAL(5, 2) DEFAULT 0.00,
    quantity INT DEFAULT 1,
    PRIMARY KEY (productId, sellerId),
    FOREIGN KEY (productId) REFERENCES Product(productId),
    FOREIGN KEY (sellerId) REFERENCES User(userId)
);

CREATE TABLE Orders (
    orderId INTEGER PRIMARY KEY AUTOINCREMENT,
    userId INT NOT NULL,
    addressId INT NOT NULL,
    totalCost INT NOT NULL,
    FOREIGN KEY (userId) REFERENCES User(userId),
    FOREIGN KEY (addressId) REFERENCES UserAddress(addressId)
);

CREATE TABLE OrderProduct (
    orderId INT NOT NULL,
    productId INT NOT NULL,
    productName VARCHAR(128) NOT NULL,
    originalPrice INT NOT NULL,
    discountPrice INT NOT NULL,
    sellerId INT NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (orderId, productId, sellerId),
    FOREIGN KEY (orderId) REFERENCES Orders(orderId),
    FOREIGN KEY (sellerId) REFERENCES User(userId),
    FOREIGN KEY (productId) REFERENCES Product(productId)
);