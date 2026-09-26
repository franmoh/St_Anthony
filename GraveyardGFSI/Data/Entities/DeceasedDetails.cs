using System.ComponentModel.DataAnnotations;

namespace GraveyardGFSI.Data.Entities
{
    public class DeceasedDetails : Auditable
    {
        //
        [Key]
        public int DeceasedDetailsId { get; set; }
        public int DeceasedStatusId { get; set; }
        public int ContactDetailsId { get; set; }
        public int NoteId { get; set; }

        //
        public ICollection<PlotDetails> Plots { get; set; }
        public ICollection<Note> Notes { get; set; }

        //
        public string FirstName { get; set; } = string.Empty;
        public string LastName { get; set; } = string.Empty;
        public string Initial { get; set; } = string.Empty;

        //
        public DateTime DateBuried { get; set; }
        public DateTime DoB { get; set; }
        public DateTime DoD { get; set; }

        public DeceasedDetails() { }
        public DeceasedDetails(string firstName, string lastName, string initial, DateTime dateBuried, DateTime dob, DateTime dod, DateTime createdDate, int createdBy, DateTime modifiedDate, int modifiedBy)
        {
            this.FirstName = firstName;
            this.LastName = lastName;
            this.Initial = initial;
            this.DateBuried = dateBuried;
            this.DoB = dob;
            this.DoD = dod;
            this.CreatedDate = createdDate;
            this.CreatedBy = createdBy;
            this.ModifiedDate = modifiedDate;
            this.ModifiedBy = modifiedBy;
        }
    }
}
