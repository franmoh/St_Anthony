using System.ComponentModel.DataAnnotations;

namespace GraveyardGFSI.Data.Entities
{
    public class MaintenanceStatus : Auditable
    {
        [Key]
        public int MaintenanceStatusId { get; set; }
        public string MaintenanceStatusConstant { get; set; } = string.Empty;

        public MaintenanceStatus() { }
        /*
        public MaintenanceStatus(string maintenanceStatusConstant, DateTime createdDate, int createdBy, DateTime modifiedDate, int modifiedBy)
        {
            this.MaintenanceStatusConstant = maintenanceStatusConstant;
            this.CreatedDate = createdDate;
            this.CreatedBy = createdBy;
            this.ModifiedDate = modifiedDate;
            this.ModifiedBy = modifiedBy;
        }
        */
    }
}
