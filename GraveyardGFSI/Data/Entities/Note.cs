using System.ComponentModel.DataAnnotations;

namespace GraveyardGFSI.Data.Entities
{
    public class Note : IAuditable
    {
        [Key]
        public int NoteId { get; set; }
        public int UserId { get; set; }

        public string Content { get; set; } = string.Empty;
        public DateTime CreatedDate { get; set; }
        public int CreatedBy { get; set; }
        public DateTime ModifiedDate { get; set; }
        public int ModifiedBy { get; set; }

        //
        public required User User { get; set; }

        public Note() { }

        public Note(string content)
        {
            this.Content = content;
        }
    }
}
