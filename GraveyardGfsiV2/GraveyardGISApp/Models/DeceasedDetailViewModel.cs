namespace GraveyardGISApp.Models
{
    public class DeceasedDetailViewModel
    {
        // Deceased info
        public int DeceasedDetailsId { get; set; }
        public string? FirstName { get; set; }
        public string? MiddleName { get; set; }
        public string? LastName { get; set; }
        public string? Gender { get; set; }
        public int? DOBYear { get; set; }
        public int? DOBMonth { get; set; }
        public int? DOBDay { get; set; }
        public int? DODYear { get; set; }
        public int? DODMonth { get; set; }
        public int? DODDay { get; set; }
        public DateTime? DateBuried { get; set; }

        // Plot / location info
        public int PlotId { get; set; }
        public int ZoneId { get; set; }
        public string? SectionName { get; set; }
        public string? Row { get; set; }
        public string? Unit { get; set; }
        public string? Side { get; set; }
        public string? Niche { get; set; }

        // Contacts
        public List<ContactViewModel> DeceasedContacts { get; set; } = new();
        public List<ContactViewModel> PlotContacts { get; set; } = new();
    }

    public class ContactViewModel
    {
        public string? FirstName { get; set; }
        public string? MiddleName { get; set; }
        public string? LastName { get; set; }
        public string? PhoneNumber { get; set; }
        public string? Email { get; set; }
        public string? Address { get; set; }
        public string? RelationshipType { get; set; }
        public bool IsPrimaryContact { get; set; }
    }
}
