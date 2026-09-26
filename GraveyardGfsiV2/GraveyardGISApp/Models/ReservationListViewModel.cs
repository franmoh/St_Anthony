namespace GraveyardGISApp.Models
{
    public class ReservationListViewModel
    {
        public int PlotDetailsId { get; set; }
        public string? SectionName { get; set; }
        public string? Row { get; set; }
        public string? ContactName { get; set; }
        public string? PhoneNumber { get; set; }
        public string? PaymentStatus { get; set; }
        public decimal? BalanceDue { get; set; }
        public decimal? BalancePaid { get; set; }
        public DateTime? ReservedDate { get; set; }
    }
}
