using System.ComponentModel.DataAnnotations;

namespace GraveyardGFSI.Data.Entities
{
    public class DeceasedStatus : Auditable
    {
        [Key]
        public int DeceasedStatusId { get; set; }
        public string DeceasedStatusConstant { get; set; } = string.Empty;

        public DeceasedStatus() { }

        public DeceasedStatus(string deceasedStatusConstant, DateTime createdDate, int createdBy, DateTime modifiedDate, int modifiedBy)
        {
            this.DeceasedStatusConstant = deceasedStatusConstant;
            this.CreatedDate = createdDate;
            this.CreatedBy = createdBy;
            this.ModifiedDate = modifiedDate;
            this.ModifiedBy = modifiedBy;
        }

    }
}
