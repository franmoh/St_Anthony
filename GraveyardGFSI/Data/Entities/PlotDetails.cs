using System.ComponentModel.DataAnnotations;

namespace GraveyardGFSI.Data.Entities
{
    public class PlotDetails : Auditable
    {
        [Key]
        public int PlotDetailsId { get; set; }
        public int PlotId { get; set; }
        public int SectionId { get; set; }
        public int MaintenanceStatusId { get; set; }
        public int ContactDetailsId { get; set; }
        public int NoteId { get; set; }


        public string Row { get; set; } = string.Empty;
        public string Unit { get; set; } = string.Empty;
        public string Side { get; set; } = string.Empty;
        public string Niche { get; set; } = string.Empty;

        //
        public PlotDetails Plot { get; set; }
        public Section Section { get; set; }
        public MaintenanceStatus MaintenanceStatus { get; set; }
        public ContactDetails ContactDetails { get; set; }
        public ICollection<Note> Notes { get; set; }


        public PlotDetails() { }

        public PlotDetails(string row, string unit, string side, string niche)
        {

        }
    }
}
