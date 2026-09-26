using System.ComponentModel.DataAnnotations;

namespace GraveyardGISApp.Models
{
    public class ReservationFormViewModel
    {
        // Plot info (display only)
        public int PlotDetailsId { get; set; }
        public string? SectionName { get; set; }
        public string? Row { get; set; }
        public string? Unit { get; set; }
        public string? Side { get; set; }
        public string? Niche { get; set; }

        // Set when reusing an existing contact instead of creating a new one
        public int? ExistingContactId { get; set; }

        // Contact info (required only when ExistingContactId is not set)
        [MaxLength(100)]
        public string? FirstName { get; set; }

        [MaxLength(100)]
        public string? MiddleName { get; set; }

        [MaxLength(100)]
        public string? LastName { get; set; }

        [MaxLength(30)]
        public string? PhoneNumber { get; set; }

        [MaxLength(200)]
        public string? Email { get; set; }

        [MaxLength(300)]
        public string? Address { get; set; }

        // Payment
        [Required]
        [Range(0.01, double.MaxValue, ErrorMessage = "Balance due must be greater than 0.")]
        public decimal BalanceDue { get; set; }
    }
}
