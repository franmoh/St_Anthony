USE cemetery;

CREATE TABLE `PlotDetails` (
    `PlotDetailsID` INT AUTO_INCREMENT NOT NULL
    `PlotID` INT,
    `SectionID` INT NOT NULL,
    `Row` NVARCHAR(100) NOT NULL,
    `Unit` NVARCHAR(100) NOT NULL,
    `Side` NVARCHAR(100) NOT NULL,
    `Niche` NVARCHAR(100) NOT NULL,
    `MaintenanceStatusID` INT NOT NULL,
    `ContactDetailsID` INT NOT NULL,
    `NoteID` INT NULL,
    `CreatedDate` DATETIME NOT NULL,
    `CreatedBy` INT NOT NULL,
    `ModifiedDate` DATETIME NULL,
    `ModifiedBy` INT NULL,
    PRIMARY KEY (`PlotID`)
) ENGINE=InnoDB;

-- Indexes
CREATE INDEX `ix_Location` ON `PlotDetails` (`SectionID`);
CREATE INDEX `ix_MaintenanceStatus` ON `PlotDetails` (`MaintenanceStatusID`);
CREATE INDEX `ix_ContactDetails` ON `PlotDetails` (`ContactDetailsID`);
CREATE INDEX `ix_Notes` ON `PlotDetails` (`NoteID`);

-- Foreign Keys
ALTER TABLE `PlotDetails`
ADD CONSTRAINT `FK_PlotDetails_Section` FOREIGN KEY (`SectionID`) REFERENCES `Section`(`SectionID`),
ADD CONSTRAINT `FK_PlotDetails_MaintenanceStatus` FOREIGN KEY (`MaintenanceStatusID`) REFERENCES `MaintenanceStatus`(`MaintenanceStatusID`),
ADD CONSTRAINT `FK_PlotDetails_ContactDetails` FOREIGN KEY (`ContactDetailsID`) REFERENCES `ContactDetails`(`ContactDetailsID`),
ADD CONSTRAINT `FK_PlotDetails_Notes` FOREIGN KEY (`NoteID`) REFERENCES `Notes`(`NoteID`),
ADD CONSTRAINT `FK_PlotDetails_CreatedBy` FOREIGN KEY (`CreatedBy`) REFERENCES `Users`(`UserID`),
ADD CONSTRAINT `FK_PlotDetails_ModifiedBy` FOREIGN KEY (`ModifiedBy`) REFERENCES `Users`(`UserID`);
