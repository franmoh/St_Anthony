USE cemetery

CREATE TABLE `Notes`(
	`NoteID` INT AUTO_INCREMENT NOT NULL,
	`Note` VARCHAR(4000) NOT NULL,
	`CreatedDate` DATETIME NOT NULL,
	`CreatedBy` INT NOT NULL,
	`ModifiedDate` DATETIME NULL,
	`ModifiedBy` INT NULL,
    PRIMARY KEY (`NoteID`)
) ENGINE=InnoDB;

/****** Indexes ******/
/**No indexes needed**/

/****** Constraints ******/
ALTER TABLE `Notes`
ADD CONSTRAINT `FK_Notes_CreatedBy`
FOREIGN KEY (`CreatedBy`) REFERENCES `Users`(`UserID`),
ADD CONSTRAINT `FK_Notes_ModifiedBy`
FOREIGN KEY (`ModifiedBy`) REFERENCES `Users`(`UserID`);