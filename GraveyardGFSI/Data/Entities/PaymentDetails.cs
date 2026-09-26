using System.ComponentModel.DataAnnotations;

namespace GraveyardGFSI.Data.Entities
{
    public class PaymentDetails : Auditable
    {
        [Key]
        public int PaymentDetailsID { get; set; }
        public int PlotId { get; set; }
        public int DeceasedDetailsId { get; set; }
        public int PaymentStatusId { get; set; }
        public int ContactDetailsId { get; set; }
        public int NoteId { get; set; }

        public decimal BalancePaid { get; set; }
        public decimal BalanceDue { get; set; }

        //
        public PlotDetails Plot { get; set; }
        public DeceasedDetails DeceasedDetails { get; set; }
        public PaymentStatus PaymentStatus { get; set; }
        public ContactDetails ContactDetails { get; set; }


        public PaymentDetails() { }
        public PaymentDetails(decimal balancePaid, decimal balanceDue)
        {
            this.BalancePaid = balancePaid;
            this.BalanceDue = balanceDue;
        }
    }
}
