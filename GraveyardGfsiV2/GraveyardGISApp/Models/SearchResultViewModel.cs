namespace GraveyardGISApp.Models
{
    public class SearchResultViewModel
    {
        public int DeceasedDetailsId { get; set; }
        public string? FirstName { get; set; }
        public string? MiddleName { get; set; }
        public string? LastName { get; set; }
        public string? Gender { get; set; }
        public DateTime? DateBuried { get; set; }
        public int? DOBYear { get; set; }
        public int? DOBMonth { get; set; }
        public int? DOBDay { get; set; }
        public int? DODYear { get; set; }
        public int? DODMonth { get; set; }
        public int? DODDay { get; set; }
        public int PlotId { get; set; }
        public int ZoneId { get; set; }
        public string? SectionName { get; set; }
        public string? Row { get; set; }
    }
}
