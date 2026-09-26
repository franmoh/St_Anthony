USE cemetery

CREATE TABLE `PaymentStatus`(
	`PaymentStatusID` INT AUTO_INCREMENT NOT NULL,
	`PaymentStatusConstant` VARCHAR(100) NOT NULL,
	`CreatedDate` DATETIME NOT NULL,
	`CreatedBy` INT NOT NULL,
	`ModifiedDate` DATETIME NULL,
	`ModifiedBy` int NULL,
    PRIMARY KEY (`PaymentStatusID`)
) ENGINE=InnoDB;

/****** Indexes ******/
CREATE UNIQUE INDEX `ixPaymentStatusConstant` 
ON `PaymentStatus` (`PaymentStatusConstant`);

/****** Constraints ******/
ALTER TABLE `PaymentStatus`
ADD CONSTRAINT `FK_PaymentStatus_CreatedBy`
FOREIGN KEY (`CreatedBy`) REFERENCES `Users`(`UserID`),
ADD CONSTRAINT `FK_PaymentStatus_ModifiedBy`
FOREIGN KEY (`ModifiedBy`) REFERENCES `Users`(`UserID`);