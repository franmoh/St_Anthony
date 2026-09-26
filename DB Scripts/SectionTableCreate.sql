USE cemetery

CREATE TABLE `Section`(
	`SectionID` INT AUTO_INCREMENT NOT NULL,
	`SectionConstant` VARCHAR(100) NOT NULL,
	`CreatedDate` DATETIME NOT NULL,
	`CreatedBy` INT NOT NULL,
	`ModifiedDate` DATETIME NULL,
	`ModifiedBy` INT NULL,
    PRIMARY KEY (`SectionID`)
) ENGINE=InnoDB;

/****** Indexes ******/
CREATE INDEX `ixSectionConstant` ON `Section` (`SectionConstant`, `SectionID`);

/****** Constraints ******/
ALTER TABLE `Section`
ADD CONSTRAINT `FK_Section_CreatedBy`
FOREIGN KEY (`CreatedBy`) REFERENCES `Users`(`UserID`),
ADD CONSTRAINT `FK_Section_ModifiedBy`
FOREIGN KEY (`ModifiedBy`) REFERENCES `Users`(`UserID`);