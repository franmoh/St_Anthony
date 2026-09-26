using System.ComponentModel.DataAnnotations;

namespace GraveyardGFSI.Data.Entities
{
    public class PaymentStatus : Auditable
    {
        [Key]
        public int PaymentStatusId { get; set; }
        public string PaymentStatusConstant { get; set; } = string.Empty;

        public PaymentStatus() { }
        public PaymentStatus(string paymentStatusConstant, DateTime createdDate, int createdBy, DateTime modifiedDate, int modifiedBy)
        {
            this.PaymentStatusConstant = paymentStatusConstant;
            this.CreatedDate = createdDate;
            this.CreatedBy = createdBy;
            this.ModifiedDate = modifiedDate;
            this.ModifiedBy = modifiedBy;
        }
    }
}
