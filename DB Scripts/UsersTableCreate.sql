USE cemetery

CREATE TABLE `Users`(
	`UserID` int AUTO_INCREMENT NOT NULL,
	`Password` binary(64) NOT NULL,
	`FirstName` varchar(100) NOT NULL,
	`LastName` varchar(100) NOT NULL,
	`Username` varchar(50) NOT NULL,	
	`IsActive` TINYINT(1) NOT NULL DEFAULT 1,	
	`LastLogin` DATE NULL,
	`CreatedDate` DATETIME NOT NULL,
	`CreatedBy` INT NOT NULL,
	`ModifiedDate` DATETIME NULL,
	`ModifiedBy` INT NULL,
	 PRIMARY KEY (`UserID`)
) ENGINE=InnoDB;

/****** Indexes ******/
CREATE UNIQUE INDEX `ixUniqueUserName` ON Users (Username);
CREATE INDEX `ixActiveUser` ON Users (Username, IsActive);

/****** Constraints ******/
ALTER TABLE `Users`
ADD CONSTRAINT `FK_User_CreatedBy`
FOREIGN KEY (CreatedBy) REFERENCES Users(UserID),
ADD CONSTRAINT `FK_User_ModifiedBy`
FOREIGN KEY (ModifiedBy) REFERENCES Users(UserID);