CREATE DATABASE crm_system;
USE crm_system;

CREATE TABLE Managers (
    ManagerID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100),
    Phone VARCHAR(15)
);
CREATE TABLE DealItems (
    ItemID INT PRIMARY KEY AUTO_INCREMENT,
    DealID INT NOT NULL,
    ItemName VARCHAR(100) NOT NULL,
    Quantity INT NOT NULL,
    Price DECIMAL(15,2) NOT NULL,
    FOREIGN KEY (DealID) REFERENCES Deals(DealID)
);

CREATE TABLE Clients (
    ClientID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100),
    Phone VARCHAR(15),
    ManagerID INT,
    LifecycleStage VARCHAR(20) DEFAULT 'Новый',
    FOREIGN KEY (ManagerID) REFERENCES Managers(ManagerID)
);

CREATE TABLE Interactions (
    InteractionID INT PRIMARY KEY AUTO_INCREMENT,
    ClientID INT NOT NULL,
    ContactPerson VARCHAR(100) NOT NULL,
    InteractionType ENUM('call', 'meeting') NOT NULL,
    InteractionDate DATETIME NOT NULL,
    Content TEXT NOT NULL,
    FOREIGN KEY (ClientID) REFERENCES Clients(ClientID)
);

CREATE TABLE Deals (
    DealID INT PRIMARY KEY AUTO_INCREMENT,
    ClientID INT NOT NULL,
    DealName VARCHAR(100) NOT NULL,
    TotalAmount DECIMAL(15,2) NOT NULL,
    ManagerID INT NOT NULL,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ClientID) REFERENCES Clients(ClientID),
    FOREIGN KEY (ManagerID) REFERENCES Managers(ManagerID)
);

CREATE TABLE Payments (
    PaymentID INT PRIMARY KEY AUTO_INCREMENT,
    DealID INT NOT NULL,
    PaymentAmount DECIMAL(15,2) NOT NULL,
    PaymentDate DATETIME NOT NULL,
    FOREIGN KEY (DealID) REFERENCES Deals(DealID)
);

CREATE TABLE Projects (
    ProjectID INT PRIMARY KEY AUTO_INCREMENT,
    ClientID INT NOT NULL,
    ProjectName VARCHAR(100) NOT NULL,
    ResponsibleManagerID INT,
    StartDate DATE,
    EndDate DATE,
    FOREIGN KEY (ClientID) REFERENCES Clients(ClientID),
    FOREIGN KEY (ResponsibleManagerID) REFERENCES Managers(ManagerID)
);

CREATE TABLE Tasks (
    TaskID INT PRIMARY KEY AUTO_INCREMENT,
    ClientID INT NOT NULL,
    ProjectID INT,
    TaskName VARCHAR(100) NOT NULL,
    Description TEXT,
    DueDate DATE NOT NULL,
    Status ENUM('todo', 'in_progress', 'done') NOT NULL DEFAULT 'todo',
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    ResponsibleManagerID INT NOT NULL,
    FOREIGN KEY (ClientID) REFERENCES Clients(ClientID),
    FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID),
    FOREIGN KEY (ResponsibleManagerID) REFERENCES Managers(ManagerID)
);

CREATE TABLE ClientNotes (
    NoteID INT PRIMARY KEY AUTO_INCREMENT,  
    ClientID INT NOT NULL,           
    NoteText TEXT NOT NULL,            
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ClientID) REFERENCES Clients(ClientID)
);