using Microsoft.AspNetCore.Mvc.Rendering;

namespace GraveyardGISApp.Models
{
    public class ReservationDetailViewModel
    {
        // Plot
        public int PlotDetailsId { get; set; }
        public string? SectionName { get; set; }
        public string? Row { get; set; }
        public string? Unit { get; set; }
        public string? Side { get; set; }
        public string? Niche { get; set; }

        // Contact
        public int ContactDetailsId { get; set; }
        public string? FirstName { get; set; }
        public string? MiddleName { get; set; }
        public string? LastName { get; set; }
        public string? PhoneNumber { get; set; }
        public string? Email { get; set; }
        public string? Address { get; set; }
        public DateTime? ReservedDate { get; set; }

        // Payment
        public int? PaymentDetailsId { get; set; }
        public int? PaymentStatusId { get; set; }
        public string? PaymentStatusName { get; set; }
        public decimal? BalanceDue { get; set; }
        public decimal? BalancePaid { get; set; }

        public List<SelectListItem> AvailablePaymentStatuses { get; set; } = new();
    }
}
