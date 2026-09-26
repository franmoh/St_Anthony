USE cemetery;

CREATE TABLE `MaintenanceDetails` (
    `MaintenanceDetailsID` INT AUTO_INCREMENT NOT NULL,
    `PlotDetailsID` INT NOT NULL,
    `MaintenanceStatusID` INT NOT NULL,
    `ContactDetailsID` INT NULL,
    `NoteID` INT NULL,
    `CreatedDate` DATETIME NOT NULL,
    `CreatedBy` INT NOT NULL,
    `ModifiedDate` DATETIME NULL,
    `ModifiedBy` INT NULL,
    PRIMARY KEY (`MaintenanceDetailsID`)
) ENGINE=InnoDB;

-- Indexes
CREATE INDEX `ix_PlotMaintenanceDetails` ON `MaintenanceDetails` (`PlotID`, `MaintenanceStatusID`);

-- Foreign Keys
ALTER TABLE `MaintenanceDetails`
ADD CONSTRAINT `FK_MaintenanceDetails_Plot` FOREIGN KEY (`PlotDetailsID`) REFERENCES `PlotDetails`(`PlotID`),
ADD CONSTRAINT `FK_MaintenanceDetails_Status` FOREIGN KEY (`MaintenanceStatusID`) REFERENCES `MaintenanceStatus`(`MaintenanceStatusID`),
ADD CONSTRAINT `FK_MaintenanceDetails_Contact` FOREIGN KEY (`ContactDetailsID`) REFERENCES `ContactDetails`(`ContactDetailsID`),
ADD CONSTRAINT `FK_MaintenanceDetails_Notes` FOREIGN KEY (`NoteID`) REFERENCES `Notes`(`NoteID`),
ADD CONSTRAINT `FK_MaintenanceDetails_CreatedBy` FOREIGN KEY (`CreatedBy`) REFERENCES `Users`(`UserID`),
ADD CONSTRAINT `FK_MaintenanceDetails_ModifiedBy` FOREIGN KEY (`ModifiedBy`) REFERENCES `Users`(`UserID`);
