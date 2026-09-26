/*
==============================
Author: Adam Myles
Create Date: 2025-11-06
Description: TBD
==============================
*/

-- Used to ensure that ; doesn't end the stored procedure early as it's a terminator command
DELIMITER //

DROP PROCEDURE IF EXISTS uspStoredProcedureTemplate //
CREATE PROCEDURE uspStoredProcedureTemplate (
    IN p_UserID             INT, -- ID of the user making the query
    IN p_UserDateTime       DATETIME, -- Date and time of the query based on user date and time
    IN p_MaxSearchResults   INT, -- Maximum amount of data to be returned (this can be tuned for performance purposes/pagination)
    IN p_PlotID             INT -- Sample parameter for use with the PlotDetails table
)
BEGIN
    -- Example of pulling records from a table
    SELECT 
        pd.PlotID
        ,pd.SectionID
        ,pd.Row
        ,pd.Unit
        ,pd.Side
        ,pd.Niche
        ,pd.MaintenanceStatusID
        ,pd.ContactDetailsID
        ,pd.NoteID
        ,pd.CreatedDate
        ,pd.CreatedBy
        ,pd.ModifiedDate
        ,pd.ModifiedBy
    FROM PlotDetails pd
    WHERE pd.PlotID = p_PlotID;

    -- Example of selecting records into a temporary table for manipulation
    CREATE TEMPORARY TABLE TempPlotDetailsTable AS
    SELECT
        pd.PlotID
        ,pd.SectionID
        ,pd.Row
        ,pd.Unit
        ,pd.Side
        ,pd.Niche
        ,pd.MaintenanceStatus
        ,pd.ContactDetailsID
        ,pd.NoteID
        ,pd.CreatedDate
        ,pd.CreatedBy
        ,pd.ModifiedDate
        ,pd.ModifiedBy
    FROM PlotDetails pd
    WHERE pd.PlotID = p_PlotID;

    -- Example of updating records in a table
    UPDATE PlotDetails pd
    SET pd.row = 100
    WHERE pd.PlotID = p_PlotID
        AND pd.row <> 100;

    -- Example: Get all plots in Section 5, sorted by Row number
    SELECT 
        PlotID
        ,SectionID
        ,Row
        ,Unit
        ,CreatedDate
    FROM PlotDetails
    WHERE SectionID = 5
    ORDER BY Row ASC;

    -- Example: Get a list of unique Section IDs that exist in the PlotDetails table
    SELECT DISTINCT SectionID
    FROM PlotDetails;

    -- Example (exclusive joins/inner joins): Get plots with their maintenance status constants
    SELECT 
        pd.PlotID
        ,pd.SectionID
        ,ms.MaintenanceStatusConstant
    FROM PlotDetails pd
    INNER JOIN MaintenanceStatus ms
        ON pd.MaintenanceStatusID = ms.MaintenanceStatusID;

    -- Example (inclusive joins/left joins): Get all plots, even if they don’t have a maintenance record
    SELECT 
        pd.PlotID
        ,pd.SectionID
        ,ms.MaintenanceStatusConstant
    FROM PlotDetails pd
    LEFT JOIN MaintenanceStatus ms
        ON pd.MaintenanceStatusID = ms.MaintenanceStatusID;

    -- Example: Add a new plot record
    INSERT INTO PlotDetails (
        SectionID
        ,Row
        ,Unit
        ,Side
        ,Niche
        ,MaintenanceStatusID
        ,ContactDetailsID
        ,CreatedDate
        ,CreatedBy
    )
    VALUES (
        3           -- SectionID
        ,12         -- Row
        ,4          -- Unit
        ,'A'        -- Side
        ,NULL       -- Niche
        ,1          -- MaintenanceStatusID
        ,45         -- ContactDetailsID
        ,NOW()      -- CreatedDate
        ,1          -- CreatedBy
    );

    -- Example: Delete a plot record (keep in mind that if this ID is referenced elsewhere all references will have to be deleted first)
    DELETE FROM PlotDetails
    WHERE PlotID = p_PlotID;

    -- Example (aggregating): Count how many plots are in each section
    SELECT 
        SectionID
        ,COUNT(*) AS TotalPlots
    FROM PlotDetails
    GROUP BY SectionID
    ORDER BY TotalPlots DESC;

    -- Example (subqueries): Get all plots that were created by the most recent user to add a record
    SELECT *
    FROM PlotDetails
    WHERE CreatedBy = (
        SELECT CreatedBy
        FROM PlotDetails
        ORDER BY CreatedDate DESC
        LIMIT 1
    );

    -- Example: Update maintenance status for all plots linked to a specific contact
    UPDATE PlotDetails pd
    INNER JOIN ContactDetails cd
        ON pd.ContactDetailsID = cd.ContactDetailsID
    SET pd.MaintenanceStatusID = 2
    WHERE cd.LastName = 'Smith';

    -- Example: Create a temp table and filter results
    CREATE TEMPORARY TABLE PlotsForSection10 AS
    SELECT *
    FROM PlotDetails
    WHERE SectionID = 10;

    -- Work with the temp table
    SELECT COUNT(*) AS PlotsInSection10
    FROM PlotsForSection10;

    -- Example (partial pattern matching): Find all plots created by users whose name starts with 'f'
    SELECT 
        pd.PlotID
        ,dd.FirstName
    FROM PlotDetails pd
    INNER JOIN DeceasedDetails dd
        ON dd.PlotID = pd.PlotID
    WHERE dd.FirstName LIKE 'f%';

    -- Example (conditional logic): Show a readable maintenance status based on ID
    SELECT 
        PlotID
        ,CASE 
            WHEN MaintenanceStatusID = 1 THEN 'Good'
            WHEN MaintenanceStatusID = 2 THEN 'Damaged'
            ELSE 'Unknown'
        END AS MaintenanceStatus
    FROM PlotDetails;
END //

DELIMITER ;
