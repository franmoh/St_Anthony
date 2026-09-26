using System.ComponentModel.DataAnnotations;
using System.Numerics;

namespace GraveyardGFSI.Data.Entities
{
    public class ContactDetails : Auditable
    {
        [Key]
        public int ContactDetailsId { get; set; }
        public int PlotId { get; set; }
        public int DeceasedDetailsId { get; set; }
        public int NoteId { get; set; }

        public string FirstName { get; set; } = string.Empty;
        public string LastName { get; set; } = string.Empty;
        public string PhoneNumber { get; set; } = string.Empty;
        public string Address { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;

        //
        public PlotDetails PlotDetails { get; set; }
        public DeceasedDetails DeceasedDetails { get; set; }
        public ICollection<Note> Notes { get; set; }


        public ContactDetails() { }

        public ContactDetails(string firstName, string lastName, string phoneNumber, string address, string email, DateTime createdDate, int createdBy, DateTime modifiedDate, int modifiedBy)
        {
            this.FirstName = firstName;
            this.LastName = lastName;
            this.PhoneNumber = phoneNumber;
            this.Address = address;
            this.Email = email;
            this.CreatedDate = createdDate;
            this.CreatedBy = createdBy;
            this.ModifiedDate = modifiedDate;
            this.ModifiedBy = modifiedBy;
        }

    }
}
