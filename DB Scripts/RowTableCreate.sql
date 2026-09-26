USE cemetery

CREATE TABLE `Row`(
	`RowID` INT AUTO_INCREMENT NOT NULL,
	`RowConstant` VARCHAR(100) NOT NULL,
	`CreatedDate` DATETIME NOT NULL,
	`CreatedBy` INT NOT NULL,
	`ModifiedDate` DATETIME NULL,
	`ModifiedBy` INT NULL,
    PRIMARY KEY (`SectionID`)
) ENGINE=InnoDB;

/****** Indexes ******/
CREATE INDEX `ixRowConstant` ON `Row` (`Rowonstant`, `RowID`);

/****** Constraints ******/
ALTER TABLE `Row`
ADD CONSTRAINT `FK_Row_CreatedBy`
FOREIGN KEY (`CreatedBy`) REFERENCES `Users`(`UserID`),
ADD CONSTRAINT `FK_Row_ModifiedBy`
FOREIGN KEY (`ModifiedBy`) REFERENCES `Users`(`UserID`);