using System.ComponentModel.DataAnnotations;

namespace GraveyardGFSI.Data.Entities
{
    public class MaintenanceDetails : Auditable
    {
        [Key]
        [Required]
        public int MaintId { get; set; }
        public string Description { get; set; } = string.Empty;

        //
        public required PlotDetails Plot { get; set; }
        public required MaintenanceStatus MaintenanceStatus { get; set; }
        public ICollection<Note> Notes { get; set; } = new List<Note>();


        public MaintenanceDetails() { }

        public MaintenanceDetails(string description)
        {
            this.Description = description;
        }
    }
}
